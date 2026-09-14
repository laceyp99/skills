# Skills Lifecycle

The workflow is intentionally flexible. `/grill-me` and `/blueprint` are optional, while `/assembly` is the implementation handoff. Review and validation can happen before or alongside `/babysit`, depending on whether the work is being done step by step or autonomously.

```mermaid
flowchart TD
    START([Task arrives]) --> PRELUDE["/prelude<br/>Understand and scope task"]
    PRELUDE --> NARROW{Does the direction<br/>need more narrowing?}

    NARROW -- Yes --> GRILL["/grill-me<br/>Resolve key decisions"]
    GRILL --> PLAN_DECISION

    NARROW -- No --> PLAN_DECISION{Does the task need<br/>a written plan?}
    PLAN_DECISION -- Yes --> BLUEPRINT["/blueprint<br/>Create executable plan"]
    PLAN_DECISION -- No --> ASSEMBLY["/assembly<br/>Implement in controlled units"]
    BLUEPRINT --> ASSEMBLY

    ASSEMBLY --> MODE{Execution mode}
    MODE -- Autopilot --> AUTO_VALIDATION[Automated validation<br/>and review as configured]
    AUTO_VALIDATION --> BABYSIT_AUTO["/babysit<br/>Publish ready PR and verify"]

    MODE -- Hand holding --> HUMAN[Human review point<br/>Check work and choose next step]
    HUMAN --> HAND_DECISION{Continue implementation?}
    HAND_DECISION -- Yes --> ASSEMBLY
    HAND_DECISION -- No --> HAND_REVIEW["/gauntlet or personal checks"]
    HAND_REVIEW --> POSTED{PR posted and<br/>ready for review?}
    POSTED -- No --> BABYSIT["/babysit<br/>Publish and verify PR"]
    POSTED -- Yes --> REALITY["/reality-check<br/>Review PR"]

    BABYSIT --> REALITY
    BABYSIT_AUTO --> REALITY
    REALITY --> FINDINGS{Findings or<br/>failed validation?}

    FINDINGS -- No --> DONE([Task lifecycle complete])
    FINDINGS -- Yes --> DECISION[Human decision point<br/>Interpret findings and choose next action]
    DECISION -. Re-scope or clarify .-> PRELUDE
    DECISION -. Revise implementation .-> ASSEMBLY
    DECISION -. Ignore or justify findings .-> DONE
```
