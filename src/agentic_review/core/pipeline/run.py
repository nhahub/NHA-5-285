"""The pipeline — the only owner of the order of operations (ADR-0001, ADR-0009, contracts/internal-seams.md §1).

The order is **declared as a graph** rather than written as statements: one node per phase of SRS §2.1, including
the phases that are purely deterministic and the three whose capability is not built yet. Each node is a thin
adapter — it reads ``PipelineRun``, calls one core function, and writes the result back. Nothing worth testing
lives in a node; it lives in the core function, which imports no framework and is callable on its own (FR-5.8).

This graph is **acyclic**. CF-6's graph, reached through the review port, is the only place a cycle may occur.
``core/pipeline`` and ``core/agent`` are the only packages that may import LangGraph, and this one may not import a
provider client (import contracts 3, 3b).

After preflight, a failure the spec names is recorded as a degradation and the run continues to a report
(Principle V). Every stage that runs is timed.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agentic_review import __version__
from agentic_review.core.agent.build import build_review_port
from agentic_review.core.assembly.prompt import assemble
from agentic_review.core.changeset.model import ChangeSet, ScopeRequest
from agentic_review.core.changeset.resolve import resolve
from agentic_review.core.changeset.summary import measure_new_files, summarise
from agentic_review.core.config.credentials import Credential
from agentic_review.core.config.redact import redact
from agentic_review.core.config.settings import AgentSettings
from agentic_review.core.findings.port import ReviewContext, ReviewOutcome, ReviewPort
from agentic_review.core.findings.report import ChangeSummary, ReviewReport, ScopeKind
from agentic_review.core.output.build import build_report
from agentic_review.core.pipeline.preflight import PreflightFailure, PreflightOk, preflight
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


@dataclass
class PipelineRun:
    """Everything the nodes read and write — one mutable object, as CF-6's ``ReviewRun`` is for the review step."""

    request: ReviewRequest
    env: Mapping[str, str]
    clock: Callable[[], float]
    now: Callable[[], datetime]
    port_factory: PortFactory | None
    timer: StageTimer = field(init=False)
    started_at: str = field(init=False)
    run_started: float = field(init=False)

    checked: PreflightOk | None = None
    agent: AgentSettings | None = None
    change_set: ChangeSet | None = None
    change_summary: ChangeSummary | None = None
    line_counts: Mapping[str, int] | None = None
    context: ReviewContext | None = None
    outcome: ReviewOutcome | None = None
    result: PreflightFailure | Reviewed | None = None

    def __post_init__(self) -> None:
        self.timer = StageTimer(self.clock)
        self.started_at = self.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.run_started = self.clock()


class PipelineState(TypedDict):
    run: PipelineRun


# CF-9 · repository, configuration, credential — the only stage that may stop the run
def _preflight(state: PipelineState) -> PipelineState:
    run = state["run"]
    with run.timer.stage("preflight"):
        checked = preflight(run.request.cwd, run.request.config_path, run.env)
    if isinstance(checked, PreflightFailure):
        run.result = checked
        return {"run": run}
    run.checked = checked
    agent = checked.loaded.settings.agent
    if run.request.ceiling is not None:
        agent = agent.model_copy(update={"tool_call_ceiling": run.request.ceiling})
    run.agent = agent
    return {"run": run}


def _route_after_preflight(state: PipelineState) -> str:
    return "end" if state["run"].result is not None else "continue"


# CF-1 · the only package that runs git
def _resolve_change_set(state: PipelineState) -> PipelineState:
    run = state["run"]
    assert run.checked is not None
    settings = run.checked.loaded.settings
    with run.timer.stage("changeSet"):
        scope_kind = run.request.scope or settings.scope
        was_defaulted = run.request.scope is None and not run.checked.loaded.scope_from_file
        run.change_set = resolve(
            run.checked.repo_root,
            ScopeRequest(kind=scope_kind, base=run.request.base),
            settings.exclude,
            was_defaulted=was_defaulted,
        )
        run.change_summary = summarise(run.change_set)
        run.line_counts = measure_new_files(run.change_set)
    return {"run": run}


# CF-2 · syntax trees and related context — built by feature 004
def _parse_and_context(state: PipelineState) -> PipelineState:
    return state


# CF-3 · run the project's checks and record evidence — built by feature 002
def _execute_checks(state: PipelineState) -> PipelineState:
    return state


# CF-8 · the pattern library the prompt is given — built by feature 003
def _load_patterns(state: PipelineState) -> PipelineState:
    return state


# CF-4 · the only budget owner
def _assemble_context(state: PipelineState) -> PipelineState:
    run = state["run"]
    assert run.checked is not None and run.change_set is not None and run.line_counts is not None
    with run.timer.stage("assembly"):
        run.context = assemble(run.change_set, run.line_counts, run.checked.loaded.settings.budget)
    return {"run": run}


# CF-6 · the only step that calls a model, and the only graph with a cycle
def _review(state: PipelineState) -> PipelineState:
    run = state["run"]
    assert run.checked is not None and run.agent is not None and run.context is not None
    with run.timer.stage("review"):
        factory = run.port_factory or build_review_port
        run.outcome = factory(run.agent, run.checked.credential).review(run.context)
    return {"run": run}


# CF-5 → CF-7 · canonical findings, then the one report both renderers share
def _build_report(state: PipelineState) -> PipelineState:
    run = state["run"]
    assert run.checked is not None and run.agent is not None and run.outcome is not None
    outcome = run.outcome
    secret = run.checked.credential.reveal()
    degradations = [d.model_copy(update={"detail": redact(d.detail, secret)}) for d in outcome.degradations]

    def report(output_ms: int) -> ReviewReport:
        return build_report(
            change_summary=run.change_summary,
            completion=outcome.completion_status,
            outcome=outcome,
            degradations=degradations,
            agent=run.agent,
            provider=outcome.provider,
            budget_limit=run.checked.loaded.settings.budget.max_tokens,
            budget_hit=False,
            started_at=run.started_at,
            duration_ms=max(0, round((run.clock() - run.run_started) * 1000)),
            stage_durations_ms={**run.timer.durations_ms, "output": output_ms},
            tool_version=__version__,
        )

    with run.timer.stage("output"):
        report(0)
    run.result = Reviewed(
        report=report(run.timer.durations_ms["output"]),
        ignored_settings=run.checked.loaded.ignored_settings,
    )
    return {"run": run}


def build_pipeline_graph() -> CompiledStateGraph:
    """The order of operations, as an object. ``contracts/internal-seams.md`` §1 is what this must agree with."""
    graph = StateGraph(PipelineState)
    graph.add_node("preflight", _preflight)
    graph.add_node("resolve_change_set", _resolve_change_set)
    graph.add_node("parse_and_context", _parse_and_context)
    graph.add_node("execute_checks", _execute_checks)
    graph.add_node("load_patterns", _load_patterns)
    graph.add_node("assemble_context", _assemble_context)
    graph.add_node("review", _review)
    graph.add_node("build_report", _build_report)

    graph.set_entry_point("preflight")
    graph.add_conditional_edges("preflight", _route_after_preflight, {"continue": "resolve_change_set", "end": END})
    graph.add_edge("resolve_change_set", "parse_and_context")
    graph.add_edge("parse_and_context", "execute_checks")
    graph.add_edge("execute_checks", "load_patterns")
    graph.add_edge("load_patterns", "assemble_context")
    graph.add_edge("assemble_context", "review")
    graph.add_edge("review", "build_report")
    graph.add_edge("build_report", END)
    return graph.compile()


_PIPELINE = build_pipeline_graph()


def run_review(
    request: ReviewRequest,
    *,
    env: Mapping[str, str],
    clock: Callable[[], float] = time.monotonic,
    now: Callable[[], datetime] = utc_now,
    port_factory: PortFactory | None = None,
) -> PreflightFailure | Reviewed:
    run = PipelineRun(request=request, env=env, clock=clock, now=now, port_factory=port_factory)
    _PIPELINE.invoke({"run": run})
    assert run.result is not None
    return run.result
