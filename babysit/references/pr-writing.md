# PR Writing Reference

Read when composing a PR title, body, template-based publication, or
incremental update comment.

## Title

Write a short outcome-focused title. Prefer verbs and user-visible effects over
implementation mechanics. Avoid vague titles such as `updates`, `misc fixes`,
or `work on feature`.

## Body

Use the repository template when available. When no useful template exists:

```markdown
## Summary
- ...
- ...

## Testing
- `command` - passed

## Notes
- ...
```

Include `Testing` only when tests were run or a passing result was directly
observed. Use `Notes` for meaningful risks, follow-ups, migrations, screenshots
that still need human review, or plan/diff mismatches. Never claim approvals,
screenshots, deployments, passing CI, or test results that were not observed.

For an already open PR, an update comment should describe only the incremental
change since the last pushed commit visible on the PR:

```markdown
## Update summary
- ...
- ...

## Testing
- `command` - passed

## Notes
- ...
```

## Templates and plans

Preserve applicable template headings and leave checklist items unchecked unless
directly verified. Remove placeholder instructions when replacing them with
real content; do not invent issue links, screenshots, reviewers, approvals, or
deployment notes. If `plan.md` exists, use it as intent context, not proof;
the observed diff and command output win when they conflict.
