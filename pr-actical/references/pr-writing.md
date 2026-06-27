# PR Writing Reference

## Title

Write a short outcome-focused title. Prefer verbs and user-visible effects over implementation mechanics.

Good patterns:

- `add course application status filtering`
- `fix duplicate enrollment sync jobs`
- `support draft invoice exports`
- `remove legacy auth fallback`

Avoid vague titles such as `updates`, `misc fixes`, or `work on feature`.

## New PR or Draft PR Body

Use the repository template when available. When no useful template exists, use this compact structure:

```markdown
## Summary
- ...
- ...

## Testing
- `command` - passed

## Notes
- ...
```

Include `Testing` only when tests were run or a passing result was directly observed. If tests were not run, omit `Testing` from the PR body and mention that only in the final chat response.

Good summary bullets group changes by theme rather than mirroring every commit. Explain what changed and why it matters.

Use `Notes` only for meaningful risks, follow-ups, migrations, screenshots that still need human review, or mismatches between `./plan.md` and the observed diff.

Never claim approvals, screenshots, deployments, passing CI, or test results that were not observed.

## Published PR Update Comment

For an already open non-draft PR, write a comment that logs the incremental change since the last pushed commit visible on the PR before this run.

Use this structure:

```markdown
## Update summary
- ...
- ...

## Testing
- `command` - passed

## Notes
- ...
```

Mention only the new change range. Do not restate the entire PR unless necessary for clarity. Include `Testing` only for commands run during this update.

## Template Handling

When a repo template has required headings or checklists:

- Preserve the headings that apply.
- Leave checklist items unchecked unless directly verified.
- Remove placeholder instructions when replacing them with real content.
- Do not invent issue links, screenshots, reviewers, approvals, or deployment notes.
- If the template asks for information not available from the branch, leave a brief `TODO` only when the section seems required.

## Using plan.md

When `./plan.md` exists, use it as intent context, not as proof. Useful material includes goals, acceptance criteria, risks, and rollout notes. The observed diff and command outputs are authoritative when they conflict with the plan.
