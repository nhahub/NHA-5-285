# Requirements Audit — Inventory, Conformance and Consolidation

**Audited:** 2026-10-27 · **Repository state:** HEAD `8089324` plus the uncommitted working tree as found (deleted `Docs/Draft/agentic-code-review-srs-ar.md` and `Docs/Draft/enterpenuership/Target/CAI5_IND5_G1-agentic-pr-review-documentation.md`, modified `Docs/README.md`, untracked `Docs/CAI5_IND5_G1-agentic-pr-review-documentation.md`, `.aider*`).
**Build target audited against:** `Docs/agentic-code-review-srs-v1.md`, Version 1.5 (2026-10-09).
**Not modified by this audit:** anything under `src/`, `tests/`, `specs/`, `Docs/`; no ADR. This file is the only output.
**Follow-up, same day:** the gaps and drift this audit found were then acted on, with srs-v2's amendments adopted wherever srs-v1 and srs-v2 conflicted. srs-v1 is now Version 1.6. What changed, and what each change did to the verdicts, is in the section "Follow-up: changes applied" below; the rows of Parts 1–3 are updated to the new state and say so where they changed.

This file has three parts, in this order:

1. Inventory of the documents, with conflicts and open questions
2. Conformance matrix (86 SRS functional requirements, then AC-1 to AC-17; 85 and 16 before the follow-up)
3. Consolidated requirements document, with appendices for open questions, conformance gaps and removed content

A note on names used throughout. The two files `agentic-code-review-srs-v1.md` and `agentic-code-review-srs-v2.md` are two successive attempts to cut the full catalogue down to a first implementable MVP phase. Their "v1" and "v2" are attempt numbers. They are not the product versions v1, v2 and v3 used inside the catalogue and inside srs-v1 itself (for example srs-v1 §7 "Destination: v2" means product v2, not `srs-v2.md`; srs-v2 §0.2 says the same). Below, **srs-v1** and **srs-v2** name the files; **product v2/v3** names the roadmap versions.

---

## Checks run

| Command | Result |
|---|---|
| `uv run pytest -v -p no:cacheprovider` | **426 passed**, 0 failed, 0 skipped, in 71.79 s (wall clock 1 m 17.7 s including the build). Exit 0. The Windows trampoline fallback was not needed. |
| `uv run lint-imports` | **Contracts: 6 kept, 0 broken** (81 files, 231 dependencies analysed): 1, 2, 3, 3b, 6, 8. Exit 0. |
| `uv run agentic-review --version` | `No such option: --version` |
| `uv run agentic-review schema` | `No such command 'schema'.` `--help` lists only `review` and `render`. |
| Probe: in a throwaway repository under the session scratchpad (outside this repository), with `.agentic-review.yml` containing `scope: staged`, one staged `a.ts`, and `AGENTIC_REVIEW_API_KEY=dummy-not-a-key`: `uv run --project H:/Pull-request-Reviewer agentic-review review` | Unhandled `NotImplementedError: the staged scope arrives with User Story 4` from `resolve_change_set`, Rich traceback, **exit 1**. No report. No model call was made (the failure is before the review node). |

Project claims checked against these results:

| Claim (source) | Checked | Finding |
|---|---|---|
| "424 tests run offline in under a minute" (`CLAUDE.md` line 7; `Docs/CAI5_IND5_G1-agentic-pr-review-documentation.md` line 56) | pytest run above | **Mismatch.** 426 tests, 71.79 s. |
| "47 Python modules" (`CLAUDE.md`) | `find src/agentic_review -name '*.py'` | 47 `.py` files, of which 11 are `__init__.py` (10 empty) and 1 is `__main__.py`; 35 other modules. Matches if every file counts. |
| "6 import-linter structural contracts" (`CLAUDE.md`) | `lint-imports` | Matches: 6 contracts. `technical_stack.md` §4 says "**Seven**" and tabulates eight rows (1, 2, 3, 3b, 4, 5, 6, 8); contracts 4 and 5 are absent from `pyproject.toml` (comment at `pyproject.toml` lines 45–46 defers them to feature 004). |
| "CF-1, CF-4, CF-5, CF-6, CF-7, CF-9 built; CF-2, CF-3, CF-8 not built" (`CLAUDE.md`) | Code read | CF-2, CF-3, CF-8 are pass-through nodes (`agents/pipeline_agent.py` lines 187–199). CF-1 is built for working-tree, range and pull-request scopes only (`core/changeset/resolve.py` line 198). CF-4's per-section budget and eviction are absent; `specs/README.md` assigns CF-4 to feature 004, "Not started". |
| "`review` and `render` implemented; `regression` and `schema` not built" (`CLAUDE.md`) | `--help` | Matches. |
| "Choosing what to review: uncommitted work, staged work, a range of commits — Built" (`Docs/CAI5_…documentation.md` line 52) | Code and probe | **Mismatch.** Staged is not built (`cli/app.py` line 28; `core/changeset/resolve.py` line 198). |
| "Tracing of each model call — Built" (`Docs/CAI5_…documentation.md`) | `grep -rniE "callback|CallbackHandler|langfuse" src` | **Mismatch.** No tracer is attached anywhere in `src/`. `agents/tracing.py` (tasks T106) does not exist. Langfuse is used only to fetch a system prompt (`core/assembly/prompt.py` lines 85–105). |
| Feature 001 status "Plan approved — ready for tasks" (`specs/README.md`) | `tasks.md` | **Stale.** 114 tasks marked `[X]`, 35 open. |

## Follow-up: changes applied

Instruction: apply the audit's findings, and where srs-v1 and srs-v2 conflict treat srs-v2's amendment as the right change. No ADR was edited and no requirement was renumbered.

**How "conflict" was read.** srs-v2 marks five requirements and AC-2 as "(amended in v2)" and adds FR-8.5 and AC-17 as "(new in v2)"; those are the conflicts adopted. Two rows of 1.5 were not adopted, because neither is an amendment: srs-v2's FR-10.3a lists three selections only because srs-v2 predates srs-v1 v1.4 and v1.5 (adopting it would remove the single-commit and pull-request scopes and reverse the Accepted ADR-0011), and srs-v2's FR-8.2a is a rewording that srs-v2 itself says keeps srs-v1's meaning. The 37 requirements srs-v2 places out of scope are omissions, not amendments, and stay in force; dropping FR-5.6a or FR-11.2 would need an ADR (srs-v2 §0.3).

| Change | Files | Effect on this audit |
|---|---|---|
| srs-v1 v1.6: FR-5.7, FR-6.3a, FR-8.2b, FR-8.2c, FR-8.2d and AC-2 take srs-v2's amended text, each with an amendment note; FR-8.5 (Must) and AC-17 added; Appendix B gains the FR-8.5 row; revision entries 1.2, 1.3 and 1.6 added; the FR-10.4d note no longer calls FR-8.5 a product-v2 item | `Docs/agentic-code-review-srs-v1.md` | Conflicts FR-5.7, FR-6.3a, FR-8.2b, FR-8.2c, FR-8.2d, AC-2 and FR-8.5 resolved; OQ-3 and OQ-4 closed; 86 FRs and 17 ACs. Verdicts of the amended FRs unchanged; FR-8.5 and AC-17 Not built (`grep -rniI mermaid src tests`: no hits) |
| srs-v2 §0.3 records which parts v1.6 adopted | `Docs/agentic-code-review-srs-v2.md` | OQ-1 narrowed to the unadopted cut |
| srs-v2 added to the authority tables as a Draft that is not the build target | `CLAUDE.md`, `Docs/README.md` | — |
| A scope the build cannot resolve (`scope: staged` in the config file) is refused by preflight check 3 with a message and exit 3, instead of reaching the resolver and crashing with exit 1; new unit test | `core/pipeline/preflight.py`; `tests/unit/pipeline/test_preflight.py::test_a_scope_this_build_cannot_resolve_is_refused_before_resolution`; `Docs/operation_guidelines.md` troubleshooting row | The staged-crash part of the FR-10.3a, FR-10.4c, FR-9.3 and FR-11.2 gaps is closed; each stays Partial for its other gap. Probe re-run: `The staged scope is not available in this build; choose working-tree or range.` · `Nothing was reviewed.` · exit 3 |
| `README.md` added at the repository root (install, run, exit codes, develop, documentation); it states that no licence has been chosen | `README.md` | FR-9.1 stays Partial: LICENSE is still absent, because choosing a licence is the owner's decision |
| Stale paths: spec 001 FR-022 and FR-5.1 traceability rows, the `core/findings/port.py` docstring, the CF-6 module row of `06-verification.md` | `specs/001-walking-skeleton/spec.md`, `core/findings/port.py`, `Docs/design/06-verification.md` | B.2 rows 1–3 fixed |
| Traceability rows spec 001 FR-010 and FR-028 now name what is missing (T087, T092) | `specs/001-walking-skeleton/spec.md` | B.2 rows 4–5 recorded where they belong; the code is unchanged |
| Counts: `CLAUDE.md` and the CAI5 document now say 427 tests in under two minutes; `technical_stack.md` §4 says eight contracts specified, six enforced; `specs/README.md` feature 001 status | `CLAUDE.md`, `Docs/CAI5_IND5_G1-agentic-pr-review-documentation.md`, `Docs/technical_stack.md`, `specs/README.md` | B.2 count and status rows fixed |
| The CAI5 document no longer claims staged review or tracing as built, and lists the Mermaid report as not built | `Docs/CAI5_IND5_G1-agentic-pr-review-documentation.md` | "Checks run" mismatches fixed |
| `Docs/README.md`: the broken CAI5 link points at the document's current location; srs-v2, `system-design.md` and `system-design-block.md` indexed; the SRS version corrected to v1.6 | `Docs/README.md` | OQ-23 closed |
| AC-17 recorded in the verification design as having no mechanism yet; HLR-20 now backed by FR-8.5 | `Docs/design/06-verification.md`, `Docs/design/Component-design/README.md`, `specs/README.md` | — |
| The default-model comment reads "to be chosen by test S-1" | `core/config/settings.py` line 17 | OQ-18's wording point fixed; S-1 for the default model is still unmeasured |

Checks after the changes: `uv run pytest -q -p no:cacheprovider` → **427 passed** in 86.56 s; `uv run lint-imports` → **6 kept, 0 broken**.

Not acted on, because each needs a decision or a feature rather than a correction: building the staged and single-commit scopes (User Story 4), the `schema` command and `--version` (T092), the token comparison of FR-11.1, a catch-all for unexpected errors after preflight (T096), the LICENSE, Langfuse's place in `core/` (OQ-20), the unlisted dependencies (OQ-21), and every other open question.

---

# Part 1 — Inventory

## 1.1 Documents in scope

Timestamps and sizes for the 19 listed documents are copied from the task's Context table and were not used to decide which document is newer. For reference documents the task gave no timestamps; sizes and the file-system "modified" time below come from `ls -l` and are metadata only.

| Document path | Version or date (as stated inside the file) | Created | Last modified | Size (bytes) | Kind | Status | Superseded by | Authority | Notes |
|---|---|---|---|---:|---|---|---|---|---|
| `Docs/agentic-code-review-srs-v1.md` | Version 1.5, 2026-10-09, "Baselined" (Version 1.6, 2026-10-27, after the follow-up) | 2026-10-18 11:16 | 2026-10-26 10:47 | 83,226 | SRS — MVP-phase attempt (first) | Current | none | normative | The only full statement of the v1.5 requirements, AC-1…AC-16, TBD-1…TBD-8 with placeholders, and the §5 interface-stability table. Revision history had no 1.2 or 1.3 row although FR-5.8 and AC-10 cite amendments "in v1.2" and "v1.3" (added in v1.6). §10 says "Fifteen items" but lists items 1–19. |
| `Docs/agentic-code-review-srs-v2.md` | Version 2.0, 2026-09-29, "Draft"; "Built from srs-v1 (v1.4)" | 2026-10-26 10:47 | 2026-10-26 10:47 | 40,845 | SRS — MVP-phase attempt (second, cut to the HLR diagrams) | Unclear | none asserted | non-normative (its own §0.3: "Until this draft is accepted, v1 stays the normative build target"; absent from the authority order, `CLAUDE.md`, `Docs/README.md`) | Only document defining FR-8.5 (Mermaid report), AC-17, HLR-24 and HLR-25, and listing the consequences of dropping 37 srs-v1 requirements (§9). Count mismatches: see 1.4. |
| `Docs/Draft/agentic-code-review-srs.md` | No version or date stated; "Status: Draft · Role: Non-normative catalogue and roadmap" | 2026-10-18 11:16 | 2026-10-26 10:47 | 39,504 | reference (requirement catalogue, product v1–v3) | Historical for v1 scope; current as the identifier registry | srs-v1 (v1.5), for every v1 requirement (its own line 43 says v1.1 text governs) | non-normative | Only source of the product v2/v3 identifiers (FR-1.1, FR-2.1, FR-2.3a/b, FR-3.1–3.4, FR-5.4, FR-5.5, FR-6.3, FR-7.1, FR-10.5–10.7 …) and the registry the ADRs cite. |
| `Docs/design/Component-design/srs-alignment.md` | 2026-09-29, "Non-normative analysis" | 2026-10-26 10:47 | 2026-10-26 10:47 | 16,116 | analysis | Derived (against an srs-v1 revision with 82 FRs) | none | derived | The FR→HLR classification (Fits 9 / Details 36 / Conflicts 3 / Outside 34) and nine proposed HLR edits (§3). Does not cover FR-4.8, FR-10.3d, FR-10.4d. |
| `Docs/Draft/system-analysis/system_analysis.md` | 2026-09-10, "Draft / Analysis" | 2026-10-18 11:16 | 2026-10-26 10:47 | 59,057 | analysis | Historical (analyses srs-v1 v1.0: ceiling default zero, framework confined to CF-6) | srs-v1 v1.1 and later, on every point it analyses | non-normative | Use cases, entity model, operational workflows, and analyst findings Q-1…Q-11 (§7). Count mismatches: see 1.4. |
| `specs/README.md` | No date | 2026-10-18 11:16 | 2026-10-18 11:16 | 2,008 | feature spec (index) | Current, status column stale | none | derived | Feature 001–006 plan, mapping each to an Appendix A step, core functions and ACs. Assigns CF-4 to feature 004. |
| `specs/001-walking-skeleton/spec.md` | Created 2026-09-17; approved 2026-09-17; amended 2026-10-09 | 2026-10-18 11:16 | 2026-10-26 10:47 | 40,211 | feature spec | Current | none | derived (feature-local identifiers) | The traceability table spec 001 FR-001…FR-032 → SRS (lines 225–266). Several "Realised in" paths do not exist: see Appendix B. |
| `specs/001-walking-skeleton/plan.md` | 2026-09-17; authority line cites srs-v1 **v1.1** | 2026-10-18 11:16 | 2026-10-26 10:47 | 24,742 | feature spec (plan) | Current, partly stale | none | derived | Design gaps D-1…D-5 and the planned structure. States that `agentic-review schema` prints the report schema; not built. |
| `specs/001-walking-skeleton/tasks.md` | No header date; phases added 2026-09-24, 2026-10-09, 2026-10-18 | 2026-10-26 10:47 | 2026-10-26 10:47 | 80,773 | feature spec (tasks) | Current | none | derived | The only record of what is outstanding for feature 001: 114 tasks `[X]`, 35 open (User Stories 3–5, Langfuse T102–T109, polish T094–T101, maintainer live runs). |
| `specs/001-walking-skeleton/data-model.md` | Design gaps "approved and written back to 02 on 2026-09-17" | 2026-10-18 11:16 | 2026-10-26 10:47 | 16,570 | feature spec (data model) | Current | none | derived (02 wins on disagreement) | Feature 001's selection of the design domain model, with layer placement of each type. |
| `specs/001-walking-skeleton/research.md` | 2026-09-17 | 2026-10-18 11:16 | 2026-10-26 10:47 | 41,177 | feature spec (research) | Current | none | derived | Decisions R-1…R-25 with rationale; the placeholder values used in code cite it. |
| `specs/001-walking-skeleton/quickstart.md` | No date | 2026-10-18 11:16 | 2026-10-26 10:47 | 6,534 | feature spec (validation guide) | Current, partly stale | none | derived | Manual validation groups A–C. Expects `agentic-review --version` to print a version; the option does not exist. |
| `specs/001-walking-skeleton/s1-results.md` | Written 2026-09-17 18:27 UTC by `scripts/s1_tool_calling_probe.py` | 2026-10-26 10:47 | 2026-10-26 10:47 | 5,642 | reference (measurement record) | Current | none | non-normative | The only S-1 measurement: `qwen2.5-coder:7b` on a local endpoint, 50 runs, 0 tool calls. No NIM model measured. |
| `specs/001-walking-skeleton/checklists/requirements.md` | Created 2026-09-17 | 2026-10-18 11:16 | 2026-10-18 11:16 | 2,728 | feature spec (quality checklist) | Historical | none | derived | Record of the spec's two validation iterations. |
| `specs/001-walking-skeleton/contracts/cli.md` | No date; parent `Docs/design/04-contracts.md` §6 | 2026-10-18 11:16 | 2026-10-26 10:47 | 9,186 | feature spec (contract) | Current | none | derived | Flags, exit codes and the "a flag is offered only once its scope is built" rule. Lists a `schema` command not built. |
| `specs/001-walking-skeleton/contracts/config.md` | No date; parent 04 §7, 05 §4 | 2026-10-18 11:16 | 2026-10-26 10:47 | 4,537 | feature spec (contract) | Current | none | derived | `.agentic-review.yml` shape; that a `--pr` review reads configuration only from `--config`. |
| `specs/001-walking-skeleton/contracts/emit-finding.md` | Changes dated 2026-09-17, 2026-09-24 | 2026-10-18 11:16 | 2026-10-26 10:47 | 8,788 | feature spec (contract) | Current | none | derived | Fixed rejection reasons and the repair-turn wording the code reproduces. |
| `specs/001-walking-skeleton/contracts/internal-seams.md` | No date | 2026-10-18 11:16 | 2026-10-26 10:47 | 6,603 | feature spec (contract) | Current, partly ahead of code | none | derived | Python seams. `ReviewRequest` lists a `commit` field the code lacks (`agents/pipeline_agent.py` lines 66–74). |
| `specs/001-walking-skeleton/contracts/review-report.md` | No date | 2026-10-18 11:16 | 2026-10-18 11:16 | 4,982 | feature spec (contract) | Current | none | derived | Worked JSON examples of schema 1.0. Names `agentic-review schema` as the authoritative form; not built. |

## 1.2 Reference documents checked for conflicts

| Document path | Version or date (as stated inside the file) | Created | Last modified (file system) | Size (bytes) | Kind | Status | Superseded by | Authority | Notes |
|---|---|---|---|---:|---|---|---|---|---|
| `Docs/Draft/mvp-scope.md` | 2026-09-08, "Adopted — baselined as srs-v1" | not supplied | 2026-10-18 11:16 | 21,676 | analysis | Historical | srs-v1 | non-normative | The rationale for every v1 inclusion and cut. |
| `Docs/Draft/agentic-architecture-review.md` | 2026-09-08, "Analysis · Non-normative" | not supplied | 2026-10-18 11:16 | 26,692 | analysis | Historical | srs-v1 v1.1 (adopted AC-A3 as FR-5.2c; observation type as FR-5.9; declined `finish_review`) | non-normative | Response to an external agentic-architecture review. |
| `Docs/system-design.md` | No version or date | not supplied | 2026-10-26 10:47 | 3,737 | design (diagrams only) | Unclear | none | non-normative (not in any authority table; not linked from `Docs/README.md`) | Three mermaid levels: LLM ↔ tools; rules → context → review → report. |
| `Docs/system-design-block.md` | No version or date | not supplied | 2026-10-26 10:47 | 3,956 | design (diagrams only) | Derived (a block-diagram rendering of `system-design.md`) | none | non-normative | Same components as `system-design.md`. Its Level 2 draws `CONTEXT --> RULES`; `system-design.md` draws `RULES --> CONTEXT`. |
| `Docs/CAI5_IND5_G1-agentic-pr-review-documentation.md` | No version; planned dates 2026-11-01 … 2026-12 in its Gantt | not supplied | 2026-10-26 11:57 | 23,665 | reference (project documentation for submission) | Unclear (untracked; its tracked copy under `Docs/Draft/enterpenuership/Target/` is deleted in the working tree) | none | non-normative | Planning, stakeholders, data and report UI. Plans "Add an open-source licence" for 2026-12. Contains the mismatched claims in "Checks run". |
| `Docs/operation_guidelines.md` | "Written against feature 001 through User Story 2, plus the pull-request scope and the HTML report" | not supplied | 2026-10-26 10:47 | 36,502 | reference (operating guide) | Current | none | non-normative | Consistent with the code on staged/commit not being available. The closest thing to CLI usage documentation (FR-9.1). |
| `CLAUDE.md` | No version | not supplied | 2026-10-26 10:47 | 15,112 | reference (contributor guidance) | Current | none | non-normative | Authority table and load-bearing constraints. Test-count claim mismatched. |
| `DESIGN_BLOCKERS.md` | 2026-09-14; "All 24 resolved" | not supplied | 2026-10-18 11:16 | 57,748 | reference (issue log) | Historical, with a response log | srs-v1 v1.1, ADR-0008, stack, design | non-normative | The record of 24 design-phase blockers. Response-log rows DB-04, 06, 09, 10, 12, 15 and DO-1…DO-4 are blank. Still flags "Category set still open" (DB-08). |

## 1.3 Architecture decision records (listed, not edited)

| ADR | Status (stated) | Date (stated) | Size (bytes) |
|---|---|---|---:|
| `Docs/adr/0001-fixed-pipeline-with-bounded-agency.md` | Proposed | 2026-09-08 | 13,781 |
| `Docs/adr/0002-pipeline-initiates-test-execution.md` | Proposed | 2026-09-08 | 10,558 |
| `Docs/adr/0003-untrusted-code-isolation-and-fork-triggers.md` | Proposed | 2026-09-08 | 13,992 |
| `Docs/adr/0004-findings-emitted-as-tool-calls.md` | Proposed | (not on the first lines read) | 11,546 |
| `Docs/adr/0005-cross-run-memory-as-hidden-comment-ledger.md` | Proposed | 2026-09-08 | 21,497 |
| `Docs/adr/0006-local-cli-core-action-as-adapter.md` | Accepted | 2026-09-08 | 16,159 |
| `Docs/adr/0007-python-harness-typescript-target.md` | Accepted | 2026-09-08 | 20,443 |
| `Docs/adr/0008-agent-runtime-tool-registry-and-termination.md` | Accepted | 2026-09-14 | 11,374 |
| `Docs/adr/0009-pipeline-as-declared-graph.md` | Accepted | 2026-09-20 | 13,668 |
| `Docs/adr/0010-agents-package-separate-from-core.md` | Accepted | 2026-09-20 | 9,062 |
| `Docs/adr/0011-cli-reads-a-public-pull-request.md` | Accepted | 2026-10-09 | 10,127 |
| `Docs/adr/README.md` | status index | — | 13,169 |

## 1.4 Counts and quotations taken from derived documents, checked against srs-v1

Method: `grep -oE '^- \*\*FR-[0-9]+\.[0-9]+[a-z]?' Docs/agentic-code-review-srs-v1.md` gives 84 identifiers defined in §4; FR-7.2 is declared binding in §7 (line 516) and listed in Appendix B, so srs-v1 holds **85** functional requirements. srs-v1 §6 holds **16** acceptance criteria. After the follow-up (v1.6) the same command gives 85 identifiers in §4, so 86 with FR-7.2, and §6 holds 17.

| Claim | Where | srs-v1 says | Mismatch |
|---|---|---|---|
| "v1 has 82 functional requirements" | `srs-v2.md` §0.1; `srs-alignment.md` line 5 and §1 | 85 | Yes. 82 = 85 minus FR-4.8, FR-10.3d, FR-10.4d. Neither document accounts for those three: they are not in srs-v2's 45 kept nor its 37 out-of-scope list, and not in the alignment tables. |
| srs-v2 "built from srs-v1 (v1.4)" | `srs-v2.md` header | FR-4.8 is "new in v1.4" (srs-v1 revision history) | Yes. A v1.4 base would include FR-4.8; srs-v2 omits it. Its FR-10.3a also has the three pre-v1.4 selections. |
| "Kept the 45 v1 requirements … Moved 37 requirements out of scope" | `srs-v2.md` §0.4 | — | Internally consistent (45 + 37 = 82); the 46 kept identifiers extracted from srs-v2 §4 = 45 + FR-8.5. |
| "v1 contains 72 requirements: 63 Must and 9 Should" | `system_analysis.md` §2 line 195 | 85 | Yes (analysed v1.0). |
| "all twelve acceptance criteria" | `system_analysis.md` §2.3 line 233 | 16 | Yes (AC-13…AC-16 added later). |
| "FR-5.7 sets the ceiling's default to zero" | `system_analysis.md` footnote `[^fr57]` | Positive default (FR-5.7, amended v1.1); placeholder 25 (§8) | Yes. |
| "the agent framework is confined to CF-6" | `system_analysis.md` footnote `[^fr58]` | Confined to the agents package (FR-5.8, amended v1.2, renamed v1.3) | Yes. |
| "Fifteen items from DESIGN_BLOCKERS.md" | srs-v1 §10 line 579 | §10 tables number items 1–19 | Internal mismatch within srs-v1. `DESIGN_BLOCKERS.md` says 17 were answered in srs-v1 v1.1. |
| "Seven import-linter contracts" | `technical_stack.md` §4 | — | The table beside it has eight rows; `pyproject.toml` has six. |
| "sixteen acceptance criteria" | `CLAUDE.md`, `Docs/design/06-verification.md` | 16 | No mismatch. |

## 1.5 (a) Requirement identifiers with conflicting wording in more than one document

srs-v1 wins every row by the authority order, except where noted as open. srs-v2 itself defers to srs-v1 until accepted (srs-v2 §0.3). **Follow-up:** the rows marked "Resolved in v1.6" were settled by adopting srs-v2's text into srs-v1; the location A text quoted is the v1.5 text.

| Identifier | Location A (srs-v1) | Location B | Conflict |
|---|---|---|---|
| FR-10.3a | srs-v1 §4.1: five selections (working tree, staged, branch or commit comparison, a single named commit, a public pull request by URL); a comparison may name the ref it reviews | `srs-v2.md` §4.1.1; `Docs/Draft/agentic-code-review-srs.md` line 365 | Both list only three selections. srs-v2 does not mark it amended. **Not adopted in v1.6:** not an amendment; srs-v2 predates v1.4 and v1.5, and adopting it would reverse ADR-0011. |
| FR-5.7 | srs-v1 §4.6: counts "every call, `emit_finding` included" | `srs-v2.md` §4.4 (amended in srs-v2) | srs-v2 replaces `emit_finding` with "the calls that hand over findings". `system_analysis.md` (v1.0 reading) has a default of zero. **Resolved in v1.6:** srs-v2's wording adopted. |
| FR-6.3a | srs-v1 §4.8: each rule has a wrong example, a correct example **and at least one regression case** | `srs-v2.md` §4.2 (amended) | srs-v2 drops the regression case. **Resolved in v1.6:** srs-v2's text adopted. |
| FR-8.2b | srs-v1 §4.7: the `emit_finding` tool schema equals the finding model alone | `srs-v2.md` §4.5 (amended) | srs-v2 drops the tool-schema clause. **Resolved in v1.6:** clause removed; FR-5.6a and §5 still require it. |
| FR-8.2c | srs-v1 §4.7: records requested/achieved depth, ceiling, whether investigation tools were enabled, completion status, model and schema versions, scope | `srs-v2.md` §4.5 (amended) | srs-v2 drops "investigation tools enabled" and "completion status", adds "whether [the ceiling] was reached". **Resolved in v1.6:** srs-v2's text adopted. |
| FR-8.2d | srs-v1 §4.7: minimum is total, emitting, investigating, repair turns | `srs-v2.md` §4.5 (amended) | srs-v2 minimum is total and emitting only. **Resolved in v1.6:** srs-v2's text adopted. |
| FR-8.2a | srs-v1: "serialize the review's result to JSON as a machine-readable artifact" | `srs-v2.md` §4.5: "write the review's result as a JSON file" | Wording narrower (a file); srs-v2 claims same meaning. **Not adopted in v1.6:** srs-v2 says the meaning is unchanged, so this is not a conflict. |
| AC-2 | srs-v1 §6 | `srs-v2.md` §6 (amended) | srs-v2 adds FR-4.2 to the verified set and requires a change that breaks a test or the type-check. **Resolved in v1.6:** srs-v2's text adopted. |
| FR-2.2 | srs-v1 §4.2: in-process parsing, no target toolchain; library not named | Catalogue line 288: "build a `tree-sitter` AST" | Library named in the catalogue. The catalogue's own line 43 says v1.1 text governs. |
| FR-5.2 | srs-v1 §4.5: optionally "the identifier of a matched pattern rule" | Catalogue line 321: optionally "a suggested-fix reference" | Different optional field. Not in the catalogue's list of changed identifiers (line 43). |
| FR-9.3 | srs-v1 §4.9: Must; test script, provider key, git repository, parseable tree | Catalogue line 357: Should; "test script, API key" | Must/Should and scope differ. Not in the catalogue's line-43 list. |
| FR-10.4c | srs-v1 §4.9: Must; at least four outcomes | Catalogue line 369: Should; no outcome floor | Listed on catalogue line 43. |
| FR-5.8 | srs-v1 §4.6: confined to the agents package | `system_analysis.md` footnote `[^fr58]`: confined to CF-6 | Historical wording. |
| FR-8.5 | srs-v1 §4.7 commentary (line 392): "the v2 FR-8.5 visual report, which is a Mermaid diagram" (product v2) | `srs-v2.md` §4.5: FR-8.5 "(new in v2)", Must, a Mermaid report | **Open.** The identifier is not defined in the catalogue (the identifier registry), so it is unclear whether FR-8.5 is a product-v2 requirement or an srs-v2 invention. The authority order does not settle which registry owns the identifier. **Resolved in v1.6:** srs-v2 treated as right; FR-8.5 (Must) and AC-17 are now defined in srs-v1, which owns the identifier. |

## 1.6 (b) Open questions not settled by the authoritative documents

| # | Question | Source |
|---|---|---|
| OQ-1 | Which MVP-phase attempt is the intended build target going forward? srs-v1 is normative by the authority order and by srs-v2 §0.3; srs-v2 says it becomes the target only after an ADR (it removes FR-5.6a and FR-11.2) and authority-table updates. Neither has happened. | `srs-v2.md` §0.3 **Narrowed by the follow-up:** srs-v2's amendments, FR-8.5 and AC-17 are in srs-v1 v1.6; whether its cut should follow is still open. |
| OQ-2 | srs-v1 §0 says ADRs are "normative where cited below", and it cites ADR-0001, ADR-0003, ADR-0004 and ADR-0005, which are **Proposed**. The task's authority order admits only Accepted ADRs. Are the cited Proposed ADRs normative? | srs-v1 §0, §1.4; `Docs/adr/README.md` |
| OQ-3 | ~~Ownership of identifier FR-8.5 (see 1.5).~~ **Closed by the follow-up:** defined in srs-v1 v1.6. | srs-v1 §4.7; `srs-v2.md` |
| OQ-4 | ~~srs-v1 revision history has no 1.2 or 1.3 entry although amendments are dated to them.~~ **Closed by the follow-up:** entries added in v1.6, dated from ADR-0009 and ADR-0010 (2026-09-20). | srs-v1 §0 |
| OQ-5 | Is CF-4 "built"? `CLAUDE.md` says yes; `specs/README.md` assigns CF-4 to feature 004 ("Not started"). This audit marks FR-2.3c, FR-2.5a and FR-2.5c "Not built" on the strength of the latter. | `CLAUDE.md`; `specs/README.md` |
| OQ-6 | AC-10's first clause says no module outside CF-7 imports a terminal-rendering dependency; import contract 1 allows `cli/` to import Rich, and `cli/app.py` line 14 does. Is the CLI adapter inside CF-7? | srs-v1 §6; `pyproject.toml` lines 51–64; `technical_stack.md` §4 |
| OQ-7 | TBD-1 … TBD-8 (resolver latency share, tolerated latency, context cap and split, execution budget, maximum change-set size, catch-rate and false-positive targets, cost target, ceiling default). Placeholders in force for TBD-3, TBD-4, TBD-8. | srs-v1 §8 |
| OQ-8 | The category set's contents ("the values are a product decision"). | srs-v1 §10 "Still open"; `DESIGN_BLOCKERS.md` DB-08 |
| OQ-9 | Missing test script: stop or degrade? FR-9.3 treats it as a prerequisite failure; FR-11.2 and AC-7 require a review saying the tests could not run. (Analyst finding, not decided.) | `system_analysis.md` Q-1 |
| OQ-10 | Depth-0 context units have no relation value among `imports`, `calls`, `imported-by`, `called-by`. (Analyst finding.) | `system_analysis.md` Q-4 |
| OQ-11 | State of the check in flight when the execution budget expires. (Analyst finding.) | `system_analysis.md` Q-6 |
| OQ-12 | No run-metadata field records what CF-4 evicted. (Analyst finding.) | `system_analysis.md` Q-7 |
| OQ-13 | AC-10's CF-1 and CF-7 clauses match no requirement in its Verifies column. (Analyst finding.) | `system_analysis.md` Q-8 |
| OQ-14 | "Parseable tree" is undefined; FR-9.3 treats it as a stop while FR-10.7 (tolerance) is deferred. (Analyst finding.) | `system_analysis.md` Q-11 |
| OQ-15 | The default change scope is not chosen by srs-v1 or any ADR; it is chosen only in design and feature contracts (`working-tree`). | `system_analysis.md` Q-10; `specs/001-walking-skeleton/contracts/config.md` |
| OQ-16 | Nine proposed HLR edits (split HLR-15; reword HLR-6, HLR-3, HLR-9; add type-check, related context, measurement blocks; HLR-7b, HLR-20 status). Proposals, not decisions. | `srs-alignment.md` §3 |
| OQ-17 | FR-5.7a–c conflict with HLR-15 once investigation tools are enabled. (Analyst finding.) | `srs-alignment.md` §1 "What conflicts" |
| OQ-18 | The default model `deepseek-ai/deepseek-v4.1-flash` is commented "chosen by test S-1" (`core/config/settings.py` line 17), but the only S-1 record measured `qwen2.5-coder:7b` locally with zero tool calls. S-1 is unanswered for the default provider. | `technical_stack.md` §7 S-1; `specs/001-walking-skeleton/s1-results.md` **Follow-up:** the comment now reads "to be chosen by test S-1"; the measurement is still missing. |
| OQ-19 | S-2 and S-3 (tree-sitter wheels; sidecar boot cost) are unmeasured. | `technical_stack.md` §7 |
| OQ-20 | Where Langfuse belongs: `technical_stack.md` §4 reserves contract 7 so that only `agents/` may import it (tasks T103), but `core/assembly/prompt.py` line 91 imports it. | `technical_stack.md` §4; `specs/001-walking-skeleton/tasks.md` T102–T103 |
| OQ-21 | Whether runtime dependencies absent from the stack inventory are intended: `jupyter`, `grandalf`, `langchain-ollama`, `langchain`, `groq`, `langfuse` (`pyproject.toml` lines 14–19). | `technical_stack.md` §5, §7 |
| OQ-22 | srs-v2 lists eight gaps its cut would open (findings without a fixed shape, no call-boundary validation, unreported failures, …). They stand as open consequences if srs-v2 is adopted. | `srs-v2.md` §9 |
| OQ-23 | `Docs/README.md` (working-tree change) adds a link to `Draft/enterpenuership/Target/CAI5_IND5_G1-agentic-pr-review-documentation-index.md`, which does not exist; `srs-v2.md`, `system-design.md`, `system-design-block.md` and the CAI5 document are not indexed at all. | `Docs/README.md` line 37 **Closed by the follow-up:** link repointed to `Docs/CAI5_IND5_G1-agentic-pr-review-documentation.md`; the three documents indexed. |

---

# Part 2 — Conformance matrix

**Verdicts.** Conforms: cited implementation line and a cited test that passed in the run above (all 426 passed, so every cited test passed; 427 after the follow-up, all passing). Partial / Does not conform: a cited line shows the gap. Not built: the requirement belongs to CF-2, CF-3 or CF-8 (recorded as not built in `CLAUDE.md` and `specs/README.md`), or to CF-4 work assigned to feature 004 (OQ-5). Unverified: what was searched is stated.

**Spec location.** Taken from the traceability table in `specs/001-walking-skeleton/spec.md` lines 229–266, written qualified.

**Paths.** `src/agentic_review/` is omitted from code paths; tests are `file::test_name`.

**Searches recorded once and referred to below:**

- S-CF2: `grep -rniE "tree_sitter|tree-sitter|ContextProvider|RelatedContext|resolver" src` → one hit, a comment in `core/output/html.py` line 79. No `tree-sitter` in `pyproject.toml`.
- S-CF3: `grep -rniE "subprocess|npm|tsc" src` excluding `core/changeset/_git.py` → one hit, a lockfile name in `core/changeset/exclusion.py` line 18. No check runner.
- S-CF8: `grep -rniE "regression|catch.?rate|pattern.?rule|rules?_dir|load_patterns" src` → only the pass-through node (`agents/pipeline_agent.py` lines 198, 314, 323–324), a prompt comment and the `ruleId` field description. No `regression` command (`--help`).
- S-ISO: `grep -rniE "checkpointer|isolat" tests` → only the test-environment fixture `_isolate_environment` in `tests/conftest.py`.
- S-ACYC: `grep -rniE "acyclic|get_graph|cycle" tests` → no hits.
- S-WRITE: `grep -rnE '"(commit|push|apply|am|checkout|reset|add|stash)"' src` → no hits.
- S-SO: `grep -rniE "structured.output|with_structured_output" src` → `core/findings/report.py` line 131 only.

Notes on srs-v2 appear in a row only where srs-v2 drops or rewords that requirement. "srs-v2: dropped" means listed in srs-v2 §7.1; "srs-v2: not accounted for" means absent from both its kept and dropped lists.

## 2.1 Functional requirements

### CF-1 — Change-set resolution

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-10.3a | spec 001 FR-005 | `core/changeset/resolve.py` 187–232 (working-tree, range); `core/changeset/pull_request.py` 186–264 (pull request); `core/pipeline/preflight.py` 100–158 | `tests/unit/changeset/test_resolve_working_tree.py::test_modified_tracked_file`; `tests/unit/changeset/test_resolve_range.py::test_head_defaults_to_the_current_head`, `::test_the_head_need_not_be_checked_out`; `tests/integration/test_pull_request_scope.py::test_cli_reviews_a_pull_request` | Partial | Gap: `resolve.py` line 198 raises `NotImplementedError` for any other kind; `cli/app.py` line 28 offers only `working-tree` and `range`; no single-commit scope exists (`ScopeKind`, `core/findings/report.py` line 16, has no `commit`). Probe: `scope: staged` in the config file crashed with exit 1; after the follow-up preflight refuses it with exit 3 (`core/pipeline/preflight.py` `RESOLVED_SCOPES`). srs-v2: reworded (three selections). |
| FR-10.3b | spec 001 FR-006 | `core/config/settings.py` line 73 (default `working-tree`); `core/changeset/resolve.py` 205–207 ("(default)" in the description); `core/output/terminal.py` line 36 | `tests/integration/test_story1_review_uncommitted.py::test_scenario1_default_scope_is_stated`; `tests/unit/changeset/test_resolve_working_tree.py::test_scope_description` | Conforms | |
| FR-10.3c | spec 001 FR-007 | `core/changeset/model.py` 40–75 (`ChangedFile`, `ChangeSet`, nothing git-specific); `core/changeset/pull_request.py` 158–177 | `tests/integration/test_pull_request_scope.py::test_a_source_that_never_touches_git_produces_the_same_kind_of_report`; `tests/structural/test_git_confinement.py::test_no_git_invocation_outside_changeset` | Conforms | |
| FR-10.3d | spec 001 FR-032 | `core/pipeline/preflight.py` 121–128 (config never read from a pull request), 150–157 (unreadable pull request stops in preflight, naming it); `core/changeset/pull_request.py` 110–121 (`--no-checkout`, blobless), 49 (no credential helper) | `tests/integration/test_pull_request_scope.py::test_configuration_inside_the_pull_request_is_not_honoured`, `::test_an_unknown_pull_request_stops_before_the_model`; `tests/unit/changeset/test_pull_request.py::test_the_clone_is_blobless_has_no_checkout_and_uses_no_credentials` | Conforms | The git-based reader is interim (ADR-0011). srs-v2: not accounted for. |

### CF-2 — Parsing and related context (not built)

All rows: Spec location none; implementing code: the pass-through node `agents/pipeline_agent.py` lines 187–189; search S-CF2; report depth fields are always null (`core/output/build.py` lines 45–46). Test evidence: none found for the requirement itself (search: `grep -rniE "depth|parse|context" tests` returns only the null-depth assertion in `tests/integration/test_story1_review_uncommitted.py::test_scenario4_absent_capabilities_are_stated`).

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-2.2 | none | none found (S-CF2) | none found | Not built | |
| FR-2.4 | none | none found (S-CF2) | none found | Not built | |
| FR-2.3d | none | none found (S-CF2) | none found | Not built | `ReviewReport.context` is constrained to an empty list (`core/findings/report.py` line 147). |
| FR-2.6a | none | none found (S-CF2) | none found | Not built | `context.depth` is accepted and has no effect (`core/config/settings.py` 31–35), reported as an ignored setting (`core/config/loader.py` 95–111). |
| FR-2.6b | none | none found (S-CF2) | none found | Not built | |
| FR-2.6c | none | none found (S-CF2) | none found | Not built | |
| FR-2.6d | none | none found (S-CF2) | none found | Not built | Degradation codes `no-index` and `unresolvable-imports` exist with no producer (`core/findings/report.py` 29–41). |
| FR-2.6e | none | none found (S-CF2) | none found | Not built | Import contracts 4 and 5 are absent (`pyproject.toml` lines 45–46). |
| FR-2.6f | none | none found (S-CF2) | none found | Not built | |
| FR-2.6g | none | none found (S-CF2) | none found | Not built | |
| FR-2.6h | none | none found (S-CF2) | none found | Not built | `degradations` is already a list (`core/findings/report.py` line 150), so the shape exists. srs-v2: dropped. |

### CF-3 — Execution and evidence (not built)

All rows: implementing code is the pass-through node `agents/pipeline_agent.py` lines 192–194; search S-CF3. The evidence record is fixed at `status: "not-attempted"` with an empty check list (`core/findings/report.py` lines 85–89).

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-4.1 | none | none found (S-CF3) | none found | Not built | `checks.*` settings accepted with no effect (`core/config/settings.py` 38–47). |
| FR-4.2 | none | none found (S-CF3) | none found | Not built | |
| FR-4.4a | none | none found (S-CF3) | none found | Not built | `checks.*.timeoutSeconds` placeholder 120 (`core/config/settings.py` line 42). |
| FR-4.4b | none | none found (S-CF3) | none found | Not built | Code `execution-timed-out` has no producer. |
| FR-4.5a | none | none found (S-CF3) | `tests/integration/test_story1_review_uncommitted.py::test_scenario4_absent_capabilities_are_stated` asserts only `not-attempted` | Not built | `not-attempted` is none of run, skipped, errored. |
| FR-4.5b | none | none found (S-CF3) | none found | Not built | |
| FR-4.5c | none | none found (S-CF3) | none found | Not built | |
| FR-4.6 | none | none found (S-CF3) | `tests/unit/agents/test_binding.py::test_exactly_one_tool_is_bound_with_the_generated_schema` (the only tool is `emit_finding`) | Not built | The prohibition holds trivially today: the only bound tool is `emit_finding` (`agents/review_port.py` 47–48), and nothing runs checks. |
| FR-4.7 | none | none found (S-CF3) | none found | Not built | |
| FR-4.8 | none | none found (S-CF3) | none found | Not built | Under the pull-request scope checks are not executed, but they are recorded as `not-attempted`, not as skipped with a reason (`core/findings/report.py` 85–89). No single-commit scope exists. srs-v2: not accounted for. |

### CF-4 — Context assembly

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-2.3c | none | none found; gap at `core/assembly/prompt.py` line 66 (`"No checks were run. No related context was gathered."`) and 136–144 (diff only) | `tests/unit/assembly/test_prompt.py::test_material_statement` (confirms absence) | Not built | Assigned to feature 004 (OQ-5). |
| FR-2.5 | spec 001 FR-019 | `core/assembly/budget.py` 16–25; `core/assembly/prompt.py` 161–163; `agents/pipeline_agent.py` 215–217, 259–265 | `tests/unit/assembly/test_budget.py::test_an_estimate_above_the_limit_is_budget_exhausted`; `tests/integration/test_story2_failure_modes.py::test_scenario6_diff_over_the_limit`, `::test_cli_budget_exhausted_exits_2_without_calling_the_model` | Conforms | Degradation is a `budget-exhausted` report with no model call (verdict no-judgement, exit 2). The cap is `budget.maxTokens` (placeholder 200,000, `core/config/settings.py` line 68), not the model window less a reserve that TBD-3's placeholder describes. |
| FR-2.5a | none | gap at `core/assembly/budget.py` 24–25 (one estimate over the whole prompt) and `core/config/settings.py` 67–68 (one `max_tokens`) | none found (`grep -rn "section" tests/unit/assembly`) | Not built | No per-section budget. Assigned to feature 004 (OQ-5). |
| FR-2.5b | spec 001 FR-012, FR-019 | `core/assembly/prompt.py` 141–142 (hunk text sent verbatim), 161–163 (refuse rather than truncate) | `tests/unit/assembly/test_prompt.py::test_diff_section_is_verbatim_with_headers`, `::test_estimate_covers_the_whole_prompt`; `tests/unit/assembly/test_budget.py::test_an_estimate_at_the_limit_is_accepted` | Partial | "Never truncate the diff" holds. Gap: no eviction by `distance` exists (`prompt.py` line 66 — no context units). |
| FR-2.5c | none | none found (S-CF3); gap at `core/assembly/prompt.py` line 66 | none found | Not built | No captured check output exists to reduce. |

### CF-5 — Finding model and provider interface

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-0.1 | none (no feature-001 owner) | `core/findings/model.py` 143–246 (`FindingDraft`, `Finding`) | `tests/unit/findings/test_model.py::test_accepts_each_evidence_arm`; `tests/unit/findings/test_schema.py::test_tool_schema_is_the_transform_of_the_model_schema` | Conforms | srs-v2: dropped. |
| FR-0.2 | none | `agents/review_reporting_agent.py` 144–167 (every call goes through `validate_call` into `FindingDraft`); `core/findings/validation.py` 43–60 | `tests/unit/agents/test_graph_happy_path.py::test_prose_is_discarded_and_no_call_is_recorded`, `::test_two_valid_calls_become_two_findings` | Conforms | srs-v2: dropped. |
| FR-0.3 | none (traceability: realised in `core/findings/port.py`) | `core/findings/port.py` 59–62 (`ReviewPort`); `agents/review_port.py` 77–94 (any `BaseChatModel`; default `ChatOpenAI` by base URL and model); `agents/pipeline_agent.py` 63, 230 (port factory) | `tests/unit/agents/test_binding.py::test_exactly_one_tool_is_bound_with_the_generated_schema` (a substituted chat model behind the same port) | Conforms | |
| FR-0.4 | spec 001 FR-028 | `core/findings/schema.py` line 11 (`SCHEMA_VERSION`), 83–90 (`report_schema`); `core/findings/model.py` line 244 (`schema_version` on every finding) | `tests/unit/findings/test_schema.py::test_report_schema_is_versioned_and_valid` | Conforms | The schema is generated in code and documented in `specs/001-walking-skeleton/contracts/review-report.md`; the `schema` command that would publish it (spec 001 FR-028) does not exist. srs-v2: dropped. |
| FR-5.2 | spec 001 FR-014 | `core/findings/model.py` 152–221 | `tests/unit/findings/test_model.py::test_unknown_field_is_rejected`, `::test_start_line_must_be_positive`; `tests/unit/output/test_render.py::test_finding_fields_are_all_shown` | Conforms | srs-v2: dropped. |
| FR-5.2a | spec 001 FR-014 | `core/findings/model.py` line 25; `core/output/verdict.py` line 18 (only `blocking` changes the verdict) | `tests/unit/findings/test_model.py::test_closed_vocabularies`; `tests/unit/output/test_verdict.py::test_verdict_table` | Conforms | srs-v2: dropped. |
| FR-5.2b | spec 001 FR-014 | `core/findings/model.py` 26–34 | `tests/unit/findings/test_model.py::test_closed_vocabularies` | Conforms | Values open as a product decision (OQ-8). srs-v2: dropped. |
| FR-5.2c | spec 001 FR-014 | `core/findings/model.py` 124–140 (evidence union; `unverified` needs a reason), 211–221 (evidence required); `core/findings/validation.py` 87–114 (evidence must exist in this run) | `tests/unit/findings/test_model.py::test_evidence_is_required`, `::test_unverified_needs_a_reason`; `tests/unit/findings/test_validation.py::test_check_evidence_is_rejected_when_no_checks_ran` | Conforms | srs-v2: dropped. |
| FR-5.6 | none | `core/output/build.py` 39, 67–76 (one `ReviewReport` from the outcome); terminal, JSON and HTML all render it (`core/output/terminal.py` 30, `json_out.py` 8–9, `html.py` 26) | `tests/integration/test_story1_review_uncommitted.py::test_scenario5_terminal_and_json_show_the_same_findings` | Conforms | srs-v2: dropped. |
| FR-5.6a | spec 001 FR-013 | `agents/review_port.py` 28–32, 47–48 (tool declared, never executed); `agents/review_reporting_agent.py` 144–177; `core/findings/validation.py` 43–60 | `tests/unit/findings/test_validation.py::test_valid_call_is_accepted`; `tests/unit/agents/test_graph_happy_path.py::test_prose_is_discarded_and_no_call_is_recorded`, `::test_rejected_and_invalid_json_calls_get_error_observations` | Conforms | srs-v2: dropped. |
| FR-5.6b (Should) | none | gap at `core/output/build.py` line 53 (`emit_path="tool-call"` always); `core/findings/report.py` line 131 allows `structured-output` with no producer (S-SO) | none found (S-SO over tests: no hits) | Does not conform | Should: its absence does not block release. S-1 is the measurement meant to decide whether it is pulled forward (OQ-18). srs-v2: dropped. |
| FR-5.6c | spec 001 FR-016 | `agents/review_reporting_agent.py` line 64 (`MAX_REPAIR_TURNS = 1`), 189–209 (repair decision and edge), 306–317 and 327–331 (`invalid-model-output`) | `tests/unit/agents/test_repair_turn.py::test_one_rejected_call_earns_a_repair_turn_with_the_whole_conversation`, `::test_repair_is_taken_at_most_once`; `tests/unit/agents/test_ceiling.py::test_the_repair_turn_uses_no_slot_but_its_calls_do`; `tests/integration/test_story2_failure_modes.py::test_scenario3_repair_failure_with_nothing_accepted`, `::test_outcomes_differ_pairwise` | Conforms | The turn uses no ceiling slot; calls inside it do. A repair turn is also taken when a reviewed file was never named (coverage), which the SRS does not require. srs-v2: dropped. |

### CF-6 — The review agent

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-5.1 | spec 001 FR-011 (traceability names `core/agent/graph.py`, which does not exist) | `agents/review_reporting_agent.py` line 230 (`graph.compile()` with no checkpointer), 255–263 (state built fresh per review) | none found (S-ISO) | Unverified | The isolation is visible in code; no test asserts it. srs-v2: dropped. |
| FR-5.3 | none | gap at `core/assembly/prompt.py` line 66 and `agents/pipeline_agent.py` 192–199 (CF-3 and CF-8 nodes pass state through) | `tests/integration/test_story1_review_uncommitted.py::test_scenario4_absent_capabilities_are_stated` (confirms the model is told no checks ran) | Does not conform | CF-6 is built but receives neither execution results nor rules, because CF-3 and CF-8 are not built. |
| FR-5.7 | spec 001 FR-017 | `core/config/settings.py` line 51 (default 25, labelled placeholder); `core/review/accounting.py` 25–42; `agents/review_reporting_agent.py` 145–148, 295–305, 332–333; `cli/app.py` 99–104, 115–116 | `tests/unit/agents/test_ceiling.py::test_calls_past_the_ceiling_are_denied_and_counted_as_dropped`, `::test_reaching_the_ceiling_exactly_drops_nothing`; `tests/integration/test_story2_failure_modes.py::test_scenario5_ceiling_reached_keeps_findings`, `::test_cli_ceiling_flag_overrides_the_config` | Conforms | srs-v2: amended; text adopted in v1.6, verdict unchanged. |
| FR-5.7a (Should) | spec 001 FR-011 | `core/config/settings.py` line 52 (separate switch, default false) | `tests/unit/config/test_loader.py::test_investigation_tools_true_is_reported` | Partial | Gap: `true` is accepted and ignored (`settings.py` line 52 comment; `core/output/build.py` line 47 hard-codes false; `core/review/accounting.py` line 18). No investigation tool and no versioned tool list exist in code. srs-v2: dropped. |
| FR-5.7b | none | `agents/review_port.py` 47–48 (only `emit_finding` bound); `core/output/build.py` line 47 | `tests/unit/agents/test_binding.py::test_exactly_one_tool_is_bound_with_the_generated_schema`; `tests/unit/config/test_loader.py::test_investigation_tools_true_is_reported` | Conforms | Holds because investigation cannot be enabled at all; no baseline exists yet (CF-8 not built). srs-v2: dropped. |
| FR-5.7c (Should) | none | `agents/review_reporting_agent.py` 332–334 (`ceiling-reached` versus `emitted`) | `tests/unit/agents/test_ceiling.py::test_calls_past_the_ceiling_are_denied_and_counted_as_dropped` | Partial | Gap: no turn is told how many calls remain (search `grep -rn "remaining" src`: no hits). Traceability row spec 001 FR-017 defers it to feature 005. srs-v2: dropped. |
| FR-5.7d (Should) | none | `core/findings/model.py` 237–246 (no ceiling-dependent field) | `tests/integration/test_story2_failure_modes.py::test_scenario5_ceiling_reached_keeps_findings` (findings at ceiling 1 validate against the same schema) | Conforms | srs-v2: dropped. |
| FR-5.8 | spec 001 FR-030 | `pyproject.toml` contracts 3 and 3b (lines 84–100); `agents/pipeline_agent.py` 132–304 (nodes call one core function each), 307–330 (forward edges only) | `tests/structural/test_import_contracts.py::test_every_import_contract_is_kept`; `uv run lint-imports` (contracts 3, 3b kept) | Unverified | The import clause is verified. The acyclic-graph and thin-node clauses have no test (S-ACYC); they hold on inspection only. |
| FR-5.9 | none | `core/findings/model.py` 249–262 (`ok`/`error`/`denied`, reason required unless ok); `agents/review_reporting_agent.py` 145–148, 163–166, 169–177 | `tests/unit/agents/test_ceiling.py::test_calls_past_the_ceiling_are_denied_and_counted_as_dropped`; `tests/unit/agents/test_graph_happy_path.py::test_rejected_and_invalid_json_calls_get_error_observations` | Conforms | `denied` has a producer in this build (calls past the ceiling). srs-v2: dropped. |
| FR-5.10 | spec 001 FR-018 | `agents/review_port.py` line 43 (no `tool_choice`); `agents/review_reporting_agent.py` 290–294 (`no-tool-call`); `core/output/view.py` 18–21 | `tests/unit/agents/test_binding.py::test_no_tool_choice_is_set`; `tests/unit/agents/test_no_tool_call.py::test_a_first_reply_with_no_call_is_no_tool_call`; `tests/unit/output/test_html.py::test_a_no_tool_call_run_is_never_shown_as_clean` | Conforms | |

### CF-7 — Output

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-8.1b | spec 001 FR-024 | `core/output/terminal.py` 36 (scope), 57–58 (states no checks ran), 64–65 (counts), 72 (verdict) | `tests/unit/output/test_render.py::test_required_content_in_order` | Conforms | Checks are reported as not run, which is true of this build. |
| FR-8.2a | spec 001 FR-025 | `core/output/json_out.py` 8–9; `cli/app.py` 129–130 | `tests/unit/output/test_render.py::test_json_round_trips_the_same_report`; `tests/integration/test_html_report.py::test_review_writes_an_html_file_whose_findings_match_the_json_report` | Conforms | Written to a file only; stdout form not offered (`cli/app.py` 30–33). |
| FR-8.2b | none | `core/findings/report.py` 143–151 (report embeds `Finding`); `core/findings/schema.py` 71–80 (tool schema from `FindingDraft` only) | `tests/unit/findings/test_schema.py::test_tool_schema_is_the_transform_of_the_model_schema`, `::test_report_schema_is_versioned_and_valid` | Conforms | srs-v2: amended; text adopted in v1.6. The tool-schema property is still tested here and is still required by FR-5.6a. |
| FR-8.4 (Should) | none | `core/findings/schema.py` 11, 30–34, 83–90 | `tests/unit/findings/test_schema.py::test_report_schema_is_versioned_and_valid` | Conforms | Documented in `specs/001-walking-skeleton/contracts/review-report.md`; not published by a command. |
| FR-10.4a | spec 001 FR-027 | `core/output/terminal.py` 30–72; `core/output/view.py` (shared derivations) | `tests/integration/test_story1_review_uncommitted.py::test_scenario5_terminal_and_json_show_the_same_findings` | Conforms | |
| FR-10.4b | spec 001 FR-025 | `cli/app.py` 105–108, 120, 129–130 | `tests/unit/cli/test_output_files.py::test_an_output_flag_with_a_path_passes_the_guard`; `tests/integration/test_html_report.py::test_review_writes_an_html_file_whose_findings_match_the_json_report` | Conforms | |
| FR-10.4c | spec 001 FR-023 | `cli/exit_codes.py` 7–20; `core/output/verdict.py` 10–20 | `tests/unit/cli/test_exit_codes.py::test_verdict_to_exit_code`, `::test_preflight_exit_code`; `tests/integration/test_story2_failure_modes.py::test_cli_provider_failure_exits_2` | Partial | Gap: `cli/app.py` line 125 calls the pipeline with no handling of an unexpected error, so a crash exits 1 — the code for "found a blocking finding". Probe: `scope: staged` → exit 1 (exit 3 after the follow-up; the uncaught-error path remains). srs-v2: dropped. |
| FR-10.4d (Should) | none (built in tasks Phase 11) | `core/output/html.py` 26–73 (autoescape on, strict undefined); `core/output/load.py` 23–54; `cli/app.py` 137–164 (`render`) | `tests/unit/output/test_html.py::test_model_authored_prose_is_escaped_and_never_executed`, `::test_the_document_is_one_self_contained_html_file`, `::test_a_no_tool_call_run_is_never_shown_as_clean`; `tests/unit/cli/test_render_command.py::test_render_reproduces_what_review_would_have_written`; `tests/structural/test_template_escaping.py::test_the_template_fetches_nothing_and_runs_nothing` | Conforms | srs-v2: not accounted for. |
| FR-8.2c | spec 001 FR-026 | `core/findings/report.py` 118–140; `core/output/build.py` 40–66 | `tests/integration/test_story1_review_uncommitted.py::test_scenario4_absent_capabilities_are_stated`; `tests/integration/test_pull_request_scope.py::test_range_report_records_both_refs` | Partial | Gap: requested and achieved depth are always null (`core/output/build.py` 44–45) until CF-2 exists. Ceiling, investigation flag, completion status, model, schema version and scope are recorded; under v1.6 the completion status `ceiling-reached` is what records whether the ceiling was reached. srs-v2: amended; text adopted in v1.6. |
| FR-8.2d | none | `core/findings/report.py` 126–129; `core/review/accounting.py` 16–19, 39–42 | `tests/unit/agents/test_ceiling.py::test_the_repair_turn_uses_no_slot_but_its_calls_do` | Conforms | Investigation count is always 0 (no tools). srs-v2: amended; text adopted in v1.6 (minimum now total and emitting). |
| FR-8.5 | none | none found (`grep -rniI mermaid src tests`: no hits) | none found | Not built | Added in srs-v1 v1.6 from srs-v2. CF-7 is built, so this is a missing CF-7 surface, not an unbuilt block. |
| FR-8.2e | spec 001 FR-022 (traceability names `core/pipeline/run.py`, which does not exist) | `core/findings/report.py` 92–95, 150; `agents/pipeline_agent.py` 268–279; `agents/provider_errors.py` 27–56 | `tests/integration/test_story2_failure_modes.py::test_scenario1_provider_failure_is_no_judgement`; `tests/unit/output/test_html.py::test_degradations_are_listed_with_source_code_and_detail` | Conforms | srs-v2: dropped. |

### CF-8 — Pattern library and regression harness (not built)

All rows: implementing code is the pass-through node `agents/pipeline_agent.py` lines 197–199; search S-CF8; no `regression` command.

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-6.1 | none | none found (S-CF8) | none found | Not built | |
| FR-6.2a | none | none found (S-CF8) | `tests/unit/findings/test_validation.py::test_rule_id_is_discarded_when_no_rules_are_loaded` (shows the field is discarded) | Not built | With no rules loaded, any `ruleId` is discarded (`core/findings/validation.py` 51–56). |
| FR-6.2b | none | none found (S-CF8) | none found | Not built | srs-v2: dropped. |
| FR-6.2d | none | none found (S-CF8) | none found | Not built | srs-v2: dropped. |
| FR-6.2e (Should) | none | none found (S-CF8) | none found | Not built | srs-v2: dropped. |
| FR-6.2f | none | none found (S-CF8) | none found | Not built | A position-independent fingerprint exists (`core/findings/fingerprint.py`), not a catch predicate. srs-v2: dropped. |
| FR-6.3a | none | none found (S-CF8) | none found | Not built | srs-v2: amended; text adopted in v1.6 (no regression case per rule). |

### CF-9 — Configuration and diagnostics

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-1.2a | spec 001 FR-002 | `core/pipeline/preflight.py` line 38, 124–126; `core/config/loader.py` 35–69 | `tests/unit/config/test_loader.py::test_per_field_merge`, `::test_scope_named_by_file_is_recorded` | Conforms | srs-v2: dropped. |
| FR-1.2b | spec 001 FR-002 | `core/config/loader.py` 37–40; `core/config/settings.py` 71–78 | `tests/unit/config/test_loader.py::test_absent_file_gives_defaults`; `tests/unit/config/test_settings.py::test_defaults` | Conforms | srs-v2: dropped. |
| FR-1.2c | spec 001 FR-002 | `core/config/settings.py` 31–78 (a default on every field) | `tests/unit/config/test_loader.py::test_per_field_merge`, `::test_empty_file_gives_defaults` | Conforms | srs-v2: dropped. |
| FR-1.2d | spec 001 FR-002, FR-003 | `core/config/settings.py` 21–28 (`extra="forbid"`); `core/config/loader.py` 47–67 | `tests/unit/config/test_loader.py::test_unknown_field_is_named`, `::test_invalid_value_is_named`, `::test_duplicate_key_is_an_error`, `::test_yaml_syntax_error_names_line_and_column` | Conforms | `scope: staged` is a valid value under the documented schema, so its crash is recorded under FR-10.3a, FR-10.4c, FR-9.3 and FR-11.2, not here. srs-v2: dropped. |
| FR-1.3a | spec 001 FR-004 | `core/config/credentials.py` 55–107 (environment, then user file), 85–90 (a file inside the repository is refused); `core/config/settings.py` (no credential field) | `tests/unit/config/test_credentials.py::test_environment_wins`, `::test_user_file_inside_repository_is_refused`; `tests/unit/config/test_settings.py::test_no_field_can_hold_a_credential`; `tests/unit/config/test_loader.py::test_api_key_is_an_unknown_field` | Conforms | srs-v2: dropped. |
| FR-3.5 | spec 001 FR-008 | `core/changeset/exclusion.py` 13–49; `core/changeset/resolve.py` 101–109 (applied at resolution); `core/findings/report.py` 59–61 (`ExcludedPath` recorded) | `tests/unit/changeset/test_exclusion.py::test_default_rules_are_named`, `::test_adding_a_pattern_keeps_every_default`; `tests/unit/changeset/test_resolve_working_tree.py::test_excluded_paths_are_recorded_not_listed`; `tests/unit/changeset/test_resolve_range.py::test_exclusions_apply_to_a_range` | Conforms | |
| FR-9.1 | none | CLI usage: `cli/app.py` help text; `Docs/operation_guidelines.md` | none found | Partial | Gap: no README or LICENSE (`git ls-files | grep -iE "readme|license|copying"` finds only `Docs/**/README.md` and `specs/README.md`; `pyproject.toml` lines 1–5 declare neither). Follow-up: `README.md` added; LICENSE still absent. srs-v2: dropped. |
| FR-9.3 | spec 001 FR-001 | `core/pipeline/preflight.py` 100–158 (git missing, not a repository, configuration, scope arguments, credential, refs, pull request) | `tests/unit/pipeline/test_preflight.py::test_the_credential_is_checked_before_any_ref`, `::test_range_without_a_base_names_the_option`, `::test_a_pull_request_that_cannot_be_read_is_a_preflight_failure`; `tests/unit/config/test_credentials.py::test_missing_names_both_places` | Partial | Gap: no test-script check (`preflight.py` lines 3–4 say so; feature 002); a configured `staged` scope ended in a traceback, not a message (probe; fixed in the follow-up, `tests/unit/pipeline/test_preflight.py::test_a_scope_this_build_cannot_resolve_is_refused_before_resolution`). srs-v2: dropped. |

### Cross-cutting

| Requirement ID | Spec location | Implementing code | Test evidence | Verdict | Evidence note |
|---|---|---|---|---|---|
| FR-10.1 | none | `cli/app.py` 67–134; `core/changeset/pull_request.py` 47–49 (no token, no API) | `tests/integration/test_story1_review_uncommitted.py::test_cli_review_with_no_options` | Conforms | srs-v2: dropped. |
| FR-10.2 | spec 001 FR-030 | `core/output/verdict.py` 13–20 (verdict in core); `cli/exit_codes.py` 19–20 (lookup only); `pyproject.toml` contract 6 | `tests/unit/output/test_verdict.py::test_verdict_table`; `tests/structural/test_import_contracts.py::test_every_import_contract_is_kept` | Conforms | |
| FR-9.2a | none | not demonstrable offline | none found; maintainer tasks T101 and T127 (live runs) are open in `specs/001-walking-skeleton/tasks.md` | Unverified | Needs a live run on a free provider tier. The only S-1 record shows a local model making zero tool calls. srs-v2: dropped. |
| FR-11.1 | spec 001 FR-019 | `core/review/accounting.py` 25–34 (call budget); `core/assembly/prompt.py` 161–163 (token estimate before the call) | `tests/unit/agents/test_ceiling.py::test_calls_past_the_ceiling_are_denied_and_counted_as_dropped`; `tests/unit/assembly/test_budget.py::test_an_estimate_above_the_limit_is_budget_exhausted` | Partial | Gap: tokens actually spent are summed but never compared with a limit (`core/review/accounting.py` 57–61), so a repair turn's tokens are unbounded by the token budget. srs-v2: dropped. |
| FR-11.2 | spec 001 FR-020, FR-022 | `agents/review_reporting_agent.py` 97–133, 279–334; `agents/provider_errors.py` 19–56; `agents/pipeline_agent.py` 239–279 | `tests/integration/test_story2_failure_modes.py::test_scenario1_provider_failure_is_no_judgement`, `::test_scenario4_no_tool_call`, `::test_scenario6_diff_over_the_limit`, `::test_outcomes_differ_pairwise`; `tests/unit/agents/test_provider_errors.py::test_each_provider_failure_is_a_provider_error` | Partial | Gap: the "checks unrunnable" mode cannot occur (CF-3 not built); an unexpected error after preflight produces no report (`cli/app.py` line 125; tasks T096 open). The probe's staged crash is closed by the follow-up. srs-v2: dropped. |
| FR-11.3 (Should) | spec 001 FR-021, FR-026, FR-029 | `core/findings/report.py` 103–140; `core/pipeline/timing.py` 12–23 | `tests/integration/test_story1_review_uncommitted.py::test_scenario4_absent_capabilities_are_stated`; `tests/unit/agents/test_graph_happy_path.py::test_tokens_are_none_when_not_reported` | Partial | Gap: achieved depth is null (`core/output/build.py` 44–45); checks executed are always none. Scope, tokens and stage durations are recorded. srs-v2: dropped. |
| FR-7.2 | none | No write path found (S-WRITE). The only git writes are `git config` inside a temporary clone (`core/changeset/pull_request.py` 233–234) | none found | Unverified | Satisfied by absence on inspection; no test asserts the absence. srs-v2: dropped. |

**Verdict totals (86):** Conforms 37 · Partial 11 · Does not conform 2 · Not built 32 · Unverified 4 (FR-5.1, FR-5.8, FR-7.2, FR-9.2a). Counted mechanically from the Verdict column above. Before the follow-up: 85 rows, Not built 31; adding FR-8.5 is the only change to the totals.

## 2.2 Acceptance criteria

| AC | Verifies | Evidence | Verdict | Note |
|---|---|---|---|---|
| AC-1 | FR-9.2a, FR-10.1 | No live run recorded; T101 open | Unverified | Needs a real provider key and network. |
| AC-2 | FR-4.5c, FR-5.3, FR-4.2 | CF-3 not built | Not built | Amended in v1.6 (srs-v2's text): a run of its own whose change breaks a test or the type-check. |
| AC-3 | FR-8.2b, FR-8.2c | `tests/support/report_assertions.py` `assert_valid_report` used by `tests/integration/test_story2_failure_modes.py::_check`; `tests/unit/findings/test_schema.py::test_report_schema_is_versioned_and_valid` | Partial | JSON validates against the generated schema and records model and scope. Gap: depth is null (`core/output/build.py` 44–45); no published schema artefact or `schema` command. |
| AC-4 | FR-6.2a | CF-8 not built | Not built | |
| AC-5 | FR-6.2b, FR-6.2d | CF-8 not built | Not built | Flagged by srs-v1 as one of two to defend. |
| AC-6 | FR-6.2d, FR-2.6a | CF-2, CF-8 not built | Not built | |
| AC-7 | FR-4.5a, FR-11.2 | CF-3 not built | Not built | Flagged by srs-v1 as one of two to defend. |
| AC-8 | FR-2.6d | CF-2 not built | Not built | |
| AC-9 | FR-1.2d, FR-9.3 | `tests/unit/config/test_loader.py::test_unknown_field_is_named`; `tests/unit/config/test_credentials.py::test_missing_names_both_places`; `tests/unit/pipeline/test_preflight.py::test_a_missing_credential_never_costs_a_fetch` | Conforms | "Neither costs a check execution" holds because no check is ever executed. |
| AC-10 | FR-10.2, FR-2.6e, FR-5.8 | `uv run lint-imports` (6 kept); `tests/structural/test_import_contracts.py::test_every_import_contract_is_kept`; `tests/structural/test_git_confinement.py::test_no_git_invocation_outside_changeset` | Partial | Framework and git clauses verified. Gap: the CF-2 clause has no contract (contracts 4, 5 absent, `pyproject.toml` lines 45–46); the CF-7 clause is open (OQ-6). |
| AC-11 | FR-5.7b, FR-6.2d, FR-6.2e, FR-8.2d | CF-8 and investigation tools not built | Not built | |
| AC-12 | FR-2.6f, FR-2.6g, FR-11.2 | CF-2 not built | Not built | |
| AC-13 | FR-5.6c | `tests/unit/agents/test_repair_turn.py::test_one_rejected_call_earns_a_repair_turn_with_the_whole_conversation`; `tests/integration/test_story2_failure_modes.py::test_scenario3_repair_failure_with_nothing_accepted`, `::test_outcomes_differ_pairwise` | Conforms | |
| AC-14 | FR-2.6h, FR-8.2e | CF-2 not built | Not built | |
| AC-15 | FR-5.2c | `tests/unit/findings/test_model.py::test_evidence_is_required`, `::test_unverified_needs_a_reason`; `tests/unit/findings/test_validation.py::test_unverified_evidence_is_accepted` | Conforms | |
| AC-16 | FR-5.10 | `tests/integration/test_story2_failure_modes.py::test_scenario4_no_tool_call`, `::test_outcomes_differ_pairwise`; `tests/unit/output/test_html.py::test_a_no_tool_call_run_is_never_shown_as_clean` | Conforms | |
| AC-17 | FR-8.5 | none found (`grep -rniI mermaid src tests`: no hits) | Not built | New in v1.6 (from srs-v2). No mechanism is designed yet (`Docs/design/06-verification.md` §3). |

---

# Part 3 — Consolidated requirements document

## 3.0 About this consolidation

This part restates the current normative requirements: srs-v1 v1.6 (v1.5 before the follow-up) for every requirement, and `Docs/technical_stack.md` for technology selection only. Each requirement keeps its original identifier and Must/Should tag, and its text is srs-v1's, with explanatory commentary left out. Each is followed by its source and its verdict from Part 2. Where srs-v2, the catalogue or a feature document says the same thing, the requirement appears once. Diagrams, user stories and analysis tables are not reproduced; they are cited by path.

Background, rationale and diagrams: `Docs/agentic-code-review-srs-v1.md` §1–§3, §9; `Docs/Draft/mvp-scope.md`; ADR-0001 … ADR-0011 (`Docs/adr/`); `Docs/design/`.

Definitions used below are srs-v1 §1.3 (change set, context depth, context unit, core, adapter, evidence record, finding, finding model, pattern rule, regression harness, host language, resolver sidecar, Must/Should). Must is required for the version to be complete; Should is included if time allows and its absence does not block release.

### Core functions

Requirements are grouped by srs-v1's nine function blocks (from: `Docs/agentic-code-review-srs-v1.md`, §3): CF-1 change-set resolution; CF-2 parsing and related context; CF-3 execution and evidence; CF-4 context assembly; CF-5 finding model and provider interface; CF-6 the review agent; CF-7 output; CF-8 pattern library and regression harness; CF-9 configuration and diagnostics; plus cross-cutting requirements.

## 3.1 CF-1 — Change-set resolution

- **FR-10.3a (Must)** The system shall resolve the change scope from an explicit selection among: uncommitted working-tree changes, staged changes only, a comparison against a named branch or commit, the changes introduced by a single named commit, or a public pull request named by its URL. A comparison reviews the current head unless another ref is named.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.1) · Verdict: Partial
- **FR-10.3b (Must)** The system shall apply a documented default change scope when none is specified, and shall state the resolved scope in its output.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.1) · Verdict: Conforms
- **FR-10.3c (Must)** The resolved change set shall be expressed as a list of changed files and diff hunks, in a structure independent of how it was resolved.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.1) · Verdict: Conforms
- **FR-10.3d (Must)** When the change set comes from a pull request, the system shall execute nothing from it and shall read no configuration from it. A pull request that cannot be read shall stop the run before any model call, with a message naming the pull request.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.1; decided in ADR-0011) · Verdict: Conforms

## 3.2 CF-2 — Parsing and related context

- **FR-2.2 (Must)** The system shall build a syntax tree for changed TS/JS files in the host process, without invoking the target language's toolchain, and shall tolerate a parse failure on any single file by reporting it rather than failing the invocation.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2) · Verdict: Not built
- **FR-2.4 (Should)** The system shall include relevant surrounding context — function, class, and type boundaries — rather than raw line windows.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2) · Verdict: Not built
- **FR-2.3d (Must)** The system shall record which related files were included and why, for traceability.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2) · Verdict: Not built

Context depth ladder: depth 0 is the changed hunks expanded to enclosing function, class or type boundaries; depth 1 is the definitions of symbols the changed code imports and calls; v1 implements depths 0 and 1. Depths 2 and 3 are product v2. (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.1)

- **FR-2.6a (Must)** The system shall expose related-context retrieval through a single interface parameterised by depth, with the implementation selected at run time.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.2) · Verdict: Not built
- **FR-2.6b (Must)** v1 shall provide a parser-backed implementation serving depths 0 and 1 without requiring any repository-wide index.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.2) · Verdict: Not built
- **FR-2.6c (Must)** Every returned context unit shall carry the relation by which it was included (`imports`, `calls`, `imported-by`, `called-by`) and its distance from the change.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.2) · Verdict: Not built
- **FR-2.6d (Must)** A retrieval result shall state the depth actually achieved and, where that is lower than requested, every reason it was lower. The system shall not silently downgrade.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.2) · Verdict: Not built
- **FR-2.6e (Must)** No consumer of the interface shall branch on which implementation served the request.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.2) · Verdict: Not built
- **FR-2.6f (Must)** Depth-1 module-specifier resolution shall use the target language's own resolution algorithm, so that path aliases, directory index files, package export maps, and workspace links resolve as that language's toolchain resolves them. The resolver shall be shipped with the package rather than fetched at review time, shall not be observable outside CF-2 (FR-2.6e), and shall consume no more than the share of the review latency budget set in §8 (TBD-1).
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.2) · Verdict: Not built
- **FR-2.6g (Must)** Where authoritative resolution is unavailable or fails, the system shall fall back to heuristic path resolution, mark the retrieval result degraded with a machine-readable reason distinguishing unresolved imports from successful resolution, and complete the review. The absence of the resolver shall never fail an invocation (FR-11.2).
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.2) · Verdict: Not built
- **FR-2.6h (Must)** Where more than one condition degrades a retrieval, the result shall carry all of them. A result shall not be able to report only one of several simultaneous degradations.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.2) · Verdict: Not built

Interface obligations (normative; the declaration belongs to design): retrieval is requested at a depth, and depth is a request rather than a guarantee; every returned unit carries its relation and distance; every result states the depth achieved; a lower depth is reported with every reason; no consumer branches on the implementation; each implementation declares the maximum depth it can serve. Whether retrieval is synchronous or concurrent is not specified. v1 implementation: `ParserContextProvider`, maximum depth 1. (from: `Docs/agentic-code-review-srs-v1.md`, §4.2.3; signatures in `Docs/design/02-domain-model.md` and `Docs/design/04-contracts.md`)

## 3.3 CF-3 — Execution and evidence

- **FR-4.1 (Must)** The system shall run the project's test suite on the developer's machine and capture pass/fail results and output.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3) · Verdict: Not built
- **FR-4.2 (Must)** The system shall run build/type checks (e.g. `tsc`) and capture results.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3) · Verdict: Not built
- **FR-4.4a (Must)** The system shall enforce a configurable time budget on the execution phase and terminate execution when it is exceeded.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3) · Verdict: Not built
- **FR-4.4b (Must)** On termination due to timeout, the system shall mark execution as `timed-out`, skip remaining checks, and continue to produce a review reporting the timeout.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3) · Verdict: Not built
- **FR-4.5a (Must)** The system shall record, for each check, whether it was run, skipped, or errored.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3) · Verdict: Not built
- **FR-4.5b (Must)** The system shall record each executed check's pass/fail result and captured output.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3) · Verdict: Not built
- **FR-4.5c (Must)** The system shall make this execution record available to the review agent and include it in the structured output.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3) · Verdict: Not built
- **FR-4.6 (Must)** The review agent shall not be able to trigger check execution. Execution occurs once per invocation, before the review pass.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3; ADR-0002) · Verdict: Not built
- **FR-4.7 (Must)** Checks shall be executed as subprocesses invoking the reviewed project's own toolchain and package manager, discovered from its manifest or named in configuration. The system shall not import the reviewed project's dependencies into the host runtime, and shall not require the reviewed project to install anything belonging to the system.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3; ADR-0007) · Verdict: Not built
- **FR-4.8 (Must)** Under the single-commit and pull-request change scopes (FR-10.3a) the system shall not execute checks. Each check shall be recorded as skipped (FR-4.5a) with a reason stating that checks do not apply to that scope, and the review agent shall be told that no check was run.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.3) · Verdict: Not built

## 3.4 CF-4 — Context assembly

- **FR-2.3c (Must)** The system shall include the source of related definitions and call sites in the review context passed to the agent, up to the context cap.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.4) · Verdict: Not built
- **FR-2.5 (Must)** The system shall cap context size to stay within model token limits, degrading gracefully when exceeded.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.4) · Verdict: Conforms
- **FR-2.5a (Must)** Context shall be budgeted per section — instructions and rules, the diff, related context, and evidence — so that no section can starve another.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.4) · Verdict: Not built
- **FR-2.5b (Must)** When the budget is exceeded, the system shall evict context units in descending order of `distance`, and shall never truncate the diff itself.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.4) · Verdict: Partial
- **FR-2.5c (Must)** Captured check output shall be reduced to failing test names, assertion messages, and stack frames referring to changed files before entering the context. Full output is retained for the structured output only.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.4) · Verdict: Not built

## 3.5 CF-5 — Finding model and provider interface

- **FR-0.1 (Must)** The system shall define a provider-independent internal finding representation — "the finding model" — as the single canonical structure for all review findings.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-0.2 (Must)** All model output shall be converted into the finding model before any downstream use; no component shall consume raw provider responses directly.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-0.3 (Must)** A new provider shall be integratable by mapping its output to the finding model without changes to downstream components. The system shall define this as a provider-independent interface; the client implementing it may live in CF-6, so that FR-5.8's confinement of the agent framework is not breached by CF-5.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-0.4 (Must)** The finding model shall have a documented, versioned schema carrying a schema-version field.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-5.2 (Must)** Each finding shall contain: file path, line or line-range, severity, category, rationale, and optionally the identifier of a matched pattern rule.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-5.2a (Must)** Severity shall be one of `blocking`, `important`, `nit`. `blocking` carries the blocking/non-blocking distinction deferred as FR-5.4 until that requirement lands, and is the only value that affects exit status (FR-10.4c).
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-5.2b (Must)** Category shall be one of: `correctness`, `error-handling`, `interface-contract`, `test-evidence`, `security`, `performance`, `maintainability`. The set is closed, so that a category can be counted, filtered, and compared across runs; it is fixed in the finding-model schema and changing it is a schema change (FR-0.4).
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-5.2c (Must)** Each finding shall carry an evidence reference identifying what supports it — a recorded check result, a related-context unit, or the change itself — or shall be explicitly marked unverified, with a reason. A finding shall not be emitted carrying neither.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-5.6 (Must)** The agent's output shall conform to the finding model; all outputs shall be derived from it, not produced independently by the model.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms
- **FR-5.6a (Must)** Findings shall enter the system exclusively through an `emit_finding` tool call validated against the finding-model schema at the call boundary. Prose the model produces shall not be parsed for findings.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5; ADR-0004) · Verdict: Conforms
- **FR-5.6b (Should)** Where the provider cannot perform tool calls, the system shall fall back to schema-validated structured output with a documented retry cap, and shall report which path was used.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Does not conform
- **FR-5.6c (Must)** Where an `emit_finding` call fails validation, the system shall return the offending field to the model and permit one repair turn per review. A repair turn is not an investigation and does not consume the tool-call ceiling (FR-5.7). Where the repair turn also fails validation, the run shall record that the model's output could not be validated, and that run shall be distinguishable in both outputs from a run that found nothing.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.5) · Verdict: Conforms

## 3.6 CF-6 — The review agent

- **FR-5.1 (Must)** The review agent shall operate in a context isolated from any code-writing agent — no shared history or state.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6) · Verdict: Unverified
- **FR-5.3 (Must)** The agent shall incorporate execution results (CF-3) and pattern-library rules (CF-8) into its findings.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6) · Verdict: Does not conform
- **FR-5.7 (Must)** The review step shall enforce a tool-call ceiling: a configuration value bounding the total number of tool calls the model may make in one review, counted as an agent runtime counts them — every call, including the calls that hand over findings (FR-5.6a). Its documented default shall be a positive number sized to stop a runaway agent without truncating a review a reader would have wanted. Reaching the ceiling shall be reported, and findings emitted before it was reached shall be retained.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6; ADR-0008, amended in v1.6 from `Docs/agentic-code-review-srs-v2.md`) · Verdict: Conforms
- **FR-5.7a (Should)** Whether investigation tools are exposed to the model shall be a separate configuration value from the ceiling, defaulting to off. When they are enabled, every such tool shall be read-only, free of side effects, and unable to trigger check execution (FR-4.6). The tools exposed shall be a documented, versioned list.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6) · Verdict: Partial
- **FR-5.7b (Must)** Investigation tools shall not be enabled until a single-pass baseline catch rate has been recorded on the regression corpus (FR-6.2d). Any subsequent configuration shall be justified by a measured comparison against that baseline.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6) · Verdict: Conforms
- **FR-5.7c (Should)** When investigation tools are enabled, each model turn shall be told how many tool calls remain, and the review shall report whether it ended because the agent finished or because the ceiling was reached.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6) · Verdict: Partial
- **FR-5.7d (Should)** Findings shall have the same structure and meaning at every ceiling value. A change of ceiling shall change how much is found, never what a finding is.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6) · Verdict: Conforms
- **FR-5.8 (Must)** The agent framework shall be confined to the agents package, which holds the pipeline orchestrator and CF-6's review step and nothing else. No core package shall import it, and every pipeline step outside CF-6 shall be callable as an ordinary function without it. Where the orchestrator expresses the fixed order as a graph, each node shall be a thin adapter over a core function that holds no orchestration logic of its own, and the orchestrator's graph shall be acyclic — CF-6 remains the only step in which a cycle may occur.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6; ADR-0009, ADR-0010) · Verdict: Unverified
- **FR-5.9 (Must)** Every tool result returned to the model shall be a structured observation carrying a status — at minimum ok, error, and denied — and, where the status is not ok, a reason. A refused call shall be returned as denied, distinct from an error, so that the model can choose a different action rather than retrying the same one.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6) · Verdict: Conforms
- **FR-5.10 (Must)** The system shall not oblige the model to make a tool call. A reply containing no tool call is the model's termination signal and shall be accepted as one. Where such a reply produces no findings, the run shall record that no tool call was made, so that a review which found nothing is distinguishable from one in which the model never used the tool.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.6; ADR-0008) · Verdict: Conforms

## 3.7 CF-7 — Output

- **FR-8.1b (Must)** The terminal summary shall state the resolved change scope, the checks run and their results, the count of findings by severity, and an overall verdict.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7) · Verdict: Conforms
- **FR-8.2a (Must)** The system shall serialize the review's result to JSON as a machine-readable artifact.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7) · Verdict: Conforms
- **FR-8.2b (Must)** The artifact shall conform to a documented, versioned review-report schema containing the findings, the evidence record, and the run metadata of FR-8.2c. The finding model (FR-0.1) is the findings portion of that schema and nothing more: the report is a wider structure that embeds it. Both are versioned together.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7, amended in v1.6 from `Docs/agentic-code-review-srs-v2.md`) · Verdict: Conforms
- **FR-8.4 (Should)** The structured output schema shall be documented and versioned.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7) · Verdict: Conforms
- **FR-10.4a (Must)** The system shall render findings to the terminal, derived from the finding model and not produced independently.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7) · Verdict: Conforms
- **FR-10.4b (Must)** The system shall provide machine-readable output on request, conforming to the schema in FR-8.2b.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7) · Verdict: Conforms
- **FR-10.4c (Must)** The system shall exit with a status code reflecting the review outcome, documented and stable across versions. The codes shall distinguish at least four outcomes: a review that completed; a review that completed and found a `blocking` finding; a review that could not be produced because the model was unreachable or its output could not be validated; and an invocation that could not start because a prerequisite was missing. A review that completed in a degraded state shall report as completed, because a degraded review is still a review (FR-11.2).
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7) · Verdict: Partial
- **FR-10.4d (Should)** The system shall render a review's result to a self-contained HTML document on request, derived from the same review-report structure as the terminal summary and the JSON artifact (FR-8.2b) and not produced independently. One renderer shall serve both a rendering taken during a review and a rendering taken from a previously written JSON report. The document shall state the resolved change scope, every finding with its evidence reference, the counts by severity, every degradation, the run metadata of FR-8.2c–e, and the verdict; it shall preserve the distinction FR-5.10 requires between a change that was reviewed and found nothing and a run in which the model never used the tool; and it shall reference no network resource and execute no script, so that model-authored text in a finding's rationale or a degradation's detail is displayed and never interpreted.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7) · Verdict: Conforms

- **FR-8.5 (Must)** The system shall produce, on request, a visual report of the review as a Mermaid diagram, derived from the same findings as the terminal summary and the JSON artifact and not produced independently. The diagram shall be valid Mermaid that renders. What the diagram shows is a design decision.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7, new in v1.6 from `Docs/agentic-code-review-srs-v2.md` §4.5) · Verdict: Not built
- **FR-8.2c (Must)** The structured output shall record the requested and achieved context depth; the tool-call ceiling in force and whether it was reached; the model and schema versions used; and the resolved change scope — so a run can be reproduced and compared.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7, amended in v1.6 from `Docs/agentic-code-review-srs-v2.md`) · Verdict: Partial
- **FR-8.2d (Must)** The structured output shall record tool calls as both a total and a breakdown by purpose — at minimum the total and the number spent emitting findings. A single total shall not be the only figure reported.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7, amended in v1.6 from `Docs/agentic-code-review-srs-v2.md`) · Verdict: Conforms
- **FR-8.2e (Must)** The structured output shall record every degradation that occurred during the run, each identifying the stage that raised it and a machine-readable reason. This is the record FR-11.2's reporting obligation is discharged into.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.7) · Verdict: Conforms

## 3.8 CF-8 — Pattern library and regression harness

- **FR-6.1 (Must)** The system shall load a configurable pattern library of "wrong vs. correct" examples and project standards.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.8) · Verdict: Not built
- **FR-6.2a (Must)** When a finding is generated from a pattern-library rule, the finding shall reference the identifier of the matched rule.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.8) · Verdict: Not built
- **FR-6.2b (Must)** The system shall support a regression set of pattern examples with expected outcomes, runnable as a test, so pattern-matching behaviour can be verified and monitored across changes.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.8) · Verdict: Not built
- **FR-6.2d (Must)** The regression harness shall report a catch rate over the corpus, and shall accept both a context depth and a tool-call ceiling so that results at different settings are directly comparable.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.8) · Verdict: Not built
- **FR-6.2e (Should)** Regression runs shall pin the settings that affect reproducibility — depth, ceiling, model, and sampling parameters — and record them with the result, so that measurement runs stay comparable even where production runs vary.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.8) · Verdict: Not built
- **FR-6.2f (Must)** The harness shall apply a documented rule for deciding when an emitted finding counts as catching an expected defect, and that rule shall be independent of line numbers, so that an unrelated edit shifting a file does not change the score. The corpus shall include cases containing no defect, and the harness shall report a false-positive figure alongside the catch rate.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.8) · Verdict: Not built
- **FR-6.3a (Must)** v1 shall ship at least five pattern rules, each with a wrong example and a correct example.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.8, amended in v1.6 from `Docs/agentic-code-review-srs-v2.md`) · Verdict: Not built

## 3.9 CF-9 — Configuration and diagnostics

- **FR-1.2a (Must)** The system shall read configuration from `.agentic-review.yml` at the repository root when present.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.9) · Verdict: Conforms
- **FR-1.2b (Must)** When the file is absent, the system shall apply a documented built-in default configuration.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.9) · Verdict: Conforms
- **FR-1.2c (Must)** When the file is present but a field is missing, the system shall apply that field's documented default value.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.9) · Verdict: Conforms
- **FR-1.2d (Must)** When the file is present but malformed, the system shall fail with an error message identifying the offending field, and shall not fall back silently.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.9) · Verdict: Conforms
- **FR-1.3a (Must)** The system shall read the model provider credential from the local environment or user-level configuration, never from a hard-coded key and never from a file committed to the repository.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.9) · Verdict: Conforms
- **FR-3.5 (Must)** The system shall exclude configured generated, vendored, and build-output paths from review, using a documented default exclusion list. The exclusion shall be applied when the change set is resolved (CF-1), so that no later stage parses, executes against, or budgets for a file that was never going to be reviewed, and the resolved change set shall record what was excluded so that the stated scope (FR-10.3b) is true.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.9) · Verdict: Conforms
- **FR-9.1 (Must)** The system shall ship with README, LICENSE, and CLI usage documentation.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.9) · Verdict: Partial
- **FR-9.3 (Must)** The system shall provide clear failure messages when prerequisites — a test script, a provider key, a git repository, a parseable tree — are missing or unusable.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.9) · Verdict: Partial

## 3.10 Cross-cutting

- **FR-10.1 (Must)** The system shall provide a command-line interface that reviews a local change set without requiring GitHub API access or repository credentials.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.10) · Verdict: Conforms
- **FR-10.2 (Must)** No adapter shall contain logic that determines whether something is a finding.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.10; ADR-0006) · Verdict: Conforms
- **FR-9.2a (Must)** The system shall complete an end-to-end review of a public TS/JS repository on a developer machine, using only a free model provider tier.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.10) · Verdict: Unverified
- **FR-11.1 (Must)** The system shall enforce a token and call budget per invocation and stop cleanly when it is reached, reporting that it did so.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.10) · Verdict: Partial
- **FR-11.2 (Must)** The system shall produce a review under every failure mode — checks unrunnable, context over budget, provider error, budget exhausted — reporting the degradation rather than exiting silently.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.10) · Verdict: Partial
- **FR-11.3 (Should)** The system shall record a trace of the invocation — resolved scope, achieved depth, checks executed, tokens spent — sufficient to explain why a finding was produced.
  (from: `Docs/agentic-code-review-srs-v1.md`, §4.10) · Verdict: Partial
- **FR-7.2 (binding; Must/Should not stated in srs-v1)** Suggestions are advisory, with no commit, push, or auto-apply.
  (from: `Docs/agentic-code-review-srs-v1.md`, §7 and Appendix B) · Verdict: Unverified

## 3.11 Interface stability

(from: `Docs/agentic-code-review-srs-v1.md`, §5)

| Interface | Defined in | Stability |
|---|---|---|
| Change set (files and hunks) | FR-10.3c | Frozen; the product-v3 adapter substitutes its producer |
| Related-context provider obligations | §4.2.3 | Frozen; product v2 adds an implementation, not an obligation. The concrete signature is design's |
| Module resolution mechanism | FR-2.6f | Internal to CF-2; free to change; no consumer may observe it (FR-2.6e) |
| Check invocation (project toolchain) | FR-4.7 | A subprocess boundary, not a linked one |
| Finding model and schema | FR-0.1, FR-0.4 | Versioned; changes require a schema-version bump |
| `emit_finding` tool schema | FR-5.6a | Equals the finding model, not the review report (FR-8.2b). One definition, not two |
| Review report schema | FR-8.2b–e | Embeds the finding model; versioned with it |
| Provider interface | FR-0.3 | A new provider is a new implementation behind it; the client may live in CF-6 (FR-5.8) |
| Investigation tool registry | FR-5.7a | Documented and versioned; adding a tool is a registry change |
| CLI flags and exit codes | FR-10.3a, FR-10.4c | Documented and stable across v1 patch releases |

## 3.12 Acceptance criteria

v1 is complete when all of the following hold; each is verifiable by execution, not inspection. (from: `Docs/agentic-code-review-srs-v1.md`, §6) AC-5 and AC-7 are the two to defend under schedule pressure; AC-8, AC-10, AC-12 and AC-14 are structural.

| AC | Criterion | Verifies | Verdict |
|---|---|---|---|
| AC-1 | A single command reviews a public TS/JS repository end to end and prints findings, using only a free provider tier | FR-9.2a, FR-10.1 | Unverified |
| AC-2 | A review of a TS/JS project whose change breaks a test or the type-check produces at least one finding that cites that result rather than text inference | FR-4.5c, FR-5.3, FR-4.2 | Not built |
| AC-3 | The JSON output validates against the published schema, and records depth, model, and resolved scope | FR-8.2b, FR-8.2c | Partial |
| AC-4 | Findings originating from a pattern rule name that rule | FR-6.2a | Not built |
| AC-5 | The regression harness runs as a test and reports a catch rate over the corpus | FR-6.2b, FR-6.2d | Not built |
| AC-6 | The harness produces comparable catch rates when run at depth 0 and depth 1 | FR-6.2d, FR-2.6a | Not built |
| AC-7 | A run where the tests could not execute says so, and is distinguishable in both outputs from a run that found nothing | FR-4.5a, FR-11.2 | Not built |
| AC-8 | Requesting depth 2 reports an achieved depth of 1 with a machine-readable reason naming the absent index, and completes the review | FR-2.6d | Not built |
| AC-9 | A malformed config fails with the offending field named; a missing provider key fails with a message saying so; neither costs a check execution first | FR-1.2d, FR-9.3 | Conforms |
| AC-10 | No module outside CF-7 imports a terminal-rendering dependency; no module outside CF-1 resolves a change scope; no core package imports the agent framework — only the agents package may; no module outside CF-2 names a concrete related-context implementation or references the resolver | FR-10.2, FR-2.6e, FR-5.8 | Partial |
| AC-11 | A single-pass baseline catch rate is recorded on the corpus before investigation tools are enabled, and the harness can report catch rate, total tool calls and investigation tool calls at two settings on that same corpus | FR-5.7b, FR-6.2d, FR-6.2e, FR-8.2d | Not built |
| AC-12 | With authoritative resolution made unavailable, a review of the same repository still completes and reports the degradation, distinguishably from a run where every import resolved | FR-2.6f, FR-2.6g, FR-11.2 | Not built |
| AC-13 | A run whose sole `emit_finding` call is malformed produces a repair turn; where that also fails, the output is distinguishable from a run that found nothing | FR-5.6c | Conforms |
| AC-14 | Requesting depth 2 on a machine without authoritative resolution reports both degradations, not one | FR-2.6h, FR-8.2e | Not built |
| AC-15 | Every finding in a run either cites a specific evidence reference or is marked unverified with a reason. No finding carries neither | FR-5.2c | Conforms |
| AC-16 | A run in which the model made no tool call is distinguishable in both outputs from a run that reviewed the change and found nothing | FR-5.10 | Conforms |
| AC-17 | Requesting the visual report produces Mermaid that renders without error and shows the same findings as the JSON report | FR-8.5 | Not built |

## 3.13 Numbers not yet decided, and the placeholders in force

(from: `Docs/agentic-code-review-srs-v1.md`, §8) No requirement, acceptance criterion or design decision may be justified by one of these numbers. Replacing a placeholder is a configuration change. Every stage records its own duration on every run (FR-8.2c, FR-11.3). The open items themselves are in Appendix A (OQ-7).

| # | Open item | Cited by | Placeholder |
|---|---|---|---|
| TBD-1 | Share of review latency module resolution may consume | FR-2.6f | none |
| TBD-2 | The latency a developer will tolerate, to be established by observing real MVP users; the end-to-end budget; whether stages may overlap | §2.4, FR-4.4a | none; no design decision may cite a latency threshold |
| TBD-3 | Context token cap and per-section split | FR-2.5, FR-2.5a | The configured model's window less a stated reply reserve, split by section |
| TBD-4 | Default execution time budget | FR-4.4a | A documented default, reported when exceeded |
| TBD-5 | Maximum change-set size handled | FR-10.3c | none |
| TBD-6 | Quantitative catch-rate and false-positive targets | FR-6.2f, AC-5 | none |
| TBD-7 | Cost target per invocation and the model-selection policy | §2.4 | none |
| TBD-8 | Tool-call ceiling default | FR-5.7 | 25 |

Also carried without a citing requirement: supported operating systems and Python versions, and a documented minimum Node version (FR-10.6, product v2); execution isolation and the untrusted-code security model (product v3). (from: `Docs/agentic-code-review-srs-v1.md`, §8)

## 3.14 Excluded from v1

(from: `Docs/agentic-code-review-srs-v1.md`, §7; reasoning in `Docs/Draft/mvp-scope.md` §4) Out of v1 scope, with destination: FR-2.3a, FR-2.3b (context depth 2 and above; product v2); FR-3.1–FR-3.4 (risk triage; product v2); FR-4.3 (dependency audit; product v2); FR-5.4 (blocking distinction beyond severity; product v2); FR-5.5, FR-10.5 (cross-run de-duplication and local state; product v2); FR-6.2c (pattern coverage; product v2); FR-6.3 (broad rule set; product v2); FR-7.1a, FR-7.3 (fix snippets, evidence links; product v2); FR-10.6 (platform matrix, prebuilt binaries, containers; product v2); FR-10.7 (unparseable working trees; product v2); FR-1.1, FR-1.3, FR-1.4, FR-2.1, FR-7.1, FR-8.1a, FR-8.1c, FR-8.3, FR-9.2 (all GitHub integration except reading a public pull request; product v3). `get_check_result` and `lookup_pattern_rule` are not planned as tools.

## 3.15 Technology selection

(from: `Docs/technical_stack.md`, §1–§5, §8; decided by ADR-0007, ADR-0009, ADR-0010) Normative for technology only; it never relaxes a requirement above.

| Choice | Serves | Observed in the code |
|---|---|---|
| Python host, distributed as a PyPI package with a console entry point | FR-9.1, FR-10.6 | `pyproject.toml`: hatchling wheel, `agentic-review` entry point |
| LangChain for provider interface and tool binding; LangGraph for the pipeline orchestrator and the review step, both only in `agents/` | FR-0.3, FR-5.6a, FR-5.7, FR-5.8 | Contracts 3 and 3b kept |
| OpenAI-compatible client; NVIDIA NIM free tier default | FR-0.3, FR-9.2a | `core/config/settings.py` lines 17–18 |
| Pydantic for the finding model, report schema and config | FR-0.1, FR-0.4, FR-5.2 | `core/findings/model.py`, `core/config/settings.py` |
| Typer and Rich for the CLI and terminal (Rich only in `core/output/` and `cli/`) | FR-10.4a | Contract 1 kept |
| Jinja2 for the HTML report, only in `core/output/` | FR-10.4d | Contract 8 kept |
| `tree-sitter` in-process for parsing | FR-2.2, FR-2.4 | Not installed (CF-2 not built) |
| Bundled Node resolver sidecar for depth-1 resolution, heuristic fallback | FR-2.6f, FR-2.6g | Not present (CF-2 not built) |
| Checks as subprocesses against the project's toolchain | FR-4.1, FR-4.2, FR-4.7 | Not present (CF-3 not built) |
| pytest for the regression harness | FR-6.2b, FR-6.2d, FR-6.2e | Not present (CF-8 not built) |
| Import-linter contracts 1, 2, 3, 3b, 4, 5, 6, 8 | FR-5.8, FR-10.2, FR-10.4a, FR-2.6e, FR-2.6f | 1, 2, 3, 3b, 6, 8 present; 4 and 5 deferred |
| Our own trace record, not a hosted tracing service | FR-11.3 | The report's run metadata and stage durations |

---

## Appendix A — Open questions (all open)

Every item in Part 1 §1.6, OQ-1 to OQ-23, was open when audited. The follow-up closed OQ-3, OQ-4 and OQ-23 and narrowed OQ-1; the rest remain open. In short:

- **Which document is the target:** OQ-1 (srs-v1 or srs-v2), OQ-2 (cited Proposed ADRs), OQ-3 (FR-8.5), OQ-4 (missing revision entries), OQ-5 (status of CF-4).
- **Interpretation:** OQ-6 (AC-10's CF-7 clause), OQ-13, OQ-15.
- **Waiting on measurement:** OQ-7 (TBD-1…TBD-8), OQ-18 (S-1 for the default model), OQ-19 (S-2, S-3).
- **Product decision:** OQ-8 (category values).
- **Analyst findings, not decided:** OQ-9 to OQ-12, OQ-14, OQ-16, OQ-17, OQ-22.
- **Stack and dependency hygiene:** OQ-20 (Langfuse placement), OQ-21 (unlisted runtime dependencies).
- **Document index:** OQ-23.

## Appendix B — Conformance gaps

### B.1 Requirement gaps (from Part 2)

| ID | Verdict | Gap | Evidence |
|---|---|---|---|
| FR-10.3a | Partial | Staged and single-commit scopes not built (the configured-`staged` crash is fixed: exit 3 with a message) | `core/changeset/resolve.py` line 198; `cli/app.py` line 28; probe |
| FR-2.5b | Partial | No eviction by distance | `core/assembly/prompt.py` line 66 |
| FR-5.6b (Should) | Does not conform | No structured-output fallback | `core/output/build.py` line 53 |
| FR-5.3 | Does not conform | Agent receives no execution results or rules | `core/assembly/prompt.py` line 66; `agents/pipeline_agent.py` 192–199 |
| FR-5.7a (Should) | Partial | Switch accepted and ignored; no tools; no versioned tool list | `core/output/build.py` line 47 |
| FR-5.7c (Should) | Partial | No remaining-calls signal | no `remaining` in `src/` |
| FR-10.4c | Partial | An unhandled error exits 1, the "blocking" code (the staged probe now exits 3) | `cli/app.py` line 125 |
| FR-8.2c | Partial | Depth always null | `core/output/build.py` 44–45 |
| FR-9.1 | Partial | No LICENSE (README added in the follow-up) | `git ls-files`; `pyproject.toml` 1–5 |
| FR-9.3 | Partial | No test-script check (the staged crash now has a message) | `core/pipeline/preflight.py` 3–4 |
| FR-11.1 | Partial | Spent tokens never compared with a limit | `core/review/accounting.py` 57–61 |
| FR-11.2 | Partial | Checks-unrunnable mode absent; an unexpected error gives no report | `cli/app.py` line 125 |
| FR-11.3 (Should) | Partial | Achieved depth and checks executed absent | `core/output/build.py` 44–45 |
| FR-5.1 | Unverified | No test of agent isolation | S-ISO |
| FR-5.8 | Unverified | Acyclic and thin-node clauses untested | S-ACYC |
| FR-7.2 | Unverified | No test asserts the absence of a write path | S-WRITE |
| FR-9.2a | Unverified | No live end-to-end run recorded | tasks T101, T127 open |
| AC-1 | Unverified | as FR-9.2a | |
| AC-3 | Partial | Depth null; no published schema artefact | `core/output/build.py` 44–45; no `schema` command |
| AC-10 | Partial | CF-2 clause has no contract; CF-7 clause open | `pyproject.toml` 45–46; OQ-6 |

All requirements of CF-2, CF-3 and CF-8, FR-2.3c, FR-2.5a and FR-2.5c, and FR-8.5 (added in v1.6), are **Not built**. AC-17 cannot pass until FR-8.5 exists. Of those, AC-2, AC-4–AC-8, AC-11, AC-12 and AC-14 cannot pass until those blocks exist. That includes AC-5 and AC-7, which srs-v1 names as the two to defend.

### B.2 Documents and code that disagree with each other (the SRS is not involved)

The SRS decides what is required. These rows record where feature documents, project notes and code comments describe something the code does not do. Nothing was edited by the audit; the follow-up corrected every row except the `schema` command, `--version`, `ReviewRequest.commit`, Langfuse and the dependency rows, which describe planned work or open questions (see "Follow-up: changes applied").

| Where | Says | Code |
|---|---|---|
| `specs/001-walking-skeleton/spec.md` traceability, spec 001 FR-022 | Realised in `core/pipeline/run.py` | File does not exist; logic is in `agents/pipeline_agent.py` |
| `specs/001-walking-skeleton/spec.md` line 266 | FR-5.1 realised in `core/agent/graph.py` | File does not exist; `agents/review_reporting_agent.py` |
| `core/findings/port.py` line 3 (docstring) | LangChain implementation lives in `core/agent/` | It lives in `agents/` (ADR-0010) |
| `specs/001-walking-skeleton/spec.md` traceability, spec 001 FR-010 | "Nothing to review" realised in `agents/pipeline_agent.py` | No code path sets completion status `nothing-to-review`; `tests/integration/test_story2_failure_modes.py` line 191 says it is built by User Story 4 (T087) |
| spec 001 FR-028; `contracts/cli.md`; `contracts/review-report.md`; `plan.md` | `agentic-review schema` prints the report schema | No such command |
| `quickstart.md` | `agentic-review --version` prints a version | No such option |
| `contracts/internal-seams.md` §1 | `ReviewRequest.commit` | No such field (`agents/pipeline_agent.py` 66–74) |
| `technical_stack.md` §4 | Contract 7 reserved so that only `agents/` imports Langfuse | `core/assembly/prompt.py` line 91 imports `langfuse` |
| `technical_stack.md` §5, §7 | Dependency inventory and pins | `pyproject.toml` lines 14–19 add `jupyter`, `grandalf`, `langchain-ollama`, `langchain`, `groq`, `langfuse`, unlisted |
| `core/config/settings.py` line 17 | Default model "chosen by test S-1" | `s1-results.md` measured a different model only |
| `CLAUDE.md`; `Docs/CAI5_…documentation.md` | 424 tests, under a minute; staged built; tracing built | 426 tests in 71.79 s; staged not built; no tracer attached |
| `specs/README.md` | Feature 001 "Plan approved — ready for tasks" | Built through User Story 2 plus Phases 10–11 |

## Appendix C — Content removed in consolidation

| Removed | Source | Why |
|---|---|---|
| Revision history and the narrative of each amendment ("Amended in v1.1 / v1.2 / v1.3 / v1.4 / v1.5" paragraphs) | srs-v1 §0, §4.1–§4.10 italic commentary | Historical; the current text is kept |
| "What changed in v1.1" (contradictions fixed, mechanism withdrawn, gaps closed, considered and declined, withdrawn, still open) | srs-v1 §10 | Historical. Its "Still open" items are kept as OQ-7 and OQ-8 |
| Delivery sequence | srs-v1 Appendix A | States itself non-normative; cited by path |
| Traceability table | srs-v1 Appendix B | Replaced by the source notes and Part 2 |
| Known risks R-1 … R-8 | srs-v1 §9 | Risks, not requirements; cited by path. R-1 and R-5 (the thesis is unproven at depth 1; v1 serves the author, not the reviewer) still have to be restated whenever v1 is demonstrated |
| Introduction, overall description, users, operating environment, assumptions, "what v1 deliberately is not", pipeline diagram | srs-v1 §1–§2 | Background and diagrams; cited by path. The technology parts appear in 3.15 |
| Tool-exclusion reasoning (`get_check_result`, `lookup_pattern_rule`, `find_references`) and the "why investigation is off by default" note | srs-v1 §4.6 | States itself non-normative |
| Every srs-v2 requirement (45 kept from srs-v1 plus FR-8.5) and AC-17 | `Docs/agentic-code-review-srs-v2.md` §4, §6 | The kept 45 duplicate srs-v1 in simpler words, and srs-v1 governs (srs-v2 §0.3). The five amended texts, AC-2, FR-8.5 and AC-17 were adopted into srs-v1 v1.6 and appear above from there |
| srs-v2 HLR tables, diagrams and pie charts | `srs-v2.md` §2–§3; `Docs/design/Component-design/README.md` | Analysis and diagrams; cited by path |
| The v1–v3 requirement catalogue | `Docs/Draft/agentic-code-review-srs.md` | Superseded for v1 by srs-v1; product v2/v3 requirements are not part of this build target (summarised in 3.14) |
| FR→HLR classification and proposed HLR edits | `srs-alignment.md` | Analysis; proposals recorded as OQ-16 and OQ-17 |
| Use cases, entity model, workflows, resilience matrix, Q-1…Q-11 | `system_analysis.md` | Historical analysis of v1.0. The analyst findings that remain open are OQ-9 to OQ-14. Q-2, Q-3, Q-5 and Q-9 are settled by srs-v1 v1.1 (FR-5.7c status and §8.2c, FR-2.6h, FR-5.2c, FR-5.2a/b with FR-10.4c) |
| Rationale for every scope cut | `Docs/Draft/mvp-scope.md` | Historical rationale; cited by path |
| The external review response and its AC-A1…A4 | `Docs/Draft/agentic-architecture-review.md` | Historical; the adopted parts are FR-5.2c and FR-5.9 |
| Feature-local requirements spec 001 FR-001…FR-032, user stories, success criteria, design gaps D-1…D-5, research R-1…R-25, tasks, contracts | `specs/001-walking-skeleton/**` | Feature slice documents, subordinate to srs-v1; mapped through `spec.md`'s traceability table. spec 001 FR-009, FR-010 and FR-031 have no SRS parent and are not consolidated |
| Design blocker log | `DESIGN_BLOCKERS.md` | Historical issue log; outstanding points are carried as OQ-7 and OQ-8 |
| System design diagrams | `Docs/system-design.md`, `Docs/system-design-block.md` | Diagrams only; cited by path |
| Project planning, stakeholders and report UI | `Docs/CAI5_IND5_G1-agentic-pr-review-documentation.md` | Non-normative; its mismatched claims are recorded in "Checks run" |
| Operating instructions | `Docs/operation_guidelines.md`, `CLAUDE.md` | Non-normative; describe the code |
