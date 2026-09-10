# State Diagram — Check Execution Lifecycle

Part of the [v1 System Analysis](../system_analysis.md#54-check-execution-lifecycle) · Mermaid `stateDiagram-v2`

The execution phase runs once per invocation, before the review pass (FR-4.6). Every check ends in one of four recorded states, and a phase-level timeout can cut the phase short at any point. `Passed` and `Failed` are both `run` in FR-4.5a terms; the pass/fail outcome is recorded separately (FR-4.5b). The state of a check that is still running when the timeout fires is not specified (Q-6).

```mermaid
stateDiagram-v2
    [*] --> ExecutionPhase

    state ExecutionPhase {
        [*] --> Pending
        Pending --> Skipped : no command in manifest or config
        Pending --> Executing : subprocess started through the project toolchain
        Pending --> Errored : subprocess failed to start
        Executing --> Passed : exit 0
        Executing --> Failed : non-zero exit
        Executing --> Errored : crashed or output unusable
        Passed --> [*]
        Failed --> [*]
        Skipped --> [*]
        Errored --> [*]
    }

    Passed : run, pass
    Failed : run, fail
    Skipped : skipped
    Errored : errored

    ExecutionPhase --> Recorded : every configured check reached a final state
    ExecutionPhase --> TimedOut : phase time budget exceeded (FR-4.4a)
    TimedOut --> Recorded : remaining checks marked skipped (FR-4.4b)
    Recorded --> [*] : evidence record passed to context assembly and output
```
