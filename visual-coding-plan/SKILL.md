---
name: visual-coding-plan
description: create github-safe and vs-code-safe visual coding project plans in a single plan.md file. use when asked to plan a coding project, prepare work for a code agent, turn an issue or feature request into an executable implementation plan, or make a plan more visually readable without mdx. outputs structured markdown with human summaries, decision logs, stable task ids, file impact matrices, risk matrices, verification plans, acceptance criteria, restricted details/summary html, and simple mermaid diagrams when they clarify the work.
---

# Visual Coding Plan

## Purpose

Create a single `plan.md` that is readable in plain Markdown, helpful in GitHub or VS Code previews, and executable by a coding agent. Favor structured Markdown as the source of truth. Use Mermaid and restricted HTML only as safe visual enhancements.

## Output Contract

Always produce one Markdown file named or formatted as `plan.md` unless the user explicitly asks otherwise.

The plan must prioritize, in this order:
1. Human summary and narrative reviewability.
2. Visual overview for fast review.
3. Decision log.
4. Risk matrix.
5. Agent task list with stable IDs.
6. Phase implementation plan.
7. File impact matrix.
8. Test/verification plan.
9. Acceptance criteria.
10. Restricted HTML blocks.

Do not create MDX. Do not use custom JSX components. Do not rely on a custom renderer. The plan must remain useful if Mermaid does not render and if HTML collapsibles are displayed as plain markup.

## Workflow

1. Determine the planning target from the user request, issue, repo context, or provided notes.
2. If repo context is available, inspect enough to avoid inventing file paths, frameworks, or commands. If repo context is not available, mark uncertain details in `Unknowns to Resolve First` instead of guessing.
3. Draft `plan.md` using the required section order below.
4. Add visual enhancements only when they clarify execution:
   - Use Markdown tables for snapshots, decisions, files, and risks.
   - Use Mermaid `flowchart TD` for one simple execution map when useful.
   - Use Mermaid architecture or sequence diagrams only for multi-part systems or request/response flows.
   - Use restricted HTML only for `<details>` and `<summary>` collapsible context.
5. Review the plan against the self-check checklist before finalizing.

## Required Section Order

Use this section order by default. Omit optional diagram sections only when they do not help or would be misleading.

```markdown
# Plan: {{title}}

## Human Summary

## Visual Overview

### Execution Map

### Architecture Sketch

### Sequence Diagram

## Decision Log

## Risk Matrix

## Agent Task List

## Phase Implementation Plan

## File Impact Matrix

## Test / Verification Plan

## Acceptance Criteria

## Assumptions and Unknowns

## Stop Conditions

## Agent Handoff Prompt

## Additional Context
```

### Human Summary

Write a plain-language narrative for Pat as a junior-ish developer reviewing the plan before handing it to a code agent. Explain what will happen, why the order matters, and what to watch for. Keep it concise but engaging.

### Decision Log

Use a Markdown table. Include meaningful choices only; do not invent fake decisions.

```markdown
| Decision | Choice | Why | Confidence |
|---|---|---|---|
| {{decision}} | {{chosen approach}} | {{reason}} | High/Medium/Low |
```

If no meaningful decisions are known yet, include a short note: `No major implementation decisions are locked yet; resolve the unknowns first.`

### Visual Overview

Place review-helpful visuals near the top of the plan so they orient the human reviewer before the detailed task tables. Use this section for a compact execution map and, when useful, architecture or sequence diagrams.

Keep the visuals summarizing the plan, not replacing it. The executable source of truth remains the Markdown task list, phase plan, risk matrix, verification plan, and acceptance criteria.

### Risk Matrix

Use a Markdown table with practical mitigations. Put risks before the task list so they can shape execution order, stop conditions, and verification.

```markdown
| Risk | Level | Why it matters | Mitigation |
|---|---|---|---|
| {{risk}} | High/Medium/Low | {{impact}} | {{specific mitigation}} |
```

### Agent Task List

Every actionable task must have a stable, unique, kebab-case ID in backticks. Tasks should be ordered for execution.

```markdown
- [ ] `inspect-routing` Identify the current routing structure before editing.
- [ ] `inspect-auth-patterns` Check for existing auth/session utilities.
- [ ] `implement-login-ui` Create or update the login UI.
```

Good task IDs are short, durable, and action-oriented. Avoid vague tasks like `fix-stuff` or `update-code`.

Tasks should be ordered enough to guide execution, but do not turn the task list into a commit-by-commit script unless the user explicitly asks for that level of control. Preserve room for the executing agent to inspect the codebase, follow local patterns, and adjust file-level details while keeping the plan's intent.

### Phase Implementation Plan

Use phases to balance structure with agent judgment. Each phase should define:

- `Goal`: what this phase is trying to accomplish.
- `Likely work`: stable-ID tasks that are expected but may adjust after inspection.
- `Expected outcome`: what should be true when the phase is complete.
- `Flexibility`: what the agent may adapt without asking for review.

```markdown
### Phase 1: Inspect and Confirm Direction

Goal: Verify the repo facts that the plan depends on.

Likely work:
- [ ] `inspect-current-flow` Confirm the relevant files, routes, data flow, or APIs.
- [ ] `confirm-existing-patterns` Identify existing helpers, conventions, and test commands.

Expected outcome:
The agent knows whether the proposed path still fits the codebase.

Flexibility:
The agent may adjust later tasks if inspection finds a better existing pattern.
```

Do not prescribe exact commits, exact file edits, or rigid sequencing unless those details are confirmed and necessary. A fully flooded commit plan belongs in a stricter planning workflow; this skill should usually create an intent-driven implementation plan.

### File Impact Matrix

Use a Markdown table. If files are known, list paths. If files are uncertain, list areas or inspection targets and say they are unconfirmed.

```markdown
| File / Area | Action | Purpose | Risk |
|---|---|---|---|
| `src/example.ts` | Modify | {{purpose}} | Medium |
| Routing layer | Inspect | Confirm where protected routes are defined | Medium |
```

Actions should usually be `Inspect`, `Create`, `Modify`, `Delete`, `Move`, or `Unknown`.

### Test / Verification Plan

Keep verification proportional. Do not require new test infrastructure unless the task warrants it or the repo already has tests.

Separate checks when helpful:

```markdown
### Manual Checks

- [ ] `verify-ui-loads` Visit the affected page and confirm it loads.

### Automated Checks

- [ ] `verify-existing-tests` Run the existing relevant test command if present.
```

### Acceptance Criteria

Use observable done conditions, not vague claims.

Good:
```markdown
- [ ] Unauthenticated users are redirected to `/login` when visiting protected routes.
```

Avoid:
```markdown
- [ ] Auth works.
```

### Assumptions and Unknowns

Separate assumptions from unknowns. Unknowns that must be resolved before implementation should become tasks or stop conditions.

```markdown
### Assumptions

- {{assumption}}

### Unknowns to Resolve First

- [ ] `unknown-existing-auth` Check whether an auth provider already exists.
```

### Stop Conditions

Include conditions where the executing agent should pause rather than improvise.

```markdown
Stop and ask for review if:

- Existing infrastructure conflicts with this plan.
- The work requires a schema migration not covered here.
- The expected files or framework are not present.
```

### Agent Handoff Prompt

End with a short prompt another coding agent can follow.

```markdown
Execute this plan phase by phase. Start by resolving unknowns, then complete tasks in order. Do not skip the acceptance criteria or verification plan. If a stop condition is hit, pause and report the finding before continuing.
```

## Visual Enhancement Rules

### Restricted HTML

Allowed HTML:
- `<details>`
- `<summary>`

Use it only for collapsible supporting information such as alternatives considered, extra notes, or lower-priority context.

```markdown
<details>
<summary>Alternatives considered</summary>

- Option A: {{description}}
- Option B: {{description}}

</details>
```

Banned HTML:
- inline styles
- scripts
- iframes
- custom classes
- arbitrary layout divs
- custom web components

### Mermaid Execution Map

Use at most one default execution map. Prefer `flowchart TD`. Keep labels short. Maximum 10 nodes unless the user asks for more detail.

````markdown
```mermaid
flowchart TD
  A[Inspect current state] --> B[Confirm implementation path]
  B --> C[Make smallest coherent change]
  C --> D[Verify behavior]
  D --> E[Handoff results]
```
````

Avoid long file paths, backticks, quotes, braces, parentheses, and punctuation-heavy labels inside Mermaid nodes. Put detailed file paths in tables, not diagrams.

### Architecture Sketch

Include only when the task involves at least three interacting parts. Label uncertain architecture as proposed.

````markdown
```mermaid
flowchart LR
  UI[UI] --> API[API route]
  API --> Service[Service layer]
  Service --> Data[Data store]
```
````

### Sequence Diagram

Include only for request/response, webhook, auth, event, or multi-system flows. Keep participants to 5 or fewer.

````markdown
```mermaid
sequenceDiagram
  participant User
  participant UI
  participant API
  participant Service

  User->>UI: Submit request
  UI->>API: Send request
  API->>Service: Run operation
  Service-->>API: Return result
  API-->>UI: Return response
```
````

### Phase Implementation Plan

Use Markdown as the source of truth. Keep phases open enough for task completion and repo-aware judgment, but specific enough that the agent understands the intended order and expected outcomes. Add a very small Mermaid phase summary only if it clarifies the plan. Do not use Gantt charts by default.

## Simplicity and Fallback Rules

- If a visual element risks becoming brittle, use a Markdown table or list instead.
- If Mermaid syntax becomes complex, simplify or remove the diagram.
- If repo facts are unknown, say so and make inspection the first task.
- Never let visuals replace the actionable Markdown plan.
- Keep the plan readable if all diagrams fail to render.

## Self-Check Before Finalizing

Before finalizing, verify:

- The plan is a single `plan.md`-style Markdown output.
- No MDX, JSX, imports, or custom components are present.
- Every actionable task has a unique stable ID.
- The Human Summary explains the work and order clearly.
- The Visual Overview appears near the top when diagrams help review.
- The Decision Log includes real decisions or explicitly says none are locked.
- The Risk Matrix appears before execution tasks and includes specific mitigations.
- The Phase Implementation Plan defines goals, likely work, expected outcomes, and flexibility boundaries without becoming a commit script.
- The File Impact Matrix distinguishes confirmed files from uncertain areas.
- The Verification Plan is proportional to the work.
- Acceptance Criteria are observable.
- Stop Conditions are included.
- HTML, if present, is limited to `<details>` and `<summary>`.
- Mermaid diagrams, if present, have short labels and simple syntax.
- The plan remains useful as plain Markdown.

## References

Load these references only when useful:

- `references/plan-template.md` for the complete reusable plan skeleton.
- `references/visual-components.md` for component-by-component guidance and examples.
- `references/anti-patterns.md` for common failure modes to avoid.
