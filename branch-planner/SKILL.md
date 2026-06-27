---
name: branch-planner
description: "Guide feature, fix, refactor, and chore work from a rough idea to a scoped branch plan. Ask targeted questions, inspect repo conventions, suggest branch names, and write or update plan.md with a sequenced commit plan, commit message suggestions, validation, risks, and open questions."
argument-hint: "<idea or ticket>"
---

# Branch Planner

Use this skill when a change idea needs to be narrowed down before implementation.

## When to Use This Skill

- User has a rough feature, fix, refactor, or chore idea and wants a concrete plan
- User wants branch name suggestions based on repository conventions
- User wants a commit-by-commit rollout with commit message suggestions
- User wants a local `plan.md` written in the active workspace

## Workflow

1. Clarify the change until the scope is specific enough to plan.
   - Ask the minimum targeted questions needed to remove ambiguity.
   - Do not ask for anything already answered by the prompt or repo context.
2. Read the repo for conventions.
   - Inspect the current branch, recent branch names, recent commit subjects, and any planning docs or contributor guidance.
   - Follow a repo-specific planning template if one exists.
3. Draft branch options.
   - Suggest 3 branch names.
   - Match the repo's naming style when visible.
   - Default to `feature/`, `fix/`, `refactor/`, or `chore/` prefixes when no style is obvious.
4. Build a commit plan.
   - Break the work into small sequential commits.
   - Keep each commit focused on one logical change.
   - For every commit, include a detailed message suggestion, likely files or areas, and validation.
   - If a commit would be risky or too broad, split it further before writing the plan.
5. Write or update `plan.md`.
   - Use the workspace root unless the repo documents a different location.
   - Preserve any existing user notes in `plan.md` and update in place.
   - Follow [plan output template](./references/plan-template.md).
6. Finish with next actions.
   - Call out the recommended branch name.
   - Call out the first commit to make.
   - List remaining questions if the plan still depends on user input.

## Gotchas

- Do not invent files, dependencies, or repo conventions without checking the workspace.
- Do not combine unrelated cleanup into the plan.
- If the repo already defines branch naming or planning conventions, follow those instead of the defaults.
- If git is unavailable, still write a plan from the available workspace context and note the limitation.
- If the scope is still ambiguous after the minimum targeted questions, stop and ask before writing `plan.md`.