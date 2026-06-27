# Visual Components Reference

This skill uses Markdown patterns, not MDX components. Use these components in this preference order.

## Human Summary

Purpose: keep the reviewer engaged and oriented. Explain the work in normal language before tables and tasks.

Format: paragraphs, optionally followed by a compact snapshot table.

## Visual Overview

Purpose: make diagrams part of the review path instead of appendix material. Use this section immediately after the Human Summary when visuals help the reviewer understand flow, architecture, or runtime interactions.

Format: optional subsections for Execution Map, Architecture Sketch, and Sequence Diagram. Keep diagrams compact and summarize the Markdown plan rather than replacing it.

## Decision Log

Purpose: expose the choices behind the plan so a junior-ish developer can review the reasoning and a code agent has fewer chances to wander.

Format: Markdown table with `Decision`, `Choice`, `Why`, and `Confidence`.

## Risk Matrix

Purpose: prevent reckless execution and help the human reviewer judge the plan before reading implementation tasks. Risks should influence task order, verification, and stop conditions.

Format: Markdown table with `Risk`, `Level`, `Why it matters`, and `Mitigation`.

## Agent Task List with Stable IDs

Purpose: make the plan executable, trackable, resumable, and easy to reference.

Format: Markdown task list. Each task starts with a unique kebab-case ID in backticks.

Keep tasks ordered enough to guide execution, but do not turn them into a commit-by-commit script unless the user explicitly asks for strict commit planning.

## Phase Implementation Plan

Purpose: provide a review-friendly implementation path while preserving room for repo-aware judgment.

Format: Markdown phase sections with `Goal`, `Likely work`, `Expected outcome`, and `Flexibility`.

Use `Likely work` for stable-ID tasks that are expected but may adapt after inspection. Use `Flexibility` to say what the executing agent may adjust without asking for review.

## File Impact Matrix

Purpose: show likely scope and risk. Use confirmed paths only when known. Use areas/inspection targets when uncertain.

Format: Markdown table with `File / Area`, `Action`, `Purpose`, and `Risk`.

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

## Phase Implementation Plan Diagrams

Purpose: optionally summarize the phase breakdown visually.

Markdown phase sections are the source of truth. Mermaid summaries are optional and should stay small. Do not use Gantt charts by default.
