# Options phase response template: solution options and trade-offs

Use this template after the issue has been investigated and the real problem is reasonably understood.

## Solution options

Present the meaningful options only. Avoid filler options that technically exist but do not make sense for the project.

For each option, include:

### Option [A/B/C]: [short name]

**What it changes**
Explain the implementation direction in practical terms.

**Why it makes sense**
Name the scenario where this option is the right fit.

**Trade-offs**
Cover maintainability, architecture, UX, test impact, risk, scope, and project focus.

**Evidence fit**
Explain how well this option matches the evidence found in the understanding phase.

## Comparison table

Use a compact table when there are two or more viable options.

| Option | Best for | Pros | Cons | Risk | Fit |
|---|---|---|---|---|---|
| A |  |  |  | low/medium/high | weak/okay/strong |
| B |  |  |  | low/medium/high | weak/okay/strong |

## Simple explanation or real-world analogy

Use an analogy that compares the solution choices.

Example:

> Option A is like changing the sign on a door so people stop trying the wrong entrance. Option B is like rebuilding the hallway so that entrance actually works. The right choice depends on whether the entrance was supposed to be usable in the first place.

## Recommended path

Recommend one path clearly. Include the reason it best serves the project’s intended use.

Suggested phrasing:

> I recommend Option B because it fixes the rule at the source, aligns with the existing domain model, and gives us a clean place to add regression tests. Option A is smaller, but it would leave the backend behavior surprising for future callers.

## Implementation decision questions

Ask narrow questions that unlock implementation.

Examples:

- “Should this behavior apply globally or only when the feature flag is enabled?”
- “Do we want to treat existing records as legacy exceptions?”
- “Should the user see a blocking error, a warning, or automatic correction?”
- “Is preserving the current API response shape required?”

## Suggested next step

End with one clear next step:

- “Choose Option A or B and I can turn it into an implementation plan.”
- “I recommend Option B; confirm the product behavior and then implementation can start.”
- “This needs product clarification before code changes because both behaviors are defensible.”
