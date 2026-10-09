# Pitch Deck — Agentic Code Review

**Status: non-normative.** A business-side working document, not a specification. It defines nothing to build.

Step 3 of the *Pitch Implementation Guidelines* (2026-10-03): the deck prompt run on [`0061-pitch-input.md`](./0061-pitch-input.md) and on nothing else. This is a slide-by-slide specification to design from, not designed slides. Two of the ten slides are skeletons (team, financials), because the references hold nothing for them, and four more lack key numbers (results so far, market, business model, and the ask on the closing slide). The Gaps report lists what each one needs.

## Order

The audience is the DEPI jury. The deck leads with the problem and the results so far, as the guide's row for juries and funders says. The ask comes last: on 2026-10-09 it was merged into the closing slide, which departs from that row's advice to lead with the use of funds. The guide's other rule, to state the ask early, is still met by the title slide's one-line ask. No money is requested, so "use of funds" becomes "what the pilot delivers", shown on the closing slide.

| # | Slide | State |
|---|---|---|
| 1 | Title | Ready, apart from the logo and the ask's numbers |
| 2 | Problem | Ready |
| 3 | Solution | Ready, apart from the screenshot |
| 4 | Results so far | Build progress only; traction missing |
| 5 | Market | TAM and SAM set with a proxy price; revenue SOM missing |
| 6 | Business model | Model set; price, cost and margin missing |
| 7 | Competition | Ready |
| 8 | Team | Skeleton |
| 9 | Financials | Skeleton |
| 10 | The ask and close | Action set; the ask's numbers and dates, the contact details and the logo missing |

---

## Slides

### Slide 1 — Title

- **Headline:** Agentic Code Review: review that shows its evidence
- **Body:**
  - We help TypeScript teams catch AI-written code that passes its tests but doesn't fit their codebase, by reviewing every change against the project's own rules and test results.
  - Ask: `[MISSING: number]` TypeScript teams for a `[MISSING: length]` pilot.
- **Key number:** none
- **Visual:** `[MISSING: logo file]`
- **Speaker notes:** Green no longer means right. We built a reviewer that shows its evidence, and we are here to ask for pilot teams, not money.

### Slide 2 — Problem

- **Headline:** Green no longer means right
- **Body:**
  - An AI-written change used the legacy v1 auth backend.
  - The tests passed: both backends resolved.
  - Nothing in the diff looked wrong.
- **Key number:** 32.7% of AI-assisted pull requests merged within 30 days, against 84.5% of manual ones — Source: LinearB 2026, 8.1M PRs across ~4,800 teams, cited second-hand through AIBuilderClub 2026. A cohort comparison, not a trend.
- **Visual:** bar chart with two bars, the 30-day merge rate: manual 84.5%, AI-assisted 32.7%.
- **Speaker notes:** This comes from one tech lead's first-hand account of their own team. Three sources describe clean-looking AI code hiding a defect, and none measures how often it happens. LinearB's figures show AI-assisted pull requests are merged far less often, but they compare two groups and do not show the cause.

### Slide 3 — Solution

- **Headline:** A reviewer that shows evidence for every finding
- **Body:**
  - Checks each change against the project's own rules.
  - Runs the project's own tests and type-check.
  - Each finding cites evidence, or says "unverified".
- **Key number:** 1 command, 1 model pass per review — Source: `specs/001-walking-skeleton/contracts/cli.md`; SRS v1 §2.1.
- **Visual:** `[MISSING: screenshot of a real agentic-review review run]`. Until it exists: the pipeline flowchart from SRS v1 §2.1.
- **Speaker notes:** A developer runs one command in their repository and reads the findings in the terminal. Today's build reviews uncommitted changes in one model pass; running the tests is the next step and is not in that build. This version serves the author before they push; the reviewer on GitHub is served when the same core reaches GitHub in version 3.

### Slide 4 — Results so far

- **Headline:** Built so far: a single-pass command-line review
- **Body:**
  - 2026-09-17: reviews uncommitted changes in one model pass.
  - Not built yet: test runs, catch-rate benchmark.
  - Users, pilots, letters of intent: `[MISSING: each with a date]`
- **Key number:** `[MISSING: users, pilots or signed letters of intent, each with a date]` — Source: `[SOURCE MISSING]`
- **Visual:** none
- **Speaker notes:** These are build milestones, not traction: the references record no user outside the team, no pilot and no letter of intent. The package scaffold and CI were merged on 2026-09-26, and on 2026-09-28 the first feature had 78 of its 109 tasks ticked. We cannot yet show that the tool catches wrong-shaped code, because the benchmark that measures a catch rate is not built.

### Slide 5 — Market

- **Headline:** Up to $10.5B–$13.1B a year, at rivals' prices
- **Body:**
  - TAM: 36.5M developers × $288–360 a year (proxy price).
  - SAM: 7.0M–11.2M TS/JS, AI-using team developers: $2.0B–$4.0B.
  - SOM: `[MISSING: hosted-service conversion from the pilot]`
- **Key number:** $10.5B–$13.1B a year — Source: Calculated: 36.5M professional developers (SlashData, early 2025) × $24–30 per developer per month × 12, from `004-market-study.md`. The price is rivals' entry price, a proxy for ours.
- **Visual:** three nested bars for TAM, SAM and SOM; the TAM and SAM bars can be drawn today.
- **Speaker notes:** The ceiling assumes every professional developer pays rivals' entry price; narrowed to TypeScript or JavaScript developers in pull-request teams who use AI tools, it is $2.0B–$4.0B. The category leader reaches about 0.4% of professional developers, and no open-source review Action has passed 460 repositories. Until our pilot measures review volume and we set the markup, rivals' entry price stands in for ours.

### Slide 6 — Business model

- **Headline:** Free CLI; hosted reviews at cost plus markup
- **Body:**
  - Command-line tool: open source and free.
  - Hosted review service: price = variable cost + markup.
  - Markup, cost per review, margin: `[MISSING]`
- **Key number:** `[MISSING: margin per review, and whether gross or contribution]` — Source: `[SOURCE MISSING]`
- **Visual:** none
- **Speaker notes:** The command-line tool stays free; revenue comes from a hosted review service priced at its variable cost plus a markup. Our cost sheet has unit prices, for example $0.0248 per 1M input tokens and $4.35 per 1M output tokens for one model, but not yet how many tokens a review uses. The hosted service is not designed yet and has no version assigned. `[MISSING: what the hosted service gives a customer that the free tool does not]`

### Slide 7 — Competition

- **Headline:** Rivals verify with a model; ours runs the tests
- **Body:**
  - CodeRabbit $24/developer/month; Greptile $30 per seat per month; Qodo credit-based.
  - Claude Code Review: $15–25 per review.
  - Ours: open engine, findings backed by test runs.
- **Key number:** $15–25 average cost per review for Claude Code Review — Source: `tool-reference.md`, from the vendor's own pages, September 2026 snapshot. The pricing template says it "should be independently re-verified".
- **Visual:** the "Verification" and "Cost model" rows of the positioning table in `competitive-landscape.md`.
- **Speaker notes:** The real alternatives are hosted reviewers priced per seat or per review, manual review, and free rule-based tools such as DangerJS. Our difference is specified but not yet built: findings backed by the project's own test run, in an engine anyone can inspect. Our stated limits are a feature set of about CodeRabbit's entry tier, a free-tier model that is likely noisier, and no benefit on repositories without a runnable test suite.

### Slide 8 — Team

- **Headline:** `[MISSING: who the team is, in one line]`
- **Body:**
  - `[MISSING: 2–4 people: name, role, one line on why each matters for this venture]`
- **Key number:** none
- **Visual:** `[MISSING: team photos]`, optional
- **Speaker notes:** `[MISSING: for each person, the relevant skill or experience, not the title]` The references name no team member; the git history has one author.

### Slide 9 — Financials

- **Headline:** `[MISSING: three-year forecast and break-even point]`
- **Body:**
  - Revenue and costs, years 1 to 3: `[MISSING]`
  - Break-even customers = F / [P - (C × R)]
  - F, P, C and R: `[MISSING]`
- **Key number:** `[MISSING: break-even point]` — Source: `[SOURCE MISSING]`
- **Visual:** none until the numbers exist.
- **Speaker notes:** Our pricing template defines break-even as fixed monthly infrastructure divided by the contribution per customer, and every variable in it is still blank. The only money figure we have is a spending limit: a free tier, or a single plan of about $20 a month for model access. Two reference costs for a hosted service in Frankfurt are $19.71 a month for one load balancer and $37.96 a month for one NAT gateway, before usage.

### Slide 10 — The ask and close

- **Headline:** We ask for pilot teams, not money
- **Body:**
  - We help TypeScript teams catch AI-written code that passes its tests but doesn't fit their codebase, by reviewing every change against the project's own rules and test results.
  - Ask: `[MISSING: number]` TypeScript teams, a `[MISSING: length]` pilot from `[MISSING: date]`, reaching `[MISSING: measurable result]` by `[MISSING: date]`.
  - Contact: `[MISSING: contact details]`
- **Key number:** `[MISSING: number of pilot teams]` — Source: `[SOURCE MISSING]`
- **Visual:** none. No funds are requested, so there is no use-of-funds chart; the slide lists what the pilot measures instead. `[MISSING: logo file]`
- **Speaker notes:** We ask for pilot teams, not money. A pilot measures what our plan still leaves blank: pull requests per month, review time, current tools and spending, and willingness to pay, and it gives us our own cost per review from real changes. Repeat the ask in one sentence, then leave this slide on screen during questions. `[MISSING: how and when a pilot team can install the build]`

---

## Gaps report

### 1. Missing information, by slide

| Slide | Missing |
|---|---|
| 1 Title | Logo; the number of teams and the pilot length in the ask line |
| 2 Problem | A quote from a reviewer the team interviewed itself. The slide stands without it |
| 3 Solution | A screenshot of a real review run |
| 4 Results so far | Users, pilots or signed letters of intent, each with a date |
| 5 Market | Revenue SOM: hosted-service conversion from the pilot; a path from the pilot to the v3 adoption target; our own yearly spend, to replace the proxy |
| 6 Business model | What the hosted service gives a customer that the free tool does not; the markup and the unit it applies to; cost per review; margin and its type |
| 7 Competition | A reason to choose us over Qodo specifically |
| 8 Team | 2–4 people: name, role, one line each |
| 9 Financials | Revenue and costs for years 1 to 3; break-even point; the assumptions behind them |
| 10 The ask and close | Number of teams; length; start date; a measurable milestone and its date; how and when a team can install the build; contact details; logo |

### 2. Numbers shown without a source

None on the slides: every number carries its source on the "Key number" line or in the table of sources below. Two inputs are assumptions with no source at all: the 10-minute slot and the live format. The market's yearly spend is a stated proxy, rivals' entry price, used until the pilot's review volume and the markup exist.

### 3. Contradictions between inputs

Full quotations and links are in [`0061-pitch-input.md`](./0061-pitch-input.md). Neither side is chosen here.

| # | One input says | Another says | Where it stands |
|---|---|---|---|
| 1 | Canvas §5: "Open core, decided 2026-10-03", with revenue from "a hosted review service" | Requirement catalogue §2.2: a hosted GitHub App is "out of scope entirely". ADR-0005: "The product is deliberately **not** a hosted service." SRS §2.1: "It operates no server" | Open. The business model is recorded in the canvas, the landscape and a catalogue note, but the paid product has no specification, version or ADR. Expect "why pay if the tool is free?": the canvas says the hosted tier's added value "is not stated" |
| 2 | Canvas §1: the customer is "peer reviewers of AI-assisted TS/JS pull requests". Entrepreneurship problem statement §4: "an open-source GitHub Action" | SRS §2.2: "v1's primary user is the **author**, not the reviewer". SRS §1.2: "GitHub integration of any kind (v3)" | Open. Slide 3 says it aloud, as SRS §9 (R-5) requires |
| 3 | Problem definition: reviewers cannot judge "clean-looking, test-passing changes" | Landscape, differentiator 2: "We verify by running the actual test suite". The same file: "the execution-backed claim thins on a machine where the developer can already run their own tests" | Open. Running tests cannot by itself catch code that passes its tests. The pitch names the project's rules as what catches it and the test run as the evidence. Expect this question |
| 4 | Cost sheet: Qwen3.8 27B at "$4.35 / 1M output tokens" | Model comparison: deploy Qwen "exclusively for workloads requiring vision-language processing or document context exceeding 131K tokens"; gpt-oss at "$0.018 / $0.09" and "$0.03 / $0.17". The built tool defaults to the NVIDIA NIM free tier | Open. Cost per review cannot be computed until one model is chosen |
| 5 | Pricing template: "F = Fixed monthly infrastructure", with break-even at "F / [P - (C × R)]" | Cost sheet: every resource is usage, and "we should not write 'Elastic IP = $3.65/month' as a fixed cost" | Open. Decide which costs are passed through and which the markup must cover |
| 6 | Tool reference: Qodo "Uses a credit-based system; specific tiers are on the pricing page (not enumerated here)" | Pricing template: Qodo at "$30" per "/team/mo", no source | Open. The slide uses "credit-based" |

**A conflict inside the guide itself.** Slides 1 and 10 must carry the one-liner and the ask line, and together they exceed the 25-word body limit of rule 9: the one-liner alone is 28 words. The guide's own laundry one-liner is 22 words, so it would break the limit the same way once an ask line is added. Both slides keep the one-liner whole. The 23-word short form in [`0062-one-liner-and-elevator-pitch.md`](./0062-one-liner-and-elevator-pitch.md) brings them closer, not under.

### 4. Every calculation made

| What | Formula and inputs | Result |
|---|---|---|
| Tasks in feature 001 | 78 ticked + 31 open | 109 |
| One load balancer a month (the source's sum, re-checked) | 730 hours × $0.027 | $19.71 |
| One NAT gateway a month (the source's sum, re-checked) | 730 hours × $0.052 | $37.96 |
| Yearly spend per developer (proxy) | $24 × 12; $30 × 12 | $288; $360 |
| TAM (the market study's figure, re-checked) | 36.5M × $288; 36.5M × $360 | $10.512B; $13.14B, shown as $10.5B–$13.1B |
| SAM, developers (re-checked) | 36.5M × 68.8% × 55% × 50.6%; 36.5M × 68.8% × 55% × 80.8% | 6.99M; 11.16M, shown as 7.0M–11.2M |
| SAM, dollars (re-checked) | 6.99M × $288; 11.16M × $360 | $2.01B; $4.02B, shown as $2.0B–$4.0B |

The speaking-time estimates are in [`0062-one-liner-and-elevator-pitch.md`](./0062-one-liner-and-elevator-pitch.md).

### 5. Use-of-funds check

No. No split was given: the ask is an action, not an amount, so there are no shares to add up.

---

## Sources and caveats for every number

Prepared for questions, as the guide advises.

| Number | Slide | Source | If asked |
|---|---|---|---|
| 84.5% and 32.7% | 2 | LinearB 2026 through AIBuilderClub 2026; background study A2 | A vendor's own platform data on 8.1M PRs across ~4,800 teams, read second-hand. It compares two groups of pull requests and does not show that AI caused the gap |
| One team; three sources | 2, notes | Background study A3 and A4 | Anecdote. Nobody has measured how often this happens; the benchmark and the pilot exist to find out |
| 1 command, 1 model pass | 3 | `contracts/cli.md`; SRS v1 §2.1 | In version 1 the model is called once per review |
| 2026-09-17 | 4 | Git history, branch `001-us2-no-finding-clean-review` | The build is on a feature branch that is not merged to `main` |
| 2026-09-26; 78 of 109; 2026-09-28 | 4, notes | Git history; `specs/001-walking-skeleton/tasks.md` on that branch | The task count covers the first feature only |
| 36.5M | 5 | SlashData, early 2025, via `004-market-study.md` (confidence A) | Professional developers worldwide. GitHub's 180M+ counts accounts and is not used |
| $10.5B–$13.1B | 5 | Our calculation in the market study (confidence C) | An upper bound at rivals' entry prices, which stand in for ours until the pilot; not our serviceable market |
| About 0.4% | 5, notes | Market study (confidence C): $40M ARR ÷ $288 per seat per year | Rests on Sacra's revenue estimate for CodeRabbit |
| 7.0M–11.2M; $2.0B–$4.0B | 5 | Market study SAM (confidence C), from Stack Overflow 2025 (A) and JetBrains 2025 (B, proxy) | The pull-request-team share is a proxy (regular CI/CD use) read from a search excerpt; the shares are multiplied as if independent |
| 460 repositories | 5, notes | Sun et al., arXiv 2508.18771, via the market study (A) | Public repositories configuring the most-adopted open-source review Action, January 2025; private use is invisible |
| $0.0248 and $4.35 per 1M tokens | 6, notes | `pr-variable-pricing-model.md` | List prices for one model; our own comparison sheet recommends a cheaper one for text-only work (contradiction 4) |
| $24 and $30 | 7 | `tool-reference.md`, September 2026 snapshot | Entry paid tiers from the vendors' own pages; CodeRabbit's is billed annually |
| $15–25 | 7 | `tool-reference.md` | The vendor's own average token cost per review; our pricing template says to re-verify it |
| About $20 a month | 9, notes | Canvas §6 | A spending limit, not a forecast |
| $19.71 and $37.96 | 9, notes | `pr-variable-pricing-model.md` | 730 hours at the hourly list price for one resource in Frankfurt, before usage; the source says to verify them with the AWS calculator |

---

## Pre-delivery checklist

The guide's twelve boxes. Three can be ticked today.

- [ ] Audience, ask and format are written down, and the deck order matches the audience. **Not yet:** the audience and order are set, but the ask has no number or dates, and the format and slot are assumed. The order now ends with the ask, by decision of 2026-10-09, rather than following the guide's jury row.
- [ ] A stranger can repeat the one-liner after hearing it once. **Not tested.**
- [ ] The elevator pitch runs under 60 seconds out loud and ends with one clear ask. **Not tested:** 121 words is about 48 to 56 seconds by word count, and the ask has two placeholders.
- [x] The deck has 10–12 slides; anything extra is in an appendix. 10 slides.
- [ ] Every slide passes the three-second test and uses 30-point text or larger. **Not tested:** the designed draft has not been checked against it, and slides 1 and 10 are over 25 words.
- [ ] The market size shows its bottom-up calculation and data source. **Partly:** TAM and SAM show their calculations and sources, with a proxy price; revenue SOM is missing.
- [ ] SOM is reachable from current traction, or the gap is explained. **Missing:** revenue SOM and traction do not exist, and the v3 adoption target (100–500 repositories) has no path from today yet.
- [x] The competition slide names real alternatives. Four on the slide, seven in the input sheet.
- [ ] Every figure matches across all slides (price, margin, traction, ask). **Not yet:** the figures that exist agree, but price, margin, traction and the ask's numbers do not exist.
- [ ] Use-of-funds shares add up to 100% and each links to the milestone. **Does not apply as written:** no funds are requested. The milestone is still missing.
- [ ] The ask appears early and is repeated at the close, with contact details on screen. **Not yet:** the ask is on slides 1 and 10; the contact details are missing.
- [x] Every AI-generated number has been checked against a source or removed. Each number was searched for in the file it cites on 2026-10-03. Check the three calculations above yourself.

---

## For the second pass

Fill these in [`0061-pitch-input.md`](./0061-pitch-input.md), then regenerate the script and the deck.

1. **The ask:** number of teams, pilot length, start date, the measurable milestone and its date, and what you want from the jury itself.
2. **Team:** 2–4 people, each with a role and one line on why they matter.
3. **Business model and unit economics:** what the hosted service gives a customer that the free tool does not; one model choice; tokens per review from a measured run; the markup; and which costs the markup must cover.
4. **Market:** hosted-service conversion from the pilot for revenue SOM, a path from the pilot to the v3 adoption target, and, once review volume and the markup exist, our own yearly spend in place of the proxy.
5. **Financials:** revenue and costs for years 1 to 3, and the break-even point.
6. **Close and visuals:** contact details, a logo, and one screenshot of a real review run.
7. **Pilot readiness:** a LICENSE file, and a way for a team to install the build.
