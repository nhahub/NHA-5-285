"""The pipeline — the only owner of the order of operations (ADR-0001, contracts/internal-seams.md §1).

preflight → change set → assembly → review → output. Every stage that runs is timed. After preflight, a failure the
spec names is recorded as a degradation and the run continues to a report (Principle V).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from agentic_review import __version__
from agentic_review.core.agent.build import build_review_port
from agentic_review.core.assembly.prompt import assemble
from agentic_review.core.changeset.model import ScopeRequest
from agentic_review.core.changeset.resolve import resolve
from agentic_review.core.changeset.summary import measure_new_files, summarise
from agentic_review.core.config.credentials import Credential
from agentic_review.core.config.redact import redact
from agentic_review.core.config.settings import AgentSettings
from agentic_review.core.findings.port import ReviewPort
from agentic_review.core.findings.report import ReviewReport, ScopeKind
from agentic_review.core.output.build import build_report
from agentic_review.core.pipeline.preflight import PreflightFailure, preflight
from agentic_review.core.pipeline.timing import StageTimer

PortFactory = Callable[[AgentSettings, Credential], ReviewPort]


@dataclass(frozen=True)
class ReviewRequest:
    cwd: Path
    scope: ScopeKind | None = None  # None = not given on the command line
    base: str | None = None
    config_path: Path | None = None
    ceiling: int | None = None


@dataclass(frozen=True)
class Reviewed:
    report: ReviewReport
    """The verdict is already computed, in core."""
    ignored_settings: tuple[str, ...]


def utc_now() -> datetime:
    return datetime.now(UTC)


def run_review(
    request: ReviewRequest,
    *,
    env: Mapping[str, str],
    clock: Callable[[], float] = time.monotonic,
    now: Callable[[], datetime] = utc_now,
    port_factory: PortFactory | None = None,
) -> PreflightFailure | Reviewed:
    started_at = now().strftime("%Y-%m-%dT%H:%M:%SZ")
    run_started = clock()
    timer = StageTimer(clock)

    with timer.stage("preflight"):
        checked = preflight(request.cwd, request.config_path, env)
    if isinstance(checked, PreflightFailure):
        return checked

    settings = checked.loaded.settings
    agent = settings.agent
    if request.ceiling is not None:
        agent = agent.model_copy(update={"tool_call_ceiling": request.ceiling})
    secret = checked.credential.reveal()

    with timer.stage("changeSet"):
        scope_kind = request.scope or settings.scope
        was_defaulted = request.scope is None and not checked.loaded.scope_from_file
        change_set = resolve(
            checked.repo_root,
            ScopeRequest(kind=scope_kind, base=request.base),
            settings.exclude,
            was_defaulted=was_defaulted,
        )
        change_summary = summarise(change_set)
        line_counts = measure_new_files(change_set)

    with timer.stage("assembly"):
        context = assemble(change_set, line_counts, settings.budget)

    with timer.stage("review"):
        factory = port_factory or build_review_port
        outcome = factory(agent, checked.credential).review(context)

    degradations = [d.model_copy(update={"detail": redact(d.detail, secret)}) for d in outcome.degradations]

    def report(output_ms: int) -> ReviewReport:
        return build_report(
            change_summary=change_summary,
            completion=outcome.completion_status,
            outcome=outcome,
            degradations=degradations,
            agent=agent,
            provider=outcome.provider,
            budget_limit=settings.budget.max_tokens,
            budget_hit=False,
            started_at=started_at,
            duration_ms=max(0, round((clock() - run_started) * 1000)),
            stage_durations_ms={**timer.durations_ms, "output": output_ms},
            tool_version=__version__,
        )

    with timer.stage("output"):
        report(0)
    return Reviewed(report=report(timer.durations_ms["output"]), ignored_settings=checked.loaded.ignored_settings)
