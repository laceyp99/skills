---
name: assembly
description: Execute a local plan.md, commit plan, phase plan, or step-by-step implementation plan in controlled units. Use when the user asks to read or implement a local plan, walk through a commit plan one unit at a time, implement changes phase by phase, validate after each unit, make commits from a plan, leave planning artifacts uncommitted, continue from a previous plan unit, or autonomously deliver completed work as a GitHub draft pull request.
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

Read `plan.md` or `decisions.md` files fully before making changes, if they exist. Identify planning artifacts that must remain uncommitted by default, including `plan.md`, `decisions.md`, or another scratch or review markdown files.

If `plan.md` is missing, ensure you have enough conversational context to change intent map into work units, if not, stop and ask clarifying questions for direction.

## Determine Mode

Use the user's current request to choose the mode.

- **Hand Holding mode**: Use when the user asks to implement or walk through the plan together. If the user doesn't explicitly ask for commits, assume this mode of implementation.
- **Autopilot mode**: Use only when the user explicitly asks the agent to make commits, walk the commit plan autonomously, or run in autopilot. Complete the plan, commit its units, then use the `pr-actical` workflow to push the branch and create or update a GitHub draft pull request for the user's final pass.

Treat plan commit entries as logical work boundaries in both modes. Do not run `git commit` in hand holding mode, even if the plan contains commit messages; just pass those onto the user.

Selecting autopilot authorizes ordinary commits, a normal push of the current non-default branch, and creation or update of a draft pull request. It does not authorize publishing the PR as ready for review, force-pushing, rewriting history, resolving synchronization conflicts, or bypassing `pr-actical` safety checks.

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

Never commit `plan.md`, `decisions.md`, or another scratch/review markdown file unless the user explicitly asks to include them. Do not commit a unit with failing validation unless the user explicitly overrides.

### Autopilot delivery

After the final plan unit is validated and committed:

1. Confirm there are no intended source, test, or documentation changes left uncommitted.
2. Load and follow the complete `pr-actical` skill workflow. Do not duplicate or weaken its branch, authentication, synchronization, testing, push, or pull-request safeguards.
3. Create or update a draft pull request and leave it as a draft for the user's final pass. Never mark it ready for review.
4. If `pr-actical` refuses because the repository is unsafe or not ready to publish, keep the completed local commits intact and report the exact blocker and safest next action.
5. If `pr-actical` is unavailable, finish the local implementation and commits, stop before pushing, and tell the user that draft-PR delivery requires that skill.

The publication phase is part of autopilot's normal completion target; do not request a second confirmation before an ordinary push or draft-PR operation. Hand holding mode does not inherit this authorization and must only transition to `pr-actical` if the user requested to.

In hand holding mode, the final report after the plan is complete is the implementation handoff. Do not create per-unit report artifacts. If the user wants behavioral validation, they may invoke `/gauntlet`; if they want publication, they may invoke `/pr-actical` in the same session or later from the same branch. The final report should give those next skills the changed files, validation already run, remaining risks, and the intended next action.

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
- Draft PR URL and base/head branches, when autopilot delivery succeeds.
- Remaining risks, blockers, or manual checks.
