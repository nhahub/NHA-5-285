# Sequence Diagram — End-to-End Review Pass

Part of the [v1 System Analysis](../system_analysis.md#52-end-to-end-review-pass) · Mermaid `sequenceDiagram`

One invocation at the default ceiling of zero. The outer `alt` separates the fail-fast path, where no review is produced, from the pipeline path. Inside the pipeline, each `alt` shows a degradation that still ends in a review. Context retrieval is summarised in one exchange here; the depth 0 and depth 1 flows are decomposed in their own diagrams.

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant CLI as Local CLI<br/>fixed pipeline
    participant AST as AST Parser<br/>tree-sitter, CF-2
    participant TC as Toolchain Executable<br/>project's own tests and tsc
    participant AG as Isolated Review Agent<br/>CF-6
    participant LLM as Model Provider

    Dev->>CLI: review, with optional scope, depth and JSON flags
    CLI->>CLI: load config, check git repository and provider key (CF-9)
    alt precondition fails
        CLI-->>Dev: error naming the cause, non-zero exit (FR-1.2d, FR-9.3)
    else preconditions met
        CLI->>CLI: resolve change set, drop excluded paths (CF-1, FR-3.5)
        par related context
            CLI->>AST: resolve(changeSet, depth, budget)
            AST-->>CLI: units, achievedDepth, degraded if any
        and evidence
            CLI->>TC: run tests and type check as subprocesses (FR-4.7)
            alt within the time budget
                TC-->>CLI: exit codes and captured output
            else time budget exceeded
                CLI->>TC: terminate
                Note over CLI,TC: execution marked timed-out, remaining checks skipped (FR-4.4b)
            end
        end
        CLI->>CLI: build evidence record: run, skipped or errored, pass or fail (FR-4.5)
        CLI->>CLI: assemble per-section budgets, reduce check output, evict by distance (CF-4)
        CLI->>AG: review(context), no shared history (FR-5.1)
        AG->>LLM: single pass, emit_finding is the only tool (ceiling 0)
        alt provider responds
            LLM-->>AG: emit_finding calls
            AG->>AG: validate each call against the finding schema (FR-5.6a)
        else provider error or token budget reached
            AG->>AG: record the degraded completion (FR-11.1, FR-11.2)
        end
        AG-->>CLI: finding model: findings and completion status
        CLI-->>Dev: terminal summary: scope, checks, counts by severity, verdict
        opt JSON requested
            CLI-->>Dev: JSON artifact in the versioned schema (FR-8.2)
        end
        CLI-->>Dev: exit status (FR-10.4c)
    end
```
