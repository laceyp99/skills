---
name: gauntlet
description: Review a code patch or pull request by inspecting its diff, running read-only automated sanity checks, designing risk-based human validation, and interactively grilling the user through manual testing while maintaining a local review.md record. Use when given a PR number, branch name, or both and asked to validate that changes work beyond lint/tests, especially for UI, device-specific, interactive, environment-sensitive, integration, persistence, or other behavior where human observation adds confidence. Intended for coding-agent environments with shell access.
---

# Gauntlet

Validate patches without becoming the patch author. Treat automated checks as the mechanical baseline, then use the human to establish behavioral confidence where direct observation is more valuable.

Maintain `review.md` at the repository root as the review source of truth. Keep it local and untracked by default. Read [references/review-template.md](references/review-template.md) before creating or restructuring it.

## Non-negotiable boundaries

- Remain read-only with respect to the patch and committed project files. Never fix, refactor, format, rewrite, stage, commit, or otherwise modify the reviewed code.
- Permit writing only to `review.md` for this workflow. Treat caches or test artifacts produced incidentally by normal checks as tooling side effects, not review output.
- Never run auto-fix or write-mode formatting commands. Prefer check-only forms.
- Never install, upgrade, or change dependencies, lockfiles, migrations, generated code, or environment configuration without explicit user intent outside this review workflow.
- Never change branches automatically. If the current worktree does not represent the requested branch/PR, explain the mismatch and ask the user to switch to the intended target.
- Do not treat passing tests as proof that the feature is correct.
- Do not manufacture concerns. Tie every requested manual test to a changed behavior, credible regression surface, model limitation, or meaningful risk.
- Never claim to have manually validated behavior that only the human observed.

## Inputs and target resolution

Accept a PR number, branch name, or both.

1. Inspect repository status, current branch, HEAD, remotes, and available project instructions.
2. If a PR number is supplied and `gh` is available, inspect PR metadata and diff without changing branches. Use the PR base/head information to understand scope.
3. If a branch is supplied, compare it with the current worktree and determine the intended base branch from repository/PR context.
4. If both are supplied, verify they refer to the same change set.
5. Record target identity and review start state in `review.md`.
6. If the current worktree does not match the target required for execution, stop before tests and tell the user exactly what needs to be switched.

Never assume the base branch when it can be determined from PR metadata, remote tracking, or repository conventions.

## Workflow

Follow three phases in order. Apply the review-depth gate after understanding the diff.

### Phase 1: Automated sanity validation

Establish whether the patch is mechanically healthy enough for human validation.

1. Inspect the diff and changed files before running checks.
2. Discover the project's existing validation conventions from files such as `pyproject.toml`, `package.json`, task runners, CI workflows, contributor docs, or repository instructions.
3. Select checks that already belong to the project. Typical categories include:
   - diff/whitespace integrity
   - formatting in check-only mode
   - linting
   - type checking when configured
   - focused tests for changed behavior
   - import/build/compile checks when appropriate
4. Prefer focused checks first. Expand to broader tests only when the change surface or project convention justifies it.
5. Record the exact command, result, relevant output summary, and any blocked checks in `review.md`.
6. If a command would rewrite files, auto-fix findings, mutate schema/state, or otherwise alter the patch, do not run it. Use a check-only equivalent or mark it blocked.
7. If automated checks fail, explain the failure and record it. Continue to human validation only when useful and safe; do not hide a mechanical failure behind manual testing.

Automated validation answers: **Does the patch clear the project's basic mechanical checks?** It does not answer whether the behavior is fully correct.

### Review-depth gate

After inspecting the patch and Phase 1 evidence, classify the review depth internally and record the decision with rationale.

**Light review**
Use for changes that do not alter runtime/source behavior, such as documentation-only edits, comments, pure formatting, or similarly isolated low-risk changes.

- Explain why a full grilling session would add little value.
- Run only proportionate checks.
- Suggest a small number of human review steps.
- Complete `review.md` with the decision and stop unless the user requests deeper validation.

Do not automatically treat configuration, dependency, workflow, schema, security, or deployment changes as light merely because they are small.

**Standard review**
Use when source/runtime behavior changes and meaningful human testing can increase confidence.

**Elevated review**
Increase depth when changes affect authentication/authorization, persistence, migrations, destructive actions, concurrency, serialization, shared abstractions, external APIs, deployment/configuration, security boundaries, broad dependency behavior, or other high-impact paths.

Depth controls thoroughness, not alarmism.

### Phase 2: Design the human validation path

Translate the changed behavior into a small, risk-based testing map before grilling the user.

1. Identify each meaningful changed behavior and credible regression surface.
2. Map existing automated evidence to those behaviors.
3. Identify where human observation is stronger than model inference or automated tests.
4. Prioritize human testing for areas such as:
   - visual layout, styling, spacing, clipping, and component appearance
   - responsive behavior and different screen sizes
   - animations, transitions, focus states, and perceived responsiveness
   - mouse, touch, keyboard, drag/drop, and multi-step interaction flows
   - browser, operating-system, device, or hardware-specific behavior
   - accessibility behavior that benefits from real assistive technology or human perception
   - audio, video, microphone, camera, or media behavior
   - external integrations where mocks do not establish real behavior
   - persisted state, restart/reload behavior, and real environment configuration
   - workflows whose correctness depends on what a user actually sees or understands
5. Add the initial validation map and a Mermaid coverage/flow diagram to `review.md` when a diagram improves comprehension.
6. For every proposed manual test, be able to answer: **Why does this test follow from this patch?** Remove tests that do not have a concrete answer.

Do not dump a generic QA checklist. Build the plan from the actual diff.

### Phase 3: Interactive human validation

Guide the human through the planned validation one coherent area at a time.

For each validation item:

1. Explain why the test matters in relation to the patch.
2. Give concrete steps the user can perform.
3. State the expected observable behavior in plain language.
4. Ask what the user actually observed.
5. Request stronger evidence only when it materially improves clarity or confidence, such as:
   - pasted terminal/application output
   - copied error text or logs
   - screenshots for visual/UI behavior
   - device/browser details
   - before/after behavior
6. Interpret the evidence with the user. Make sure the user understands what the output demonstrates and what it does not demonstrate.
7. Challenge vague answers. If the user says "works," "looks fine," or similar, ask what action they took and what outcome they observed.
8. Update `review.md` immediately after each meaningful result, including observed behavior, evidence level, status, and follow-up if any.
9. If a test fails, record the failure and continue only where further validation remains useful. Do not modify the patch.
10. Stop grilling once the meaningful changed paths, likely regression surfaces, and relevant failure conditions have sufficient evidence or are explicitly unresolved.

Use `Pending`, `Passed`, `Failed`, or `Blocked` consistently for manual test status.

## `review.md` as persistent review memory

Treat `review.md` as the authoritative local record of review progress.

- Create it only after Phase 2 has produced a concrete testing path, unless a light review needs a short record.
- Keep it untracked by default. Check whether Git already tracks it before writing. If it is tracked unexpectedly, warn the user and do not alter repository tracking state.
- Never add `review.md` to `.gitignore`, stage it, commit it, or publish it automatically.
- Package or publish it only when the user explicitly asks.
- On a later agent session, read `review.md` before resuming.
- If the user's remembered progress is ahead of the last documented checkpoint, return to the last documented step and repeat the undocumented validation rather than retroactively marking it complete.
- If the reviewed diff/HEAD has materially changed since the recorded target, explain that prior behavioral evidence may no longer apply, refresh the validation map, and revalidate affected paths rather than carrying results forward blindly.

Use Markdown structure aggressively for readability: concise headings, tables, checklists where useful, callouts through bold text, and Mermaid code blocks for flows or coverage maps when they make the review easier to interpret or act on. Avoid decorative diagrams.

## Evidence and confidence

Keep four concepts separate:

1. **Automated evidence**: commands the agent actually ran and their results.
2. **Human evidence**: observations, screenshots, pasted output, or other results reported by the user.
3. **Unverified areas**: behaviors neither side has established.
4. **Assessment**: a scoped conclusion based only on the evidence above.

Do not turn confidence into a numeric score unless the user asks. Prefer statements such as "mechanically clean, core behavior manually exercised, browser-specific behavior still unverified."

## Completion

Finish only when the applicable review path is complete.

Ensure `review.md` contains:

- target and scope
- review-depth decision and rationale
- automated checks and exact outcomes
- validation map
- human validation steps and observed results
- evidence notes where useful
- unresolved or blocked areas
- a final scoped assessment
- Mermaid visualization where it materially improves understanding

In chat, summarize the current conclusion and point the user to `review.md`. Do not create PR comments or modify the repository unless the user separately asks for a different workflow.
