# Requirement Diagram — CF-2 Drill-Down: The Related-Context Interface

Part of the [v1 System Analysis](../system_analysis.md#23-requirement-diagrams) · Mermaid `requirementDiagram`

CF-2 carries the most risk in v1 (R-1, R-3, R-7). This view breaks out the FR-2.6 family and the three structural acceptance criteria that exercise it. FR-2.2, FR-2.3d, FR-2.4 and FR-2.6c are omitted; they are verified only incidentally, by AC-1.

```mermaid
requirementDiagram

functionalRequirement CF2 {
    id: "CF-2"
    text: "Parsing and related context"
    risk: high
    verifymethod: test
}

interfaceRequirement FR26A {
    id: "FR-2.6a"
    text: "One depth-parameterised retrieval interface, implementation chosen at run time"
    risk: medium
    verifymethod: test
}

functionalRequirement FR26B {
    id: "FR-2.6b"
    text: "Parser-backed provider serves depth 0 and 1 without a repository index"
    risk: high
    verifymethod: test
}

functionalRequirement FR26D {
    id: "FR-2.6d"
    text: "Report the achieved depth and the reason, never downgrade silently"
    risk: medium
    verifymethod: test
}

designConstraint FR26E {
    id: "FR-2.6e"
    text: "No consumer branches on which implementation served the request"
    risk: medium
    verifymethod: test
}

interfaceRequirement FR26F {
    id: "FR-2.6f"
    text: "Bundled resolver sidecar, started at most once, invisible outside CF-2"
    risk: medium
    verifymethod: test
}

functionalRequirement FR26G {
    id: "FR-2.6g"
    text: "Without the sidecar, fall back to heuristics and mark unresolvable-imports"
    risk: medium
    verifymethod: test
}

element AC6 {
    type: "harness run"
}

element AC8 {
    type: "capability-removal run"
}

element AC10 {
    type: "import-graph check"
}

element AC12 {
    type: "capability-removal run"
}

CF2 - contains -> FR26A
CF2 - contains -> FR26B
CF2 - contains -> FR26D
CF2 - contains -> FR26E
CF2 - contains -> FR26F
CF2 - contains -> FR26G
FR26G - refines -> FR26D

AC6 - verifies -> FR26A
AC6 - verifies -> FR26B
AC8 - verifies -> FR26D
AC10 - verifies -> FR26E
AC12 - verifies -> FR26F
AC12 - verifies -> FR26G
```
