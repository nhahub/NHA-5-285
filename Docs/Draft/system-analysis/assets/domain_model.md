# Conceptual Domain Model

Part of the [v1 System Analysis](../system_analysis.md#43-conceptual-class-diagram) · Mermaid `classDiagram`

This diagram shows analysis entities, not implementation classes: attributes and structural relationships only, no operations. `ContextUnit` and `RelatedContextResult` follow the normative interface in SRS v1 §4.2.2. The other entities are drawn from the FR text. Value-set types (`ChangeScope`, `Relation`, `Degradation`, `RunState`, and so on) are listed in the main document, §4.2.

```mermaid
classDiagram
    direction LR

    class ChangeSet {
        +scope : ChangeScope
        +baseRef : string [0..1]
    }
    class ChangedFile {
        +path : string
    }
    class Hunk {
        +range : line range
        +patch : string
    }
    class RelatedContextResult {
        +achievedDepth : int
        +degraded : Degradation [0..1]
    }
    class ContextUnit {
        +file : string
        +symbol : string [0..1]
        +range : line range
        +source : string
        +relation : Relation
        +distance : int
    }
    class EvidenceRecord {
        +executionStatus : ExecutionStatus
    }
    class CheckResult {
        +check : string
        +runState : RunState
        +outcome : pass or fail [0..1]
        +capturedOutput : string
    }
    class FindingModel {
        <<aggregate>>
        +schemaVersion : string
    }
    class Finding {
        +file : string
        +lines : line or line range
        +severity : Severity
        +category : Category
        +rationale : string
        +ruleId : string [0..1]
    }
    class RunMetadata {
        +resolvedScope : ChangeScope
        +achievedDepth : int
        +toolCallCeiling : int
        +toolCallsMade : int
        +completionStatus : CompletionStatus
        +modelVersion : string
    }
    class PatternRule {
        +id : string
        +standard : string
        +wrongExample : string
        +correctExample : string
    }
    class RegressionCase {
        +id : string
        +fixture : change set
        +expectedOutcome : string
    }

    ChangeSet "1" *-- "1..*" ChangedFile : contains
    ChangedFile "1" *-- "1..*" Hunk : contains
    RelatedContextResult ..> ChangeSet : retrieved for
    RelatedContextResult "1" o-- "0..*" ContextUnit : units, by distance
    EvidenceRecord "1" *-- "0..*" CheckResult : checks
    FindingModel "1" *-- "0..*" Finding : findings
    FindingModel "1" *-- "1" EvidenceRecord : evidence
    FindingModel "1" *-- "1" RunMetadata : run
    FindingModel ..> ChangeSet : reviews
    Finding "0..*" --> "0..1" PatternRule : cites ruleId
    Finding ..> CheckResult : grounded in, via prose only
    PatternRule "1" *-- "1..*" RegressionCase : proven by

    note for Finding "FR-5.2 fields. No structured link to evidence, see Q-5"
```
