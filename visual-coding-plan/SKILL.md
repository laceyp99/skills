---
name: visual-coding-plan
description: Create GitHub-safe and VS Code-safe visual coding project plans in a single plan.md file. Use when asked to plan a coding project, prepare work for a code agent, turn an understood issue or feature request into an executable implementation plan, or make planning notes visually readable without MDX. Do not use for read-only root-cause investigation before the problem is understood; use prelude first. Do not use to execute an existing plan; use assembly.
---

# Visual Coding Plan

## Purpose

Create one `plan.md`-style Markdown artifact that a human can review and a coding agent can execute. Keep Markdown as the source of truth. Use Mermaid diagrams and `<details>/<summary>` only as optional review aids.

## Discovery Boundary

Use this skill when the expected output is a planning artifact. If the user is still trying to understand whether an issue is real, where a bug lives, or which solution path is right, use `prelude` before writing a plan. If the user asks to implement an existing plan, use `assembly`. If the user asks for a code review, use `reality-check`.

If the user asks for both investigation and a plan, investigate enough to avoid inventing facts, then produce the plan only after the problem and direction are reasonably understood. Put unresolved facts in `Assumptions and Unknowns` and make them early tasks or stop conditions.

## Core Contract

- Produce one plain Markdown plan named or formatted as `plan.md` unless the user asks otherwise.
- Do not create MDX, JSX, custom components, custom classes, inline styles, scripts, iframes, or renderer-specific markup.
- Preserve usefulness when Mermaid or HTML collapsibles do not render.
- Inspect repo context when available before naming files, frameworks, routes, commands, or test tools.
- Mark uncertain details as unknowns instead of guessing.
- Give every actionable task a stable, unique, kebab-case ID in backticks.
- Keep verification proportional to risk and existing project tooling.
- Include stop conditions that tell the executing agent when to pause instead of improvising.

## Workflow

1. Determine the planning target from the user request, issue, repo context, or notes.
2. Inspect enough repository context to avoid hallucinated file paths, commands, architecture, or acceptance criteria.
3. Decide whether supporting references are needed:
   - Load `references/plan-template.md` when a reusable skeleton would speed up drafting or when the user asks for a full plan structure.
   - Load `references/visual-components.md` when section formatting, examples, task structure, phase wrapping, or diagram choices need more detail.
   - Load `references/anti-patterns.md` before finalizing complex plans, plans with diagrams, or plans that risk becoming renderer-dependent.
4. Draft the plan using the required section order.
5. Add visuals only when they clarify execution or review.
6. Run a final quality pass against the core contract and anti-patterns before returning the plan.

## Required Section Order

Use this order by default. Omit optional diagram subsections only when they do not help or would be misleading.

1. `# Plan: {{title}}`
2. `## Human Summary`
3. `## Visual Overview`
4. `### Execution Map`
5. `### Architecture Sketch`
6. `### Sequence Diagram`
7. `## Decision Log`
8. `## Risk Matrix`
9. `## Agent Task List`
10. `## Phase Implementation Plan`
11. `## File Impact Matrix`
12. `## Test / Verification Plan`
13. `## Acceptance Criteria`
14. `## Assumptions and Unknowns`
15. `## Stop Conditions`
16. `## Additional Context`

## Decision Rules and Constraints

- Put a concise human narrative before tables and task lists.
- Include real decisions only. If no decisions are locked, say so and identify what must be resolved first.
- Put risks before execution tasks so risk shapes sequencing and verification.
- Use confirmed file paths only when repo evidence supports them. Otherwise list areas such as `Routing layer` or `Auth utilities`.
- Use phases to express intent, expected outcome, and flexibility. Do not turn the plan into a rigid commit script unless the user explicitly asks for commit-level planning.
- Use Mermaid sparingly: one compact `flowchart TD` execution map by default, architecture sketches only for multi-part systems, and sequence diagrams only for runtime interactions.
- Keep Mermaid labels short and free of long paths, backticks, quotes, braces, and punctuation-heavy text.
- Use `<details>` blocks only for supporting context such as alternatives considered. Do not hide primary tasks, risks, acceptance criteria, or stop conditions in collapsibles.
- Do not include a separate `Agent Handoff Prompt` section by default. Put execution guidance in the phase plan, stop conditions, and acceptance criteria.

## Reference Routing

`references/plan-template.md` contains the reusable skeleton. Read it when the user wants a full plan artifact or when starting from a blank `plan.md`.

`references/visual-components.md` contains detailed guidance and examples for each plan section. Read it when the plan needs richer task shaping, diagram choice, tables, phase wrapping, or acceptance criteria.

`references/anti-patterns.md` contains the quality checklist and common failure modes. Read it when the plan is large, visually complex, uncertain, or likely to be handed to another agent for execution.
