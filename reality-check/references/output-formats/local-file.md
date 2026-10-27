# Local review record

Use for a local review whose findings may need implementation work, so the record can route back into `/assembly` or `/prelude`.

Write or update repository-root `artifacts/review-findings.md` by default using the full Findings format, including Necessity and Reproduction/evidence. Include unresolved concerns, relevant out-of-scope follow-ups, review coverage and limits, and a recommended `/assembly` task or `/prelude` question. Keep generated records ignored and untracked; never stage or commit them.

## Checkpoint quiz

Automatically use `/checkpoint-quiz` to write a markdown quiz section at the very bottom of `review-findings.md`, after the complete review and recommended next action. Preserve findings, useful evidence, unresolved concerns, coverage, and limits before the quiz so the user can skim the report and then test understanding. Source questions from the highest-severity confirmed findings. Use decision-capture questions for unresolved User decision items; do not require user selection for None or Technical choice items unless they also depend on user intent. Comprehension is self-graded and does not gate the report. Confirm any decision-capture selections with the user before updating the relevant Decision needed and Recommendation fields in `review-findings.md`.

In HTML report mode, use `/checkpoint-quiz` HTML report mode to bake an interactive quiz into the bottom of the report instead (see `html.md`).
