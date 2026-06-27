# Visual Components Reference

This skill uses Markdown patterns, not MDX components. Use these components in this preference order.

## Human Summary

Purpose: keep the reviewer engaged and oriented. Explain the work in normal language before tables and tasks.

Format: paragraphs, optionally followed by a compact snapshot table.

## Decision Log

Purpose: expose the choices behind the plan so a junior-ish developer can review the reasoning and a code agent has fewer chances to wander.

Format: Markdown table with `Decision`, `Choice`, `Why`, and `Confidence`.

## Agent Task List with Stable IDs

Purpose: make the plan executable, trackable, resumable, and easy to reference.

Format: Markdown task list. Each task starts with a unique kebab-case ID in backticks.

## File Impact Matrix

Purpose: show likely scope and risk. Use confirmed paths only when known. Use areas/inspection targets when uncertain.

Format: Markdown table with `File / Area`, `Action`, `Purpose`, and `Risk`.

## Risk Matrix

Purpose: prevent reckless execution. Risks should influence task order, verification, and stop conditions.

Format: Markdown table with `Risk`, `Level`, `Why it matters`, and `Mitigation`.

## Test / Verification Plan

Purpose: define practical checks without overbuilding test requirements.

Format: grouped task lists for manual and automated checks. Use existing project test commands only when known.

## Acceptance Criteria

Purpose: define done in observable terms.

Format: Markdown checklist. Each item should be externally verifiable or directly inspectable.

## Restricted HTML Blocks

Purpose: hide supporting detail while keeping the main plan readable.

Allowed only:

```html
<details>
<summary>Additional context</summary>

Markdown content here.

</details>
```

Use for alternatives considered, extra background, or lower-priority context.

## Execution Map

Purpose: provide a quick visual sequence.

Format: simple Mermaid `flowchart TD`, short node labels, max 10 nodes by default.

## Architecture Sketch

Purpose: show proposed interaction between system parts.

Use when the plan has at least three interacting parts such as UI, API, service, database, middleware, jobs, or external systems.

## Sequence Diagram

Purpose: show runtime interactions over time.

Use only for auth, API, webhook, event, or request/response flows. Keep participant count low.

## Phase Timeline

Purpose: show the work breakdown in review-friendly chunks.

Markdown headings and task lists are the source of truth. Mermaid summaries are optional and should stay small.
