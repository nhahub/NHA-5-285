# Review Volume and Cost per Review — Measurement Report

**Status: non-normative.** A business-side working document, not a specification. It defines nothing to build.

**Date:** 2026-10-09 · **Task:** 5 of the pitch rework list, "measure average review volume".

Pricing the hosted review service needs two numbers: what one review costs, and how many reviews a customer runs in a month. This report records the runs made so far, the data collected, the runs proposed to finish the measurement, and the decisions still open.

**The product is still experimental, so this report does not pick a model or a price.** Both are inputs to the cost. The report measures tokens, lists prices as scenarios, and keeps cost per review as a formula (section 3).

Confidence labels follow [`004-market-study.md`](../../004-market-study.md): **A** is primary data (the GitHub API, OpenRouter's own price list, a run's own report), **C** is our calculation from A inputs.

---

## Summary

- **Usage is measured, as a proxy.** Across ten public TypeScript repositories, a core developer opens about 11 to 13 pull requests a month. For a team of five that is 55 to 65 reviews a month if each pull request is reviewed once, and up to about three times that if every push is re-reviewed (C, from A).
- **Cost per review is a formula, not a number:** tokens × price. The tokens depend on the pull request and the model; the price depends on the model and the provider. Neither model nor price is fixed here.
- **Tokens have been measured twice,** both with gpt-oss-120b: a small demo change (4,634 input, 2,660 output) and one real pull request, microsoft/playwright#43199 (12,441 input, 4,888 output).
- **Prices spread widely, which is why they stay variables.** For the real pull request, the six price scenarios collected so far range from $0.0007 to $0.036 a review, about 54 times apart. Two sources disagree on the price of the same model, and one model's price varies about 20 times between providers (A).
- **Output tokens carry most of the cost:** 66% to 99% of it, in both runs and every scenario. Output is the part that changes most from model to model, so it is the main thing the runs have to measure.
- **The tool's default budget would refuse a share of real pull requests.** It fits about 575 changed lines. Between 4% and 37% of pull requests per repository are larger, 25% across the whole sample (C, an upper bound).
- **Provisional reading, from one real pull request:** in every scenario that review costs under four cents, and a developer's month of reviews comes to between about one cent and about $1.30, against rivals' $24 to $30 per seat. If more runs confirm this, the price will be set by the markup and the fixed costs, not by the model cost.
- **Next:** a proposed ladder of five pull requests, run three times each per model (section 4), and four open decisions (section 5).

---

## 1. The runs made so far

### 1.1 The demo run

The first run is saved in [`run_review_quickstart.ipynb`](../../../../../notebooks/run_review_quickstart.ipynb) and predates this task: it reviewed the demo repository, not a real pull request.

| | |
|---|---|
| When | 2026-09-26, 16:35 UTC |
| What was reviewed | Uncommitted changes in the demo repository `review-demo`: 7 files changed, 4 reviewed (20 changed lines), 3 listed but not reviewed, 1 excluded |
| Model and provider | `openai/gpt-oss-120b` on Groq, temperature 0 |
| Duration | 7.9 seconds, 7.5 of them in the model step |
| Tokens | 4,634 input and 2,660 output, summed over two model calls (one repair turn) |
| Findings | 1 blocking, 0 important, 1 nit, from 2 `emit_finding` calls |
| Checks and context | None. The build states "No checks were run in this build." and "No related context was gathered in this build." |
| Degradation reported | CF-6 `incomplete-file-coverage`: no finding call named `src/search.ts` or `src/users.ts` |
| Verdict | blocking |

**Against the planted defects.** The demo repository plants six defects ([`make_review_demo.py`](../../../../../scripts/make_review_demo.py)). The run caught two.

| Planted defect | File | Caught? |
|---|---|---|
| A computed value never used | `src/format.js` | Yes, as a nit |
| Every error swallowed; the caller gets `undefined` | `src/retry.ts` | Yes, as blocking |
| SQL injection through string concatenation | `src/search.ts` | No |
| A rejected promise escapes the `try` (missing `await`) | `src/users.ts` | No |
| Loop reads one element past the end | `src/users.ts` | No |
| Empty-array guard removed, so the average is NaN | `src/users.ts` | No |

The four misses are all in the two files the degradation names, so the run reported its own gap.

What this run costs under each price scenario is in section 3.

### 1.2 Pull-request runs

On 2026-10-09 the build gained a pull-request scope, and microsoft/playwright#43199 (section 2.1) was reviewed from the notebook three times. The notebook's saved outputs come from different executions, so each row says where its figures come from.

| Run | Model as set | Outcome | Tokens | Time | Where it is recorded |
|---|---|---|---|---|---|
| A | `openai/gpt-oss-120b` on Groq | Completed: 1 finding call, 1 repair turn | 12,441 input, 4,888 output | 63.8 s: 11.9 s reading the pull request, 50.5 s in the model step | The notebook's saved run metadata, started 15:10 UTC |
| B | `qwen/qwen3.8-27b` on Groq | One finding, then the provider refused the next request: HTTP 413, 7,126 input tokens requested against a limit of 7,000 a minute | Not recorded | 14.6 s | The notebook's saved output |
| C | Not recorded in the output | Completed: 1 finding, a nit, and a reported gap: no finding call named 9 of the 10 reviewed files | Not recorded | 125.4 s, including the clone | Output supplied by the founder; shown on the deck's MVP slide |

What these runs add (A):

- **The first real token counts:** 12,441 input and 4,888 output for a 188-line change, with gpt-oss-120b.
- **Input per model call is about 6,200 to 7,100 tokens** for this pull request: run A used 12,441 over two calls, and run B's refused request was 7,126. The tool's own estimate was 7,200, so it is close.
- **A provider's rate limit is a third variable beside model and price.** Groq serves `qwen/qwen3.8-27b`, but its on-demand tier allows 7,000 input tokens a minute for it, less than one request for this pull request.
- **Still unknown:** which model produced run C, and the token counts of runs B and C.

---

## 2. Data collected

### 2.1 The pull request chosen for the first real run

| | |
|---|---|
| Pull request | [microsoft/playwright#43199](https://github.com/microsoft/playwright/pull/43199), "fix(core): make playwright-core bundlable into a single file" |
| State on 2026-10-09 | Open, not a draft, 1 commit, opened 2026-10-07, head `af4a20e`, targets `main` |
| Size | +169 −38 lines in 16 files |
| What the tool will review | 10 TypeScript/JavaScript files, 188 changed lines |
| Listed but not reviewed | 6 files, 19 changed lines: four `DEPS.list` files, one workflow file, one shell script |
| Diff size | 21,472 characters in all; 18,635 in the reviewed files |
| Against the budget | About 7,200 estimated tokens with the instructions, inside the 20,000 default (C) |

"Estimated tokens" is the tool's own estimate, characters divided by three ([`budget.py`](../../../../../src/agentic_review/core/assembly/budget.py)).

How the build will read it: the pull-request scope added on 2026-10-09 ([ADR-0011](../../../../adr/0011-cli-reads-a-public-pull-request.md)) clones the repository without checking it out and compares the pull request's head with the default branch. No checks run and no settings are read from the pull request.

### 2.2 Pull-request volume in ten public TypeScript repositories

Every pull request opened in September 2026 in ten repositories was read from the GitHub API on 2026-10-09: 8,849 pull requests, 7,670 of them opened by human accounts (A). July and August add the opened counts only. Appendix A has the query and the definitions.

A **core developer** is a non-bot account that opened at least four pull requests in the month, about one a week.

| Repository | Opened Jul / Aug / Sep | Bot share (Sep) | Human authors | Core developers | Share of human PRs from core | PRs per core developer, median (mean) | Commits per PR, median (mean) |
|---|---|---|---|---|---|---|---|
| angular/angular | 354 / 370 / 504 | 0% | 65 | 23 | 87% | 11 (19.0) | 1 (1.1) |
| excalidraw/excalidraw | 137 / 162 / 142 | 0% | 95 | 4 | 29% | 4.5 (10.2) | 1 (17.6) |
| microsoft/playwright | 377 / 261 / 316 | 13% | 58 | 10 | 79% | 10 (21.8) | 1 (1.6) |
| microsoft/vscode | 2,093 / 2,418 / 2,593 | 12% | 270 | 59 | 89% | 20 (34.4) | 2 (5.0) |
| n8n-io/n8n | 1,691 / 1,724 / 2,200 | 22% | 167 | 83 | 94% | 14 (19.3) | 3 (8.5) |
| nestjs/nest | 143 / 211 / 270 | 47% | 39 | 8 | 67% | 10.5 (12.0) | 1 (1.7) |
| supabase/supabase | 825 / 911 / 945 | 6% | 203 | 41 | 76% | 11 (16.4) | 2 (4.1) |
| trpc/trpc | 23 / 94 / 51 | 8% | 24 | 1 | 45% | 21 (21.0) | 1 (2.3) |
| twentyhq/twenty | 1,106 / 1,292 / 1,633 | 9% | 104 | 29 | 93% | 16 (47.3) | 3 (8.5) |
| vitest-dev/vitest | 131 / 196 / 195 | 7% | 95 | 5 | 42% | 7 (15.2) | 1 (3.9) |

**Pull requests per developer** (C).

- The median across the ten repositories is **11 a month**, from 4.5 to 21.
- Pooled over all 263 core developers the median is **13 a month**. A quarter open 6 or fewer and a quarter open 31 or more.
- The pooled mean is 25, pulled up by a few people who open 100 to 200 a month. This report uses the median.

**From pull requests to reviews** (C).

Reviews per developer per month = pull requests per developer per month × reviews per pull request.

| Trigger assumed | Reviews per pull request | Per developer per month | Team of five per month |
|---|---|---|---|
| Once, when the pull request is opened | 1 | 11 to 13 | 55 to 65 |
| On every push | 1 to 3, from the median commits per pull request | 11 to 39 | 55 to 195 |

The team of five is an illustration; it is the team size [`dummy-pricing-example.md`](../dummy-pricing-example.md) assumes. That example's 120 reviews a month falls inside this range.

**Bots.** Bot accounts opened 1,179 of the 8,849 pull requests, 13%. Most are dependency and release automation. AI coding agents appear as bot accounts in three repositories: `copilot-swe-agent` opened 86 pull requests in VS Code and 1 in Playwright, and `claude` opened 28 in Supabase.

**Limits of this proxy.**

- These are open-source projects, most of them backed by a company. They stand in for company teams until the pilot measures real ones.
- The per-pull-request details cover September only.
- Commit count is a rough stand-in for pushes. Squash and force-push workflows hide pushes (Angular's mean is 1.1), and one push can carry several commits.
- AI-written pull requests opened from a person's own account cannot be told apart from hand-written ones.

### 2.3 Pull-request size and the tool's budget

"Changed lines" is additions plus deletions, for human-authored pull requests opened in September.

| Repository | Median | P75 | P90 | Share over about 575 changed lines |
|---|---|---|---|---|
| angular/angular | 53 | 187 | 644 | 10% |
| excalidraw/excalidraw | 183 | 817 | 1,798 | 30% |
| microsoft/playwright | 48 | 107 | 318 | 6% |
| microsoft/vscode | 151 | 470 | 1,314 | 22% |
| n8n-io/n8n | 286 | 885 | 1,889 | 35% |
| nestjs/nest | 96 | 201 | 597 | 11% |
| supabase/supabase | 81 | 298 | 838 | 15% |
| trpc/trpc | 124 | 964 | 3,726 | 30% |
| twentyhq/twenty | 291 | 1,092 | 2,814 | 37% |
| vitest-dev/vitest | 42 | 97 | 205 | 4% |

- **Pooled over all 7,670 pull requests:** median 155 changed lines, P75 581, P90 1,625, P95 2,923. The mean is 3,267, dominated by a few enormous pull requests, so it is not used.
- **The Playwright pull request**, at 207 changed lines, sits a little above the pooled median. Within Playwright it is larger than 86% of September's pull requests.
- **The default budget fits about 575 changed lines** (C). The estimate comes from one pull request: its reviewed files carry 99 characters of diff per changed line, which is 33 estimated tokens a line, plus about 1,000 for the instructions, against the 20,000 default in [`settings.py`](../../../../../src/agentic_review/core/config/settings.py).
- **So a share of real pull requests would be refused as the build stands:** 4% to 37% by repository, 18% at the median repository, 25% of the pooled sample. This is an upper bound, because it counts every changed line as TypeScript or JavaScript, and lock files, snapshots and generated files are not reviewed.

That default is a stated placeholder (SRS §8, TBD-3). This figure is a first input for setting it.

### 2.4 Model prices collected

These are scenarios, not a choice. Prices are per 1M tokens.

| Model | Source | Input | Output | Cache read |
|---|---|---|---|---|
| gpt-oss-20b | [`model-comparison.md`](./model-comparison.md), dated 2026-10-01 | $0.018 | $0.09 | not given |
| gpt-oss-120b | [`model-comparison.md`](./model-comparison.md) | $0.03 | $0.17 | not given |
| Qwen3.8 27B | The cost sheet, [`pr-variable-pricing-model.md`](./pr-variable-pricing-model.md) | $0.0248 | $4.35 | $0.0198 |
| Qwen3.8 27B | OpenRouter's default listing, read 2026-10-09 (A) | $0.425 | $2.55 | $0.085 |
| Qwen3.8 27B | OpenRouter, range across its 19 providers (A, Appendix C) | $0.045 to $0.99 | $1.40 to $5.25 | $0.0198 to $0.99 |

Three things in this table are the reason prices are treated as variables:

- **Two sources disagree on the same model.** No OpenRouter provider lists the cost sheet's input or output price for Qwen3.8 27B today; only its cache-read price matches one provider.
- **One model has many prices.** Qwen3.8 27B's input price varies about 20 times between providers. OpenRouter routes each request to one of them, so the price paid changes from request to request unless a provider is pinned.
- **The model itself is open.** The comparison sheet recommends gpt-oss for text-only work, the cost sheet prices Qwen, and the build's default is a placeholder model on NVIDIA NIM's free tier.

The gpt-oss prices and the cost sheet's 5.5% OpenRouter fee were taken as written and not re-checked.

---

## 3. The cost model: model and price as variables

### 3.1 The formula

```text
cost per review                    = (T_in × P_in + T_out × P_out) × (1 + f)
model cost per developer per month = R × cost per review
```

| Variable | Meaning | Depends on | Known so far |
|---|---|---|---|
| `T_in` | Input tokens per review | The size of the pull request, the instructions, and how many model calls the review takes. Roughly the same for every model | Two runs, each over two calls: 4,634 for 20 changed lines, and 12,441 for 188. The tool's own estimate is about 1,000 plus 33 per changed line, per call, and it overestimates on purpose |
| `T_out` | Output tokens per review, including any reasoning tokens | **The model**, and how many findings it reports | Two runs, one model: 2,660 and 4,888 |
| `P_in`, `P_out` | Price per input and output token | The model and the provider. A provider's rate limits decide whether a request is served at all | Six scenarios in section 2.4 |
| `f` | Platform fee | The route to the model | 0 when calling a provider directly; 5.5% for OpenRouter in the cost sheet |
| `R` | Reviews per developer per month | The team and the trigger | 11 to 13 if each pull request is reviewed once; up to 39 on every push (section 2.2) |

The build does not report cached tokens separately, so a cache-read term is left out for now.

### 3.2 The demo run under each price scenario

The token counts are the demo run's: 4,634 input and 2,660 output, from gpt-oss-120b on a 20-line change. Applying another model's price to them is an illustration, because another model would produce a different output count. Costs are before the platform fee. `R` is shown at 12, the middle of the once-per-pull-request range, and at 36, three times that.

| Scenario | `P_in` / `P_out` per 1M | Cost per review | Per developer per month, `R` = 12 | `R` = 36 |
|---|---|---|---|---|
| gpt-oss-20b | $0.018 / $0.09 | $0.0003 | $0.004 | $0.012 |
| gpt-oss-120b, the model that produced these tokens | $0.03 / $0.17 | $0.0006 | $0.007 | $0.021 |
| Qwen3.8 27B, cost sheet | $0.0248 / $4.35 | $0.0117 | $0.14 | $0.42 |
| Qwen3.8 27B, OpenRouter default listing | $0.425 / $2.55 | $0.0088 | $0.11 | $0.32 |
| Qwen3.8 27B, cheapest provider for this run | $0.14 / $1.40 | $0.0044 | $0.05 | $0.16 |
| Qwen3.8 27B, dearest provider | $0.80 / $5.25 | $0.0177 | $0.21 | $0.64 |

What the table shows already (C):

- **The spread is about 55 times** between the cheapest and the dearest scenario, for the same tokens.
- **Output tokens carry 74% to 99% of the cost** in every scenario. `T_out` is also the variable that depends most on the model, so it is what the runs most need to measure.
- **Every scenario is small against a seat price.** Rivals charge $24 to $30 per developer per month; the largest figure here is $0.64. Real pull requests are larger than this demo change, so the measured figures will be higher, but the gap is wide.

### 3.3 The real pull-request run under each price scenario

The same scenarios applied to run A: 12,441 input and 4,888 output tokens, from gpt-oss-120b on microsoft/playwright#43199, a 188-line change. The same caution holds: another model would produce a different output count.

| Scenario | `P_in` / `P_out` per 1M | Cost per review | Per developer per month, `R` = 12 | `R` = 36 |
|---|---|---|---|---|
| gpt-oss-20b | $0.018 / $0.09 | $0.0007 | $0.008 | $0.024 |
| gpt-oss-120b, the model that produced these tokens | $0.03 / $0.17 | $0.0012 | $0.014 | $0.043 |
| Qwen3.8 27B, cost sheet | $0.0248 / $4.35 | $0.0216 | $0.26 | $0.78 |
| Qwen3.8 27B, OpenRouter default listing | $0.425 / $2.55 | $0.0178 | $0.21 | $0.64 |
| Qwen3.8 27B, cheapest provider for this run | $0.14 / $1.40 | $0.0086 | $0.10 | $0.31 |
| Qwen3.8 27B, dearest provider | $0.80 / $5.25 | $0.0356 | $0.43 | $1.28 |

- **The spread is the same:** about 54 times between the cheapest and the dearest scenario.
- **Output tokens carry 66% to 99% of the cost** here, a little less than in the demo run, because a real change has a longer prompt.
- **The gap to a seat price holds on real code:** the largest figure is $1.28 a developer a month, against rivals' $24 to $30.

This is one pull request of roughly median size, run once with one model. The ladder in section 4 is what turns it into an average.

---

## 4. Proposed runs

One pull request cannot give an average, so the proposal is a ladder of five open pull requests of different sizes. Each is almost entirely TypeScript or JavaScript, and all were open on 2026-10-09.

| Step | Pull request | Changed lines | Files | Head | Repository size |
|---|---|---|---|---|---|
| Small | [trpc/trpc#7614](https://github.com/trpc/trpc/pull/7614) | 50 | 2 | `43379bf` | 73 MB |
| Median | [trpc/trpc#7616](https://github.com/trpc/trpc/pull/7616) | 160 | 3 | `4bf746b` | 73 MB |
| Your choice, already run (section 1.2) | [microsoft/playwright#43199](https://github.com/microsoft/playwright/pull/43199) | 207 (188 reviewed) | 16 | `af4a20e` | 245 MB |
| Budget edge | [n8n-io/n8n#39795](https://github.com/n8n-io/n8n/pull/39795) | 574 | 15 | `5fc5db8` | 686 MB |
| Large, about P90 | [excalidraw/excalidraw#12142](https://github.com/excalidraw/excalidraw/pull/12142) | 1,690 | 8 | `88acf0d` | 107 MB |

**How they would be run.**

- **The model and the provider are parameters of each run.** The script in Appendix B takes them on the command line, and each result records which model and provider produced it, so results from different models sit side by side.
- **More than one model is worth running.** The ladder on a second model costs cents and shows how `T_out` moves with the model, which is the largest unknown in the formula.
- **A run only works if the provider serves the model and its limits allow the request.** Run B shows the second half: Groq serves `qwen/qwen3.8-27b`, but its on-demand limit of 7,000 input tokens a minute refused a request for the Playwright pull request.
- **Three runs per pull request per model**, 15 per model, because output tokens vary between runs.
- **Budget raised to 80,000** for these runs, so the two largest are measured, not refused. The large one comes to about 57,000 estimated tokens.
- **Recorded per run:** model, provider, input and output tokens, duration, repair turns, findings by severity, degradations, and the full JSON report.
- **Head commits are noted above** because an open pull request can change before it is run.

**Estimated cost: under $1 per model, even at the dearest prices collected** (C). The 15 runs come to about 280,000 estimated input tokens, $0.28 at the dearest input price. Output is unknown; assuming up to 8,000 tokens a run, it adds $0.63 at the dearest output price. At gpt-oss-120b's prices the same runs cost about 3 cents.

**What the results become.** Input tokens against changed lines give the fixed part and the per-line part of `T_in`. Output tokens per run give `T_out` for each model. With the size distribution in section 2.3, that gives average tokens per review; section 3's formula then turns any model's price into a cost per review and a cost per developer per month.

---

## 5. Open decisions

1. **Go-ahead to run the ladder.** The runs call a paid or rate-limited provider with your key. The Playwright pull request has now been run from the notebook; the other four steps have not.
2. **Which models to measure first.** This is not a choice of model for the product, only of what to measure now. Recommended: start with whatever the keys you have can reach, and add models as keys appear. So far gpt-oss-120b on Groq completes the Playwright pull request, and `qwen/qwen3.8-27b` on Groq's on-demand tier does not.
3. **The five-step ladder, or the Playwright pull request alone.** Recommended: the ladder, since an average needs more than one size.
4. **Which trigger to assume when turning pull requests into reviews:** once per pull request, or on every push. The two differ by up to three times. Recommended: carry both, once per pull request as the base case, until the pricing unit is settled (task 4).

**No longer a decision:** which model the service uses and what it costs. On 2026-10-09 both were left as variables while the product is experimental.

**Carried forward, not decisions for this task:**

- The 20,000-token default budget refuses up to a quarter of real pull requests. That belongs to the engineering side (TBD-3).
- The cost sheet writes Qwen's prices into its equation as fixed numbers. When the financials are built (task 6), they become the parameters `P_in` and `P_out`.

---

## Appendix A — How the volume data was collected

- **Source:** GitHub's GraphQL search API, called through the `gh` command-line tool on 2026-10-09. Read-only.
- **Sample:** ten repositories whose main language on GitHub is TypeScript, active in the period, of different sizes, most with a company-employed core team.
- **Period:** every pull request created from 2026-09-01 to 2026-09-30, with its author, account type, additions, deletions, changed files, commit count and state. For July and August, only the count of pull requests opened, from the REST search API.
- **Query**, one per repository and date range. A range with more than 1,000 results was split in half, because the search API returns 1,000 at most.

```graphql
query($q: String!, $after: String, $n: Int!) {
  search(query: $q, type: ISSUE, first: $n, after: $after) {
    issueCount
    pageInfo { hasNextPage endCursor }
    nodes { ... on PullRequest {
      number createdAt merged isDraft state additions deletions changedFiles
      commits { totalCount }
      author { login __typename }
    } }
  }
}
```

with `$q` set to, for example, `repo:microsoft/playwright is:pr created:2026-09-01..2026-09-30`.

- **Definitions.** A *human* pull request has an author whose account type is not `Bot`; a pull request with a deleted author counts as a bot. A *core developer* opened at least four human pull requests in September. *Changed lines* is additions plus deletions. *Commits per pull request* is the count at the time of reading.
- **The raw data is not in the repository.** It is 8,849 records in a temporary working folder, and the query above reproduces it in about 15 minutes.

---

## Appendix B — The measurement script and settings

Neither file is in the repository yet, and neither has been run. The script calls the same `run_review` the command line calls, then reads the token counts from the report the pipeline already builds. It depends on the `pr` field added to `ReviewRequest` on 2026-10-09.

**Settings.** Model-neutral on purpose: the model and the provider are passed to each run.

```yaml
schemaVersion: 1
agent:
  requestTimeoutSeconds: 180   # a guess: a reasoning model on a real pull request can pass the 60-second default
budget:
  maxTokens: 80000             # for the measurement only, so the largest pull requests are measured, not refused
```

**One run**, from the project root:

```text
uv run --env-file .env python measure_review.py --pr <pull request URL> --config measure.yml --out <folder>
    --model <model id> --base-url <provider address> --key-env <variable holding that provider's key>
```

`--key-env` lets `.env` hold one key per provider. The tool itself reads only `AGENTIC_REVIEW_API_KEY`, so the script copies the named variable into it for that run. It never prints or stores the key.

**Script**

```python
"""Run one review of a public pull request and record what it used: tokens, time, findings.

    uv run --env-file .env python measure_review.py --pr https://github.com/OWNER/REPO/pull/N --config measure.yml \
        --out DIR --model MODEL_ID --base-url PROVIDER_ADDRESS [--key-env NAME_OF_KEY_VARIABLE]

The model and the provider are parameters of a run, not fixed choices: each result records which model produced it,
so results from different models can sit side by side. The provider key is read from the environment, as the tool
itself does; this script never prints or stores it.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from agentic_review.agents.pipeline_agent import ReviewRequest, Reviewed, run_review
from agentic_review.agents.review_port import build_review_port
from agentic_review.core.output.json_out import to_json

sys.stdout.reconfigure(encoding="utf-8")

KEY_VARIABLE = "AGENTIC_REVIEW_API_KEY"  # the only variable the tool reads a credential from

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--pr", required=True, help="the pull request URL")
parser.add_argument("--config", required=True, type=Path, help="settings file (budget, timeouts)")
parser.add_argument("--out", required=True, type=Path, help="directory for the report and the summary line")
parser.add_argument("--model", help="model id for this run; overrides the settings file")
parser.add_argument("--base-url", help="provider address for this run; overrides the settings file")
parser.add_argument("--key-env", default=KEY_VARIABLE, help=f"variable holding this provider's key (default {KEY_VARIABLE})")
parser.add_argument("--label", default="", help="a note stored with the summary, e.g. the size step")
args = parser.parse_args()

env = dict(os.environ)
if args.key_env != KEY_VARIABLE:
    if not env.get(args.key_env):
        print(f"COULD NOT START:\nThe environment variable {args.key_env} is not set.")
        sys.exit(3)
    env[KEY_VARIABLE] = env[args.key_env]


def with_model(agent_settings, credential):
    overrides = {k: v for k, v in {"model": args.model, "base_url": args.base_url}.items() if v}
    return build_review_port(agent_settings.model_copy(update=overrides), credential)


request = ReviewRequest(cwd=Path.cwd(), pr=args.pr, config_path=args.config)
started = time.perf_counter()
result = run_review(request, env=env, port_factory=with_model if (args.model or args.base_url) else None)
elapsed = time.perf_counter() - started

if not isinstance(result, Reviewed):
    print("COULD NOT START:\n" + result.message)
    sys.exit(3)

report = result.report
run = report.run
files = report.change_summary.files
reviewed = [f for f in files if f.reviewed]
summary = {
    "pr": args.pr,
    "label": args.label,
    "model": run.model,
    "provider": run.provider,
    "verdict": report.verdict,
    "completion": run.completion_status,
    "seconds": round(elapsed, 1),
    "tokens_in": run.tokens_in,
    "tokens_out": run.tokens_out,
    "repair_turns": run.repair_turns,
    "tool_calls": run.tool_calls_total,
    "files_listed": len(files),
    "files_reviewed": len(reviewed),
    "lines_added_reviewed": sum(f.added_lines for f in reviewed),
    "lines_removed_reviewed": sum(f.removed_lines for f in reviewed),
    "findings": len(report.findings),
    "findings_by_severity": {s: sum(1 for f in report.findings if f.severity == s) for s in ("blocking", "important", "nit")},
    "degradations": [f"{d.source} {d.code}" for d in report.degradations],
}

args.out.mkdir(parents=True, exist_ok=True)
stem = args.pr.rstrip("/").split("/")[-3] + "-" + args.pr.rstrip("/").split("/")[-1] + "-" + str(run.model).replace("/", "_")
(args.out / f"{stem}.report.json").write_text(to_json(report), encoding="utf-8")
with (args.out / "runs.jsonl").open("a", encoding="utf-8") as log:
    log.write(json.dumps(summary) + "\n")

print(json.dumps(summary, indent=2))
```

---

## Appendix C — Qwen3.8 27B providers on OpenRouter

Read on 2026-10-09 from OpenRouter's public endpoint list for `qwen/qwen3.8-27b` (A). Prices are per 1M tokens. All 19 support tool calls, which the build requires.

| Provider | Input | Output | Cache read |
|---|---|---|---|
| Wafer | $0.0450 | $2.30 | $0.0198 |
| DekaLLM | $0.0490 | $3.00 | $0.0200 |
| Darkbloom | $0.0500 | $2.20 | $0.0250 |
| Ionstream | $0.0893 | $2.35 | $0.0850 |
| Reka | $0.1400 | $1.40 | $0.0350 |
| Phala | $0.1500 | $1.875 | $0.0375 |
| DeepInfra | $0.1500 | $1.875 | $0.0375 |
| Mancer 2 | $0.2000 | $2.50 | not listed |
| AkashML | $0.2250 | $1.98 | $0.0500 |
| Parasail | $0.2400 | $2.20 | $0.0500 |
| Chutes | $0.2400 | $2.20 | $0.0240 |
| CoreWeave | $0.4000 | $3.00 | $0.1500 |
| Novita | $0.4200 | $3.00 | $0.0850 |
| Alibaba | $0.4250 | $2.55 | $0.0850 |
| Near AI | $0.4400 | $3.30 | $0.0440 |
| Cloudflare | $0.4500 | $3.20 | $0.0500 |
| Venice | $0.4500 | $3.20 | not listed |
| ModelRun | $0.8000 | $5.25 | $0.1500 |
| Cerebras | $0.9900 | $1.49 | $0.9900 |

The default listing ($0.425 / $2.55 / $0.085) is Alibaba's. For the saved run's token mix, Reka is the cheapest and ModelRun the dearest.
