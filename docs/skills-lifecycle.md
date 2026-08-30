# Skills Lifecycle

The workflow is intentionally flexible. `/grill-me` and `/blueprint` are optional, while `/assembly` is the implementation handoff. Review and validation can happen before or after `/pr-actical`, depending on whether the work is being done step by step or autonomously.

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
    AUTO_VALIDATION --> PRACTICAL_AUTO["/pr-actical<br/>Push and create or update draft PR"]

    MODE -- Hand holding --> HUMAN[Human review point<br/>Check work and choose next step]
    HUMAN --> HAND_DECISION{Continue implementation?}
    HAND_DECISION -- Yes --> ASSEMBLY
    HAND_DECISION -- No --> HAND_REVIEW["/gauntlet or personal checks"]
    HAND_REVIEW --> POSTED{PR posted and<br/>ready for review?}
    POSTED -- No --> PRACTICAL["/pr-actical<br/>Prepare or update draft PR"]
    POSTED -- Yes --> REALITY["/reality-check<br/>Review PR"]

    PRACTICAL --> DRAFT([Draft PR ready for user review])
    PRACTICAL_AUTO --> DRAFT
    DRAFT -. User marks PR ready .-> REALITY
    REALITY --> FINDINGS{Findings or<br/>failed validation?}

    FINDINGS -- No --> DONE([Task lifecycle complete])
    FINDINGS -- Yes --> DECISION[Human decision point<br/>Interpret findings and choose next action]
    DECISION -. Re-scope or clarify .-> PRELUDE
    DECISION -. Revise implementation .-> ASSEMBLY
    DECISION -. Ignore or justify findings .-> DONE
```
