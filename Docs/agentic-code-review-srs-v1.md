# Software Requirements Specification — Agentic Code Review v1

**Status:** Baselined · **Version:** 1.0 · **Date:** 2026-09-08
**Scope:** Local command-line reviewer for TypeScript/JavaScript
**Audience:** Contributors building v1, and reviewers verifying that a change meets it

---

## 0. About this document

This is the **authoritative specification for the version being built**. It is self-contained: everything required to implement and verify v1 is here.

It was derived from the analysis in [`Draft/mvp-scope.md`](./Draft/mvp-scope.md), which selected this subset from the larger requirement catalogue in [`Draft/agentic-code-review-srs.md`](./Draft/agentic-code-review-srs.md). Those documents remain as the record of *why* — the rationale, the options weighed, and the requirements deferred. **Where they disagree with this document, this document wins.**

| Document | Role |
|---|---|
| **This document** | What v1 is. Normative. |
| [`adr/`](./adr/) | Architecture decisions and their reasoning. Normative where cited below. |
| [`Draft/agentic-code-review-srs.md`](./Draft/agentic-code-review-srs.md) | The full requirement catalogue across v1–v3 and beyond. Historical and forward-looking; not the build target. |
| [`Draft/mvp-scope.md`](./Draft/mvp-scope.md) | The analysis that selected this scope. Explains every inclusion and every cut. |
| [`Draft/agent-harness-design.md`](./Draft/agent-harness-design.md) | Plain-language design guide for the harness layer. |
| [`Draft/`](./Draft/) (remainder) | Problem definition, competitive landscape, tool reference, feature inventory. Background. |

**Requirement identifiers are inherited unchanged** from the catalogue, so every cross-reference in the ADRs and design documents stays valid. Requirements introduced by this baseline are marked **(new in v1)**.

---

## 1. Introduction

### 1.1 Purpose

v1 delivers a reviewing engine that a developer runs from a terminal against their own uncommitted work, and an instrument that measures how good that engine is. It is an **engineering milestone, not the product**: the product claim — reducing a reviewer's queue on pull requests — is made in v3, when the same core reaches GitHub.

Two commands constitute the deliverable:

```mermaid
flowchart LR
    A["review — resolve a change,<br/>gather context, run checks,<br/>call the model"] --> B["findings in the terminal<br/>+ schema-valid JSON"]
    C["regression — run the<br/>curated defect corpus"] --> D["a catch rate"]
    A -.->|"same core, same code path"| C

    style B fill:#e8f7e8
    style D fill:#e8f7e8
```

### 1.2 Scope

**In scope for v1**

- A local CLI reviewing a working tree, staged changes, or a branch range in a TS/JS repository
- Syntax-tree parsing and related-context retrieval behind a depth-parameterised interface, with the parser-backed implementation serving depths 0 and 1
- Execution of the project's tests and type-check, with a recorded evidence trail
- A single-pass review agent, isolated from any code-writing agent, grounded in that evidence and in a pattern library
- A canonical finding model with a versioned schema, terminal rendering, and JSON output
- A pattern library and a runnable regression harness reporting a catch rate
- Configuration, credential handling, and diagnosable failure messages

**Deliberately not in v1** — §7 lists these with their destination version. In summary: GitHub integration of any kind (v3), context depths 2 and above, risk triage, the agent tool loop, cross-run de-duplication, and fix-patch generation.

### 1.3 Definitions

| Term | Definition |
|---|---|
| **Change set** | The resolved answer to "what am I reviewing?": a list of changed files and diff hunks. |
| **Context depth** | How far from the changed code the system reaches when gathering related source. Defined as a ladder in §4.2.1. |
| **Context unit** | One piece of related source included in the review context, carrying why it was included and how far away it is. |
| **Core** | The surface-independent reviewing engine. In v1 the CLI is its only caller. |
| **Adapter** | A layer translating between a surface and the core. It resolves what to review, renders findings, and stores state; **it never decides what counts as a finding**. |
| **Evidence record** | The structured outcome of executing checks: per check, whether it ran, was skipped, or errored, plus its result and captured output. |
| **Finding** | One review observation: file, line or range, severity, category, rationale, and optionally a matched rule identifier. |
| **Finding model** | The single canonical typed structure for findings (FR-0), from which all outputs are derived. |
| **Pattern rule** | A "wrong vs. correct" example with an identifier, applied by the agent when producing findings. |
| **Regression harness** | A runnable test over a curated corpus of known defects, reporting how many the reviewer caught. |
| **Must / Should** | **Must** = required for v1 to be complete. **Should** = required if time allows; its absence does not block release. |

### 1.4 References

- Architecture decisions: [`adr/`](./adr/) — particularly [ADR-0001](./adr/0001-fixed-pipeline-with-bounded-agency.md) (pipeline and step ceiling), [ADR-0004](./adr/0004-findings-emitted-as-tool-calls.md) (findings as tool calls), [ADR-0006](./adr/0006-local-cli-core-action-as-adapter.md) (CLI core, Action as adapter)
- Scope derivation: [`Draft/mvp-scope.md`](./Draft/mvp-scope.md)
- Full catalogue: [`Draft/agentic-code-review-srs.md`](./Draft/agentic-code-review-srs.md)
- Non-functional requirements: deferred to a dedicated pass (§8)

---

## 2. Overall Description

### 2.1 Product Perspective

The system is a self-contained command-line program. It runs on a developer's machine, reads a git repository, executes that repository's own test commands, and makes HTTPS calls to one external model provider. It operates no server, holds no remote state, and requires no account beyond a provider API key.

Internally it is **one core behind a thin adapter**, per [ADR-0006](./adr/0006-local-cli-core-action-as-adapter.md). v1 builds one adapter (the CLI). The constraint that adapters never decide what counts as a finding binds from the first line of code, because it is what allows v3 to add the GitHub Action without a rewrite.

Orchestration is a **fixed pipeline** owned by our code, per [ADR-0001](./adr/0001-fixed-pipeline-with-bounded-agency.md):

```mermaid
flowchart TD
    A["CLI invocation"] --> B["1 · Resolve the change set — CF-1"]
    B --> C["2 · Parse changed files — CF-2"]
    C --> D["3 · Gather related context at the requested depth — CF-2"]
    B --> E["4 · Execute checks, record evidence — CF-3"]
    D --> F["5 · Assemble context within budget — CF-4"]
    E --> F
    F --> G["6 · One review pass — CF-6"]
    G --> H["7 · Findings in canonical form — CF-5"]
    H --> I["8a · Terminal output — CF-7"]
    H --> J["8b · JSON artifact — CF-7"]

    style G fill:#fff4e0
```

Step 6 is the only step involving a model. In v1 it is a **single pass** — the step ceiling is zero (FR-5.7).

### 2.2 Users

| User | Need v1 serves |
|---|---|
| **The developer author** | A review of their own work before they push it |
| **The contributor building this system** | A fast iteration loop and a measurable engine |
| **The maintainer** | Evidence that a change to prompts, context, or rules improved or worsened the reviewer |

Note that v1's primary user is the **author**, not the reviewer named as the primary persona in [`Draft/Agentic_Code_Review_Problem_Definition_v1.md`](./Draft/Agentic_Code_Review_Problem_Definition_v1.md). This is a known and accepted consequence of sequencing GitHub integration into v3 (§9, R-5).

### 2.3 Operating Environment

- **Platform:** a developer workstation — Linux, macOS, or Windows
- **Runtime:** Node.js, with `tree-sitter` as a native module
- **Repository under review:** a TypeScript/JavaScript project with a runnable test script, under git
- **External dependency:** one AI model provider reachable over HTTPS (NVIDIA NIM free tier as the default)
- **Credentials:** a provider API key supplied through the environment or user-level configuration

### 2.4 Assumptions and Constraints

- **Budget:** free provider tiers, or a single plan around $20/month. No paid inference infrastructure.
- **Binding constraint is latency, not runner minutes.** A developer waiting at a prompt abandons the tool after roughly 10–30 seconds. Cost is borne per invocation and is visible to the user.
- **Value depends on a runnable test suite.** Execution-backed review adds nothing to a repository whose tests cannot run; the system must say so rather than degrade silently (FR-9.3).
- **The provider must support tool calling for at least one call per review.** v1 requires exactly one reliable `emit_finding` call, not a multi-step loop — this is the documented fallback configuration in [ADR-0001](./adr/0001-fixed-pipeline-with-bounded-agency.md) and materially reduces the free-tier dependency risk.
- Single provider and single language are deliberate scoping decisions, not technical limitations.

### 2.5 What v1 deliberately is not

v1 **demonstrates that the pipeline works end to end. It does not yet demonstrate the project's thesis.** At context depth 1 the system can judge whether a change is internally sound and consistent with stated rules; it cannot judge whether the change violates an assumption held by a caller it never looked at. Inbound call sites arrive at depth 2, in v2.

This is stated here rather than buried because it governs how v1 should be demonstrated and described. See §9, R-1.

---

## 3. Core Functions

The requirements in §4 are organised around nine function blocks. Each requirement belongs to exactly one.

| # | Core function | Responsibility |
|---|---|---|
| **CF-1** | Change-set resolution | Turn an invocation into a concrete list of changed files and hunks |
| **CF-2** | Parsing and related context | Syntax trees, and related source retrieved at a requested depth |
| **CF-3** | Execution and evidence | Run the project's checks; record what happened |
| **CF-4** | Context assembly | Fit diff, related context, evidence, and rules into the model window |
| **CF-5** | Finding model and provider client | The canonical structure, its schema, and the model interface |
| **CF-6** | The review agent | One grounded, isolated review pass |
| **CF-7** | Output | Terminal rendering, JSON artifact, exit status |
| **CF-8** | Pattern library and regression harness | Rules, rule attribution, and measurement |
| **CF-9** | Configuration and diagnostics | Config, credentials, and legible failure |

---

## 4. Functional Requirements

Written as testable "the system shall…" statements. Identifiers are inherited from the catalogue except where marked **(new in v1)**.

### 4.1 CF-1 — Change-Set Resolution

- **FR-10.3a (Must)** The system shall resolve the change scope from an explicit selection among: uncommitted working-tree changes, staged changes only, or a comparison against a named branch or commit.
- **FR-10.3b (Must)** The system shall apply a documented default change scope when none is specified, and shall state the resolved scope in its output.
- **FR-10.3c (Must) (new in v1)** The resolved change set shall be expressed as a list of changed files and diff hunks, in a structure independent of how it was resolved.

*FR-10.3c is the seam that lets the v3 Action adapter substitute "PR head against base" (FR-2.1) with no downstream change.*

### 4.2 CF-2 — Parsing and Related Context

- **FR-2.2 (Must)** The system shall build a `tree-sitter` AST for changed TS/JS files.
- **FR-2.4 (Should)** The system shall include relevant surrounding context — function, class, and type boundaries — rather than raw line windows.
- **FR-2.3d (Must)** The system shall record which related files were included and why, for traceability.

#### 4.2.1 The context depth ladder

Related context is retrieved at a **depth**, defined by this ladder. v1 implements depths 0 and 1.

| Depth | What it includes | Resolvable by | Version |
|---|---|---|---|
| **0** | Changed hunks, expanded to enclosing function, class, or type boundaries | Parsing the changed files | **v1** |
| **1** | What the changed code reaches outward to: definitions of symbols it imports and calls | Parsing the changed files, then the files their imports name | **v1** |
| **2** | What reaches inward: files importing a changed symbol, direct call sites of a changed function | A reverse index over the repository | v2 |
| **3** | Transitive neighbours | The same index, traversed further | v2+ |

The ladder is ordered by **cost of resolution**, not purely by graph distance. A file's imports are inside the file; who depends on it is not.

#### 4.2.2 The related-context interface

- **FR-2.6a (Must) (new in v1)** The system shall expose related-context retrieval through a single interface parameterised by depth, with the implementation selected at run time.
- **FR-2.6b (Must) (new in v1)** v1 shall provide a parser-backed implementation serving depths 0 and 1 without requiring any repository-wide index.
- **FR-2.6c (Must) (new in v1)** Every returned context unit shall carry the relation by which it was included (`imports`, `calls`, `imported-by`, `called-by`) and its distance from the change.
- **FR-2.6d (Must) (new in v1)** A retrieval result shall state the depth actually achieved and, where that is lower than requested, the reason. The system shall not silently downgrade.
- **FR-2.6e (Must) (new in v1)** No consumer of the interface shall branch on which implementation served the request.

Normative interface:

```ts
type Relation = 'imports' | 'calls' | 'imported-by' | 'called-by';

interface ContextUnit {
  file: string;
  symbol?: string;
  range: [number, number];
  source: string;
  relation: Relation;   // FR-2.6c
  distance: number;     // FR-2.6c — drives eviction, FR-2.5
}

interface RelatedContextRequest {
  changeSet: ChangeSet;
  depth: number;        // requested, not guaranteed
  budget: TokenBudget;
}

interface RelatedContextResult {
  units: ContextUnit[];     // ordered by distance, then relevance
  achievedDepth: number;    // FR-2.6d
  degraded?: 'no-index' | 'budget-exhausted' | 'unresolvable-imports';
}

interface RelatedContextProvider {
  readonly maxDepth: number;
  resolve(req: RelatedContextRequest): Promise<RelatedContextResult>;
}
```

| Implementation | `maxDepth` | Requires | Version |
|---|---|---|---|
| `ParserContextProvider` | 1 | Nothing beyond the changed files | **v1** |
| `IndexContextProvider` | 3 | A built reverse index | v2 |

FR-2.6e is the requirement that makes v2 a new implementation rather than a change to CF-4, CF-6, and CF-7. It is the highest-value structural constraint in this document.

### 4.3 CF-3 — Execution and Evidence

- **FR-4.1 (Must)** The system shall run the project's test suite on the developer's machine and capture pass/fail results and output.
- **FR-4.2 (Must)** The system shall run build/type checks (e.g. `tsc`) and capture results.
- **FR-4.4a (Must)** The system shall enforce a configurable time budget on the execution phase and terminate execution when it is exceeded.
- **FR-4.4b (Must)** On termination due to timeout, the system shall mark execution as `timed-out`, skip remaining checks, and continue to produce a review reporting the timeout.
- **FR-4.5a (Must)** The system shall record, for each check, whether it was run, skipped, or errored.
- **FR-4.5b (Must)** The system shall record each executed check's pass/fail result and captured output.
- **FR-4.5c (Must)** The system shall make this execution record available to the review agent and include it in the structured output.
- **FR-4.6 (Must) (new in v1)** The review agent shall not be able to trigger check execution. Execution occurs once per invocation, before the review pass.

*FR-4.6 states for v1 the decision in [ADR-0002](./adr/0002-pipeline-initiates-test-execution.md). That record notes the prohibition relaxes on a local surface where a targeted run costs seconds; v1 nonetheless keeps it, because the single-pass agent (FR-5.7) has no loop in which to call such a tool. Both may be revisited together in v2.*

### 4.4 CF-4 — Context Assembly

- **FR-2.3c (Must)** The system shall include the source of related definitions and call sites in the review context passed to the agent, up to the context cap.
- **FR-2.5 (Must)** The system shall cap context size to stay within model token limits, degrading gracefully when exceeded.
- **FR-2.5a (Must) (new in v1)** Context shall be budgeted per section — instructions and rules, the diff, related context, and evidence — so that no section can starve another.
- **FR-2.5b (Must) (new in v1)** When the budget is exceeded, the system shall evict context units in descending order of `distance`, and shall never truncate the diff itself.
- **FR-2.5c (Must) (new in v1)** Captured check output shall be reduced to failing test names, assertion messages, and stack frames referring to changed files before entering the context. Full output is retained for the structured output only.

*FR-2.5c prevents the largest accidental context sink in the design: a failing suite can emit megabytes.*

### 4.5 CF-5 — Finding Model and Provider Client

- **FR-0.1 (Must)** The system shall define a provider-independent internal finding representation — "the finding model" — as the single canonical structure for all review findings.
- **FR-0.2 (Must)** All model output shall be converted into the finding model before any downstream use; no component shall consume raw provider responses directly.
- **FR-0.3 (Must)** A new provider shall be integratable by mapping its output to the finding model without changes to downstream components.
- **FR-0.4 (Must)** The finding model shall have a documented, versioned schema carrying a schema-version field.
- **FR-5.2 (Must)** Each finding shall contain: file path, line or line-range, severity, category, rationale, and optionally the identifier of a matched pattern rule.
- **FR-5.6 (Must)** The agent's output shall conform to the finding model; all outputs shall be derived from it, not produced independently by the model.
- **FR-5.6a (Must) (new in v1)** Findings shall enter the system exclusively through an `emit_finding` tool call validated against the finding-model schema at the call boundary. Prose the model produces shall not be parsed for findings.
- **FR-5.6b (Should) (new in v1)** Where the provider cannot perform tool calls, the system shall fall back to schema-validated structured output with a documented retry cap, and shall report which path was used.

*FR-5.6a states [ADR-0004](./adr/0004-findings-emitted-as-tool-calls.md) normatively.*

### 4.6 CF-6 — The Review Agent

- **FR-5.1 (Must)** The review agent shall operate in a context isolated from any code-writing agent — no shared history or state.
- **FR-5.3 (Must)** The agent shall incorporate execution results (CF-3) and pattern-library rules (CF-8) into its findings.
- **FR-5.7 (Must) (new in v1)** The agent shall complete a review in a single model pass. No tool loop shall run in v1; `emit_finding` is the only tool exposed.

*FR-5.7 is [ADR-0001](./adr/0001-fixed-pipeline-with-bounded-agency.md) at step ceiling zero — its documented fallback, adopted deliberately. Raising the ceiling in a later version is a configuration change, not a restructure.*

### 4.7 CF-7 — Output

- **FR-8.1b (Must)** The terminal summary shall state the resolved change scope, the checks run and their results, the count of findings by severity, and an overall verdict.
- **FR-8.2a (Must)** The system shall serialize the finding model to JSON as a machine-readable artifact.
- **FR-8.2b (Must)** The JSON shall conform to the finding model's versioned schema, including findings, severities, and the evidence record.
- **FR-8.4 (Should)** The structured output schema shall be documented and versioned.
- **FR-10.4a (Must)** The system shall render findings to the terminal, derived from the finding model and not produced independently.
- **FR-10.4b (Must)** The system shall provide machine-readable output on request, conforming to the schema in FR-8.2b.
- **FR-10.4c (Should)** The system shall exit with a status code reflecting the review outcome, documented and stable across versions.
- **FR-8.2c (Must) (new in v1)** The structured output shall record the achieved context depth, the model and schema versions used, and the resolved change scope, so a run can be reproduced and compared.

*FR-8.2c is what makes the depth comparison in §6 possible after the fact rather than only in a controlled harness run.*

### 4.8 CF-8 — Pattern Library and Regression Harness

- **FR-6.1 (Must)** The system shall load a configurable pattern library of "wrong vs. correct" examples and project standards.
- **FR-6.2a (Must)** When a finding is generated from a pattern-library rule, the finding shall reference the identifier of the matched rule.
- **FR-6.2b (Must)** The system shall support a regression set of pattern examples with expected outcomes, runnable as a test, so pattern-matching behaviour can be verified and monitored across changes.
- **FR-6.2d (Must) (new in v1)** The regression harness shall report a catch rate over the corpus, and shall accept a context depth so that results at different depths are directly comparable.
- **FR-6.3a (Must) (new in v1)** v1 shall ship at least five pattern rules, each with a wrong example, a correct example, and at least one corresponding regression case.

*Five rules is a floor that proves the mechanism, not a product-grade rule set. Breadth is v2 (FR-6.3).*

### 4.9 CF-9 — Configuration and Diagnostics

- **FR-1.2a (Must)** The system shall read configuration from `.agentic-review.yml` at the repository root when present.
- **FR-1.2b (Must)** When the file is absent, the system shall apply a documented built-in default configuration.
- **FR-1.2c (Must)** When the file is present but a field is missing, the system shall apply that field's documented default value.
- **FR-1.2d (Must)** When the file is present but malformed, the system shall fail with an error message identifying the offending field, and shall not fall back silently.
- **FR-1.3a (Must)** The system shall read the model provider credential from the local environment or user-level configuration, never from a hard-coded key and never from a file committed to the repository.
- **FR-3.5 (Must) (new in v1)** The system shall exclude configured generated, vendored, and build-output paths from review, using a documented default exclusion list.
- **FR-9.1 (Must)** The system shall ship with README, LICENSE, and CLI usage documentation.
- **FR-9.3 (Must)** The system shall provide clear failure messages when prerequisites — a test script, a provider key, a git repository, a parseable tree — are missing or unusable.

*FR-3.5 is v1's substitute for risk triage (FR-3.1–FR-3.4, deferred). It captures most of the benefit — not wasting a review on generated code — at a fraction of the cost. FR-9.3 is raised from Should to Must here: on a local surface a silent failure is indistinguishable from a clean review.*

### 4.10 Cross-cutting

- **FR-10.1 (Must)** The system shall provide a command-line interface that reviews a local change set without requiring GitHub API access or repository credentials.
- **FR-10.2 (Must)** No adapter shall contain logic that determines whether something is a finding.
- **FR-9.2a (Must)** The system shall complete an end-to-end review of a public TS/JS repository on a developer machine, using only a free model provider tier.
- **FR-11.1 (Must) (new in v1)** The system shall enforce a token and call budget per invocation and stop cleanly when it is reached, reporting that it did so.
- **FR-11.2 (Must) (new in v1)** The system shall produce a review under every failure mode — checks unrunnable, context over budget, provider error, budget exhausted — reporting the degradation rather than exiting silently.
- **FR-11.3 (Should) (new in v1)** The system shall record a trace of the invocation — resolved scope, achieved depth, checks executed, tokens spent — sufficient to explain why a finding was produced.

*FR-11.2 generalises the timeout rule (FR-4.4b) to every failure mode; it is the single requirement most likely to be quietly violated under schedule pressure.*

---

## 5. Interface Summary

| Interface | Defined in | Stability |
|---|---|---|
| Change set (files + hunks) | FR-10.3c | Frozen — the v3 adapter substitutes its producer |
| `RelatedContextProvider` | §4.2.2 | Frozen — v2 adds an implementation, not a signature |
| Finding model + schema | FR-0.1, FR-0.4 | Versioned; changes require a schema-version bump |
| `emit_finding` tool schema | FR-5.6a | Equals the finding model; one definition, not two |
| JSON output | FR-8.2b, FR-8.2c | Versioned with the finding model |
| CLI flags and exit codes | FR-10.3a, FR-10.4c | Documented and stable across v1 patch releases |

---

## 6. Acceptance Criteria

v1 is complete when all of the following hold. Each is verifiable by execution, not inspection.

| # | Criterion | Verifies |
|---|---|---|
| **AC-1** | A single command reviews a public TS/JS repository end to end and prints findings, using only a free provider tier | FR-9.2a, FR-10.1 |
| **AC-2** | At least one finding in that run cites a real test or type-check result rather than text inference | FR-4.5c, FR-5.3 |
| **AC-3** | The JSON output validates against the published schema, and records depth, model, and resolved scope | FR-8.2b, FR-8.2c |
| **AC-4** | Findings originating from a pattern rule name that rule | FR-6.2a |
| **AC-5** | The regression harness runs as a test and reports a catch rate over the corpus | FR-6.2b, FR-6.2d |
| **AC-6** | The harness produces comparable catch rates when run at depth 0 and depth 1 | FR-6.2d, FR-2.6a |
| **AC-7** | A run where the tests could not execute says so, and is distinguishable in both outputs from a run that found nothing | FR-4.5a, FR-11.2 |
| **AC-8** | Requesting depth 2 reports `achievedDepth: 1` with reason `no-index`, and completes the review | FR-2.6d |
| **AC-9** | A malformed config fails with the offending field named; a missing provider key fails with a message saying so | FR-1.2d, FR-9.3 |
| **AC-10** | No module outside CF-7 imports a terminal-rendering dependency, and no module outside CF-1 resolves a change scope | FR-10.2, FR-2.6e |

**AC-5 and AC-7 are the two to defend under schedule pressure.** Without measurement there is no way to know whether the reviewer improved. Without the skipped/errored distinction, "no findings" silently means both "clean" and "broken".

**AC-8 and AC-10 are structural.** They verify that v2 and v3 are additions rather than rewrites, and they are cheap to check.

---

## 7. Excluded from v1

Full reasoning for each is in [`Draft/mvp-scope.md`](./Draft/mvp-scope.md) §4.

| Excluded | Requirements | Destination |
|---|---|---|
| Context depths 2 and above — importers, call sites, transitive | FR-2.3a, FR-2.3b | **v2** — a new implementation behind §4.2.2 |
| Risk triage and depth routing | FR-3.1–FR-3.4 | **v2** — the depth parameter of §4.2.2 is what a tier will set |
| Agent tool loop above a single pass | *(ADR-0001 step ceiling > 0)* | **v2** — a configuration change |
| Dependency audit | FR-4.3 | v2 |
| Blocking vs. non-blocking distinction | FR-5.4 | v2 — severity carries this for now |
| Cross-run de-duplication and local state | FR-5.5, FR-10.5 | v2 — weak locally; essential in v3 |
| Pattern coverage reporting | FR-6.2c | v2 |
| A broad default rule set | FR-6.3 | v2 — v1 ships five (FR-6.3a) |
| Fix snippets and evidence links | FR-7.1a, FR-7.3 | v2 |
| Platform support matrix and prebuilt binaries | FR-10.6 | v2 — v1 runs from source |
| Tolerating unparseable working trees | FR-10.7 | v2 — v1 requires a parseable tree and says so |
| **All GitHub integration** — Action trigger, PR comments, suggested-change blocks, status checks, example workflow, untrusted-code isolation, comment ledger | FR-1.1, FR-1.3, FR-1.4, FR-2.1, FR-7.1, FR-8.1a, FR-8.1c, FR-8.3, FR-9.2; [ADR-0003](./adr/0003-untrusted-code-isolation-and-fork-triggers.md), [ADR-0005](./adr/0005-cross-run-memory-as-hidden-comment-ledger.md) | **v3** |

FR-7.2 — suggestions are advisory, with no commit, push, or auto-apply — is satisfied trivially in v1: the system has no write path. It remains binding.

---

## 8. Non-Functional Requirements

Deferred to a dedicated pass. Open items carried into it:

- Concrete budgets: maximum review latency, context token cap, maximum change-set size handled
- Cost target per invocation, and the model-selection policy that meets it
- A quantitative catch-rate and false-positive target for the regression corpus (§6, AC-5)
- Execution isolation and the untrusted-code security model — **a v3 concern**; v1 executes only the developer's own code on their own machine

---

## 9. Known Risks

| # | Risk | Severity | Response |
|---|---|---|---|
| **R-1** | **The thesis is unproven at v1.** At depth 1, defects depending on a caller's assumptions may go uncaught. | High | Stated in §2.5. The depth interface plus the regression harness turn it into a controlled experiment in v2: same corpus, depth 1 vs depth 2, one variable (AC-6). |
| **R-2** | **A single pass may be too shallow.** | Medium | The ceiling is configuration (FR-5.7); raising it is a flip, not a rewrite. It also buys a real de-risking: v1 needs one reliable tool call, not fifteen. |
| **R-3** | **The depth interface is designed against one implementation.** | Medium | Confined by FR-2.6e to a single consumer boundary; a wrong guess costs one module. |
| **R-4** | **Prompt and context tuning has unbounded effort.** | High | The reason the CLI surface was chosen ([ADR-0006](./adr/0006-local-cli-core-action-as-adapter.md)): iteration runs in seconds. AC-5 gives the work a stopping condition. |
| **R-5** | **v1 does not address the stated problem.** It helps an author before they push, not a reviewer clearing a queue. | High | Structural, inherited from sequencing GitHub to v3. Stated in §1.1 and §2.2, and to be restated whenever v1 is demonstrated so it is not mistaken for the product. |
| **R-6** | **Five rules is not a product.** | Medium | Accepted (FR-6.3a). v1 proves the mechanism; breadth is authoring work that should not gate a first release. |

---

## Appendix A — Delivery sequence

Not normative; the recommended order of construction.

```mermaid
flowchart TD
    S1["1 · Walking skeleton<br/>CF-1 → CF-5 → CF-7<br/>Resolve a diff, call the model with no context,<br/>get a schema-valid finding back, print it."]
    S2["2 · Evidence<br/>CF-3<br/>Run the checks, record them, put them in the prompt.<br/>The differentiator now exists."]
    S3["3 · Measurement<br/>CF-8<br/>Five rules and the regression harness.<br/>From here, every change is measurable."]
    S4["4 · Context quality<br/>CF-2, CF-4<br/>The depth interface, its depth-1 implementation,<br/>and the budget policy. Measure against step 3."]
    S5["5 · Hardening<br/>CF-6 tuning, CF-9, FR-11.x<br/>Prompt iteration, config, diagnostics, budgets, docs."]

    S1 --> S2 --> S3 --> S4 --> S5

    style S1 fill:#eef3fa
    style S3 fill:#e8f7e8
```

Measurement is third, not last, on purpose: after step 3 every subsequent change can be evaluated instead of argued about, and step 4 can be assessed at depth 0 versus depth 1 on a fixed corpus.

## Appendix B — Traceability

| Requirement | Core function | Verified by |
|---|---|---|
| FR-0.1, FR-0.2, FR-0.3, FR-0.4 | CF-5 | AC-3 |
| FR-1.2a–d, FR-1.3a | CF-9 | AC-9 |
| FR-2.2, FR-2.3d, FR-2.4 | CF-2 | AC-1 |
| FR-2.6a–e | CF-2 | AC-8, AC-10 |
| FR-2.3c, FR-2.5, FR-2.5a–c | CF-4 | AC-1, AC-3 |
| FR-3.5 | CF-9 | AC-1 |
| FR-4.1, FR-4.2, FR-4.4a–b, FR-4.5a–c, FR-4.6 | CF-3 | AC-2, AC-7 |
| FR-5.1, FR-5.3, FR-5.7 | CF-6 | AC-2 |
| FR-5.2, FR-5.6, FR-5.6a–b | CF-5 | AC-3 |
| FR-6.1, FR-6.2a, FR-6.2b, FR-6.2d, FR-6.3a | CF-8 | AC-4, AC-5, AC-6 |
| FR-7.2 | — | Satisfied by absence of a write path |
| FR-8.1b, FR-8.2a–c, FR-8.4, FR-10.4a–c | CF-7 | AC-1, AC-3 |
| FR-9.1, FR-9.3 | CF-9 | AC-9 |
| FR-9.2a, FR-10.1 | Cross-cutting | AC-1 |
| FR-10.2 | Cross-cutting | AC-10 |
| FR-10.3a–c | CF-1 | AC-1 |
| FR-11.1, FR-11.2, FR-11.3 | Cross-cutting | AC-7 |
