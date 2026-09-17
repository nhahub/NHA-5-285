# Sequence Diagram — Context Depth 0

Part of the [v1 System Analysis](../system_analysis.md#53-context-laddering) · Mermaid `sequenceDiagram`

Depth 0 is pure syntax: parse the changed files and widen each hunk to the function, class or type that encloses it. It needs no resolver sidecar, no repository index, and no target-language toolchain.

```mermaid
sequenceDiagram
    autonumber
    participant P as Pipeline<br/>interface consumer
    participant PCP as ParserContextProvider<br/>CF-2, maxDepth 1
    participant TS as tree-sitter<br/>in the host process

    P->>PCP: resolve(changeSet, depth 0, budget)
    loop each changed TS or JS file
        PCP->>TS: parse file (FR-2.2)
        TS-->>PCP: concrete syntax tree
        PCP->>PCP: widen each hunk to its enclosing function, class or type (FR-2.4)
    end
    PCP->>PCP: record why each unit was included (FR-2.3d)
    PCP-->>P: units at distance 0, achievedDepth 0
    Note over P,TS: No sidecar, no index, no target toolchain. The relation value for depth-0 units is undefined, see Q-4.
```
