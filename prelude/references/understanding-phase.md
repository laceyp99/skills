# Understanding phase response template: understanding and correction

Use this template after investigating the issue and repo evidence. Adapt headings as needed, but preserve the intent of each section.

## What the issue seems to be saying

Summarize the reported problem in plain language. Preserve the user’s framing without accepting it as proven.

Example phrasing:

> The issue is saying: “When a user does X, the app should do Y, but instead it does Z.”

## What the codebase suggests is actually happening

Explain the behavior the code appears to implement. Connect the symptom to the actual code path, configuration, data, or test behavior.

Prefer simple cause-and-effect wording:

> The UI shows the error message, but the decision is actually made in the API validation layer. So the screen is where the smoke appears, not where the fire starts.

## Where the misunderstanding may be

Use this section only when useful. Clarify mismatch between the issue’s assumption and the codebase/product model.

Common patterns:

- The issue describes a frontend problem, but the rule lives in backend validation.
- The user story asks for a new behavior, but existing tests imply the opposite behavior is intentional.
- The reporter expects a role, flag, or status to mean one thing, while the code treats it differently.
- The issue is really about unclear language or workflow, not broken logic.

## Simple explanation or real-world analogy

Explain the concept with a metaphor. Keep it connected to the actual issue.

Example:

> Think of this like a restaurant ticket system. The waiter can write “rush order” on the ticket, but the kitchen still decides whether the dish can be made faster. In this codebase, the form is the waiter and the validation layer is the kitchen.

## Evidence gathered

List concrete evidence. Include file paths, line ranges, commands, test results, issue comments, docs, or reproducible scenarios.

Suggested format:

- `path/to/file.ext:10-30` — what this shows.
- `command used` — what result mattered.
- Existing test or missing test — what confidence it gives or does not give.

Avoid dumping raw output unless the exact text matters.

## Recommended interpretation

State the clearest current understanding of the problem.

Use one of these styles:

- “This appears to be a real bug in…”
- “This appears to be a feature request disguised as a bug because…”
- “This appears to be a product-language mismatch rather than a code defect…”
- “This appears to be under-specified; the code supports multiple reasonable interpretations…”

## Questions before implementation

Ask only questions that matter for choosing a fix. Keep them narrow.

Good questions:

- “Should this behavior change for all users or only admins?”
- “Should we preserve the existing API contract and adjust the UI, or change the backend rule?”
- “Is backward compatibility with existing saved records important here?”

Bad questions:

- “Can you provide more context?”
- “What do you want me to do?”
