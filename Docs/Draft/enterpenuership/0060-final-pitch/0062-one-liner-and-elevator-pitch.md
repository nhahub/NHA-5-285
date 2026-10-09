# One-liner and Elevator Pitch — Agentic Code Review

**Status: non-normative.** A business-side working document, not a specification. It defines nothing to build.

Steps 1 and 2 of the *Pitch Implementation Guidelines* (2026-10-03). Every fact comes from [`0061-pitch-input.md`](./0061-pitch-input.md), which names the file behind it. Audience: the DEPI final-pitch jury. The ask is pilot teams, not money.

---

## Step 1: the one-liner

> We help TypeScript teams catch AI-written code that passes its tests but doesn't fit their codebase, by reviewing every change against the project's own rules and test results.

| Part of the formula | Our words | Where it comes from |
|---|---|---|
| Who | TypeScript teams | The customer is "peer reviewers of AI-assisted TS/JS pull requests in companies and funded engineering teams" (canvas §1). "Teams" covers both that reviewer and the author whom version 1 actually serves |
| Problem | AI-written code that passes its tests but doesn't fit their codebase | "Green no longer means right": AI-assisted pull requests "arrive clean-looking and test-passing, yet some still break the repo's conventions, pick the wrong backend, or erode the architecture" (entrepreneurship problem statement §1) |
| How | Reviewing every change against the project's own rules and test results | The pattern library, and "Execution of the project's tests and type-check, with a recorded evidence trail" (SRS §1.2) |

**Length.** 28 words. The guide's laundry example is 22, and it asks for about 10 seconds.

**Short form, if the long one does not survive the repeat-back test** (23 words):

> We help TypeScript teams catch AI-written code that passes its tests but doesn't fit their codebase, by checking it against their own rules.

**Done when:** you say it to someone outside the project and they repeat it back without notes. This test has not been run.

**Two things a listener may challenge:**

1. **"If the code passes its tests, how do test results help?"** The project's rules and the surrounding code are what catch a change that does not fit. The test and type-check run is the evidence a finding points to, so the reader does not have to take the finding on trust.
2. **"Does it run my tests today?"** Not yet. Today's build reviews a change in one model pass and runs no checks; test execution is the next step in the delivery sequence (SRS Appendix A).

---

## Step 2: the 60-second elevator pitch

### Three parts

| Part | Formula | Our line |
|---|---|---|
| Hook | A surprising fact or a question about the problem | "Green no longer means right." |
| Story | Who suffers + what you do + proof it works | "A reviewer can no longer tell a clean, test-passing change from one that is wrong for the codebase. We review each change against the project's own rules and test results. `[MISSING: proof — a measured catch rate or a pilot result]`" |
| Ask | Exactly what you want from this listener | "`[MISSING: number]` TypeScript teams to run it on their real changes for `[MISSING: length]`." |

### Timed script

| Part | Seconds | What we say | Words |
|---|---|---|---|
| Hook | 10 | Green no longer means right. AI-written code now arrives clean, with every test passing, and can still be wrong for the codebase it lands in. | 25 |
| Problem | 10 | On one team, an AI-written change used the legacy v1 auth backend. The tests passed because both backends resolved. That is invisible in a diff. | 25 |
| Solution | 15 | Agentic Code Review is a free, open-source command-line reviewer for TypeScript. It checks each change against the project's own rules and test results, and every finding shows its evidence or says it is unverified. | 34 |
| Proof | 10 | Today's build reviews a change from one command. Running the tests and measuring a catch rate are the next two milestones. | 21 |
| Ask | 10 | We are looking for `[MISSING: number]` TypeScript teams to run it on their real changes for `[MISSING: length]`. | 16 |
| **Total** | **55** | Under a minute, every line specific | **121** |

**Timing check (Calculated).** 121 words ÷ 150 words a minute × 60 = 48.4 seconds. At a slower 130 words a minute: 121 ÷ 130 × 60 = 55.8 seconds. Both paces are assumptions, not source figures, and the two placeholders are counted as one word each. Only a stopwatch settles it.

**Where each line comes from**

| Part | Source | What to know before saying it |
|---|---|---|
| Hook | Entrepreneurship problem statement §1, insight 1 | The team's own summary, not a customer quote |
| Problem | Ullah 2026, one team, first-hand; background study A4 | One account. Three sources describe this kind of failure and none measures how often it happens |
| Solution | SRS §1.2 and FR-5.2c; "free, open-source" is the open-core decision of 2026-10-03 (canvas §5) | It describes version 1 as specified. Today's build does not yet run tests, and the repository has no LICENSE file yet |
| Proof | Commit of 2026-09-17 on branch `001-us2-no-finding-clean-review`; SRS Appendix A, steps 2 and 3 | A build milestone, not proof that it works. Replace it with a measured catch rate or a pilot result as soon as one exists |
| Ask | Founder, 2026-10-03 | Not exact until the number of teams and the length are filled in |

**Rehearsal test:** say it out loud with a timer. If you run out of breath or pass 60 seconds, cut words. This test has not been run.

### The guide's three fixes, checked

| Fix | Status |
|---|---|
| Do not start with yourself | Met: the script opens with the problem. Names and titles do not appear |
| No jargon | **Check for this jury.** The script still contains "legacy v1 auth backend", "backends resolved", "diff", "command-line" and "open-source". The first two are the source's own words. For a non-technical listener, "the old version of the login system" is a plain reading of the first; that wording is a paraphrase, not the source's |
| Always end with an ask | Present, but incomplete: it has two placeholders |

### The ask changes per listener

The script above speaks to someone who can bring a team: a team lead, an engineering manager, a partner company. To the jury itself, say what you want the jury to do: `[MISSING: what the jury can do to get you those teams]`.
