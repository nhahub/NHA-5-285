# Software Requirements Specification — Agentic Code Review (v1)

**Status:** Draft · **Scope:** v1 (TypeScript/JavaScript, GitHub Action) · **Audience:** Open-source contributors and adopters

---

## 1. Introduction

### 1.1 Purpose

This document specifies the requirements for **Agentic Code Review**, an open-source system that performs an autonomous first-pass review on GitHub pull requests. It defines the business case, scope, and functional requirements for version 1, and serves as the reference against which the system is built, tested, and evaluated. Non-functional requirements (performance, isolation, cost budgets) are addressed in a separate pass (§5, planned).

### 1.2 Intended Audience

- **Contributors** building or extending the system — the primary readers of the functional requirements.
- **Adopters** integrating the Action into their repositories — served by the scope, assumptions, and usability requirements.
- **Reviewers/maintainers** evaluating whether a change meets the specification.

Readers seeking the business rationale need only §1–§2. Readers implementing or testing should continue to the functional requirements (§4).

### 1.3 Product Scope

Agentic Code Review automates the initial review pass on pull requests so human reviewers can concentrate on high-risk changes. It gathers full repository context, executes tests and checks in an isolated sandbox, runs a review agent in a context isolated from any code-writing agent, and proposes fixes as review comments. It ships as a GitHub Action using a single free/low-cost AI provider, and emits both a human-readable summary and a structured machine-readable artifact. v1 targets TypeScript/JavaScript repositories. Full in-scope and out-of-scope boundaries are in §2.3.

### 1.4 References

- Agentic Code Review — Project Definition (v1)
- Non-Functional Requirements — deferred pass (planned, to become §5)

---

## 2. Overall Description

### 2.1 Business Case

#### 2.1.1 Problem Definition

AI-assisted development has sharply increased the volume and size of pull requests, outpacing the capacity of human reviewers and creating a review bottleneck. Existing automated tools address only fragments of the problem: linters catch syntax but miss semantics and cross-file dependencies; single-shot LLM reviewers give shallow line comments without executing code or understanding the wider repository, and — when the same model both writes and reviews — suffer from self-confirmation bias. There is no accessible, budget-conscious tool that performs a genuinely autonomous, context-aware, execution-backed first-pass review while keeping humans focused on the changes that actually carry risk.

#### 2.1.2 Objectives

1. **Automate the first-pass review** so human attention is reserved for high-risk changes.
2. **Ground reviews in real context and execution** — full-repo context, dependency-aware analysis, and sandboxed test/build/scan runs rather than text-only inference.
3. **Eliminate self-confirmation bias** by running the review agent in a fresh context, isolated from any code-writing agent.
4. **Triage by blast radius** — deterministically route PRs so critical changes (security, core logic) get deeper review and trivial ones (docs, dep bumps) can be fast-tracked.
5. **Propose actionable fixes** as review comments, backed by execution evidence (auto-applied remediation is deferred to v2).
6. **Operate within a $20/free budget** by using a single free/low-cost provider (e.g. NVIDIA NIM free tier), with model calls wrapped behind a thin interface so the provider can be swapped later without rearchitecting.
7. **Produce dual output** — human summaries and structured data for downstream automation.
8. **Ship as a usable open-source project** — clear docs, easy adoption, and an extensible base others can build on.

#### 2.1.3 Success Criteria

- The Action runs end-to-end on a public repo using only free tiers.
- Reviews are grounded in executed test/build results, not text inference alone.
- Findings are emitted in the canonical finding model (§4, FR-0) and serialized to schema-valid JSON.
- A new contributor can adopt the Action using the shipped README, example workflow, and docs.

*(Quantitative targets for these criteria are deferred to the NFR pass.)*

### 2.2 Product Perspective

The system is a self-contained GitHub Action, not a hosted service. It runs inside the adopter's CI on GitHub-hosted runners, invoking an external AI provider over the network. It holds no persistent server-side state; review history lives in PR comments and per-run artifacts. This positions v1 deliberately below the complexity of a hosted GitHub App (webhooks, backend, database), which is out of scope.

### 2.3 Scope Boundaries

#### 2.3.1 In Scope (v1)

- GitHub Action triggered on PR open/update
- Context gathering: repo checkout, `tree-sitter`-based AST/dependency analysis (TS/JS)
- Sandboxed execution of tests, build checks, and basic security scans on GitHub-hosted runners
- Fresh-context review agent, decoupled from code authorship
- Deterministic blast-radius risk triage driving review depth (and optionally lighter vs. stronger model choice)
- Single-provider model integration (e.g. NVIDIA NIM free tier), wrapped behind a thin swap-friendly interface
- Fix suggestions delivered as review comments (including suggested-change blocks where possible)
- Dual output: PR-comment summary + structured JSON artifact
- A configurable pattern library with "wrong vs. correct" examples
- TypeScript/JavaScript support only
- Open-source project hygiene: README, LICENSE, usage docs, example workflow

#### 2.3.2 Out of Scope (v1)

- Automated/auto-applied remediation and fix-and-verify loops (deferred to v2)
- Languages other than TS/JS
- Hosted GitHub App with webhooks and persistent backend
- Web dashboard / analytics UI
- Non-GitHub platforms (GitLab, Bitbucket)
- Multimodal / architectural-diagram analysis — deferred
- Team governance, RBAC, audit-compliance features
- Self-hosted sandbox infrastructure (gVisor / Firecracker)
- Multi-provider routing, fallback chains, and config-driven provider abstraction

### 2.4 Stakeholders

| Stakeholder | Interest |
|---|---|
| Repository maintainers | Reduced review load; trustworthy first-pass triage |
| PR authors (human & AI-assisted) | Fast, actionable, execution-backed feedback |
| Open-source contributors | Clear, extensible codebase and requirements |
| Project maintainer | Shippable, budget-bound, maintainable v1 |

### 2.5 Assumptions & Constraints

- Budget limited to free tiers / a single ~$20 plan; no dedicated GPU or paid inference infrastructure.
- Runs on free GitHub Actions compute; execution time and resources are bounded by runner limits.
- Requires repositories with a runnable test suite for execution-backed verification to add value.
- As an open-source tool, model API keys must be handled via repo/org secrets, never hard-coded.
- v1 is single-provider and single-language by deliberate scoping decision, not technical limitation.

### 2.6 Operating Environment

- **Platform:** GitHub (hosted runners, Actions, PR API).
- **Trigger events:** pull request `opened`, `synchronize`.
- **External dependency:** one AI model provider reachable over HTTPS (NVIDIA NIM free tier as default).
- **Target repositories:** TypeScript/JavaScript projects with a runnable test script.

---

## 3. Glossary

| Term | Definition |
|---|---|
| **Agentic code review** | An automated review that gathers repository context, executes tools (tests/builds/scans), and reasons over the results — as opposed to static linting or single-shot LLM commenting. |
| **AST (Abstract Syntax Tree)** | A structured tree representation of source code used to analyze symbols, dependencies, and structure. Produced here via `tree-sitter`. |
| **Blast radius** | The potential impact scope of a change, used to assign a risk tier and route review depth. |
| **Context Gatherer** | The component that checks out the PR, parses changed files, and assembles cross-file review context. |
| **Finding model (FR-0)** | The provider-independent internal representation for all review findings; the single canonical structure that downstream outputs are derived from. |
| **Fresh-context review** | Running the review agent in a context isolated from any code-writing agent, to avoid self-confirmation bias. |
| **Fresh-Context Review Agent** | The component that produces findings from the gathered context, execution evidence, and pattern library. |
| **GitHub Action** | A CI workflow unit that runs in a repository's pipeline; the deployment form of v1 (as opposed to a hosted GitHub App). |
| **Pattern library** | A configurable set of "wrong vs. correct" examples and project standards the agent applies when generating findings. |
| **PR (Pull Request)** | A proposed set of changes to a repository, the unit reviewed by the system. |
| **Risk tier** | A deterministic classification (e.g. trivial / normal / critical) that drives review depth and optional model selection. |
| **Remediation Engine** | The component responsible for fix proposals; in v1 limited to advisory comment suggestions (auto-apply deferred to v2). |
| **Suggested-change block** | A GitHub review-comment feature that proposes a specific localized edit the author can accept directly. |
| **Tool Sandbox** | The isolated execution environment (GitHub-hosted runner in v1) where tests, builds, and scans run. |
| **`tree-sitter`** | An incremental parsing library used to build ASTs for dependency and structure analysis. |
| **Must / Should** | Requirement priority tags: **Must** = v1 core; **Should** = v1 if time allows. |
| **NFR** | Non-Functional Requirement (performance, isolation, cost, latency) — addressed in a separate pass. |

---

## 4. Specific Requirements (Functional)

Requirements are written as testable "the system shall…" statements, grouped by component and mapped to the Module 2 architecture. Each is tagged **Must** (v1 core) or **Should** (v1 if time allows). Concrete thresholds (time/memory budgets, isolation guarantees) are deferred to §5 (NFR pass).

### 4.0 FR-0 — Canonical Data Model (the "finding model")

The single canonical structure for all review findings. Defined once here; every other requirement references FR-0 rather than redefining it.

- **FR-0.1 (Must)** The system shall define a provider-independent internal finding representation ("the finding model") as the single canonical structure for all review findings.
- **FR-0.2 (Must)** All model output shall be converted into the finding model before any downstream use; no component shall consume raw provider responses directly.
- **FR-0.3 (Must)** A new provider shall be integratable by mapping its output to the finding model without changes to downstream components.
- **FR-0.4 (Must)** The finding model shall have a documented, versioned schema carrying a schema-version field.

### 4.1 FR-1 — Trigger & Integration

- **FR-1.1 (Must)** The system shall run as a GitHub Action triggered on pull request `opened` and `synchronize` (new commits) events.
- **FR-1.2a (Must)** The system shall read configuration from `.agentic-review.yml` at the repo root when present.
- **FR-1.2b (Must)** When the file is absent, the system shall apply a documented built-in default configuration.
- **FR-1.2c (Must)** When the file is present but a field is missing, the system shall apply that field's documented default value.
- **FR-1.2d (Must)** When the file is present but malformed (invalid YAML or schema), the system shall fail with an error message identifying the offending field, and shall not fall back silently.
- **FR-1.3 (Must)** The system shall authenticate to the model provider using a repo/org secret, never a hard-coded key.
- **FR-1.4 (Should)** The system shall allow the Action to be skipped via a label or config flag (e.g. `skip-agentic-review`).

*(Documented default configuration values live in the config-schema appendix, not in requirement text.)*

### 4.2 FR-2 — Context Gathering

- **FR-2.1 (Must)** The system shall check out the PR branch and identify the changed files and diff hunks.
- **FR-2.2 (Must)** The system shall build a `tree-sitter` AST for changed TS/JS files.
- **FR-2.3a (Must)** For each symbol modified in the diff, the system shall identify the files that import or export that symbol.
- **FR-2.3b (Must)** For each modified function or method, the system shall identify its direct call sites within the repository.
- **FR-2.3c (Must)** The system shall include the source of these related definitions and call sites in the review context passed to the agent, up to the context cap (FR-2.5).
- **FR-2.3d (Should)** The system shall record which related files were included and why (imported-by / calls / called-by), for traceability.
- **FR-2.4 (Should)** The system shall include relevant surrounding context (function/class boundaries, type definitions) rather than raw line windows.
- **FR-2.5 (Should)** The system shall cap context size to stay within model token and runner limits, degrading gracefully when exceeded.

### 4.3 FR-3 — Risk Triage (Blast Radius)

- **FR-3.1 (Must)** The system shall deterministically classify each PR into a risk tier (e.g. trivial / normal / critical) using file-path and change-type rules.
- **FR-3.2 (Must)** The triage rules shall be configurable (path globs → risk tier) so projects can mark security/core paths as critical.
- **FR-3.3 (Must)** The system shall route review depth by tier (fast-track trivial changes, deeper review for critical).
- **FR-3.4 (Should)** The system shall optionally select a lighter vs. stronger model by tier.

### 4.4 FR-4 — Sandboxed Execution

- **FR-4.1 (Must)** The system shall run the project's test suite in the isolated runner and capture pass/fail results and output.
- **FR-4.2 (Must)** The system shall run build/type checks (e.g. `tsc`) and capture results.
- **FR-4.3 (Should)** The system shall run `npm audit` and capture its findings.
- **FR-4.4a (Must)** The system shall enforce a configurable time budget on the execution phase and terminate execution when it is exceeded.
- **FR-4.4b (Must)** On termination due to timeout, the system shall mark execution as `timed-out`, skip remaining checks, and continue to produce a review reporting the timeout.
- **FR-4.5a (Must)** The system shall record, for each check, whether it was run, skipped, or errored.
- **FR-4.5b (Must)** The system shall record each executed check's pass/fail result and captured output.
- **FR-4.5c (Must)** The system shall make this execution record available to the review agent (FR-5) and include it in the structured output (FR-8.2).

*(Isolation guarantees and specific time/resource budget values are deferred to §5, the NFR pass.)*

### 4.5 FR-5 — Fresh-Context Review Agent

- **FR-5.1 (Must)** The review agent shall operate in a context isolated from any code-writing agent (no shared history/state).
- **FR-5.2 (Must)** Each finding shall contain: file path, line or line-range, severity, category, rationale, and (optionally) a suggested-fix reference — conforming to the finding model (FR-0).
- **FR-5.3 (Must)** The agent shall incorporate execution results (FR-4) and pattern-library rules (FR-6) into its findings.
- **FR-5.4 (Should)** The agent shall distinguish blocking issues from non-blocking suggestions.
- **FR-5.5 (Should)** The agent shall avoid duplicate/near-duplicate comments on unchanged findings across re-runs.
- **FR-5.6 (Must)** The agent's output shall conform to the finding model (FR-0); FR-8 outputs shall be derived from it, not produced independently by the model.

### 4.6 FR-6 — Pattern Library

- **FR-6.1 (Must)** The system shall load a configurable pattern library of "wrong vs. correct" examples and project standards.
- **FR-6.2a (Must)** When a finding is generated from a pattern-library rule, the finding shall reference the identifier of the matched rule.
- **FR-6.2b (Must)** The system shall support a regression set of pattern examples with expected outcomes, runnable as a test, so pattern-matching behavior can be verified and monitored across changes.
- **FR-6.2c (Should)** The system shall report pattern-library coverage (which rules fired) in the structured output.
- **FR-6.3 (Should)** The system shall ship a default TS/JS pattern set that projects can extend or override.

### 4.7 FR-7 — Fix Suggestions (comments only, v1)

- **FR-7.1 (Must)** The system shall propose fixes as review comments, using GitHub suggested-change blocks where the fix is a localized edit.
- **FR-7.2 (Must)** Suggestions shall be advisory only — the system shall not commit, push, or auto-apply changes in v1.
- **FR-7.3 (Should)** Each suggestion shall link to the finding and evidence that motivated it.

### 4.8 FR-8 — Output

- **FR-8.1a (Must)** The system shall post exactly one summary comment per review run on the PR.
- **FR-8.1b (Must)** The summary comment shall state the risk tier, the checks run and their results, the count of findings by severity, and an overall verdict.
- **FR-8.1c (Should)** On re-run, the system shall update its existing summary comment rather than post a new one.
- **FR-8.2a (Must)** The system shall serialize the finding model (FR-0) to JSON as a machine-readable artifact.
- **FR-8.2b (Must)** The JSON shall conform to the finding model's versioned schema (FR-0.4), including findings, severities, evidence/execution record, and triage result.
- **FR-8.3 (Should)** The system shall set a non-blocking status/check summarizing the review outcome.
- **FR-8.4 (Should)** The structured output schema shall be documented and versioned (see FR-0.4).

### 4.9 FR-9 — Open-Source Usability

- **FR-9.1 (Must)** The system shall ship with README, LICENSE, usage docs, and an example workflow file.
- **FR-9.2 (Must)** The system shall run against a public repo using only free tiers (GitHub-hosted runner + free model provider).
- **FR-9.3 (Should)** The system shall provide clear failure messages when prerequisites (e.g. test script, API key) are missing.

---

## 5. Non-Functional Requirements (Planned)

Deferred to a dedicated pass. Open items carried in from the functional work:

- Execution isolation guarantees and the security model for untrusted PR code (residue of former FR-4.4).
- Concrete budgets: max execution runtime, memory cap, max context tokens, max PR size handled.
- Latency / cost targets per risk tier.
- Quantitative targets for the §2.1.3 success criteria.

---

## Appendix A — Deferred to v2

- Automated/auto-applied remediation and fix-and-verify loops
- Advanced scanning: secret detection (e.g. TruffleHog), OWASP tooling, and supply-chain / dependency-provenance analysis
- Languages other than TS/JS
- Multi-provider routing and fallback chains (note: FR-0 finding model keeps this a data-mapping task, not a rearchitecture)
