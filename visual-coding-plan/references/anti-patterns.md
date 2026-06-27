# Anti-Patterns

Avoid these patterns when creating visual coding plans.

## Do not use MDX or JSX

Bad:

```mdx
<PlanCard status="planned" />
```

Use Markdown tables and lists instead.

## Do not invent renderer support

Do not assume custom CSS, classes, components, plugins, or Markdown extensions beyond common GitHub/VS Code-friendly Markdown, Mermaid, and `<details>/<summary>`.

## Do not let diagrams become the plan

Mermaid diagrams are summaries. The actionable plan must remain in Markdown lists, tables, and acceptance criteria.

## Do not put long file paths in Mermaid nodes

Bad:

```mermaid
flowchart TD
  A[Modify `src/app/(dashboard)/settings/profile/page.tsx` to add validation] --> B[Run tests]
```

Use short labels in diagrams and put paths in the File Impact Matrix.

## Do not over-test by default

Do not require new testing infrastructure unless the project already has it or the work is high-risk enough to justify it.

## Do not hide critical tasks in collapsible HTML

`<details>` blocks are for supporting context, not primary execution steps.

## Do not pretend uncertain files are confirmed

If repo context is missing, say `Routing layer` or `Auth utilities` instead of inventing paths.

## Do not omit stop conditions

Agent-executable plans need clear pause points when reality diverges from the plan.
