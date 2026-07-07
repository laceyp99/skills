---
name: assembly
description: Execute a local plan.md, commit plan, phase plan, or step-by-step implementation plan in controlled units. Use when the user asks to read or implement a local plan, walk through a commit plan one unit at a time, implement changes phase by phase, validate after each unit, make commits from a plan, leave planning artifacts uncommitted, or continue from a previous plan unit.
---

# Assembly

Use this skill to turn a local implementation plan into small, inspectable work units. Work from facts first, preserve the user's worktree, and keep planning artifacts out of commits unless the user explicitly says otherwise.

## Initial Inspection

Before editing, inspect the repository state:

```powershell
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git diff --stat
git diff --cached --stat
```

Read `plan.md` fully before making changes. If the user names another plan file, read that file fully instead. Identify planning artifacts that must remain uncommitted by default, including `plan.md`, `HANDOFF.md`, `Priority Ladder.md`, and scratch or review markdown files.

If `plan.md` is missing, internally contradictory, or impossible to map into work units, stop and ask for direction.

## Determine Mode

Use the user's current request to choose the mode.

- **Hand Holding mode**: Use when the user asks to implement or walk through the plan together. If the user doesn't explicitly ask for commits, assume this mode of implementation.
- **Autopilot mode**: Use only when the user explicitly asks the agent to make commits or walk the commit plan autonomously. Stop right before pushing the local branch for the user to review, unless the user explicitly asks for it.

Treat plan commit entries as logical work boundaries in both modes. Do not run `git commit` in hand holding mode, even if the plan contains commit messages; just pass those onto the user.

## Build the Checklist

Extract the commit plan, phase list, or ordered task list from the plan into a working checklist. Keep the checklist in the conversation unless editing the plan file is appropriate.

You may update plan markdown files only for checkbox/status tracking and date entries. Do not alter the plan text, scope, task definitions, or acceptance criteria without explicit user direction. Keep any plan markdown changes out of commits by default.

## Hand Holding Mode

In hand holding mode, complete exactly one logical unit, then pause for user review to commit.

For the selected unit:

1. Confirm the unit being attempted.
2. Make the source, test, and documentation changes that satisfy the unit.
3. Run relevant validation, discovering repo scripts first.
4. Leave code changes unstaged by default so the user can inspect and selectively stage them.
5. Report changed files, validation results, remaining risks, and a suggested conventional commit message.
6. Stop and wait for the user before starting the next unit.

If plan status/date updates are made, keep them separate from source changes and explicitly mention that they should remain uncommitted unless the user wants otherwise.

## Autopilot Mode

In autopilot mode, work through plan units autonomously until the plan is complete or a blocker appears.

For each unit:

1. Implement one logical unit.
2. Run the narrowest relevant validation available from repo scripts.
3. Broaden validation when the unit touches shared behavior, public interfaces, packaging, CI, or cross-cutting code.
4. Stage only intended source, test, and documentation files; no planning artifacts.
5. Inspect the staged diff before committing.
6. Commit the unit with the repo's conventional commit style or the user's preferred style.
7. Continue to the next unit only after validation passes and the commit is made.

Never commit `plan.md`, `HANDOFF.md`, `Priority Ladder.md`, or scratch/review markdown files unless the user explicitly asks to include them. Do not commit a unit with failing validation unless the user explicitly overrides.

## Validation

Prefer the repo's documented scripts over ad hoc commands. For Python, prefer direct interpreters such as `.venv\Scripts\python.exe -m pytest`, `py -3.12 -m pytest`, or the repo-documented command.

If validation fails, fix obvious root causes and rerun with a changed approach. Do not repeatedly retry the same failing command without new information. Stop and report if the failure is unclear, caused by unrelated worktree changes, or requires a risky assumption.

## Stop Conditions

Stop and report instead of guessing when:

- The plan is missing, contradictory, stale, or does not match the repository.
- The working tree contains unrelated changes that conflict with the plan.
- Required validation fails and the fix is not clear.
- A rebase, pull, merge, or cherry-pick conflict appears.
- The next unit depends on a decision the user has not made.
- A tool is unavailable due to auth, sandbox, network, or environment issues.

## Final Response

End with a concise status report:

- Plan units completed.
- Commits made, if any.
- Files changed.
- Validation commands run and whether they passed.
- Planning artifacts or other files intentionally left uncommitted.
- Remaining risks, blockers, or manual checks.
