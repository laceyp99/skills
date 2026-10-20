# Local review record

Use for a local review whose findings may need implementation work, so the record can route back into `/assembly` or `/prelude`.

Write or update `review-findings.md` at the repository root using the Findings format, with a recommended `/assembly` task or `/prelude` question. Keep it untracked and never stage or commit it.

## Checkpoint quiz

After findings are gathered, and before finalizing the record, use `/checkpoint-quiz` to write a markdown quiz section into the very bottom of `review-findings.md`, after all findings, so the user can review the record and then test what they retained. Source questions from the highest-severity confirmed findings. Use decision-capture questions for unresolved User decision items; do not require user selection for None or Technical choice items unless they also depend on user intent. Confirm the user's selections with them and update the relevant Decision needed and Recommendation fields in `review-findings.md`.

In HTML report mode, deliver the quiz through `html.md` instead.
