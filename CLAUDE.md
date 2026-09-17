# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

**This repository contains no source code yet.** It is a specification and architecture-decision repository for a planned tool. There is no `pyproject.toml`, no build, no test runner, and no lint config — do not invent commands for them or claim to have run them. The only executable content is a Claude Code skill (`git-mentor/`).

The work so far is the design of an **agentic code reviewer**: a local CLI that reviews a TypeScript/JavaScript change set by parsing it, running the repository's own tests and type-check, and passing that evidence to a single model pass that emits schema-validated findings.

## Document authority — read this before editing any doc

Exactly one document defines what to build at any time. The hierarchy is strict:

| Document | Authority |
|---|---|
| `Docs/agentic-code-review-srs-v1.md` | **Normative.** The build target. Wins on any disagreement. |
| `Docs/technical_stack.md` | **Normative for technology selection only** — which library, which protocol, which layout. Subordinate to the SRS: it never relaxes a requirement. If a library cannot satisfy one, the library is wrong. |
| `Docs/adr/*.md` | Normative *where cited by* the v1 SRS. |
| `Docs/Draft/**` | **Non-normative.** Rationale, background, and requirements for v2/v3. |

The split between the SRS and the stack document is deliberate: the SRS says *what must be true*, the stack says *what it is built with*, and ADR-0007 says *why that stack*. Library choices move — versions get pinned, packages get swapped — and those changes belong in `technical_stack.md`, not in an append-only ADR. Reversing ADR-0007's **reasoning** still needs a new ADR.

`Docs/Draft/agentic-code-review-srs.md` is the full v1–v3 requirement catalogue and the identifier registry the ADRs cite; `Docs/Draft/mvp-scope.md` is the analysis that selected v1's scope and explains every cut. Both are historical records — they are *not* the build target, even though they read like specifications.

## Conventions that must be preserved

- **Requirement identifiers are stable and are never renumbered.** A requirement keeps its `FR-x.y` identifier across versions; a version tag says when it applies. Renumbering silently breaks cross-references in the ADRs, the harness design, and the traceability table (SRS Appendix B). Requirements introduced by the v1 baseline are marked `(new in v1)`.
- **Must / Should.** Must = required for the version to be complete. Should = included if time allows; its absence does not block release.
- **ADRs are append-only.** Never edit a decision to reflect a change of mind — write a new ADR that supersedes it, and update the status table in `Docs/adr/README.md`. Status values: Proposed / Accepted / Superseded / Deprecated. ADR-0006 and ADR-0007 are Accepted; the other five are Proposed.
- **Read ADR-0006 first, then ADR-0007.** 0006 was decided late and rescoped four earlier records (0001–0003, 0005), which were written assuming a GitHub Action was the only delivery surface. 0007 is the only record naming an implementation technology, and it amends one consequence of 0006 (distribution: PyPI, not npm).
- Docs cross-link with relative paths and use mermaid diagrams throughout. Moving or renaming a file under `Docs/` requires fixing the inbound links in `Docs/README.md`, `Docs/adr/README.md`, and the SRS front matter.
- `Docs/Draft/agentic-code-review-srs-ar.md` is an Arabic translation of the catalogue. Changes to the catalogue leave it stale; say so rather than silently diverging.

## Architecture the code will take

**One surface-independent core behind thin adapters** (ADR-0006). v1 builds the CLI adapter only; the GitHub Action is v3. An adapter resolves what to review, renders findings, and stores state — **it never decides what counts as a finding** (FR-10.2).

Orchestration is a **fixed pipeline owned by our code**, not by the model (ADR-0001). Nine core-function blocks, `CF-1` through `CF-9`, each owning a disjoint set of requirements:

```
CF-1 change-set resolution → CF-2 parsing + related context ─┐
CF-3 execution + evidence ───────────────────────────────────┼→ CF-4 context assembly
                                                              → CF-6 review agent (the only model step)
                                                              → CF-5 finding model → CF-7 terminal + JSON output
CF-8 pattern library + regression harness · CF-9 config + diagnostics
```

Two commands, one core: a `review` command producing findings, and a `regression` command producing a catch rate over a curated defect corpus.

### The load-bearing constraints

These are the ones that make v2 and v3 additions rather than rewrites. Treat a change that violates one as a design change requiring an ADR, not a refactor:

- **FR-2.6e** — no consumer branches on which `RelatedContextProvider` implementation served a request. v1 ships a parser-backed provider serving depths 0–1; v2 adds an index-backed one behind the same frozen signature (SRS §4.2.2).
- **FR-5.6a** — findings enter the system *only* through an `emit_finding` tool call validated against the finding-model schema at the call boundary. Model prose is never parsed for findings (ADR-0004).
- **FR-5.7** — v1's agent completes a review in a single model pass. Step ceiling is zero; `emit_finding` is the only tool. Raising it later is configuration, not restructuring.
- **FR-4.6** — the agent cannot trigger check execution. Checks run once per invocation, before the review pass (ADR-0002).
- **FR-10.3c** — the change set is a files-and-hunks structure independent of how it was resolved. This is the seam the v3 Action adapter substitutes into.
- **FR-11.2** — a review is produced under *every* failure mode (checks unrunnable, context over budget, provider error, budget exhausted), reporting the degradation. A silent failure is indistinguishable from a clean review.
- **FR-5.8** — the agent framework lives only in CF-6. Nothing outside it imports LangGraph, and every other pipeline step is callable as an ordinary function. This is what keeps ADR-0001's "our code owns orchestration" true once a framework is in the repository.
- **FR-2.6g** — the resolver sidecar's absence degrades and reports; it never fails an invocation. An optional prerequisite must not quietly become a required one.

`Docs/agentic-code-review-srs-v1.md` §6 lists twelve acceptance criteria (AC-1…AC-12), each verifiable by execution. AC-5 and AC-7 are flagged as the ones to defend under schedule pressure; AC-8, AC-10 and AC-12 are the cheap structural checks on the constraints above.

### Planned stack and environment

Summary only — **`Docs/technical_stack.md` is the authority**, and carries the sidecar protocol, repository layout, import contracts, dependency inventory, and the version pins. Decided in **ADR-0007** (Accepted). **The host language is not the target language:** the harness is Python; the code it reviews is TypeScript.

- **Python** with `tree-sitter` bindings as a native extension, distributed as a **PyPI package** with a console entry point (`uv tool install` / `pipx`). OS/Python-version support is a distribution contract.
- **LangChain** for the provider interface, tool binding (FR-5.6a) and structured output (FR-5.6b); **LangGraph confined to CF-6** (FR-5.8) — the pipeline outside the review step is plain Python functions. At ceiling zero the review step is a one-node graph, which is what makes FR-5.7's "configuration, not restructuring" literally true.
- **A bundled Node resolver sidecar** answers depth-1 module resolution from the TypeScript compiler's own algorithm (FR-2.6f). Started at most once per invocation, shipped as package data, never fetched at review time. Node is a runtime prerequisite for authoritative depth 1 and **never** for installation — its absence degrades and reports (FR-2.6g, AC-12). The sidecar is private to CF-2; nothing outside it may know it exists.
- **Pydantic** for the finding model, so the type, the JSON Schema (FR-0.4) and the `emit_finding` tool schema come from one definition — SRS §5 requires "one definition, not two".
- **Typer + Rich** for CF-7, **pytest** for the CF-8 regression corpus.
- Checks run as **subprocesses through the reviewed project's own toolchain** (FR-4.7). The harness never imports the project's dependencies, and never asks the project to install its own.

Config lives in `.agentic-review.yml` at the repository root, with documented defaults and loud (never silent) validation failure. The provider credential comes from the environment or user-level config — never hard-coded, never committed. Default provider is the NVIDIA NIM free tier, reached through an OpenAI-compatible client so a swap is a base URL and a model name.

The binding constraint is **latency, not cost**: a developer waiting at a prompt abandons the tool after roughly 10–30 seconds.

### Build order

`Docs/agentic-code-review-srs-v1.md` Appendix A gives the recommended construction sequence: walking skeleton (CF-1 → CF-5 → CF-7), then evidence (CF-3), then **measurement (CF-8)**, then context quality (CF-2, CF-4), then hardening. Measurement is deliberately third, not last — after it, every subsequent change can be evaluated rather than argued about.

## Known gap to state honestly

v1 proves the pipeline works end to end; it does **not** yet prove the project's thesis. At context depth 1 the reviewer can judge whether a change is internally sound, not whether it violates an assumption held by a caller it never looked at. v1 also serves the *author* before they push, not the reviewer clearing a queue named as the primary persona in the problem definition. Both are stated in SRS §2.5 and §9 (R-1, R-5) and are meant to be restated whenever v1 is demonstrated.

## git-mentor skill

`git-mentor/` is a Claude Code skill (`SKILL.md` plus `references/`) for commit planning, history review, Git recovery, and PR descriptions. It is currently untracked and sits at the repository root rather than under `.claude/skills/`. Its hard rules apply when doing Git work here: never assume repository state without inspecting it, never assign one file to two commits, use Conventional Commits with scopes, and feed multi-line commit messages on stdin via a heredoc matching the invoking shell — PowerShell's `@'...'@` leaks its delimiters when used from the Bash tool.
