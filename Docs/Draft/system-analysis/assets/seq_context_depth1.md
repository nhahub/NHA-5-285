# Sequence Diagram — Context Depth 1

Part of the [v1 System Analysis](../system_analysis.md#53-context-laddering) · Mermaid `sequenceDiagram`

Depth 1 reaches outward to the definitions of symbols the change imports and calls. Syntax still comes from tree-sitter. The only new step is working out which file an import specifier names, and that is delegated to the bundled resolver sidecar. Each of the three `degraded` values is set in this flow. None of them stops the review.

```mermaid
sequenceDiagram
    autonumber
    participant P as Pipeline<br/>interface consumer
    participant PCP as ParserContextProvider<br/>CF-2, maxDepth 1
    participant TS as tree-sitter<br/>in the host process
    participant SC as Resolver Sidecar<br/>bundled, private to CF-2

    P->>PCP: resolve(changeSet, depth, budget)
    opt requested depth above maxDepth
        Note over PCP: serve depth 1, set degraded no-index (FR-2.6d, AC-8)
    end
    PCP->>PCP: depth-0 pass, as in the depth 0 flow
    PCP->>TS: extract import specifiers and called symbols
    TS-->>PCP: specifier strings and call names
    alt sidecar available
        PCP->>SC: start, at most once per invocation (FR-2.6f)
        PCP->>SC: resolve specifiers over the documented contract
        SC-->>PCP: specifier to file path
    else runtime absent or sidecar fails
        PCP->>PCP: heuristic path resolution (FR-2.6g)
        Note over PCP: set degraded unresolvable-imports, review continues (AC-12)
    end
    loop each resolved target file, while budget remains
        PCP->>TS: parse target, locate the imported or called definition
        TS-->>PCP: definition source and range
    end
    opt budget reached before all definitions are gathered
        Note over PCP: set degraded budget-exhausted
    end
    PCP-->>P: units at distance 1 (imports, calls), achievedDepth 1, degraded if any
    Note over P,PCP: The consumer never learns whether the sidecar ran (FR-2.6e)
```
