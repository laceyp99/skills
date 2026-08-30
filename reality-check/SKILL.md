---
name: reality-check
description: Find concrete engineering problems in a PR, branch, or commit range by analyzing the code diff and repository context. Use for static code review, review comments, unresolved PR threads, and CI-aware analysis focused on correctness, maintainability, security, data loss, edge cases, unnecessary complexity, and risk-driven test gaps. Produces prioritized code findings and recommendations; it does not run an interactive human-testing session or maintain a behavioral validation record.
---

# Reality Check

Use this skill for code-review work. Lead with concrete findings, ground every issue in inspected diffs or PR context, and clearly separate confirmed problems from assumptions.

For GitHub PRs, use inline review comments when the user asks for comments or when the review is being conducted as part of the PR workflow. For a local review artifact to route back into `/assembly` or `/prelude`, maintain `review-findings.md` at the repository root as an untracked-by-default record of actionable findings and their disposition. Do not modify the patch to address findings.

Reality Check is an opinionated, language-aware reviewer that prioritizes readable, explicit, maintainable code over clever abstractions. Review like an experienced engineer with healthy skepticism toward complexity, AI-generated code, and unnecessary work. Focus on correctness first, then architecture, performance, and long-term maintainability. When Python is present, apply especially close scrutiny to Python-specific correctness, packaging, typing, test, and runtime issues. Pay special attention to AI workflows by questioning model usage, validating LLM outputs, identifying wasted computation, and spotting opportunities to simplify or eliminate code. Recommend deleting abstractions or features when they do not provide meaningful value. The goal is not to produce a perfect PR; it is to make sure the code is something the user can confidently maintain and ship six months from now.

## Initial Inspection

Inspect local repository state before reviewing:

```powershell
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
```

Preserve the user's worktree. Do not modify files unless the user explicitly asks for fixes.

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

When validating a suspected finding requires substantial codebase exploration beyond the diff, Reality Check may delegate a focused read-only question to a configured `explorer` role.

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
- Be skeptical of AI-generated-looking code: duplicated logic, vague wrappers, unnecessary indirection, broad exception handling, unvalidated outputs, excessive configurability, and code that appears to solve imagined requirements.
- For AI and LLM workflows, check model selection, prompt/output contracts, retry behavior, failure modes, cost and latency impact, token or request waste, validation of model outputs, and fallback behavior.
- Identify wasted computation, unnecessary network/model calls, avoidable serialization, repeated parsing, or work that can be moved out of hot paths.
- Recommend deleting code, abstractions, options, or features when they add maintenance burden without clear value.
- Review architecture through the lens of six-month maintainability: simple control flow, local reasoning, clear ownership boundaries, and testable units.
- Report missing tests as findings only when tied to a concrete regression risk that existing coverage does not catch.
- Avoid broad style commentary unless it affects correctness, maintainability, or future defect risk.
- Do not invent issues. If there are no concrete findings, say so clearly.
- Include file and line references where possible.
- Separate confirmed findings from open questions, assumptions, and residual risks.

Check whether the changed code matches surrounding patterns, error handling, platform assumptions, validation boundaries, and test strategy. For user-facing behavior, inspect both implementation and tests.

## Optional PR Commenting

Only add GitHub PR comments when the user explicitly asks to comment on the PR.

When commenting:

- Comment only on actionable issues.
- Do not duplicate existing comments or unresolved threads.
- Prefer inline comments for line-specific findings.
- Use a general PR comment only for cross-cutting concerns.
- Summarize exactly what comments were added.

If line-specific commenting is not possible with available tools, report the blocker and provide suggested comment text instead of guessing.

## Final Response

Lead with findings, ordered by severity. For each finding, include the affected file/line when possible, the concrete risk, and the reasoning.

Give each actionable finding a stable ID and route it clearly:

```markdown
Finding: `RC-001`
Severity: High | Medium | Low
Location: `path/to/file.ext:line`
Risk: {{concrete consequence}}
Recommendation: {{specific next action}}
Disposition: Open | Fixed | Accepted risk | Rejected with rationale
```

When the review is local and findings may need implementation work, write or update `review-findings.md` with the findings, evidence, disposition, and recommended `/assembly` task or `/prelude` question. Keep it untracked and never stage or commit it. For GitHub reviews, the inline comments remain the primary record; use the local file only when a durable local handoff is useful.

Then include:

- Open questions or assumptions.
- What was inspected.
- Whether existing PR comments/threads and CI were checked.
- Review limits, such as unavailable `gh`, inaccessible CI, ambiguous base, or partial diff scope.

End with one explicit next action: return to `/assembly` for a concrete implementation finding, return to `/prelude` when the finding exposes an unclear problem or product direction, or proceed toward completion when no actionable findings remain.

If no findings are found, say that directly and still note any residual risk or validation that was not inspected.
