# HTML report

Perform the review and use `/html-communication` to create a local HTML report as the main reader-facing result. Use the full Findings format, making severity, necessity, fix complexity, decision needs, reproduction evidence, review scope and limits, and the next action easy to inspect. Place concise expected-versus-observed proof beside each finding; use screenshots, short recordings, or test output when they clarify it, with lengthy artifacts linked. Choose visuals or interaction to suit the reviewed change; do not impose a fixed layout. Keep `review-findings.md`, or PR comments when the user asked for them, as the actionable record.

Automatically use `/checkpoint-quiz` HTML report mode to bake an interactive quiz into the bottom of the report, after the complete findings, evidence, unresolved concerns, coverage and limits, and next action. The quiz supplements the review content. Use it instead of a markdown quiz in `review-findings.md`; source questions as in `local-file.md`.

Put the review conclusion and next action in the report. In chat, link its saved file without repeating inline findings; for file-only delivery, briefly state the conclusion and next action.
