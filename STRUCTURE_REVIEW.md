# Structure Review — Agentic Code Review

**Date:** 2026-09-20 · **Branch:** `001-walking-skeleton` · **Status:** Observation, not a decision

A map of what is in this repository today, how the parts relate, and where the same thing is said more than once. This document describes the repository as found. It proposes simplifications in §8 but decides nothing.

---

## 1 · In one page

The repository holds **15,152 lines of Markdown against 2,594 lines of Python** — a prose-to-code ratio of roughly **5.8 : 1**. That ratio is not by itself a fault: this project deliberately specified before it built, and the specification is the reason the code has the shape it has. But the prose has now accumulated **four layers that each restate the same requirements in different words**, and the code has begun citing two incompatible identifier schemes for them.

| | Files | Lines |
|---|---|---|
| `Docs/` | 47 | 11,504 |
| `specs/` | 13 | 2,484 |
| Root `.md` (CLAUDE, DESIGN_BLOCKERS, DESIGN_REPORT) | 3 | 1,164 |
| `src/` | 41 | 2,594 |
| `tests/` | 38 | 1,939 |

**The three findings that matter most**, in order:

1. **`CLAUDE.md` is factually wrong about the repository it describes.** It opens with *"This repository contains no source code yet… There is no `pyproject.toml`, no build, no test runner, and no lint config — do not invent commands for them or claim to have run them."* There are 41 source files, a `pyproject.toml`, pytest, import-linter and CI. It actively instructs future contributors and agents not to run checks that exist. **This is the cheapest and highest-value fix in the repository.**
2. **Two parallel requirement ID namespaces** — `FR-x.y` (SRS, 105 identifiers) and `FR-0NN` (specs, 31 identifiers) — now both appear inside `src/` and `tests/`, inconsistently.
3. **Two root documents have no inbound links at all** and one `Docs/` document is referenced only by a non-normative draft.

---

## 2 · Repository map

```mermaid
flowchart TD
    R["Pull-request-Reviewer/"]

    R --> D["<b>Docs/</b> · 47 files · 11,504 lines<br/><i>specification, decisions, design, drafts</i>"]
    R --> S["<b>specs/</b> · 13 files · 2,484 lines<br/><i>feature 001 — spec, plan, tasks, contracts</i>"]
    R --> C["<b>src/agentic_review/</b> · 41 files · 2,594 lines<br/><i>the tool</i>"]
    R --> T["<b>tests/</b> · 38 files · 1,939 lines<br/><i>unit · integration · structural</i>"]
    R --> M["<b>root .md</b> · 3 files · 1,164 lines<br/>CLAUDE · DESIGN_BLOCKERS · DESIGN_REPORT"]
    R --> X["<b>tooling</b><br/>.specify/ · .claude/ · .github/<br/>scripts/ · notebooks/"]

    style D fill:#eef3fa
    style C fill:#e8f7e8
    style M fill:#fff4e0
```

`.claude/` and `.specify/` are both gitignored. `.claude/skills/` holds the `git-mentor` skill and eleven `speckit-*` workflow skills; `.specify/` holds the Spec Kit templates, scripts and the project constitution that produced `specs/`.

---

## 3 · The document stack

Six layers, each subordinate to the one above. The hierarchy itself is sound and well-documented — the problem is how much material sits at each level.

```mermaid
flowchart TD
    SRS["<b>Docs/agentic-code-review-srs-v1.md</b><br/>666 lines · <b>NORMATIVE</b><br/>the build target"]
    ST["<b>Docs/technical_stack.md</b><br/>339 lines · normative for technology only"]
    ADR["<b>Docs/adr/</b> · 9 records + index<br/>normative where the SRS cites them"]
    DES["<b>Docs/design/</b> · 6 artifacts · 2,296 lines<br/>how it is put together"]
    SPEC["<b>specs/001-walking-skeleton/</b> · 2,484 lines<br/>feature-level spec, plan, tasks, contracts"]
    DRAFT["<b>Docs/Draft/</b> · 5,348 lines<br/><b>NON-NORMATIVE</b> — rationale, v2/v3, analysis"]

    SRS --> ST --> ADR --> DES --> SPEC
    DRAFT -.->|"fed into"| SRS
    SPEC ==>|"implemented by"| CODE["<b>src/</b>"]

    style SRS fill:#e8f7e8
    style DRAFT fill:#f0f0f0
    style CODE fill:#eef3fa
```

**This layering is genuinely good.** Every document states its own authority and what wins on disagreement. The issue in §7 is not that the layers are wrong — it is that requirements are *restated in full* at four of them rather than referenced.

---

## 4 · Code — component view

Nine core functions (CF-1…CF-9) map onto seven packages, with the CLI as the only adapter and `core/pipeline/` owning the order.

```mermaid
flowchart TD
    CLI["<b>cli/</b> · CF-7 adapter<br/>app.py · exit_codes.py<br/><i>translation only — decides no finding</i>"]

    PIPE["<b>core/pipeline/</b> · the orchestrator<br/>run.py · preflight.py · timing.py<br/><i>declares the graph (ADR-0009)</i>"]

    subgraph CAP["Capability packages — framework-free, ordinary functions"]
        CS["<b>core/changeset/</b> · CF-1<br/>resolve · diff_parser · exclusion<br/>summary · model · _git<br/><i>the only package that runs git</i>"]
        AS["<b>core/assembly/</b> · CF-4<br/>prompt.py · budget.py<br/><i>the only budget owner</i>"]
        AG["<b>core/agent/</b> · CF-6<br/>graph.py · build.py · accounting.py<br/><i>the only package with a provider client</i>"]
        OUT["<b>core/output/</b> · CF-7<br/>terminal · json_out · verdict · build"]
        FIND["<b>core/findings/</b> · CF-5<br/>model · schema · validation<br/>port · report · fingerprint"]
        CFG["<b>core/config/</b> · CF-9<br/>settings · loader · credentials · redact"]
    end

    MISSING["<b>Not built</b><br/>CF-2 parsing + context · feature 004<br/>CF-3 execution evidence · feature 002<br/>CF-8 patterns + regression · feature 003"]

    CLI --> PIPE
    PIPE --> CS & AS & AG & OUT
    CS & AS & AG & OUT --> FIND
    CS & AS & AG & OUT --> CFG
    PIPE -.->|"pass-through nodes"| MISSING

    style AG fill:#fff4e0
    style MISSING fill:#f0f0f0
    style PIPE fill:#eef3fa
```

### Enforced structural contracts

Five run in CI via import-linter, and all five currently pass:

| # | Contract | Defends |
|---|---|---|
| 1 | Only `core/output/` and `cli/` may import Rich | FR-10.4a |
| 2 | Only `core/changeset/` may import the git layer | CF-1 encapsulation |
| 3 | No core-function package may import LangChain, LangGraph or openai | FR-5.8 |
| 3b | `core/pipeline/` may import LangGraph, but never a provider client | FR-5.8 / ADR-0009 |
| 6 | Nothing imports `cli/`; capabilities do not import each other | layering |

Contracts **4** and **5** are specified in `technical_stack.md` §4 but not yet written — they arrive with CF-2 (feature 004). Contract 5 guards FR-2.6e, which the SRS calls *"the highest-value structural constraint in this document"*.

---

## 5 · Runtime — the two graphs

Since ADR-0009 the pipeline is a declared graph. It is acyclic; CF-6's graph is the only place a cycle occurs.

```mermaid
flowchart LR
    subgraph P["core/pipeline/run.py — acyclic, 8 nodes"]
        direction TB
        A(("start")) --> B["preflight · CF-9"]
        B -->|"failure"| Z(("end"))
        B --> C["resolve_change_set · CF-1"]
        C --> D["parse_and_context · CF-2"]
        D --> E["execute_checks · CF-3"]
        E --> F["load_patterns · CF-8"]
        F --> G["assemble_context · CF-4"]
        G --> H["review · CF-6"]
        H --> I["build_report · CF-5→7"]
        I --> Z
    end

    subgraph Q["core/agent/graph.py — the only cycle"]
        direction TB
        M(("start")) --> N["call_model"]
        N -->|"provider gave up"| Y(("end"))
        N --> O["process_calls"]
        O -->|"repair owed"| N
        O --> Y
    end

    H -.->|"through ReviewPort"| Q

    style D fill:#f0f0f0
    style E fill:#f0f0f0
    style F fill:#f0f0f0
    style Q fill:#fff4e0
```

Grey nodes are pass-throughs for capabilities not yet built. Two conditional edges the seams contract requires — *nothing to review* and *budget exhausted* — are **not** present in either graph; they remain open as tasks T074/T075.

`process_calls` still carries four distinct phases in one node (validate, observe, recompute coverage, decide repair). Splitting it is outstanding work discussed but not done.

---

## 6 · Tests

```mermaid
flowchart LR
    U["<b>unit/</b> · 18 files<br/>agent · assembly · changeset<br/>cli · config · findings · output"]
    I["<b>integration/</b> · 1 file<br/>story 1, end to end via CLI"]
    ST["<b>structural/</b> · 2 files<br/>import contracts · git confinement"]
    SUP["<b>support/</b> · 3 helpers<br/>repo_builder · report_assertions<br/>scripted_chat_model"]

    SUP --> U & I
    style ST fill:#e8f7e8
```

207 tests run offline in ~20s; the scripted stand-in model drives the real review graph, and an autouse fixture blocks the network. **3 currently fail**, all from uncommitted local changes that switched `DEFAULT_BASE_URL` to a local Ollama endpoint and rewrote the prompt, against tests still asserting the NVIDIA defaults.

---

## 7 · Redundancy findings

### 7.1 The same requirements, restated four times

This is the largest single source of duplication.

```mermaid
flowchart TD
    CAT["<b>Draft/agentic-code-review-srs.md</b><br/>388 lines · the v1–v3 catalogue<br/><i>the ID registry</i>"]
    SRS["<b>agentic-code-review-srs-v1.md</b><br/>666 lines · §4 restates v1's subset<br/><b>NORMATIVE</b>"]
    EXT["<b>v1-requirements.md</b><br/>222 lines · 'a requirements-only<br/>condensation of the v1 baseline'"]
    ANA["<b>Draft/system-analysis/</b><br/>1,335 lines + 4 req_*.md assets<br/><i>restates them again, as analysis</i>"]
    FEAT["<b>specs/001/spec.md</b><br/>FR-001 … FR-031<br/><i>restates them in feature words</i>"]

    CAT --> SRS --> EXT
    SRS --> ANA
    SRS --> FEAT
    FEAT ==>|"cited in"| CODE["<b>src/ and tests/</b><br/>both schemes, mixed"]
    SRS ==>|"also cited in"| CODE

    style SRS fill:#e8f7e8
    style CODE fill:#fff4e0
    style EXT fill:#f0f0f0
    style ANA fill:#f0f0f0
```

Counts of requirement references by location:

| Location | `FR-x.y` refs | `FR-0NN` refs |
|---|---|---|
| `Docs/agentic-code-review-srs-v1.md` | 357 | 0 |
| `Docs/v1-requirements.md` | 128 | 0 |
| `Docs/design/` | 234 | 0 |
| `Docs/Draft/system-analysis/` | 306 | 0 |
| `specs/` | 125 | **178** |
| **`src/`** | **39** | **33** |
| **`tests/`** | **6** | **44** |

The bottom two rows are the problem. A developer reading `src/` sees both schemes with no rule about which to use, and the mapping between them exists only as inline asides inside `specs/001/spec.md` (`FR-001 … — *FR-9.3, AC-9*`). There is **no mapping table anywhere**.

### 7.2 Orphaned and near-orphaned documents

| Document | Lines | Inbound links | Note |
|---|---|---|---|
| `DESIGN_REPORT.md` | 253 | **0** | Nothing in the repository links to it |
| `Docs/v1-requirements.md` | 222 | **1**, from a non-normative draft | Not listed in `Docs/README.md`'s index |
| `Docs/Draft/system-analysis/` | 1,995 | Self-referential + 1 from `Docs/README.md` | 10 of 11 links are internal to the cluster |
| `Docs/Draft/agentic-code-review-srs-ar.md` | 353 | 4 | Arabic translation; goes stale on every catalogue edit, by `CLAUDE.md`'s own admission |

### 7.3 Overlapping diagram sets

**82 mermaid diagrams** across four locations: `Docs/design/` (30), `Docs/adr/` (28), `Docs/Draft/system-analysis/` (24), `specs/` (6). `system-analysis/assets/domain_model.md` and `Docs/design/02-domain-model.md` model the same domain; `assets/seq_review_pass.md` and `design/03-behaviour.md` describe the same pass.

### 7.4 Stale statements

| Where | Claim | Reality |
|---|---|---|
| `CLAUDE.md` §"Current state" | "contains no source code yet… no `pyproject.toml`, no build, no test runner, no lint config" | 41 source files, 21 test files, `pyproject.toml`, pytest, import-linter, CI |
| `CLAUDE.md` §"git-mentor skill" | "untracked and sits at the repository root rather than under `.claude/skills/`" | It is at `.claude/skills/git-mentor/` |
| `Docs/design/README.md` | "Status: Complete — all six milestones delivered" | Accurate, but written before ADR-0009 changed §8's contract table |

### 7.5 Loose ends

- `scripts/__pycache__/` is on disk; `scripts/make_review_demo.py` is untracked.
- `Docs/operation_guidelines.md` (527 lines) is untracked — a substantial document at risk of being lost.
- `.env` is present and correctly gitignored (`.env*` with `!.env.example`).

---

## 8 · What simplification would look like

Ranked by value over effort. **None of this is done; it is a menu.**

| # | Action | Effort | Why |
|---|---|---|---|
| 1 | **Rewrite `CLAUDE.md`'s "Current state"** to describe the repository that exists, and fix the git-mentor path | Minutes | It currently tells contributors not to run the test suite. Everything else on this list is optional; this is not |
| 2 | **Pick one requirement ID scheme for `src/` and `tests/`** and add a mapping table where the other is needed | Hours | Removes the only ambiguity that reaches the code |
| 3 | **Commit or delete `Docs/operation_guidelines.md`** and `scripts/make_review_demo.py` | Minutes | Untracked work is lost work |
| 4 | **Retire `Docs/v1-requirements.md`** | Low | An unlinked condensation of a normative document is a second place for it to drift |
| 5 | **Fold `DESIGN_REPORT.md` into `Docs/design/README.md`**, or link it from somewhere | Low | 253 orphaned lines |
| 6 | **Collapse `Draft/system-analysis/assets/`** into its parent, or into `Docs/design/` where it duplicates | Medium | 11 files, 10 of them linked only by each other |
| 7 | **Mark the Arabic translation stale in its own front matter**, or drop it | Low | `CLAUDE.md` already says changes leave it stale; the file does not say so itself |
| 8 | **Split `core/agent/graph.py`'s `process_calls`** into one node per phase | Low | The original request that started this thread; still outstanding |

**What should not be touched:** the document authority hierarchy (§3), the nine core functions, the import contracts, and the ADR set. Those are the parts carrying their weight — the layering is what let ADR-0009 be a contained change rather than a rewrite.

---

## 9 · Honest caveats

This review counted lines, links and identifiers; it did not read all 15,152 lines of prose. The redundancy claims in §7.1 and §7.3 are based on document self-descriptions, title overlap and reference counts — a full content diff of `Docs/design/02-domain-model.md` against `Draft/system-analysis/assets/domain_model.md` would be needed before deleting either. The orphan counts in §7.2 are link-based and exact.
