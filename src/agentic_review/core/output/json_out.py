"""The JSON report (FR-025). It is serialised from the same ``ReviewReport`` the terminal renders (FR-027)."""

from __future__ import annotations

from agentic_review.core.findings.report import ReviewReport


def to_json(report: ReviewReport) -> str:
    return report.model_dump_json(by_alias=True, indent=2) + "\n"
