# Contract: Command-Line Surface (001 subset)

**Parent contract**: [`Docs/design/04-contracts.md`](../../../Docs/design/04-contracts.md) §6. This is the part
of it that feature 001 builds. Flags not listed here are **not offered** until the feature that gives them
meaning (spec Assumptions). They are not accepted and silently ignored.

Stability: 📦 stable across v1 patch releases.

---

## Commands

```
agentic-review review [OPTIONS]
agentic-review schema
agentic-review --version
```

`regression` arrives in 003.

## `review`

| Option | Value | Default | Rule |
|---|---|---|---|
| `--scope` | `working-tree \| staged \| range \| commit` | config `scope`, else `working-tree` | FR-005. The resolved scope is stated in both outputs; `wasDefaulted` is true only when neither this flag, nor `--commit`, nor `--pr`, nor the config named it. **A value is offered only once its scope is built**: `working-tree` and `range` today; `staged` and `commit` are refused with exit 3 until User Story 4 |
| `--base REF` | a git ref | — | **Required** when the scope is `range`. With `--pr`, optional: the branch the pull request targets. Rejected with any other scope. Missing → exit 3 naming `--base`. Unknown ref → exit 3 naming the ref |
| `--head REF` | a git ref | `HEAD` | `range` only: the ref reviewed, so a branch can be reviewed without checking it out. Rejected with any other scope. Unknown ref → exit 3 naming the ref. Refs that share no history → exit 3 |
| `--pr URL` | `https://github.com/<owner>/<repo>/pull/<n>` | — | Reviews a **public** GitHub pull request: its head against the branch it targets — the repository's default branch unless `--base` names another (R-25). **Selects the `pull-request` scope by itself**; with `--scope` or `--head` → exit 3. Needs no local repository and reads no file from the current directory. Nothing from the pull request is executed and no configuration is read from it (SRS FR-10.3d). Malformed URL, repository unreachable, pull request or base not found → exit 3 naming it |
| `--commit REF` | a git ref that resolves to a commit | — | Reviews what that one commit introduced, against its first parent (R-4). **Selects the `commit` scope by itself**, over the config's `scope`; `--scope commit` may be written too but is not needed. `--scope commit` without it → exit 3 naming `--commit`. With any other `--scope`, or with `--base` → exit 3 naming `--commit`. Unknown ref → exit 3 naming the ref. The config file cannot select this scope: a commit is named per run |
| `--json [PATH]` | optional path | off | No value, or `-` → the report on **stdout only**. With a path → written to that file (R-18) |
| `--config PATH` | file path | `<repo root>/.agentic-review.yml`; with `--pr`, **none** — the built-in defaults | An explicit path that does not exist → exit 3. The only way to give settings to a `--pr` review |
| `--ceiling N` | integer ≥ 1 | config `agent.toolCallCeiling` (25, **placeholder, TBD-8**) | FR-017 |

Deferred and **not offered**: `--depth`, `--no-checks` (both 002/004), `--investigate` (005).

### Streams

| Invocation | stdout | stderr |
|---|---|---|
| `review` | terminal summary | ignored-settings notice, if any |
| `review --json` | **exactly one JSON document**, UTF-8, trailing newline | terminal summary, notices |
| `review --json out.json` | terminal summary | notices |
| any preflight failure | **nothing** | the message |

The terminal summary is plain text when the stream is not a TTY, and honours `NO_COLOR`.

### Terminal summary: required content (FR-024)

In this order. Wording may vary; content may not.

1. The scope line: the resolved scope and `(default)` if it was defaulted.
2. The files reviewed, and the files **listed but not reviewed**, each with its reason.
3. The excluded paths, each with its rule. May be collapsed to a count beyond 10, with the full list in the report.
4. **"No checks were run in this build."**
5. **"No related context was gathered in this build."**
6. Each finding: `path:start[-end]`, severity, category, rationale, evidence (`diff hunk i` or
   `unverified: <reason>`), and rule if any.
7. Counts by severity, in the fixed order `blocking / important / nit`.
8. Each degradation: source, code, detail.
9. The verdict line, including for `no-judgement`: **"No review was performed"**, never "no findings".

### Exit codes (FR-023)

| Code | Meaning | Verdicts |
|---|---|---|
| **0** | Reviewed, nothing blocking, **including degraded runs and nothing-to-review** | `findings`, `no-findings`, `nothing-to-review` |
| **1** | Reviewed, ≥1 `blocking` finding | `blocking` |
| **2** | No judgement made | `no-judgement`; also an unexpected internal error after preflight (R-24) |
| **3** | Could not start | preflight failure; no report is written |

The verdict is computed in core. `cli/` holds only the verdict → integer table.

### Preflight messages (FR-001, 05 §4.4)

Every message states **what** is wrong, **where it was looked for**, and that **nothing was reviewed**.
Checks run in this order and stop at the first failure. The model is never called.

| Order | Check | Message names |
|---|---|---|
| 1 | Inside a git repository — or, with `--pr`, the URL is a GitHub pull request URL | The directory checked, or the URL and the form expected |
| 2 | Config file valid (if present, or if `--config` was given) | The file, the dotted field path, and the problem |
| 3 | Scope arguments coherent (`range` ⇔ `--base`; `--head` only with `range`; `commit` ⇔ `--commit`; `--pr` excludes `--scope` and `--head`) | The option |
| 4 | Credential available | `AGENTIC_REVIEW_API_KEY`, and the user-level credential file path for this OS |
| 5 | Range base and head exist and share history, and `HEAD` is not unborn for `range`; the commit named by `--commit` exists; **the pull request named by `--pr` can be read**, with its base branch | The ref, or the pull request and what could not be reached |

Check 5 is the only one that may use the network, and only for `--pr`. It is last on purpose: a missing credential
or a mistyped option never costs a clone. git is never allowed to prompt for a login while it runs.

Example:

```
Error in .agentic-review.yml
  agent.toolCallCeiling: Input should be greater than or equal to 1
Nothing was reviewed. Fix the field above and re-run.
```

## `schema`

Prints the **review-report JSON Schema** (draft 2020-12, generated from `ReviewReport`) to stdout, then exits 0.
It needs no repository, no config, and no credential (FR-028). Its `$id` includes the schema version, and its
top-level `description` states that consumers must ignore unknown fields.

## `--version`

Prints `agentic-review <toolVersion> (report schema <schemaVersion>)`, then exits 0.
