---
name: reality-check
description: >-
  Use when the user asks for a static code review of a PR, branch, or unresolved review thread.
  Trigger phrases include "review this PR", "find any bugs", "leave review comments", and "make a Reality Check report".
  Do not use for interactive behavioral testing or manual validation (gauntlet).
---

# Reality Check

Use this skill for code-review work. Lead with concrete findings, ground every issue in inspected diffs or PR context, and clearly separate confirmed problems from assumptions.

For GitHub PRs, use inline review comments when the user asks for comments or when the review is being conducted as part of the PR workflow. For a local review artifact to route back into `/assembly` or `/prelude`, maintain `review-findings.md` at the repository root as an untracked-by-default record of actionable findings and recommended next actions. Do not modify the patch to address findings.

## Report mode

Enter report mode only when requested, using the user's specified medium or established session preference. Ask if the medium is missing; continue independent work without generating a report. Do not default to HTML or video. Create multiple formats only when requested.

For video, invoke `/video-communication` after the review. Pass the audience, inspected revision, confirmed findings using the Findings format below, source evidence for factual grounding, review limits, and destination. Apply the same reader-facing content rules to the video; do not add evidence or disposition sections. Keep actionable findings in `review-findings.md` or the authorized GitHub review. The video package stays outside the worktree by default; it does not authorize code changes or additional publication. For a video-only report, keep the actionable findings and checkpoint quiz in local untracked `review-findings.md` and link it beside the MP4; use the ordinary chat closeout format with the video link.

For an HTML Reality Check report, perform the review and use `/html-communication` to create a local HTML report as the main reader-facing result. Use the Findings format below, making severity, fix complexity, decision needs, review scope and limits, and the next action easy to inspect. Choose visuals or interaction to suit the reviewed change; do not impose a fixed layout. Keep GitHub comments or `review-findings.md` as the actionable record where applicable. In chat, link the report and briefly state the review conclusion and next action.

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

## Checkpoint Quiz Section

After findings are gathered, and before finalizing the review record, write a quiz section into the very bottom of `review-findings.md`, after all findings, so the user can review the record and then test what they retained. Source questions from the highest-severity confirmed findings. Use decision-capture questions for unresolved User decision items; do not require user selection for None or Technical choice items unless they also depend on user intent. Confirm the user's selections with them and update the relevant Decision needed and Recommendation fields in `review-findings.md`, or fold them into the final report and authorized inline comments when no local file is used.

In HTML report mode, deliver the quiz as the report's baked section through `/checkpoint-quiz` report mode instead.

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

In HTML report mode, put the detailed findings in the HTML report; use the final chat reply to link it and summarize the conclusion and next action. Otherwise, lead with findings using the Findings format above.

When the review is local and findings may need implementation work, write or update `review-findings.md` using the same findings format, with a recommended `/assembly` task or `/prelude` question. Keep it untracked and never stage or commit it. For GitHub reviews, the inline comments remain the primary record; use the local file only when a durable local handoff is useful.

Then include:

- Open questions or assumptions.
- What was inspected.
- Whether existing PR comments/threads and CI were checked.
- Review limits, such as unavailable `gh`, inaccessible CI, ambiguous base, or partial diff scope.

End with one explicit next action: return to `/assembly` for a concrete implementation finding, return to `/prelude` when the finding exposes an unclear problem or product direction, or proceed toward completion when no actionable findings remain.

If no findings are found, say that directly and still note any residual risk or validation that was not inspected.
