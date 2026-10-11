# Report and delegation guidance

Read only the section linked by the invoking skill when its trigger applies; load another section only when its own trigger applies. The invoking skill retains its workflow, scope, and stop conditions.

## Local artifacts

Follow the user's explicitly requested artifact destination and tracking policy. Otherwise keep `plan.md`, `decisions.md`, `quiz.md`, `review.md`, `review-findings.md`, and other local planning or review artifacts local and untracked by default. Before writing, check whether Git already tracks the target. If tracking is unexpected, warn the user, preserve its tracking state, and keep its modifications out of commits. Intentional tracking permits maintaining the tracked artifact; it does not by itself authorize staging, committing, or publishing it. Without explicit authorization, do not change ignore rules or tracking state, or stage, commit, package, or publish artifacts. Respect the invoking workflow's scope and stop conditions.

## Requested reports

Enter report mode only when requested, using the user's specified medium or established session preference. Ask if the medium is missing; continue independent work without generating a report. Do not default to HTML or video. Create multiple formats only when requested.

For HTML, invoke `/html-communication` after completing the invoking skill's work. Use visuals or interaction only where they clarify the evidence; choose the layout to suit the work. Link the report in chat and briefly state the conclusion and next action.

For video, invoke `/video-communication` after completing the invoking skill's work. Supply the audience, inspected revision, destination, and the report payload supplied by the invoking skill. Keep the video package outside the worktree by default. Video creation does not authorize implementation, a branch, or additional publication. Distinguish observed behavior from proposed or hypothetical animation; label animation as illustration rather than test footage. Link the MP4 and any canonical local artifact in chat, using the invoking skill's ordinary closeout.

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
