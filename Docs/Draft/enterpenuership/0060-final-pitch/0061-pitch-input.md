# Pitch Input Sheet — Agentic Code Review

**Status: non-normative.** A business-side working document, not a specification. It defines nothing to build.

**Source discipline.** Every value below is copied from a file in this repository or was decided by the founder on 2026-10-03, and says which. Nothing was researched or estimated. A field with no source is written `[MISSING: what is needed]`. Where two files disagree, both are quoted under `[CONFLICT]` and neither is chosen.

This sheet is the INPUT section of the deck prompt in the *Pitch Implementation Guidelines* (2026-10-03), in that prompt's field order. [`0062-one-liner-and-elevator-pitch.md`](./0062-one-liner-and-elevator-pitch.md) and [`0063-pitch-deck.md`](./0063-pitch-deck.md) were written from it and from nothing else.

---

## Step 0: audience, ask and format

| Decision | Answer | Where it comes from | Passes the guide's test? |
|---|---|---|---|
| Audience | Juries and funders: the DEPI final-pitch jury | Founder, 2026-10-03 | Yes: one audience |
| Ask | TypeScript teams run the tool on their real changes in a pilot | Founder, 2026-10-03 | **Not yet.** It names an action, but not how many teams, for how long, or from when |
| Business | Open core: a free open-source command-line tool, plus a paid hosted review service priced at variable cost + markup | Founder, 2026-10-03 | Recorded in the canvas §5 and the competitive landscape. The paid service itself is not designed (see Business model) |
| Format | Presented live | Assumed, not confirmed | Confirm |
| Time slot | 10 minutes | Assumed: the guide's default when no slot is given | Confirm |
| Language | English | Founder, 2026-10-03 | Yes |

---

## INPUT

### [Pitch setup]

- **Venture name:** Agentic Code Review. Source: [`pr-agent-pricing-template.md`](../0050-financial-planning/pr-agent-pricing-template.md) ("Product: Agentic Code Review"). The canvas title says "Agentic Code Reviewer", and the installed command is `agentic-review`.
- **One-liner:** We help TypeScript teams catch AI-written code that passes its tests but doesn't fit their codebase, by reviewing every change against the project's own rules and test results. Source: written in [`0062-one-liner-and-elevator-pitch.md`](./0062-one-liner-and-elevator-pitch.md).
- **Audience:** juries and funders.
- **Format:** presented live (assumed).
- **Time slot in minutes:** 10 (assumed).
- **Language:** English.

### [Problem]

- **Who has the problem:** "peer reviewers of AI-assisted TS/JS pull requests in companies and funded engineering teams" (primary) and "OSS TS/JS maintainers and contributors" (secondary). Source: [`003-business-model-canvas.md`](../003-business-model-canvas.md) §1.
  - `[CONFLICT]` Same section of the canvas: "Today's actual user: the change author reviewing their own work, plus the contributors building the system." [`agentic-code-review-srs-v1.md`](../../../agentic-code-review-srs-v1.md) §1.1 says v1 "is an **engineering milestone, not the product**: the product claim — reducing a reviewer's queue on pull requests — is made in v3, when the same core reaches GitHub."
- **The problem in the customer's own words:**
  - `[MISSING: a quote from a reviewer the team interviewed itself]`. [`problem-statrment-entrepreneurship`](../../problem-statrment-entrepreneurship) §1 says the insights "come from a background study (secondary sources and a small first-hand anecdote, N=3), not from our own interviews."
  - Second-hand quotes that exist, all from [`chat_result_ai_pr_review_background_study.md`](../chat_result_ai_pr_review_background_study.md) A3 and A5 unless noted:
    - "looks like senior work wrapped around a missing authorization check": Nguyen, relayed by AIBuilderClub; a single case ([`001-chat_result_needs_vs_pains_analysis.md`](../001-chat_result_needs_vs_pains_analysis.md), Segment 5).
    - "gave up and just started hitting approve": a Reddit account relayed by AIBuilderClub, N≈1.
    - "the repetition, not the difficulty": Ullah, from the reviewer's seat.
    - "two AIs are not two independent reviewers": Ullah.
  - The team's own summary, not a customer's words: "Green no longer means right." ([`problem-statrment-entrepreneurship`](../../problem-statrment-entrepreneurship) §1).
- **Evidence (number, story or quote) + source:**
  - **Story.** "Correct-looking but context-wrong (legacy v1 auth; tests passed because both backends resolved)." Source: Ullah 2026, one team, first-hand; background study A4. The same account gives two more cases: "Silent convention drift (`"completed"` string vs `Status.Completed` enum)" and "Architecture erosion (controller → repo, skipping app layer; self-written tests pass against wrong shape)."
  - **Numbers.** All from the background study A2.

    | Figure | Value | Source and sample | Caveat stated in the study |
    |---|---|---|---|
    | Manual vs AI-assisted 30-day merge rate | 84.5% vs 32.7% | LinearB 2026: 8.1M PRs, ~4,800 teams, own platform data | Second-hand via AIBuilderClub 2026; cohort comparison, not a trend |
    | Reviewer pickup time | ~200 → ~1,050 min | Same | Same |
    | Diff size at P75 | 157 → 400+ LOC | Same | Same |
    | Feature-branch throughput YoY | +59% (largest ever) | CircleCI 2026: 28M+ runs, 22,000+ orgs | Measures CI runs, not AI authorship |
    | Median main-branch throughput | −7% | Same | Same |
    | Build success rate | 70.8%, 5-yr low | Same | Same |

  - **Evidence tier.** "'Clean-looking' code hides subtle omissions" is "Corroborated by 3 sources" and "entirely anecdotal" (A3). The study's own verdict: "No source is an independent, controlled measurement of the problem", and "No figure demonstrates AI *caused* the effect."

### [Solution]

- **What the product or service does:**
  - **As specified for v1** ([`agentic-code-review-srs-v1.md`](../../../agentic-code-review-srs-v1.md) §1.2): "A local CLI reviewing a working tree, staged changes, or a branch range in a TS/JS repository"; "Execution of the project's tests and type-check, with a recorded evidence trail"; "A review agent isolated from any code-writing agent, grounded in that evidence and in a pattern library"; "A pattern library and a runnable regression harness reporting a catch rate". Each finding carries an evidence reference or is "explicitly marked **unverified**, with a reason" (FR-5.2c). v1 ships "at least five pattern rules" (FR-6.3a).
  - **As built today.** On branch `001-us2-no-finding-clean-review` (tip `b11d548`, 2026-09-28, not merged to `main`), `agentic-review review` reviews uncommitted changes in one model pass. The contract for that build, [`contracts/cli.md`](../../../../specs/001-walking-skeleton/contracts/cli.md), requires the output to say "No checks were run in this build." and "No related context was gathered in this build.", and states "`regression` arrives in 003." So today's build runs no tests and has no catch rate. This is taken from the commit history and the contract; the build was not re-run for this sheet.
- **How the customer uses it, step by step** (SRS §2.3 and [`contracts/cli.md`](../../../../specs/001-walking-skeleton/contracts/cli.md)):
  1. Install the tool. Distribution is specified as "A PyPI package with a console entry point, installed with `uv tool install` or `pipx`". `[MISSING: whether and when a release is published]`
  2. Supply a model-provider key in `AGENTIC_REVIEW_API_KEY`. The default provider is the NVIDIA NIM free tier.
  3. Run `agentic-review review` inside the repository. The scope is the working tree by default, or `staged`, or a `range` with `--base`.
  4. Read the findings in the terminal, or as JSON with `--json`. The exit code is 1 when at least one finding is blocking.

### [Market]

**Price proxy (decided 2026-10-08).** Until a pilot measures review volume per team and the hosted service's markup is set, yearly spend per customer is **rivals' entry price, not ours**. Every figure below that uses it is marked "proxy". Once those two numbers exist, yearly spend becomes price per review × reviews per team per month × 12, the customer unit changes from developers to teams, and TAM, SAM and SOM are recomputed in that unit.

- **All possible customers (count) + source:** 36.5M professional developers worldwide, early 2025. Source: SlashData, cited in [`004-market-study.md`](../004-market-study.md), confidence A. The study does not use GitHub's "180M+ developers", which counts accounts.
- **Customers you can actually reach (count) + source:** 7.0M–11.2M professional developers (SAM, the market study's calculation, confidence C): 36.5M × 68.8% who use TypeScript or JavaScript (JavaScript's share is the floor; Stack Overflow 2025, A) × 55% in pull-request teams (proxy: regular CI/CD use; JetBrains 2025, B, read from a search excerpt) × 50.6%–80.8% who use AI tools daily or at all (Stack Overflow 2025, A). At the proxy price this is $2.0B–$4.0B a year. GitHub reach is not applied, because the command-line tool works on any git repository.
- **Yearly spend per customer, or price × how often they buy:** $24–30 per developer per month (proxy). Source: the entry tiers of CodeRabbit Essentials ($24, billed annually) and Greptile Pro ($30), from the market study, confidence A. Calculated: $24 × 12 = $288 and $30 × 12 = $360 per developer per year.
- **TAM (Calculated, proxy):** 36.5M × $288–360 = $10.5B–$13.1B per year, the market study's ceiling. It is an upper bound: it assumes every professional developer pays rivals' entry price for standalone review.
- **Reality check:** the category leader, CodeRabbit, reaches about 0.4% of professional developers (the market study's own calculation, confidence C: $40M ARR ÷ $288 per seat per year ≈ 139K seats).
- **Target share of reachable customers in the first years (%) + reason:**
  - Revenue SOM: `[MISSING: hosted-service conversion from the pilot]`.
  - Adoption target for the v3 GitHub Action: about 100–500 public repositories in three years, roughly a quarter of them active, matching the open-source review Actions in Sun et al. (the market study). It does not measure v1, whose command-line users leave no public trace; v1 adoption is the pilot teams.
  - Cap: the leader's ~139K paid seats are 1.5%–4.9% of the GitHub-reachable SAM, reached with $231M raised.
- The guide's sanity check, "SOM is reachable from current traction", cannot be run: traction is also `[MISSING]`.

### [Business model]

- **Price per unit:**
  - Command-line tool: free. Source: founder, 2026-10-03.
  - Hosted review service: "Customer Price = C + Markup". Source: [`pr-variable-pricing-model.md`](../0050-financial-planning/0051-cost-structure/pr-variable-pricing-model.md) §13. `[MISSING: the markup, and the unit it applies to (per review or per month)]`
- **Cost per unit:** `[MISSING: cost per review. Needs input, output and cached tokens per review, measured, plus the infrastructure choices still marked TBD]`
  - Known unit prices, from the same file §12. It labels them "USD list prices before taxes, discounts" and says to "verify with AWS Pricing Calculator before committing cash".

    | Resource | Billing unit | Unit price |
    |---|---|---|
    | Qwen3.8 27B input, on OpenRouter | 1M tokens | $0.0248 |
    | Qwen3.8 27B output | 1M tokens | $4.35 |
    | Qwen3.8 27B cache read | 1M tokens | $0.0198 |
    | OpenRouter Standard platform fee | inference/platform spend | 5.5% |
    | Network Load Balancer, eu-central-1 | NLB-hour | $0.027 ($19.71/month for one, before capacity units) |
    | NAT Gateway | gateway-hour | $0.052 ($37.96/month for one, before data processing) |
    | NAT Gateway data | GB processed | $0.052 |
    | Public IPv4 | IP-hour | $0.005 ($3.65/month each) |
    | EC2 | instance-hour | TBD |

  - `[CONFLICT]` **Which model the cost is based on.** The cost sheet prices Qwen3.8 27B at "$4.35 / 1M output tokens". [`model-comparison.md`](../0050-financial-planning/0051-cost-structure/model-comparison.md) says to "Deploy `Qwen3.8 27B` exclusively for workloads requiring vision-language processing or document context exceeding 131K tokens", and lists gpt-oss-20b at "$0.018 / $0.09" and gpt-oss-120b at "$0.03 / $0.17". The built code defaults to the NVIDIA NIM free tier with a placeholder model.
  - `[CONFLICT]` **Fixed or variable infrastructure.** The pricing template defines "F = Fixed monthly infrastructure" and "Break-even Customers = F / [P - (C × R)]". The cost sheet treats every resource as usage ("we should not write 'Elastic IP = $3.65/month' as a fixed cost") and passes the whole cost through.
- **Margin per unit + type (gross or contribution):** `[MISSING]`
- **Revenue streams:** the hosted review service. Source: [`003-business-model-canvas.md`](../003-business-model-canvas.md) §5, "Open core, decided 2026-10-03".
  - `[MISSING: what the hosted service gives a customer that the free tool does not]`. The canvas §2 says this "is not stated", and [`competitive-landscape.md`](../competitive-landscape.md) notes that rivals already offer free hosted tiers.
  - `[CONFLICT]` **The paid product is not designed, and the engineering record rules it out.** The requirement catalogue [`agentic-code-review-srs.md`](../../agentic-code-review-srs.md) §2.2 calls a hosted GitHub App "out of scope entirely". ADR-0005: "The product is deliberately **not** a hosted service." SRS §2.1: "It operates no server, holds no remote state". [`feature-inventory.md`](../feature-inventory.md) §2 rates a hosted app "Very High" complexity. The catalogue carries a note of the decision; no requirement, version or ADR exists for the service.

### [Traction]

- **Sales, users, pilots or signed letters of intent, each with a date:** `[MISSING]`. The canvas records none: "no evidence anyone would pay", and today's user is "the change author reviewing their own work, plus the contributors building the system."
- **Build progress. This is not traction; label it as progress wherever it is shown.** Source: git history of this repository.
  - 2026-09-17: commit "feat(review): review uncommitted changes in one model pass", on the branch named above.
  - 2026-09-26: "build: scaffold the agentic-review package, lockfile and CI" merged to `main` (pull request #11).
  - 2026-09-28: feature 001 has 78 tasks ticked and 31 open in `specs/001-walking-skeleton/tasks.md` on that branch. Calculated: 78 + 31 = 109 tasks.
  - The v1 specification lists 16 acceptance criteria, AC-1 to AC-16 (SRS §6).
  - Not built yet: test execution and the regression harness, so there is no measured catch rate.

### [Competition]

- **Alternatives customers use today, and why customers would choose you over each.** Prices are a September 2026 snapshot from [`tool-reference.md`](../../tool-reference.md); the reasons are quoted from [`competitive-landscape.md`](../competitive-landscape.md).

  | Alternative | What it is | Entry price | Why choose us, as the landscape states it |
  |---|---|---|---|
  | CodeRabbit | Hosted AI reviewer; "The market-share leader" | $24/developer/month (Essentials, billed annually) | "Our edge is openness, zero cost, and auditability — not breadth." |
  | Greptile | Hosted AI reviewer; "The closest match to our architectural thesis" | Free for one active developer; $30 per seat per month (Pro) | Its "engine is a hosted black box. Ours is inspectable and forkable end to end." |
  | Qodo | Review and governance platform with an open-source lineage (PR-Agent) | "Uses a credit-based system; specific tiers are on the pricing page (not enumerated here)" | `[MISSING: a reason specific to Qodo; the landscape gives none]` |
  | Claude Code Review | Managed multi-agent reviewer | "Each review averages **$15–25**" | "we verify **deterministically**, by running the real test suite, where they verify **agentically**" |
  | Danger / DangerJS | CI process linter, rule-based, no model | Free (MIT) | A complement: "Danger checks that you followed the process; Agentic Code Review checks whether the code is actually correct." |
  | Graphite | Stacked-diffs workflow with an AI reviewer | $20/user/month (Starter) | A complement: it attacks the problem "from the **input side** (make PRs smaller)" |
  | Manual peer review, no tool | The status quo | none | Implied by the problem definition; the landscape does not analyse it |

  - `[CONFLICT]` **Qodo's price.** [`pr-agent-pricing-template.md`](../0050-financial-planning/pr-agent-pricing-template.md) gives an entry price of "$30" per "/team/mo" and an overage of "$0.012 / credit pooled across the team", with no source; the tool reference gives no figure.
  - "zero cost" in the CodeRabbit row describes the open-source tool only; the landscape's business-model caveat of 2026-10-03 says so.
- **Limits the landscape states about us** (keep them ready for questions):
  - "Our v1 is roughly CodeRabbit's entry tier against a product with a massive install base."
  - "A free NIM-tier model without agentic verification is very likely noisier than a frontier-model-with-verification reviewer."
  - "'Execution-backed' only adds value on repositories with a runnable test suite."
  - Until v3 "the project competes only where every tool in this document also offers a local mode".
  - On the paid tier: "What it adds is not stated yet."

### [Team]

- **Name — role — one line on why they matter for this venture (2–4 people):** `[MISSING]`. No reference names a team member. The git history has one author, Mohammed Kenawy.

### [Financials]

- **Revenue and costs for years 1, 2 and 3:** `[MISSING]`
- **Break-even point:** `[MISSING]`. The formula exists with every variable blank: "Break-even Customers = F / [P - (C × R)]", where C is cost per review, R reviews per customer per month, F fixed monthly infrastructure and P customer price per month ([`pr-agent-pricing-template.md`](../0050-financial-planning/pr-agent-pricing-template.md)).
- **Key assumptions behind the forecast:** `[MISSING]`. The only money figure is a spending limit, not a forecast: "Model-provider access on a free tier, or a single plan of about $20/month" (canvas §6).

### [Ask and use of funds]

- **The ask (exact amount or exact action):** `[MISSING: number]` TypeScript teams run the tool on their real changes for `[MISSING: length]`, starting `[MISSING: date]`.
- **Split by category (% or amount):** not applicable. No funds are requested.
- **Milestone the ask reaches + target date:** `[MISSING: a measurable result and its date]`
- **What a pilot can measure.** These are the blanks in [`pr-agent-pricing-template.md`](../0050-financial-planning/pr-agent-pricing-template.md) §1 and §3: cost per review; PRs per month; average review time; number of reviewers; AI-generated PR percentage; rework frequency; time spent on rework; current code-review tooling; current monthly spending; perceived pain; willingness to pay; price sensitivity.
- **Readiness.** `[MISSING: how and when a pilot team can install the build]`. The working build is on an unmerged branch, and the repository has no LICENSE file although FR-9.1 requires the system to "ship with README, LICENSE, and CLI usage documentation".

### [Close]

- **Contact details to show on screen:** `[MISSING]`. The repository's remote is `https://github.com/MoKenawy/Pull-request-Reviewer`.

### [ASSETS]

| File | What it shows | Usable as is? |
|---|---|---|
| [`agentic-code-review-srs-v1.md`](../../../agentic-code-review-srs-v1.md) §2.1 | Pipeline flowchart, eight steps (mermaid) | Yes, once rendered to an image |
| [`agentic-code-review-srs-v1.md`](../../../agentic-code-review-srs-v1.md) §1.1 | The two commands, `review` and `regression` (mermaid) | Yes, once rendered |
| [`competitive-landscape.md`](../competitive-landscape.md) | Positioning summary table, six rows by five tools | Too dense for a slide; cut it to two rows |
| [`003-business-model-canvas.md`](../003-business-model-canvas.md) | Canvas at a glance (mermaid) | Background only |
| [`pr-review-agent-Component-design.drawio`](../../../pr-review-agent-Component-design.drawio) | Component design diagram | Needs exporting to an image |
| [`render_agent_graphs.ipynb`](../../../../notebooks/render_agent_graphs.ipynb) | Renders the agent graphs | Technical; background only |
| `[MISSING: logo file]` | | |
| `[MISSING: screenshot of a real agentic-review review run]` | The product shown, which the guide asks for on the solution slide | |
| `[MISSING: team photos]` | Optional | |

---

## Kept out on purpose

| What | Why |
|---|---|
| Every figure in [`dummy-pricing-example.md`](../0050-financial-planning/dummy-pricing-example.md) ($0.29 per review, $149.00 per team, $3,007.50 of value, 5 break-even customers, its competitor prices) | Its first line says it is "populated with realistic, coherent hypothetical numbers" |
| AIDev: "61.38%" of agent PRs with no recorded review | The study marks it "**arXiv ID unverified / future-dated**" |
| A latency threshold of "roughly 10–30 seconds" | SRS §2.4 withdrew it: "an estimate that nobody measured" |
| Graphite's "less than 3% of AI comments rated unhelpful" | A vendor claim with "no methodology/N" |
| Ullah's "−35% burden month one" and "90–95%" caught before opening | "unbaselined N=1" |
| The two charts in `0051-cost-structure/` (`1690307118-4.webp`, `1690307126-5.webp`) | Graphite's own charts of 2022 pull-request sizes; third-party, and not about AI-written code |
| `Pull-request-decisions-explained-zhang et al.pdf` | Not read: the file is password-protected |
