# Competitive Landscape

This document positions **Agentic Code Review** against existing tools in and around the automated code-review space. It is written for contributors and adopters deciding whether this project fits their needs, and for maintainers keeping the project honest about where it does and does not compete.

For plain, non-comparative descriptions of each tool, see [`tool-reference.md`](./tool-reference.md).

> Snapshot as of September 2026. Pricing and features change quickly; re-verify before relying on specifics.

## How to read this

The tools people mention in the same breath as this project are not actually competing on one axis. They fall into three groups:

1. **Full-context AI reviewers** — the direct conceptual competitors (Greptile, CodeRabbit, Qodo).
2. **Managed multi-agent reviewers** — architecturally different, but the best design reference (Claude Code — Code Review).
3. **Different categories entirely** — a process linter (Danger/DangerJS) and a workflow tool (Graphite) that attack the same underlying problem from other angles.

Our scope is deliberately narrow: an **open-source GitHub Action with a local CLI over the same core** ([ADR-0006](../adr/0006-local-cli-core-action-as-adapter.md)), **TypeScript/JavaScript only**, a **single free/low-cost model provider** behind a thin interface, **fix suggestions as comments only** (auto-remediation deferred to v2), and a **canonical, versioned finding model** as the single source of truth for output.

Note that the CLI is not a differentiator — Greptile, CodeRabbit and Claude Code all ship one. It is **table stakes we now meet**, adopted primarily because developing a review agent through a four-minute CI loop is untenable. The differentiators below are unchanged by it.

**Sequencing caveat (2026-09-08).** GitHub integration is now deferred to **v3** ([SRS §2.3.3](./agentic-code-review-srs.md)), so v1 and v2 ship the CLI alone. Read the positioning below as describing the product at v3. Until then the project competes only where every tool in this document also offers a local mode — which is the weakest ground of the three differentiators, since the execution-backed claim thins on a machine where the developer can already run their own tests. This is a deliberate engineering sequence, not a repositioning; it does mean the competitive claim is not testable against real adopters until v3.

---

## Tier 1 — Full-context AI reviewers (direct competitors)

### Greptile
The closest match to our architectural thesis — reviews grounded in whole-repository context rather than diff-local feedback. Its credit-metered economics (one standard review = one credit) are a useful confirmation that **per-review inference cost is the binding constraint** in this category, which is exactly what our blast-radius triage and single-free-provider decisions are built around. Its free tier for OSS projects competes directly with our "free for public repos" goal — an adopter can already get context-aware reviews at no cost from a hosted tool.

### CodeRabbit
The market-share leader, and it has already shipped, as paid features, several things that sit on our roadmap or in our design: blast-radius triage, a deterministic "codegraph" (a more ambitious cousin of our tree-sitter dependency analysis), and continuous "Learnings" (adjacent to our pattern library). Realistically, our v1 feature set is close to CodeRabbit's entry tier minus the polish and the six-million-repo moat. **We do not try to out-feature CodeRabbit.** Our edge is openness, zero cost, and auditability — not breadth.

### Qodo (formerly Codium)
The most important one for contributors to study, because its PR-review engine (**PR-Agent / Qodo Merge**) has an open-source lineage and is the closest existing thing to what we are building. Its self-learning "rules system" is a more mature take on our pattern library, and its governance/audit-trail framing validates our decision to make the finding model a versioned, serializable source of truth.

---

## Tier 2 — Managed multi-agent reviewer (best design reference)

### Claude Code — Code Review
Architecturally different (a fleet of frontier-model agents on managed infrastructure) but the single most instructive design precedent for this project. Several of its choices mirror ours and are worth citing as prior art:

- **Non-blocking by design.** Its check run always completes with a neutral conclusion. This is exactly our FR-8.3.
- **A verification step.** It checks candidate findings against actual code behavior before posting them. Our execution-backed findings (FR-4) are our version of this — but we verify **deterministically**, by running the real test suite, where they verify **agentically**. That determinism is a genuine, nameable differentiator.
- **A machine-readable output contract.** A parseable comment in the check-run details yields per-severity counts. Our JSON artifact (FR-8.2) is a more principled, schema-versioned version of the same idea.
- **The cost reality.** Each review averages **$15–25** in token cost, scaling with PR size and how many findings need verification.

That cost figure is the most important number in this analysis. It quantifies what our free-tier budget is up against and is the empirical justification for triage-by-blast-radius (don't spend $25 reviewing a docs typo) and context capping. Our bet is that deterministic execution + a cheap model + aggressive triage captures most of the value at a small fraction of the cost. That is defensible — but the gap between "frontier model with verification" and "free NIM-tier model" is also the honest risk to our review **quality**, and we hold that tension consciously rather than assume the architecture erases it.

---

## Tier 3 — Different categories

### Danger / DangerJS
Not a competitor — a complement and a positioning foil. Danger is deterministic and rule-based; it checks that you followed the process (CHANGELOG present, ticket linked, labels set), not whether the code is correct. The cleanest one-line framing of this project to a skeptical audience:

> **Danger checks that you followed the process; Agentic Code Review checks whether the code is actually correct.**

Two practical implications: we should aim to **compose with** DangerJS rather than replace it (many TS/JS repos already run it), and its Dangerfile is a proven ergonomic model for user-authored, in-repo rules — worth borrowing for our pattern library and config UX.

### Graphite (stacked diffs)
A workflow alternative that attacks the **same root problem we state** — the AI-driven surge in PR volume and size — from the **input side** (make PRs smaller) rather than the **review side** (review them better). Complementary, not competing. The strategic signal worth internalizing: Graphite's acquisition by Cursor is the industry betting that **code writing and code review converge into one vendor's loop**. Our fresh-context, decoupled review agent (Objective 3) is a deliberate bet **against** that direction, to avoid the self-confirmation bias of a model reviewing its own output.

---

## Where this project stands

### What the landscape confirms we got right
- **Non-blocking output** — Claude Code does the same, for the same reason.
- **Blast-radius triage** — CodeRabbit monetizes exactly this; it is a real axis of value.
- **A canonical, versioned finding model** — Qodo's governance framing and Claude Code's machine-readable output both point the same way; ours is more rigorous than either.
- **Cost as an architectural driver** — Claude Code's $15–25/review and Greptile's credit metering prove the constraint is real, not theoretical.

### Genuine differentiators (lead with these, not features)
1. **Open-source, self-hostable GitHub Action with no per-seat cost.** The Tier 1 tools have OSS-free *programs*, but the engine is a hosted black box. Ours is inspectable and forkable end to end.
2. **Deterministic, execution-backed verification.** Competitors verify agentically (expensive, non-reproducible). We verify by running the actual test suite (cheap, auditable, reproducible). This is our strongest technical story.
3. **Fresh-context decoupling as a stated anti-bias principle** — a deliberate stance against the writer/reviewer convergence the Cursor–Graphite deal represents.

### Honest limitations (kept here on purpose)
- **Feature breadth.** Our v1 is roughly CodeRabbit's entry tier against a product with a massive install base. We will not win on breadth, and shouldn't try.
- **Quality gap.** A free NIM-tier model without agentic verification is very likely noisier than a frontier-model-with-verification reviewer. The NFR pass should set an explicit **accuracy / false-positive** target, not only latency and cost targets. The pattern-library regression set (FR-6.2b) is currently the main guard against shipping a noisy reviewer — and noise is what kills adoption of tools in this category.
- **The test-suite assumption.** "Execution-backed" only adds value on repositories with a runnable test suite. On the median public TS/JS repo that may not hold, which erodes differentiator #2 for part of the target audience. Worth measuring the size of that gap before making execution the headline feature.

---

## Positioning summary

| | Agentic Code Review (this project) | Tier 1 hosted reviewers | Claude Code Review | Danger/DangerJS | Graphite |
|---|---|---|---|---|---|
| Category | Open-source AI reviewer | Hosted AI reviewer | Managed multi-agent reviewer | CI process linter | Stacked-diffs workflow |
| Cost model | Free / single low-cost provider | Per-seat subscription | Per-review token usage | Free (MIT) | Per-seat subscription |
| Verification | Deterministic (real test run) | Agentic / model-based | Agentic behavior check | None (rule-based) | Agentic (add-on) |
| Openness | Fully open, forkable | Closed engine | Closed | Fully open | Closed |
| Bias stance | Decoupled fresh-context agent | Varies | Fresh agents | N/A | Converging with writer (Cursor) |
| Scope | TS/JS, GitHub Action + local CLI | Multi-language, hosted | Multi-language, managed | Any lang, CI glue | GitHub-native workflow |

*See [`tool-reference.md`](./tool-reference.md) for detailed, non-comparative descriptions and sourced pricing.*
