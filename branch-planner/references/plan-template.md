# Plan Output Template

Use this structure for the generated `plan.md` unless the repository documents a stricter one.

## Goal

State the change in one sentence.

## Context

Summarize the current problem, relevant repo conventions, and any assumptions.

## Branch Name Suggestions

- `feature/...` - when the work adds user-facing behavior
- `fix/...` - when the work corrects a bug
- `refactor/...` - when the work changes structure without changing behavior
- `chore/...` - when the work is maintenance or tooling

## Recommended Branch

Include one preferred branch name and a short reason.

## Scope

List the in-scope changes.

## Non-Goals

List anything explicitly excluded.

## Commit Plan

Use one numbered subsection per commit.

### Commit 1

- **Goal:** What this commit accomplishes
- **Suggested commit message:**
  - **Subject:** `type(scope): concise summary` or a repo-appropriate imperative subject
  - **Body:** Add a few lines explaining the why, the main files, and any verification
- **Files / areas:** Likely files or subsystems touched
- **Validation:** The cheapest check that should pass after this commit
- **Notes:** Risks, follow-ups, or why this commit stands alone

### Commit 2

- Repeat the same structure for the next step.

## Validation

List the checks that should pass before the branch is considered ready.

## Risks and Open Questions

List assumptions, unknowns, and items needing confirmation.

## Definition of Done

Describe the conditions that make the branch ready to implement.