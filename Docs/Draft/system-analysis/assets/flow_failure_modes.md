# Flowchart — Fail Fast versus Degrade and Report

Part of the [v1 System Analysis](../system_analysis.md#61-fail-fast-versus-degrade) · Mermaid `flowchart`

v1 has exactly two failure behaviours. A missing prerequisite stops the run before any review exists, and the error names the cause. Everything that goes wrong after that point degrades: the review is still produced, and it states what was lost. The boundary between the two is where FR-9.3 and FR-11.2 meet, and two of its cases are ambiguous in the SRS (Q-1, Q-11).

```mermaid
flowchart TD
    I(["Invocation"]) --> P{"Preconditions<br/>CF-9"}
    P -->|"fail"| FAIL
    P -->|"pass"| R["Fixed pipeline runs<br/>CF-1 to CF-7"]

    subgraph FAIL["Fail fast: named cause, non-zero exit, no review"]
        direction TB
        F1["Malformed config<br/>offending field named<br/>FR-1.2d · AC-9"]
        F2["Provider key missing<br/>FR-1.3a · FR-9.3 · AC-9"]
        F3["Not a git repository<br/>FR-9.3"]
        F4["Unparseable tree<br/>FR-9.3 · see Q-11"]
    end

    subgraph DEG["Degrade and report: a review is always produced, FR-11.2"]
        direction TB
        D1["No test script, or a check skipped or errored<br/>FR-4.5a · AC-7 · see Q-1"]
        D2["Execution phase timed out<br/>FR-4.4b"]
        D3["Depth requested above maxDepth<br/>degraded no-index · AC-8"]
        D4["Resolver sidecar unavailable<br/>degraded unresolvable-imports · AC-12"]
        D5["Context over budget<br/>evict by distance, diff kept · FR-2.5b"]
        D6["Provider error<br/>FR-11.2"]
        D7["Token or call budget reached<br/>FR-11.1"]
        D8["Tool-call ceiling reached<br/>FR-5.7c, ceiling above zero only"]
    end

    R -.->|"any, alone or combined"| DEG
    R --> OUT["Review produced<br/>terminal summary and JSON state every degradation"]
    DEG --> OUT

    style FAIL fill:#ffe6e6,color:#1a1a1a
    style DEG fill:#fff4e0,color:#1a1a1a
    style OUT fill:#e8f7e8,color:#1a1a1a
```
