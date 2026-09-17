"""Assembling what the model is given (FR-012, data-model §4).

The prompt is deliberately minimal: prompt quality is measured and tuned only after feature 003 exists (SRS Appendix A).
"""

from __future__ import annotations

from collections.abc import Mapping

from agentic_review.core.assembly.budget import estimate_tokens
from agentic_review.core.changeset.model import ChangedFile, ChangeSet
from agentic_review.core.config.settings import BudgetSettings
from agentic_review.core.findings.port import ReviewContext, ReviewedFile, RunMaterial

INSTRUCTIONS = """\
You are reviewing a change to a TypeScript/JavaScript repository. You are given the diff of every reviewed file.

How to report:
- Report each finding by calling the emit_finding tool, once per finding. This is the ONLY way a finding is recorded. \
Any prose you write is discarded and never read.
- file must be one of the reviewed files. startLine and endLine are line numbers in the new version of that file; \
the @@ header of each hunk gives where its new lines start.
- severity is one of: blocking (must be fixed before merging), important (should be fixed), nit (minor).
- category is one of: correctness, error-handling, interface-contract, test-evidence, security, performance, \
maintainability.
- rationale says what is wrong and why, in one or two sentences.
- evidence is required. Cite the diff as {"kind": "diff", "file": ..., "hunkIndex": ...} using the [hunk i] labels, \
or, when the diff alone does not show it, mark the finding {"kind": "unverified", "reason": ...}.
- Do not set ruleId.
- Report only real problems introduced or exposed by this change. Do not restate the diff.

When you have reported every finding, reply without a tool call. If there is nothing to report, reply without a \
tool call.
"""

MATERIAL_STATEMENT = "No checks were run. No related context was gathered."


def prompt_text(instructions: str, material_statement: str, diff_section: str) -> str:
    """The full text sent to the model: the system message, then the user message. The budget is estimated over it."""
    return f"{instructions}\n\n{user_message(material_statement, diff_section)}"


def user_message(material_statement: str, diff_section: str) -> str:
    return f"{material_statement}\n\n{diff_section}"


def _file_header(changed: ChangedFile) -> str:
    if changed.change_type == "renamed" and changed.previous_path:
        return f"{changed.path} (renamed, renamed from {changed.previous_path})"
    return f"{changed.path} ({changed.change_type})"


def _diff_section(change_set: ChangeSet) -> str:
    blocks = []
    for changed in change_set.reviewable_files:
        lines = [_file_header(changed)]
        for index, hunk in enumerate(changed.hunks):
            # Hunk text is sent exactly as recorded, never truncated (FR-2.5b).
            lines.append(f"[hunk {index}] {hunk.header}\n{hunk.text}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def assemble(change_set: ChangeSet, line_counts: Mapping[str, int], budget: BudgetSettings) -> ReviewContext:
    diff_section = _diff_section(change_set)
    material = RunMaterial(
        reviewed_files={
            f.path: ReviewedFile(line_count=line_counts[f.path], hunk_count=len(f.hunks))
            for f in change_set.reviewable_files
        }
    )
    return ReviewContext(
        instructions=INSTRUCTIONS,
        material_statement=MATERIAL_STATEMENT,
        diff_section=diff_section,
        estimated_tokens=estimate_tokens(prompt_text(INSTRUCTIONS, MATERIAL_STATEMENT, diff_section)),
        material=material,
    )
