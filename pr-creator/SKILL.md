---
name: pr-creator
description: "Prepare a branch for pull request review. Inspect the current branch, compare it to the base branch, summarize the commit range, follow any repo PR template, and write or update PR.md with a suggested title, description, testing notes, and checklist."
argument-hint: "[base branch or issue]"
---

# PR Creator

Use this skill when the branch is ready to be turned into a pull request draft.

## When to Use This Skill

- User wants a PR title and description for the current branch
- User wants a draft that reflects the commits and diff already on the branch
- User wants the draft to follow a repository PR template when one exists
- User wants a local `PR.md` file ready for review or paste into GitHub

## Workflow

1. Identify the PR scope.
   - Read the current branch and infer the base branch from repo defaults or local config.
   - Collect the commits that belong to the branch.
   - If the branch range is unclear, ask before drafting.
2. Summarize the changes.
   - Review commit subjects, diff stats, and the full diff when needed.
   - Group the changes by theme instead of repeating every commit verbatim.
   - Do not claim tests or approvals that were not actually observed.
3. Find repo PR guidance.
   - Look for `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/*`, or other documented PR instructions.
   - If multiple templates exist, choose the closest match for the current change.
   - Preserve required headings and checklist items.
4. Draft `PR.md`.
   - Write a concise title that reflects the change outcome.
   - Explain what changed, why it changed, and how it was verified.
   - Include risks, follow-ups, screenshots, or migration notes when relevant.
   - Follow [PR output template](./references/pr-template.md) or mirror the repo template when one exists.
5. Save the draft in the workspace.
   - Use the workspace root unless the repo says otherwise.
   - Preserve existing user edits in `PR.md` and update the draft in place.
6. Finish with a short summary.
   - Mention the suggested title, base branch, and any template sections that still need user input.

## Gotchas

- Use the merge base or repo default branch for scope, not the entire git history.
- Ignore unrelated local changes unless the user explicitly wants them included.
- If the repo has a PR template with required checkboxes or headings, keep them intact.
- If tests were not run, say so clearly.
- Do not fabricate links, screenshots, or approvals.