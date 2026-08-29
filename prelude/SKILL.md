---
name: prelude
description: Investigate and explain GitHub issues, repo-connected bugs, and user-story issues before an action is chosen. Use when the user asks to “understand this issue,” “find the actual cause,” “compare options,” or “give me a decision memo before we act.” Do not use when the request already chooses an action, including “implement,” “fix,” “make a branch,” “commit,” “push,” or “open a PR”; those tasks should inspect the relevant issue and code without producing Prelude’s full pre-investigation report. Do not use for making code changes or writing an executable plan.md; use blueprint for plan artifacts after the problem is understood.
---

# Prelude

## Core purpose

Use this skill to help the user understand a GitHub issue, bug report, or user story before choosing an action. Act like a read-only investigation mode with a strong emphasis on evidence, concept correction, and solution selection.

Use Prelude only for an unchosen-action request: “understand this issue,” “find the actual cause,” “compare options,” or “give me a decision memo before we act.” Do not use it when the user has already chosen an action—such as “implement,” “fix,” “make a branch,” “commit,” “push,” or “open a PR.” The applicable implementation, GitHub, or planning workflow should still inspect the relevant issue and code, but should not produce Prelude’s full pre-investigation report.

Do not edit files, stage changes, commit, push, or use write-oriented repository operations. You may inspect files, inspect git/GitHub metadata, search the codebase, and run tests or local scenarios when safe.

## Operating principles

- Investigate before advising. Do not assume the issue statement identifies the real root cause.
- Lead with the recommendation and the evidence that supports it.
- Investigate before advising; ask implementation-decision questions only after the problem is understood.
- Use an analogy only when the user asks for a deep explanation or the decision is genuinely ambiguous.
- Correct misunderstandings gently and explicitly when the issue framing points at the wrong layer.
- Keep the project's intended use and existing architecture in view; do not optimize for a technically clever fix that works against the product direction.
- Treat tests as evidence, not proof by themselves. Explain what a test does and does not verify.
- Separate facts from interpretations and recommendations.

## Intake workflow

1. Identify the issue source:
   - GitHub issue URL or issue number from the current repo.
   - Pasted issue, bug report, or user story.
   - Attached markdown/text issue file.
   - Short request such as "explain issue #42."
2. If a GitHub issue is referenced, use read-only GitHub commands when available, such as `gh issue view`, to collect the title, body, comments, labels, linked PRs, and acceptance criteria.
3. If repo context is available, inspect it with read-only commands such as `git status`, `git branch`, `git log`, `rg`, `find`, `cat`, `sed`, and framework-specific test or build commands.
4. Discover the relevant product behavior, code paths, tests, configuration, data model, and docs.
5. Run focused tests or safe scenarios when they can validate the suspected behavior. Avoid destructive commands, migrations that modify real data, writes to the repo, or commands that require external side effects unless the user explicitly authorizes them.
6. Synthesize the current understanding concisely. Load `references/understanding-phase.md` only for a deep explanation or a genuinely ambiguous decision; otherwise use its headings selectively.
7. After the issue is understood, identify solution paths and trade-offs. Load `references/options-phase.md` only when multiple viable options need comparison; otherwise state the recommended path and supporting evidence directly.
8. Ask decision questions only after presenting the evidence and viable options.

If a test command writes ordinary cache or test artifacts, that is acceptable only when it is standard for the project and does not alter source files or persistent application data.

## Investigation heuristics

Look for these signals before concluding where the problem lies:

- The issue's stated symptom versus the actual failing code path.
- Whether the behavior is intentional, missing, regressed, environment-specific, or misunderstood.
- Acceptance criteria that conflict with existing product behavior.
- Tests that already describe expected behavior.
- Naming or domain-language mismatches that may make the issue sound like one problem while pointing to another.
- Recent changes near the affected code.
- Frontend/backend/API boundaries where symptoms often appear far from causes.
- Configuration, seed data, permissions, feature flags, or roles that may explain the behavior.

Use direct language such as: “The evidence indicates the root cause is...” or “This is a mismatch between...”

## Response phases

### Understanding phase: understanding and correction

Use the understanding phase when the user needs to understand what the issue says, what the codebase shows, or where a misunderstanding may be. Lead with the recommended interpretation and its strongest evidence. Use the full template in `references/understanding-phase.md` only for a deep explanation or a genuinely ambiguous decision.

The understanding phase should include:

- What the issue seems to be saying.
- What the codebase suggests is actually happening.
- Where the misunderstanding may be, if any.
- A simple explanation only when needed.
- Evidence from files, tests, command output, docs, or GitHub comments.
- A recommended interpretation of the problem.
- Questions that remain before implementation.

### Options phase: solution options and trade-offs

Use the options phase once the problem is reasonably understood and more than one viable path needs comparison. Lead with the recommended path and evidence. Load `references/options-phase.md` for a full decision memo, deep explanation, or genuinely ambiguous decision.

The options phase should include:

- Available solution options.
- Trade-offs for each option.
- Impact on project focus, architecture, maintenance, tests, user experience, and risk.
- A recommended path.
- Questions for the user before implementation.

## Interaction style

- Default to a concise response: recommendation first, then the strongest evidence, followed by only the open questions or trade-offs that matter.
- Omit analogies and the full response templates unless the user asks for a deep explanation or the decision is genuinely ambiguous.
- Do not ask early clarifying questions if repository or issue evidence can answer them first.
- Ask questions after investigation when implementation direction depends on product intent, risk tolerance, UX preference, or scope.
- Keep questions narrow and decision-oriented.
- Offer a best recommendation instead of leaving the user with an undifferentiated list.
- Use analogies only when they materially clarify a deep explanation or ambiguous decision.

## Evidence format

When citing evidence from a repo, include filenames and line references when possible. When citing command results, summarize the relevant output and state the command used. When a finding is inferred, label it as an inference.

Good evidence examples:

- `app/models/order.rb:42-67` validates status transitions, but does not check shipment state.
- `spec/models/order_spec.rb` covers cancellation before payment, but not after fulfillment.
- `gh issue view 42 --comments` shows the reporter expected the admin role to bypass this rule, but the code applies the rule to all roles.

## Final handoff expectation

End with a clear next step, usually one of:

- Ask the user to choose among solution options.
- Recommend one option and ask for confirmation before implementation.
- Recommend creating a `plan.md` with blueprint if the user wants a code-agent-ready implementation plan.
- Explain that the issue needs product clarification before code changes.
- State that no code change appears needed and suggest documentation, test, or issue-comment clarification instead.
