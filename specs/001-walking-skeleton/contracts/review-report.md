# Contract: Review Report JSON, schema 1.0 (as produced by 001)

**Parent contract**: [`Docs/design/04-contracts.md`](../../../Docs/design/04-contracts.md) §5. The authoritative
machine-readable form is the output of `agentic-review schema`, generated from `ReviewReport`.
Stability: 📦 versioned. **Consumers must ignore unknown fields.**

Types and invariants are in [data-model.md §6](../data-model.md#6--run-level-types--corefindings).

---

## Example: a completed review with one blocking finding

```jsonc
{
  "schemaVersion": "1.0",
  "run": {
    "startedAt": "2026-09-17T10:04:11Z",
    "durationMs": 3412,
    "stageDurationsMs": {"preflight": 38, "changeSet": 121, "assembly": 4, "review": 3240, "output": 9},
    "requestedDepth": null, "achievedDepth": null,
    "toolCallCeiling": 25, "investigationToolsEnabled": false,
    "toolCallsTotal": 2, "toolCallsEmission": 2, "toolCallsInvestigation": 0, "repairTurns": 1,
    "completionStatus": "emitted",
    "emitPath": "tool-call",
    "model": "meta/llama-3.3-70b-instruct", "provider": "integrate.api.nvidia.com",
    "sampling": {"temperature": 0, "seed": null},
    "tokensIn": 2140, "tokensOut": 188, "budgetLimit": 20000, "budgetHit": false,
    "schemaVersion": "1.0", "toolVersion": "0.1.0"
  },
  "changeSummary": {
    "scope": {"kind": "working-tree", "baseRef": null, "headRef": null, "wasDefaulted": true,
              "description": "uncommitted changes in the working tree (default) · 3 files"},
    "excluded": [{"path": "dist/index.js", "rule": "default:build-output"}],
    "files": [
      {"path": "src/auth/login.ts", "changeType": "modified", "previousPath": null, "language": "ts",
       "isBinary": false, "reviewed": true, "notReviewedReason": null,
       "hunkCount": 2, "addedLines": 14, "removedLines": 3},
      {"path": "README.md", "changeType": "modified", "previousPath": null, "language": "other",
       "isBinary": false, "reviewed": false, "notReviewedReason": "not-typescript-or-javascript",
       "hunkCount": 0, "addedLines": 2, "removedLines": 0}
    ]
  },
  "context": [],
  "evidence": {"status": "not-attempted", "checks": []},
  "findings": [
    {"id": "f-1", "schemaVersion": "1.0", "turnIndex": 1, "fingerprint": "a3f19c02be71",
     "file": "src/auth/login.ts", "startLine": 42, "endLine": 47,
     "severity": "blocking", "category": "error-handling",
     "rationale": "The expired-token branch returns before releasing the session lock.",
     "evidence": {"kind": "diff", "file": "src/auth/login.ts", "hunkIndex": 1}}
  ],
  "degradations": [],
  "verdict": "blocking"
}
```

*Note `turnIndex: 1` and `repairTurns: 1`: the first call was rejected and corrected in the repair turn, so nothing is
recorded as damaged (spec US2-AS2).*

## The eight outcomes (SC-003)

What differs between outcomes. Every row differs from every other in at least one column. A zero-finding review is always the "no tool call" row
(D-5, decided).

| Outcome | `completionStatus` | `degradations[].code` | `verdict` | Exit |
|---|---|---|---|---|
| Findings, none blocking | `emitted` | — | `findings` | 0 |
| Blocking finding | `emitted` | — | `blocking` | 1 |
| Provider failure | `provider-error` | `provider-error` | `no-judgement` | 2 |
| Output not validatable, nothing accepted | `invalid-model-output` | `invalid-model-output` | `no-judgement` | 2 |
| No tool call | `no-tool-call` | `no-tool-call` | `no-findings` | 0 |
| Ceiling reached | `ceiling-reached` | `tool-budget-exhausted` if calls were dropped | by findings | 0 / 1 |
| Diff over the limit | `budget-exhausted` | `budget-exhausted` | `no-judgement` | 2 |
| Nothing to review | `nothing-to-review` | — | `nothing-to-review` | 0 |

## Per-outcome differences from the example

| Outcome | `stageDurationsMs` keys | Counters | `findings` | `tokensIn/Out` | `budgetHit` |
|---|---|---|---|---|---|
| Nothing to review | preflight, changeSet, output | all 0 | `[]` | null | false |
| Diff over the limit | + assembly | all 0 | `[]` | null | **true** |
| Provider failure (first turn) | + assembly, review | all 0 | `[]` | null | false |
| No tool call | + assembly, review | all 0 | `[]` | as reported | false |

## Schema-level rules

- `degradations` is **required** and may be empty. An empty array asserts a clean run (04 §5).
- `context` has `maxItems: 0` and `evidence.checks` has `maxItems: 0` in 1.0. Features 002 and 004 widen these in minor versions (R-22).
- `requestedDepth` and `achievedDepth` are `integer | null`. **null means "related context not gathered"** and is documented as such in the schema.
- The `DegradationCode` enum lists all of 02 §3.5 (additions are minor bumps). Only five codes are reachable in 001.
- No field anywhere may hold the credential. The schema has no such field, and the tests scan for the planted canary (SC-007).
- Diff text is **never** in the report (02 §3.1).
