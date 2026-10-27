---
name: reality-check
description: >-
  Use when the user asks for a code review of a PR, branch, or unresolved review thread,
  including focused, isolated reproductions of suspected defects.
  Trigger phrases include "review this PR", "find any bugs", "leave review comments", and "make a Reality Check report".
  Use gauntlet for broader interactive acceptance testing or guided manual validation.
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

Use `/html-communication` for HTML storage, delivery, and validation. Full video presentations and multiple report formats require a request; short evidence recordings may support an individual finding. Preserve local review records and authorized PR comments as the actionable source of truth.

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

## Trace behavior and establish findings

Inspect the full requested diff. For each materially changed behavior, inspect direct callers, relevant state changes, dependency behavior, and tests. Trace plausible failure and recovery paths, going deeper where consequences or uncertainty justify it.

A finding needs a supported trigger, causal path, and observable consequence. Check guards, caller behavior, and accepted decisions for counterevidence before reporting it. Respect accepted tradeoffs; report violations or distinct consequences that were not accepted, explaining the difference. Reopen a tradeoff only when new evidence materially changes its understood impact.

Report defects introduced, worsened, or exposed by the change as findings. Put consequential pre-existing problems outside the requested scope in a concise follow-up section, explaining their connection. Avoid unrelated cleanup. An existing problem that makes the changed behavior unsafe should affect the completion recommendation.

Pursue a concern while it plausibly connects to changed behavior and a concrete next check could confirm or dismiss it. Stop when resolved, the remaining impact is minor, access is unavailable, or further work requires a broader investigation. For consequential unresolved concerns, group related uncertainties and state the suspected consequence, available evidence, and smallest next check. Explain when uncertainty prevents a confident completion recommendation; do not present unresolved suspicions as confirmed findings.

## Reproduction and proof

Attempt a focused reproduction when practical and within the review's permissions, prioritizing serious issues and consequential uncertainty. A reproduction strengthens a finding; inspected code can establish a failure when reproduction is impractical. State why it was not reproduced and what remains unverified.

Allow focused tests and disposable reproductions using isolated fixtures, scratch scripts, or temporary services outside tracked source. Use an isolated copy for temporary mutations. Preserve the reviewed patch and user data; stop if a check would require changing them or exceeds authorization. Clean up temporary processes and fixtures, retain useful evidence under the artifact rules, and disclose any cleanup left unresolved. Route broader interactive acceptance testing to `/gauntlet`.

Put expected versus observed behavior and concise proof beside the finding: an annotated screenshot for a visible state, a brief recording for a sequence or timing issue, or focused test output for internal behavior. Capture media when it clarifies the issue; do not require it for every finding. Identify the reviewed revision and relevant setup. Link lengthy logs and traces as artifacts, and distinguish what the evidence demonstrates from what remains unverified. Evidence collection does not authorize external uploads or publication.

## Delegated repository investigation

Delegate a bounded investigation when a question needs substantial tracing or independent verification. Use parallel explorers only for sufficiently independent questions.

Suitable questions include:
- tracing callers
- locating established invariants
- mapping dependency boundaries
- determining whether existing tests cover a specific regression path

Provide the explorer with:
- one concrete question
- the minimum relevant diff and repository context
- the expected answer and file- or symbol-level evidence
- source-preservation boundaries and any permitted isolated reproduction
- a stopping condition

The primary agent inspects the full diff, verifies returned evidence, reconciles disagreements, and owns the final findings and severity. Do not delegate the complete review or treat an explorer's suspicion as a finding without verifying it against the reviewed change.

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
- Report architecture and maintainability issues when changed code creates a concrete maintenance burden or future defect risk. Name the affected behavior and how the structure makes it harder to change safely; avoid preference-only alternatives. Favor simple control flow, local reasoning, clear ownership, and testable units.
- Review documentation for current project use. Flag stale, duplicated, excessive, or journal-like historical narration when it obscures useful guidance. Keep history that explains a constraint or supports migration.
- Recommend deleting, consolidating, or replacing docs, tests, code, or abstractions when their value is absent or duplicated. Explain what guidance or protection remains; preserve useful edge cases and necessary migration guidance.
- Flag patch content that violates authoring rules in applicable `AGENTS.md` or `CLAUDE.md` files, such as test or documentation conventions.
- For important tests, identify the application behavior or failure protected. Inspect whether setup reaches that behavior and assertions distinguish correct behavior from a plausible defect. For important or doubtful coverage, use a focused reproduction or temporary mutation in an isolated copy when practical. Flag tautological assertions and mocks that bypass the behavior claimed.
- Recommend the smallest test exercising the real failure boundary: unit tests for isolated logic, integration tests for component interactions, and end-to-end tests when the user-visible flow cannot be established reliably below that level. Additional layers need distinct protection. Avoid test-per-function requirements and treating coverage percentages as proof.
- Report missing tests only for a concrete regression risk that existing coverage does not catch.
- Avoid broad style commentary unless it affects correctness, maintainability, or future defect risk.
- Do not invent issues. If there are no concrete findings, say so clearly.
- Include file and line references where possible.
- Separate confirmed findings from open questions, assumptions, and residual risks.

Check whether the changed code matches surrounding patterns, error handling, platform assumptions, validation boundaries, and test strategy. For user-facing behavior, inspect both implementation and tests.

## Findings format

Use these fields across chat, local review records, authorized PR comments, and requested reports. Adapt presentation without dropping fields. Order findings by severity and give each a stable ID.

Begin with what goes wrong and why it matters. Include the trigger, observable consequence, affected file/line where possible, and enough causal explanation to understand the issue. Keep concise proof beside the finding; omit raw code dumps and disposition fields. Avoid repeating explanations across fields.

```markdown
Finding: `RC-001` {{short problem title}}
Problem: {{trigger, observable behavior, and consequence}}
Severity: High | Medium | Low
Necessity: Fix before completion | Advisable in this change | Optional follow-up. {{brief reason}}
Location: `path/to/file.ext:line`
Fix complexity: Small | Moderate | Large | Unknown. {{concrete reason}}
Decision needed: None | Technical choice | User decision. {{choice or blocking question and recommendation, when applicable}}
Recommendation: {{specific fix or next action}}
Reproduction/evidence: {{expected versus observed behavior and focused reproduction or evidence link; otherwise Not reproduced, with reason and supporting code analysis}}
```

### Necessity

Keep necessity separate from severity, fix complexity, and decision needs. Severity describes impact; necessity states whether the issue should block completion, is advisable within this change, or is optional follow-up. Base necessity on requirements, likelihood, consequences, and scope, with a brief reason. A simple fix is not automatically necessary; an expensive fix is not automatically optional.

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

Keep severity, necessity, fix complexity, and decision needs independent. A difficult fix can need no user decision; a one-line change can need a product decision. Do not ask the user to settle questions that inspected code or requirements already answer.

Keep straightforward findings concise. Expand only to explain meaningful consequences, dependencies, uncertainty, or trade-offs; do not add detail solely because severity is high. Avoid repeating the problem in the recommendation or turning a finding into an implementation plan.

## Final Response

Lead with findings using the Findings format above, unless a loaded format file says otherwise. Then include:

- Consequential open questions with available evidence and the smallest next check, and any assumptions.
- Consequential pre-existing issues outside scope, when relevant.
- The reviewed commit or working-tree scope, materially changed behaviors, and failure/recovery paths inspected.
- Tests actually run, tests only read, and CI results observed, distinguished explicitly.
- Whether existing PR comments/threads and CI were checked.
- Review limits, such as unavailable `gh`, inaccessible CI, ambiguous base, or partial diff scope.

Include one explicit next action before any automatic quiz: return to `/assembly` for a concrete implementation finding, return to `/prelude` for an unclear problem or consequential unresolved investigation, or proceed toward completion when no actionable findings remain and the limits permit it.

If no findings are found, say "No actionable findings within this scope" and provide the same coverage and limits. Passing tests and an absence of findings do not prove correctness.

For local and HTML findings reports, append the automatic checkpoint quiz after the complete review, including evidence, unresolved concerns, coverage, and next action. The quiz supplements that content; follow the applicable output reference.
