# Business Model Canvas — Agentic Code Reviewer

**Status: non-normative.** A business-side working document, not a specification. It defines nothing to build.

**Source discipline.** Every line below comes from what was stated about the idea, the customers, the money and the evidence — nothing else. No partner names, prices, market sizes, or customer counts have been supplied, and none are invented here. A block ending in **GUESS** is one where no information was given; the lines in it are placeholders, not findings.

**Revised 2026-10-03 — open core.** The business model was decided on this date: the command-line tool stays free and open source, and revenue is planned from a paid hosted review service. Blocks 2, 5, 8 and 9, the first of the three risks, the diagram and the evidence table now say so; everything else stands as written. Still no price has been supplied. The only pricing input is a rule, variable cost plus a markup, from the cost sheet in [`pr-variable-pricing-model.md`](./0050-financial-planning/0051-cost-structure/pr-variable-pricing-model.md).

---

## The nine blocks

### 1. Customer Segments
- Primary: peer reviewers of AI-assisted TS/JS pull requests in companies and funded engineering teams.
- Secondary: OSS TS/JS maintainers and contributors. Today's actual user: the change author reviewing their own work, plus the contributors building the system.

### 2. Value Propositions
- Local CLI review of a TS/JS change set, with the repository's own tests and type-check run as evidence attached to every finding.
- Answers "does this clean, test-passing code fit this repo?" — not just "does it pass?".
- The paid hosted review service: what it gives a customer that the free tool does not is not stated.

### 3. Channels
- Not stated. No distribution, discovery, or install route has been decided.
- Only anchor: it is a local command-line tool, so it reaches a user on their own machine. **GUESS**

### 4. Customer Relationships
- Not stated. No support, onboarding, or community model has been decided.
- Only anchor: self-serve, unattended use by a developer at a prompt. **GUESS**

### 5. Revenue Streams
- Open core, decided 2026-10-03: the command-line tool is free and open source, and revenue comes from a hosted review service priced at variable cost plus a markup.
- Still not stated: the markup, the billing unit, the payment method — and there is no evidence anyone would pay.

### 6. Key Resources
- Model-provider access on a free tier, or a single plan of about $20/month.
- The contributors building the system, and the specification and ADRs they work from.

### 7. Key Activities
- Build the pipeline: parse the change set, run the repo's tests and type-check, attach that evidence to findings.
- Measure review quality, and test the pain claims that are still anecdote.

### 8. Key Partnerships
- Not stated. No partner or channel relationship has been named.
- Only anchors: dependence on some model provider's free tier for the tool, and the two suppliers the cost sheet assumes for the hosted service, AWS and OpenRouter. **GUESS**

### 9. Cost Structure
- Building the tool: inference capped at free tiers or ~$20/month; no paid inference infrastructure.
- Running the hosted service: model tokens and cloud infrastructure, billed by usage. The cost sheet lists unit prices; the cost of one review is not yet measured.
- Contributor time — the dominant input, and unpriced.

---

## The three riskiest blocks

### 1. Revenue Streams — a model, but no price and no product
The model is now stated: open core, with a hosted review service sold at variable cost plus a markup. The markup, the billing unit and the payment method are not, and no one has said they would pay.

Two gaps are new. Nothing says what the hosted service gives a customer that the free tool does not, while rival hosted reviewers already offer free tiers ([`tool-reference.md`](../tool-reference.md)). And the hosted service is not designed: the requirement catalogue calls a hosted app "out of scope entirely" ([`agentic-code-review-srs.md`](../agentic-code-review-srs.md) §2.2), so the paid product has no specification, no version and no architecture decision.

The free tool can still be built without answering any of this, which is the same trap as before: the question stays open until it is expensive to answer.

### 2. Customer Segments — the buyer is not the user
The named primary customer is the peer reviewer clearing a queue. The version being built serves the change author before they push. The paying segment and the served segment are different people, and the gap is not a marketing problem — it is a scope problem, already acknowledged in the specification.

### 3. Value Propositions — the pain is thin and partly out of reach
"Clean code hides wrong shape" is three anecdotes, unquantified. The named defect types come from a single first-hand account. Two sources disagree on how many false positives a reviewer will tolerate, so the quality bar for the core promise is unknown. The need for measurable review quality was never voiced by anyone — it was inferred. And the stated root cause is cultural, which means even a reviewer that works perfectly addresses a symptom.

---

## Canvas at a glance

```mermaid
flowchart TB
    subgraph TOP[" "]
        direction LR
        KP["<b>8. Key Partnerships</b><br/>No partner named<br/>Anchors: a model provider's<br/>free tier; AWS and OpenRouter<br/>assumed for hosting<br/><b>GUESS</b>"]
        KA["<b>7. Key Activities</b><br/>Build the pipeline: parse,<br/>run tests + type-check,<br/>attach evidence<br/>Measure review quality;<br/>test the anecdotes"]
        VP["<b>2. Value Propositions</b><br/>Local CLI review of TS/JS<br/>with the repo's own tests<br/>as evidence per finding<br/>Answers 'does this fit<br/>the repo?'<br/>Hosted tier's added<br/>value: not stated"]
        CR["<b>4. Customer Relationships</b><br/>Not stated<br/>Only anchor: self-serve,<br/>unattended<br/><b>GUESS</b>"]
        CS["<b>1. Customer Segments</b><br/>Primary: peer reviewers of<br/>AI-assisted TS/JS PRs<br/>Secondary: OSS maintainers<br/>Today: the change author"]
        KR["<b>6. Key Resources</b><br/>Model access: free tier<br/>or ~$20/month plan<br/>Contributors, plus the<br/>spec and ADRs"]
        CH["<b>3. Channels</b><br/>Not stated<br/>Only anchor: a local CLI<br/>on the developer's machine<br/><b>GUESS</b>"]

        KP --- KA
        KA --- VP
        VP --- CR
        CR --- CS
        KA -.- KR
        CR -.- CH
    end

    subgraph BOTTOM[" "]
        direction LR
        C["<b>9. Cost Structure</b><br/>Tool: free tiers or ~$20/month<br/>Hosted: tokens and cloud by usage,<br/>cost per review unmeasured<br/>Contributor time, unpriced"]
        R["<b>5. Revenue Streams</b><br/>Open core: free CLI,<br/>paid hosted review at<br/>cost plus markup<br/>Markup, unit, payer: unknown"]
        C --- R
    end

    TOP --- BOTTOM

    classDef given fill:#e8f7e8,stroke:#5a8f5a,color:#123312
    classDef guess fill:#fdecea,stroke:#c0645a,color:#3d1410
    classDef risky fill:#fff4d6,stroke:#b8912f,color:#3d2f08
    classDef frame fill:none,stroke:none

    class KA,KR,C given
    class KP,CR,CH guess
    class VP,CS,R risky
    class TOP,BOTTOM frame
```

**Legend.** Green = stated. Red = **GUESS**, nothing was given. Amber = the three riskiest blocks — note that all three are now populated, so this is not a map of what is missing; it is a map of what is unproven.

## Where the evidence stands

| Claim | Evidence given |
|---|---|
| "Clean code hides wrong shape" | 3 people, anecdotal, unquantified |
| Wrong backend / broken convention / architecture erosion | One first-hand account |
| Review quality must be measurable | Inferred, voiced by no one |
| Shared blind spot between generator and reviewer | Only for teams whose AI reviewer shares a model family with their generator |
| Tolerable false-positive rate | Two sources disagree |
| Root cause | Cultural — not fixable by a tool |
| A team would pay for the hosted review service | None |
| The hosted service is worth more than the free tool | Not stated |
