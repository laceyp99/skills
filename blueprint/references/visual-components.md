# Visual Components Reference

Use this file when a `plan.md` needs richer section guidance than the core skill provides. Keep the final plan in plain Markdown. Do not copy every example blindly; adapt the smallest useful pattern.

## Contents

- Human Summary
- Visual Overview
- Phase Implementation Plan
- File Impact Matrix
- Test / Verification Plan
- Acceptance Criteria
- Unknowns to Resolve
- Stop Conditions
- Additional Context
- Restricted HTML Blocks

## Human Summary

Purpose: orient the reviewer before tables and tasks. Explain the goal, the intended implementation shape, why the order matters, and what to watch for.

Format: short paragraphs, optionally followed by a compact snapshot table.

## Visual Overview

Purpose: make useful architecture and runtime relationships part of the review path instead of appendix material. Include an architecture sketch, a sequence diagram, both, or neither. Omit visuals when they would be trivial or misleading.

Use architecture sketches when multiple meaningful parts interact, such as UI, API, service, worker, data store, or an external system. Use sequence diagrams for request/response, webhook, auth, event, or other time-ordered flows. Keep diagrams compact and let Markdown tasks remain the source of truth.

## Phase Implementation Plan

Purpose: provide an implementation path with a clear goal, concrete work, an observable completion boundary, and conditions that require review.


Keep the phase heading visible, then wrap the detailed phase body in `<details>/<summary>` so the plan stays scannable in GitHub and VS Code. Put the phase goal in the summary. Keep critical tasks visible inside the wrapped block, not hidden elsewhere.

```markdown
### Phase 1: Inspect and Confirm Direction

<details>
<summary>Goal: Verify the repo facts that the plan depends on.</summary>.

**Tasks:**
- [ ] `inspect-current-flow` Confirm the relevant files, routes, data flow, or APIs.
  - Follow an equivalent existing repository pattern if its location differs from the expected area.
- [ ] `confirm-existing-patterns` Identify existing helpers, conventions, and test commands.

**Done when:**
- The relevant implementation path and existing project conventions are confirmed.

**Pause if:**
- The expected framework, routes, or package tooling are not present.

**Implementation notes:**
Account for any repository-specific constraint that affects later phases.
</details>
```

Put meaningful flexibility beneath the specific task it affects rather than in a separate phase-level section. `Implementation notes` is an optional aside for useful constraints or context that do not belong in the task list; omit it when it adds no value.

## File Impact Matrix

Purpose: show likely scope and risk. Use confirmed paths only when known. Use areas/inspection targets when uncertain.

```markdown
| File / Area | Action | Purpose | Risk |
|---|---|---|---|
| `src/example.ts` | Modify | {{purpose}} | Medium |
| Routing layer | Inspect | Confirm where protected routes are defined | Medium |
```

Actions should usually be `Inspect`, `Create`, `Modify`, `Delete`, `Move`, or `Unknown`.

## Test / Verification Plan

Purpose: define practical checks without overbuilding test requirements.

```markdown
### Manual Checks

- [ ] `verify-ui-loads` Visit the affected page and confirm it loads.

### Automated Checks

- [ ] `verify-existing-tests` Run the existing relevant test command if present.
```

## Acceptance Criteria

Purpose: define observable done conditions.

Good:

```markdown
- [ ] Unauthenticated users are redirected to `/login` when visiting protected routes.
```

Avoid:

```markdown
- [ ] Auth works.
```

## Unknowns to Resolve

Purpose: identify facts that must be resolved before or during implementation.

```markdown
- [ ] `unknown-existing-auth` Check whether an auth provider already exists.
```

Unknowns that block implementation should become early tasks or stop conditions.

## Stop Conditions

Purpose: tell the executing agent when to pause instead of guessing.

```markdown
Stop and ask for review if:

- Existing infrastructure conflicts with this plan.
- The work requires a schema migration not covered here.
- The expected files or framework are not present.
```

## Additional Context

Purpose: preserve relevant references, history, constraints, or alternatives that support review or execution but do not belong in the primary plan sections. Omit this section when no useful supporting context exists.

## Restricted HTML Blocks

Use `<details>` and `<summary>` only for supporting context, such as alternatives considered or lower-priority notes.

```html
<details>
<summary>Additional context</summary>

Markdown content here.

</details>
```
