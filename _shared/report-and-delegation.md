# Report and delegation guidance

Read the relevant sections when the invoking skill requests a report, writes a local planning or review artifact, or delegates work. The invoking skill retains its workflow, scope, and stop conditions.

## Local artifacts

Before writing `plan.md`, `decisions.md`, `quiz.md`, `review.md`, `review-findings.md`, or another local planning or review artifact, check whether Git already tracks it. Keep these artifacts local and untracked by default. If one is tracked unexpectedly, warn the user, do not change its tracking state, and keep its modifications out of commits. Never add them to `.gitignore`, stage, commit, or publish them automatically. Package or publish only when explicitly requested, subject to the invoking workflow's boundaries.

## Requested reports

Enter report mode only when requested, using the user's specified medium or established session preference. Ask if the medium is missing; continue independent work without generating a report. Do not default to HTML or video. Create multiple formats only when requested.

For HTML, invoke `/html-communication` after completing the invoking skill's work. For Gauntlet, Prelude, and Reality Check, the HTML report is the main reader-facing result. Use visuals or interaction only where they clarify the evidence; choose the layout to suit the work. Link the report in chat and briefly state the conclusion and next action.

For video, invoke `/video-communication` after completing the invoking skill's work. Supply the audience, inspected revision, destination, and the skill-specific context below. Keep the video package outside the worktree by default. Video creation does not authorize implementation, a branch, or additional publication. Distinguish observed behavior from proposed or hypothetical animation; label animation as illustration rather than test footage. Link the MP4 and any canonical local artifact in chat, using the invoking skill's ordinary closeout.

### Gauntlet

Use `review.md` as the persistent source of truth. For video, pass `review.md`, automated results, human observations, unverified areas, and the scoped conclusion. For HTML, show how changed behaviors map to those results and observations, state the scoped conclusion and next action, and derive the assessment from `review.md`.

### Prelude

For video, pass the evidence, root-cause interpretation, options, recommendation, and unresolved decisions. Keep the checkpoint quiz in local `quiz.md` for video-only delivery and link it beside the MP4. For HTML, present the issue interpretation, strongest evidence, viable options and trade-offs when relevant, recommendation, and unresolved decisions. The report remains a communication artifact rather than an implementation plan.

### Reality Check

For video, pass confirmed findings and dispositions, source evidence, and review limits. Keep actionable findings in `review-findings.md` or the authorized GitHub review. For video-only delivery, keep actionable findings and the checkpoint quiz in local `review-findings.md` and link it beside the MP4. For HTML, make findings, severity, evidence, dispositions, scope, limits, and the next action easy to inspect; keep GitHub comments or `review-findings.md` as the actionable record.

### Blueprint

Create a companion explanation; `plan.md` and its checkpoint quiz remain canonical. For video, pass `plan.md`, the proposed mechanism, and risks; label proposed behavior as proposed. For HTML, explain the plan without replacing it.

## Delegated tasks

Delegate focused work when it isolates substantial investigation or implementation context, rather than merely maximizing parallelism.

Give each explorer or worker:

- One concrete question or responsibility.
- The minimum relevant issue, diff, plan, and repository context.
- The expected answer, implementation, or validation report, with supporting file or symbol-level evidence.
- Explicit ownership and mutation boundaries; explorers remain read-only.
- A stopping condition for completion, exhausted evidence, conflicts, or blockers.

The primary agent evaluates returned evidence, resolves conflicts, and owns synthesis, integration, validation, lifecycle decisions, and communication with the user. Do not delegate the entire invoking workflow or user conversation. Delegation does not expand scope, authorization, or selected mode; workers must not commit unless the authorized workflow explicitly assigns that responsibility.

Prefer sequential delegation for context management. Use concurrent workers only when ownership is disjoint, work does not depend on the same uncommitted changes, and results can be integrated without ambiguity. Do not split tightly coupled work merely to delegate. If a suitable role or mechanism is unavailable, continue directly when practical and report the limitation when it prevents safe completion.
