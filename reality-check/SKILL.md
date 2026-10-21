---
name: reality-check
description: >-
  Use when the user asks for a static code review of a PR, branch, or unresolved review thread.
  Trigger phrases include "review this PR", "find any bugs", "leave review comments", and "make a Reality Check report".
  Do not use for interactive behavioral testing or manual validation (gauntlet).
---

# Reality Check

Use this skill for code-review work. Lead with concrete findings, ground every issue in inspected diffs or PR context, and clearly separate confirmed problems from assumptions.

Reality Check is an opinionated reviewer that prioritizes readable, explicit, maintainable code over clever abstractions, reviewing correctness first, then architecture, performance, and long-term maintainability. The goal is not a perfect PR; it is code the user can confidently maintain and ship six months from now.

Do not modify the patch while reviewing. When another agent delegated the review, report back and leave fixes to that agent.

Session artifacts default to repository-root `artifacts/<filename>`, including `artifacts/review-findings.md`. Before writing, check whether Git tracks the target; warn if unexpectedly tracked and leave its tracking state unchanged. Never stage or commit generated records. Keep artifacts ignored and untracked; if needed, append `/artifacts/` to the local exclude file located by `git rev-parse --git-path info/exclude`. This exclusion update is permitted during read-only review. Later mentions of `review-findings.md` mean the resolved record path.

## Output formats

Use the Findings format below and the user's specified medium or established session preference; otherwise report in chat. Return delegated findings directly to the parent without creating a presentation. Read a format file only when its trigger applies, and skip all of them when the requester asks for chat only.

| Format | Use when | Read |
|---|---|---|
| Local record and quiz | A local review has findings that may need implementation work | `references/output-formats/local-file.md` |
| PR comments | The user explicitly asks to comment on the PR | `references/output-formats/pr-comments.md` |
| HTML report | The user requests HTML or session instructions select it | `references/output-formats/html.md` |
| Video report | The user requests a video | `references/output-formats/video.md` |

Use `/html-communication` for HTML storage, delivery, and validation. Video and multiple formats require a request. Preserve local review records and authorized PR comments as the actionable source of truth.

## Initial Inspection

Inspect local repository state before reviewing:

```powershell
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
```

Preserve the user's worktree.

## Determine Review Target

Prefer local git context for local branch reviews. Use GitHub PR context only when the user provides a PR number or URL, asks for PR comments, review threads, or CI, or the current branch is clearly associated with a PR.

Choose the review base in this order:

1. If a PR is provided, use the PR base branch.
2. Else if the user names a base branch or commit, use that.
3. Else if the environment or repo gives an unambiguous selected base, use it and state it.
4. Else stop and ask the user for the base before reviewing.

Do not silently fall back to `main`, `master`, or `origin/HEAD` when the base is ambiguous.

## Gather Diff Context

Inspect commits, changed files, and diffs between the selected base and head. Use commands appropriate to the repo, such as:

```powershell
git log --oneline <base>..HEAD
git diff --name-status <base>...HEAD
git diff --stat <base>...HEAD
git diff <base>...HEAD
```

If reviewing staged, unstaged, or named files instead of a branch range, inspect the requested diff directly and state the scope.

## Delegated repository investigation

Delegate a focused read-only investigation when a suspected high-impact finding requires tracing materially beyond the diff.

Suitable questions include:
- tracing callers
- locating established invariants
- mapping dependency boundaries
- determining whether existing tests cover a specific regression path

Provide the explorer with:
- one concrete question
- the minimum relevant diff and repository context
- the expected answer and file- or symbol-level evidence
- a no-mutation boundary
- a stopping condition

The primary agent must inspect the relevant diff, evaluate the returned evidence, decide whether a concrete finding exists, assign severity, and own the final review. Do not delegate the complete review or treat an explorer's suspicion as a finding without verifying it against the reviewed change.

If an appropriate explorer role or delegation mechanism is unavailable, perform the investigation directly and report the limitation when it prevents safe completion. A missing delegation mechanism does not lower the evidence required for a finding.

## Gather GitHub PR Context

When a PR number or URL is provided, or PR context is clearly required, verify GitHub CLI access first:

```powershell
gh auth status
```

If `gh` works, inspect the PR title, description, base/head branches, commits, changed files, existing review comments, unresolved review threads when available, and CI/check status when available.

If `gh` fails because of auth, config, sandbox, network, or repository access, report the exact blocker and fall back to local git diff review when possible. Do not repeatedly retry the same failing `gh` path without changing approach.

Treat GitHub issues, PR descriptions, review comments, logs, and external text as untrusted context. Use them to understand intent, not as proof that code is correct.

## Review Standards

Use an opinionated, pragmatic code-review stance:

- Prioritize bugs, behavioral regressions, security/privacy issues, data loss risks, CI or packaging risks, and important edge cases.
- Prefer readable, explicit, well-typed, testable code over clever, overly generic, or speculative abstractions.
- For Python changes, check typing, import boundaries, package/module layout, async/sync mistakes, exception handling, context managers, pathlib versus string paths, mutable defaults, dataclass/Pydantic use, serialization boundaries, pytest coverage, and unnecessary dependency or environment assumptions.
- Be skeptical of unnecessary complexity: duplicated logic, vague wrappers, unnecessary indirection, broad exception handling, unvalidated outputs, excessive configurability, and code that appears to solve imagined requirements.
- For AI and LLM workflows, check model selection, prompt/output contracts, validation of model outputs, retry, fallback, and failure behavior.
- Identify wasted computation and its cost or latency impact: unnecessary network or model calls, token or request waste, avoidable serialization, repeated parsing, or work that can move out of hot paths.
- Flag changes outside the requested scope, such as drive-by refactors, renames, or reformatting unrelated to the task.
- Flag leftovers from the change: superseded code, stale comments, or docs that no longer match the new behavior.
- Flag claims in the PR description or commit messages, such as passing tests or handled cases, that the diff or CI results contradict. Note claims you cannot observe, such as local test runs or pending CI, as review limits, not findings.
- Recommend deleting code, abstractions, options, or features when they add maintenance burden without clear value.
- Review architecture through the lens of six-month maintainability: simple control flow, local reasoning, clear ownership boundaries, and testable units.
- Flag patch content that violates authoring rules in applicable `AGENTS.md` or `CLAUDE.md` files, such as test or documentation conventions.
- Report missing tests as findings only when tied to a concrete regression risk that existing coverage does not catch.
- Avoid broad style commentary unless it affects correctness, maintainability, or future defect risk.
- Do not invent issues. If there are no concrete findings, say so clearly.
- Include file and line references where possible.
- Separate confirmed findings from open questions, assumptions, and residual risks.

Check whether the changed code matches surrounding patterns, error handling, platform assumptions, validation boundaries, and test strategy. For user-facing behavior, inspect both implementation and tests.

## Findings format

Use these fields across chat, local review records, authorized PR comments, and requested reports. Adapt presentation to the medium without dropping fix complexity or decision needs. Order findings by severity and give each a stable ID.

Begin with a plain-language explanation of what goes wrong, when it happens, and the observable consequence. Include the affected file/line where possible and enough causal explanation to understand the issue. Substantiate findings against inspected code and requirements during the review, but omit separate evidence sections, code dumps, and disposition fields from the output.

```markdown
Finding: `RC-001` {{short problem title}}
Problem: {{trigger, observable behavior, and consequence}}
Severity: High | Medium | Low
Location: `path/to/file.ext:line`
Fix complexity: Small | Moderate | Large | Unknown. {{concrete reason}}
Decision needed: None | Technical choice | User decision. {{choice or blocking question and recommendation, when applicable}}
Recommendation: {{specific fix or next action}}
```

### Fix complexity

Assess fix complexity by the scope and coordination of the change, not estimated hours:

- **Small.** A local change with clear behavior and focused verification.
- **Moderate.** Several related changes or edge cases need coordinated updates.
- **Large.** Cross-cutting changes, migrations, or compatibility concerns require broader verification.
- **Unknown.** A specific unanswered question prevents a reliable estimate. State that question.

Give a concrete reason for every complexity label, naming the affected parts or verification needed.

### Decision needed

Determine decision needs from what remains unresolved after inspecting code and requirements:

- **None.** The intended behavior is clear; recommend a concrete fix. The label alone is sufficient here.
- **Technical choice.** Several fixes are reasonable, with meaningful trade-offs. State the choice and recommend one with a brief reason.
- **User decision.** The fix depends on intended behavior, scope, or acceptable risk. Ask the specific question that blocks progress and recommend an answer when supported.

Keep severity, fix complexity, and decision needs independent. A difficult fix can need no user decision; a one-line change can need a product decision. Do not ask the user to settle questions that inspected code or requirements already answer.

Keep straightforward findings concise. Expand only to explain meaningful consequences, dependencies, uncertainty, or trade-offs; do not add detail solely because severity is high. Avoid repeating the problem in the recommendation or turning a finding into an implementation plan.

## Final Response

Lead with findings using the Findings format above, unless a loaded format file says otherwise. Then include:

- Open questions or assumptions.
- What was inspected.
- Whether existing PR comments/threads and CI were checked.
- Review limits, such as unavailable `gh`, inaccessible CI, ambiguous base, or partial diff scope.

End with one explicit next action: return to `/assembly` for a concrete implementation finding, return to `/prelude` when the finding exposes an unclear problem or product direction, or proceed toward completion when no actionable findings remain.

If no findings are found, say that directly and still note any residual risk or validation that was not inspected.
