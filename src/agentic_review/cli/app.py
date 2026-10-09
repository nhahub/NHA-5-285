"""The command-line adapter (contracts/cli.md). It translates flags, streams and exit codes, and decides nothing about
findings (FR-10.2). Nothing imports this package (import contract 6).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from agentic_review.cli.exit_codes import EXIT_PREFLIGHT, exit_code_for
from agentic_review.core.output.terminal import render_terminal
from agentic_review.core.pipeline.preflight import PreflightFailure
from agentic_review.agents.pipeline_agent import ReviewRequest, run_review

app = typer.Typer(add_completion=False, no_args_is_help=True, help="Review a TypeScript/JavaScript change set.")

# Only the scopes this build resolves are offered (contracts/cli.md: a flag arrives with what gives it meaning).
# The pull-request scope is selected by --pr, not by --scope.
OFFERED_SCOPES = ("working-tree", "range")


@app.callback()
def _root() -> None:
    """Review a TypeScript/JavaScript change set."""


def _could_not_start(message: str) -> typer.Exit:
    # Checked here rather than by Click, whose usage error exits 2 — the code for "no judgement", not "could not
    # start" (contracts/cli.md "Exit codes").
    typer.echo(f"{message}\nNothing was reviewed.", err=True)
    return typer.Exit(EXIT_PREFLIGHT)


@app.command()
def review(
    scope: Annotated[
        str | None,
        typer.Option(
            "--scope",
            metavar="|".join(OFFERED_SCOPES),
            help="What to review; overrides the config file's scope. Default: working-tree.",
        ),
    ] = None,
    base: Annotated[
        str | None,
        typer.Option(
            "--base", metavar="REF", help="With --scope range: the ref to compare with. With --pr: its base branch."
        ),
    ] = None,
    head: Annotated[
        str | None,
        typer.Option("--head", metavar="REF", help="With --scope range: the ref to review instead of HEAD."),
    ] = None,
    pr: Annotated[
        str | None,
        typer.Option(
            "--pr",
            metavar="URL",
            help="Review a public GitHub pull request, https://github.com/OWNER/REPO/pull/N. Needs no local repository.",
        ),
    ] = None,
    config: Annotated[
        Path | None,
        typer.Option("--config", metavar="PATH", help="Configuration file to use instead of .agentic-review.yml."),
    ] = None,
    ceiling: Annotated[
        int | None,
        typer.Option(
            "--ceiling", metavar="N", help="Tool-call ceiling for this run (at least 1); overrides agent.toolCallCeiling."
        ),
    ] = None,
) -> None:
    """Review uncommitted changes, a branch range (--scope range --base REF), or a pull request (--pr URL)."""
    if ceiling is not None and ceiling < 1:
        raise _could_not_start(f"--ceiling: must be an integer of at least 1, got {ceiling}.")
    if scope is not None and scope not in OFFERED_SCOPES:
        offered = " or ".join(OFFERED_SCOPES)
        raise _could_not_start(f"--scope: {scope!r} is not available in this build; choose {offered}.")
    request = ReviewRequest(
        cwd=Path.cwd(), scope=scope, base=base, head=head, pr=pr, config_path=config, ceiling=ceiling
    )
    result = run_review(request, env=os.environ)
    if isinstance(result, PreflightFailure):
        typer.echo(result.message, err=True)
        raise typer.Exit(EXIT_PREFLIGHT)
    render_terminal(result.report, Console())
    raise typer.Exit(exit_code_for(result.report.verdict))


def main() -> None:
    app()
