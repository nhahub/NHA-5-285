# Requirement Diagram — CF-6 Drill-Down: The Review Agent and Its Ceiling

Part of the [v1 System Analysis](../system_analysis.md#23-requirement-diagrams) · Mermaid `requirementDiagram`

CF-6 carries risks R-2, R-2a and R-4. This view shows how the tool-call ceiling is constrained, and which acceptance criteria hold it in place. FR-5.7a is a Should with no direct acceptance criterion. FR-5.1 is omitted: v1 has no code-writing agent to isolate from, so it holds by construction.

```mermaid
requirementDiagram

functionalRequirement CF6 {
    id: "CF-6"
    text: "The review agent"
    risk: high
    verifymethod: test
}

functionalRequirement FR53 {
    id: "FR-5.3"
    text: "Findings incorporate execution evidence and pattern rules"
    risk: medium
    verifymethod: test
}

functionalRequirement FR57 {
    id: "FR-5.7"
    text: "Tool-call ceiling is configuration, default zero, emit_finding only"
    risk: medium
    verifymethod: test
}

functionalRequirement FR57A {
    id: "FR-5.7a (Should)"
    text: "Above zero, expose only read_file, get_outline and search_repo, all read-only"
    risk: medium
    verifymethod: demonstration
}

functionalRequirement FR57B {
    id: "FR-5.7b"
    text: "No ceiling above zero before a recorded single-pass baseline"
    risk: medium
    verifymethod: test
}

designConstraint FR58 {
    id: "FR-5.8"
    text: "The agent framework is confined to CF-6"
    risk: medium
    verifymethod: test
}

element AC2 {
    type: "end-to-end run"
}

element AC10 {
    type: "import-graph check"
}

element AC11 {
    type: "harness run"
}

CF6 - contains -> FR53
CF6 - contains -> FR57
CF6 - contains -> FR57A
CF6 - contains -> FR57B
CF6 - contains -> FR58
FR57A - refines -> FR57
FR57B - refines -> FR57

AC2 - verifies -> FR53
AC10 - verifies -> FR58
AC11 - verifies -> FR57B
```
