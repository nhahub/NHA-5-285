# v1 Requirements — Agentic Code Review (Phase 1)

**Status:** Extract · **Source:** [`agentic-code-review-srs-v1.md`](./agentic-code-review-srs-v1.md) · **Date:** 2026-09-10

A requirements-only condensation of the v1 baseline. Rationale, risks, and delivery sequencing are omitted — see the source SRS, which remains authoritative where the two differ.

**Must** = required for v1 to be complete. **Should** = required if time allows; its absence does not block release.

---

## Scope in one line

A local CLI that reviews a working tree, staged changes, or a branch range in a TypeScript/JavaScript repository — running the project's own checks, gathering context at depth 0–1, and emitting schema-valid findings — plus a regression harness that reports a catch rate.

## Core functions

| # | Core function | Responsibility |
|---|---|---|
| **CF-1** | Change-set resolution | Turn an invocation into a concrete list of changed files and hunks |
| **CF-2** | Parsing and related context | Syntax trees, and related source retrieved at a requested depth |
| **CF-3** | Execution and evidence | Run the project's checks; record what happened |
| **CF-4** | Context assembly | Fit diff, related context, evidence, and rules into the model window |
| **CF-5** | Finding model and provider client | The canonical structure, its schema, and the model interface |
| **CF-6** | The review agent | A grounded, isolated review pass |
| **CF-7** | Output | Terminal rendering, JSON artifact, exit status |
| **CF-8** | Pattern library and regression harness | Rules, rule attribution, and measurement |
| **CF-9** | Configuration and diagnostics | Config, credentials, and legible failure |

---

## 1. CF-1 — Change-Set Resolution

| ID | Level | Requirement |
|---|---|---|
| FR-10.3a | Must | Resolve the change scope from an explicit selection among: uncommitted working-tree changes, staged changes only, or a comparison against a named branch or commit. |
| FR-10.3b | Must | Apply a documented default change scope when none is specified, and state the resolved scope in output. |
| FR-10.3c | Must | Express the resolved change set as a list of changed files and diff hunks, in a structure independent of how it was resolved. |

## 2. CF-2 — Parsing and Related Context

| ID | Level | Requirement |
|---|---|---|
| FR-2.2 | Must | Build a `tree-sitter` AST for changed TS/JS files, in the host process, without invoking the target language's toolchain. |
| FR-2.4 | Should | Include relevant surrounding context — function, class, and type boundaries — rather than raw line windows. |
| FR-2.3d | Must | Record which related files were included and why, for traceability. |
| FR-2.6a | Must | Expose related-context retrieval through a single interface parameterised by depth, with the implementation selected at run time. |
| FR-2.6b | Must | Provide a parser-backed implementation serving depths 0 and 1 without any repository-wide index. |
| FR-2.6c | Must | Every returned context unit carries the relation by which it was included (`imports`, `calls`, `imported-by`, `called-by`) and its distance from the change. |
| FR-2.6d | Must | A retrieval result states the depth actually achieved and, where lower than requested, the reason. Never silently downgrade. |
| FR-2.6e | Must | No consumer of the interface branches on which implementation served the request. |
| FR-2.6f | Must | Delegate depth-1 module-specifier resolution to a bundled resolver process over a documented request/response contract — started at most once per invocation, shipped with the package rather than fetched at review time, and not observable outside CF-2. |
| FR-2.6g | Must | Where the resolver process is unavailable or fails, fall back to heuristic path resolution, mark the result `degraded: 'unresolvable-imports'`, and complete the review. Its absence never fails an invocation. |

### 2.1 Context depth ladder — v1 implements depths 0 and 1

| Depth | What it includes | Resolvable by |
|---|---|---|
| **0** | Changed hunks, expanded to enclosing function, class, or type boundaries | Parsing the changed files |
| **1** | What the changed code reaches outward to: definitions of symbols it imports and calls | Parsing the changed files, then the files their imports name |
| 2–3 | Inbound importers, call sites, transitive neighbours | *Deferred to v2 — requires a reverse index* |

### 2.2 Normative interface

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

v1 ships `ParserContextProvider` (`maxDepth: 1`).

## 3. CF-3 — Execution and Evidence

| ID | Level | Requirement |
|---|---|---|
| FR-4.1 | Must | Run the project's test suite on the developer's machine and capture pass/fail results and output. |
| FR-4.2 | Must | Run build/type checks (e.g. `tsc`) and capture results. |
| FR-4.4a | Must | Enforce a configurable time budget on the execution phase and terminate execution when it is exceeded. |
| FR-4.4b | Must | On termination due to timeout, mark execution `timed-out`, skip remaining checks, and continue to produce a review reporting the timeout. |
| FR-4.5a | Must | Record, for each check, whether it was run, skipped, or errored. |
| FR-4.5b | Must | Record each executed check's pass/fail result and captured output. |
| FR-4.5c | Must | Make the execution record available to the review agent and include it in the structured output. |
| FR-4.6 | Must | The review agent cannot trigger check execution. Execution occurs once per invocation, before the review pass. |
| FR-4.7 | Must | Execute checks as subprocesses invoking the reviewed project's own toolchain and package manager, discovered from its manifest or named in configuration. Never import the reviewed project's dependencies into the host runtime; never require the reviewed project to install anything belonging to the system. |

## 4. CF-4 — Context Assembly

| ID | Level | Requirement |
|---|---|---|
| FR-2.3c | Must | Include the source of related definitions and call sites in the review context passed to the agent, up to the context cap. |
| FR-2.5 | Must | Cap context size to stay within model token limits, degrading gracefully when exceeded. |
| FR-2.5a | Must | Budget context per section — instructions and rules, the diff, related context, evidence — so that no section can starve another. |
| FR-2.5b | Must | When the budget is exceeded, evict context units in descending order of `distance`, and never truncate the diff itself. |
| FR-2.5c | Must | Reduce captured check output to failing test names, assertion messages, and stack frames referring to changed files before it enters the context. Retain full output for the structured output only. |

## 5. CF-5 — Finding Model and Provider Client

| ID | Level | Requirement |
|---|---|---|
| FR-0.1 | Must | Define a provider-independent internal finding representation — "the finding model" — as the single canonical structure for all review findings. |
| FR-0.2 | Must | Convert all model output into the finding model before any downstream use; no component consumes raw provider responses directly. |
| FR-0.3 | Must | A new provider is integratable by mapping its output to the finding model, without changes to downstream components. |
| FR-0.4 | Must | The finding model has a documented, versioned schema carrying a schema-version field. |
| FR-5.2 | Must | Each finding contains: file path, line or line-range, severity, category, rationale, and optionally the identifier of a matched pattern rule. |
| FR-5.6 | Must | The agent's output conforms to the finding model; all outputs are derived from it, not produced independently by the model. |
| FR-5.6a | Must | Findings enter the system exclusively through an `emit_finding` tool call validated against the finding-model schema at the call boundary. Prose the model produces is not parsed for findings. |
| FR-5.6b | Should | Where the provider cannot perform tool calls, fall back to schema-validated structured output with a documented retry cap, and report which path was used. |

## 6. CF-6 — The Review Agent

| ID | Level | Requirement |
|---|---|---|
| FR-5.1 | Must | The review agent operates in a context isolated from any code-writing agent — no shared history or state. |
| FR-5.3 | Must | Incorporate execution results (CF-3) and pattern-library rules (CF-8) into findings. |
| FR-5.7 | Must | The review step's tool-call ceiling is a configuration value with a documented default of **zero** — a single model pass in which `emit_finding` is the only tool exposed. |
| FR-5.7a | Should | When the ceiling is above zero, expose exactly three read-only investigation tools: `read_file`, `get_outline`, `search_repo`. No tool has side effects; no tool triggers check execution (FR-4.6). |
| FR-5.7b | Must | The ceiling is not raised above its default until a single-pass baseline catch rate has been recorded on the regression corpus (FR-6.2d). Any subsequent ceiling is justified by a measured comparison against that baseline. |
| FR-5.7c | Should | When the ceiling is above zero, tell each model turn how many tool calls remain, and report whether the review ended because the agent finished or because the ceiling was reached. |
| FR-5.7d | Should | Findings have the same structure and meaning at every ceiling value. A change of ceiling changes how much is found, never what a finding is. |
| FR-5.8 | Must | Confine the agent framework to CF-6. No module outside CF-6 imports it, and the pipeline steps outside CF-6 are callable as ordinary functions without it. |

## 7. CF-7 — Output

| ID | Level | Requirement |
|---|---|---|
| FR-8.1b | Must | The terminal summary states the resolved change scope, the checks run and their results, the count of findings by severity, and an overall verdict. |
| FR-8.2a | Must | Serialize the finding model to JSON as a machine-readable artifact. |
| FR-8.2b | Must | The JSON conforms to the finding model's versioned schema, including findings, severities, and the evidence record. |
| FR-8.2c | Must | The structured output records the achieved context depth, the tool-call ceiling in force and the number of tool calls actually made, the completion status (FR-5.7c), the model and schema versions used, and the resolved change scope. |
| FR-8.4 | Should | Document and version the structured output schema. |
| FR-10.4a | Must | Render findings to the terminal, derived from the finding model and not produced independently. |
| FR-10.4b | Must | Provide machine-readable output on request, conforming to the schema in FR-8.2b. |
| FR-10.4c | Should | Exit with a status code reflecting the review outcome, documented and stable across versions. |

## 8. CF-8 — Pattern Library and Regression Harness

| ID | Level | Requirement |
|---|---|---|
| FR-6.1 | Must | Load a configurable pattern library of "wrong vs. correct" examples and project standards. |
| FR-6.2a | Must | When a finding is generated from a pattern-library rule, the finding references the identifier of the matched rule. |
| FR-6.2b | Must | Support a regression set of pattern examples with expected outcomes, runnable as a test, so pattern-matching behaviour can be verified across changes. |
| FR-6.2d | Must | The regression harness reports a catch rate over the corpus, and accepts both a context depth and a tool-call ceiling so that results at different settings are directly comparable. |
| FR-6.2e | Should | Regression runs pin the settings that affect reproducibility — depth, ceiling, model, sampling parameters — and record them with the result. |
| FR-6.3a | Must | Ship at least five pattern rules, each with a wrong example, a correct example, and at least one corresponding regression case. |

## 9. CF-9 — Configuration and Diagnostics

| ID | Level | Requirement |
|---|---|---|
| FR-1.2a | Must | Read configuration from `.agentic-review.yml` at the repository root when present. |
| FR-1.2b | Must | When the file is absent, apply a documented built-in default configuration. |
| FR-1.2c | Must | When the file is present but a field is missing, apply that field's documented default value. |
| FR-1.2d | Must | When the file is present but malformed, fail with an error message identifying the offending field; never fall back silently. |
| FR-1.3a | Must | Read the model provider credential from the local environment or user-level configuration — never a hard-coded key, never a file committed to the repository. |
| FR-3.5 | Must | Exclude configured generated, vendored, and build-output paths from review, using a documented default exclusion list. |
| FR-9.1 | Must | Ship with README, LICENSE, and CLI usage documentation. |
| FR-9.3 | Must | Provide clear failure messages when prerequisites — a test script, a provider key, a git repository, a parseable tree — are missing or unusable. |

## 10. Cross-cutting

| ID | Level | Requirement |
|---|---|---|
| FR-10.1 | Must | Provide a command-line interface that reviews a local change set without requiring GitHub API access or repository credentials. |
| FR-10.2 | Must | No adapter contains logic that determines whether something is a finding. |
| FR-9.2a | Must | Complete an end-to-end review of a public TS/JS repository on a developer machine, using only a free model provider tier. |
| FR-11.1 | Must | Enforce a token and call budget per invocation and stop cleanly when it is reached, reporting that it did so. |
| FR-11.2 | Must | Produce a review under every failure mode — checks unrunnable, context over budget, provider error, budget exhausted — reporting the degradation rather than exiting silently. |
| FR-11.3 | Should | Record a trace of the invocation — resolved scope, achieved depth, checks executed, tokens spent — sufficient to explain why a finding was produced. |
| FR-7.2 | Must | Suggestions are advisory: no commit, push, or auto-apply. Satisfied in v1 by the absence of a write path. |

---

## 11. Acceptance criteria

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
| **AC-10** | No module outside CF-7 imports a terminal-rendering dependency, no module outside CF-1 resolves a change scope, and no module outside CF-6 imports the agent framework | FR-10.2, FR-2.6e, FR-5.8 |
| **AC-11** | A single-pass baseline catch rate is recorded before any ceiling above zero is enabled, and the harness reports catch rate and mean tool calls at two ceilings on that same corpus | FR-5.7b, FR-6.2d, FR-6.2e |
| **AC-12** | With the resolver sidecar made unavailable, a review still completes and reports `degraded: 'unresolvable-imports'`, distinguishably from a run where every import resolved | FR-2.6f, FR-2.6g, FR-11.2 |

---

## 12. Out of scope for phase 1

Context depths 2 and above (FR-2.3a, FR-2.3b) · risk triage and depth routing (FR-3.1–FR-3.4) · `find_references` and reverse `get_definition` · `get_check_result` and `lookup_pattern_rule` as tools (preloaded instead) · dependency audit (FR-4.3) · blocking vs. non-blocking distinction (FR-5.4) · cross-run de-duplication and local state (FR-5.5, FR-10.5) · pattern coverage reporting (FR-6.2c) · a broad default rule set (FR-6.3) · fix snippets and evidence links (FR-7.1a, FR-7.3) · platform support matrix and prebuilt binaries (FR-10.6) · tolerating unparseable working trees (FR-10.7) · **all GitHub integration** (FR-1.1, FR-1.3, FR-1.4, FR-2.1, FR-7.1, FR-8.1a, FR-8.1c, FR-8.3, FR-9.2 — v3).

Non-functional requirements — latency, token caps, cost targets, catch-rate and false-positive targets, supported OS and Python versions, execution isolation — are deferred to a dedicated pass.
