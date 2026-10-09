# Final Pitch — Progress Report

**Date:** 2026-10-09 · **Status: non-normative.** A working status note, written to be copied into the "Final Pitch" page in Notion.

## Where things stand

- **The pitch pack exists:** a one-liner, a 60-second script, an 11-slide deck specification, and a designed deck (draft). Every fact in it is traced to a source, and every gap is marked instead of filled in.
- **The deck is not ready to present.** Three of the guide's twelve pre-delivery checks pass. Still missing: the ask's numbers, the team, contact details and a logo, the financials, and any traction.
- **Of the 16 rework tasks, two are done, one is closed on purpose, and one is half done.** The rest are not started or wait on input.
- **The MVP now reviews a real pull request.** The build gained a pull-request scope on 2026-10-09 (ADR-0011), and a run on an open Playwright pull request is on the deck.

Designed deck: https://claude.ai/artifact/QgbA42frcVNN3T1m3hrC2s (private until shared from the page).

## Done so far

| Date | What | Result |
|---|---|---|
| 2026-10-03 | Pitch pack built from the DEPI guide | `0061-pitch-input.md`, `0062-one-liner-and-elevator-pitch.md`, `0063-pitch-deck.md`, all in `Docs/Draft/enterpenuership/0060-final-pitch/` |
| 2026-10-03 | Business model decided: open core | Free open-source command-line tool, paid hosted review service. Recorded in the canvas, the competitive landscape, the feature inventory, the requirement catalogue and the pricing template |
| 2026-10-08 | Market study checked, corrected and filed | `004-market-study.md`. TAM $10.5B–$13.1B a year as a ceiling; SAM 7.0M–11.2M developers, $2.0B–$4.0B a year |
| 2026-10-08 | Price proxy decided | Rivals' entry price, $24–30 per developer per month, stands in for ours until the pilot |
| 2026-10-09 | Designed deck, first draft | 11 slides, with speaker notes |
| 2026-10-09 | Rework list agreed | 16 tasks, ordered by what unblocks what |
| 2026-10-09 | Task 7: the ask | Merged into the closing slide, at the end of the deck |
| 2026-10-09 | Task 5, first half: review volume | `review-volume-report.md` in `0050-financial-planning/0051-cost-structure/` |
| 2026-10-09 | Task 3: the model | Closed on purpose: the model and its price stay variables while the product is experimental |
| 2026-10-09 | Task 8: MVP slide | A real open pull request and the tool's output, on one slide |

## Numbers found so far

- **Usage:** a core developer opens about 11 to 13 pull requests a month, measured across ten public TypeScript repositories in September 2026. For a team of five that is 55 to 65 reviews a month if each pull request is reviewed once, and up to about three times that if every push is re-reviewed.
- **First real token count:** reviewing microsoft/playwright#43199, a 188-line change, used 12,441 input and 4,888 output tokens with gpt-oss-120b.
- **Cost per review is a formula, tokens × price.** For that pull request, six price scenarios give $0.0007 to $0.036 a review, and at most about $1.28 per developer per month, against rivals' $24 to $30 per seat.
- **Market:** TAM $10.5B–$13.1B a year at the proxy price; SAM $2.0B–$4.0B. Revenue SOM cannot be set until the pilot shows how many teams move to the hosted service.
- **A limit in the build:** its default budget fits about 575 changed lines, so up to a quarter of real pull requests would be refused as it stands.

## The MVP slide

- **Input:** microsoft/playwright#43199, open, +169 −38 lines in 16 files.
- **Output:** 10 files reviewed, 6 listed but not reviewed, 1 finding (a nit, with its lines and evidence), in 125.4 seconds including the clone.
- **The tool's own caveats are on the slide:** no checks ran, no related context was gathered, and no finding call named 9 of the 10 reviewed files.
- **Not yet known:** which model produced that run, its token counts, and whether Playwright's maintainers would agree with the finding.

## Task status

| # | Task | Status |
|---|---|---|
| 1 | One problem definition and one target audience | Not started. Everything in 2, 10, 11, 12 and 13 depends on it |
| 2 | Re-check the differentiator behind the competition slide | Not started |
| 3 | Model the hosted service is costed on | Closed on purpose: left as a variable |
| 4 | Pricing unit for the hosted service | Not started. A decision |
| 5 | Measure average review volume | Half done. Usage is measured; the five-step token ladder waits for a go-ahead |
| 6 | Financials slide and the markup | Not started. Needs 4 and 5 |
| 7 | Merge the ask into the closing slide | Done |
| 8 | MVP-run slide | Done, first version |
| 9 | Team slide and its script | Waiting for names, roles and one line each |
| 10 | Rework the slides touched by 1–6 | Not started |
| 11 | One-sentence pitch | Not started. Needs 1 and 2 |
| 12 | Elevator pitch in three lines | Not started. The hook is open; the software-crisis idea is one candidate |
| 13 | Refresh the business model canvas | Not started. Last |
| 14 | The pilot ask's numbers | Waiting: teams, length, start date, milestone |
| 15 | Contact details | Waiting |
| 16 | Logo | Waiting |

## Waiting on a decision or input

1. **Go-ahead for the token ladder,** and which models to measure first.
2. **Which trigger to assume:** one review per pull request, or one per push.
3. **The pilot ask:** number of teams, length, start date, and a measurable milestone with its date.
4. **Team details, contact details and a logo.**
5. **What the hosted service offers that the free tool does not.** Nothing states it yet, and a jury will ask.

## Known issues

- **The paid product is not designed.** The requirement catalogue calls a hosted app out of scope, and ADR-0005 says the product is deliberately not a hosted service.
- **The entrepreneurship problem statement is missing on the current branch;** it exists only on `main`, so one link in the pitch input sheet is broken.
- **Links broke when the entrepreneurship files moved:** three in `Docs/README.md`, three in the competitive landscape, five in the feature inventory.
- **Copies are stale:** the `.docx` versions of the canvas, landscape and feature inventory, and the Arabic translation of the requirement catalogue.
- **The repository has no LICENSE file,** which a pilot needs.
