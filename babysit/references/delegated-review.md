# Delegated review

Start one fresh-context, read-only reviewer for the checked head. Its findings
return to this thread for triage in step 5.

## Reviewer model

Default to Claude `claude-opus-5-5` at `high` effort. A provider, model, or
effort named by the user or applicable `AGENTS.md`/`CLAUDE.md` instructions
overrides the default, including reviewers on other harnesses such as Codex or
Pi.

## Mechanism

Use the first available option that supports the chosen reviewer:

1. **T3 Code:** look up the reviewer's `providerInstanceId`, `model`, and
   options in `orchestrator_capabilities`, then call `delegate_task` with the
   brief below, leaving isolation at its shared default so the reviewer works
   in this checkout. For the default reviewer:

   ```json
   {
     "task": "<brief>",
     "mode": "async",
     "target": {
       "providerInstanceId": "claudeAgent",
       "model": "claude-opus-5-5",
       "options": { "effort": "high" }
     }
   }
   ```

   Retain the task ID and verify the returned provider, model, and options.
   The task's completion wakes this thread; yield while waiting. A parent
   wait timeout does not cancel the reviewer. Follow the cleanup below before
   abandoning or replacing it.
2. **Native subagent:** spawn a fresh general-purpose subagent with the
   harness's own tool, such as Claude Code's `Agent` with
   `subagent_type: "general-purpose"`, `model: "opus"`, and `effort: "high"`.
   Never fork; a fork inherits this conversation and loses the fresh context.
   Use the harness's cancellation controls if the attempt fails or must be
   abandoned.
3. **Neither:** report the delegated review as unavailable. Do not substitute a
   review from the current context.

Send the reviewer a follow-up only when a finding needs clarification before
triage.

## Cancellation and fallback

Before replacing or abandoning a reviewer, or handing back a failed,
cancelled, or timed-out review, cancel its task and pending continuations.
Do this even when the original run already reports failure. Do not leave a
quota-blocked reviewer scheduled to resume when its limit resets.

For T3, call `task_cancel` with the retained task ID to stop later child runs
and dispose automatic parent delivery, then check `task_status` for unfinished
work or `hasPendingChildRuns`. A terminal original run alone does not establish
cleanup. On other harnesses, use the equivalent stop and queued-resume controls.
If cleanup cannot be confirmed, stop, report the unresolved task, and disregard
its later results; do not launch a replacement into the shared worktree.

After an explicit quota or session-limit failure and confirmed cleanup, make
one fallback attempt with Codex `gpt-6.1-sol` at `medium` reasoning effort,
unless the user explicitly prohibited fallback. Discover a supporting provider
and options through the available catalog; for T3 use `delegate_task` with
`target.options: { "reasoningEffort": "medium" }`. Verify the returned selection.
If the failed attempt already used this fallback, or the fallback is unavailable
or fails, clean up and report independent review as unavailable. Do not wait
for a quota reset or retry between providers indefinitely.

Keep the replacement in the parent session's workflow with the same review
brief, relevant decisions and prior findings, read-only boundary, and worktree
restrictions. Recheck the target head before launch and preserve the shared
worktree freeze until the replacement finishes. Start a fresh task with its
own task ID and a distinct `clientRequestId`, stable across retries of that
launch; do not resume the failed child or send it another review round.
Record the failed attempt, cleanup outcome, and fallback outcome in the handoff.

## Brief

Pass only this brief, never the conversation history:

```markdown
Review PR #<number> in <owner/repo> as a read-only reviewer.

- Worktree: <absolute path>
- Base: <base-branch> at <base-sha>
- Head: <head-branch> at <head-sha> (may include check repairs not yet pushed)

First run `git rev-parse HEAD` in the worktree. If it does not equal <head-sha>,
stop and report the mismatch.

Use the reality-check skill to review <base-sha>..<head-sha>. If the skill is 
unavailable, stop and say so. Read the PR title and description with 
`gh pr view <number> --repo <owner/repo>` for the requested scope and claims.

Do not modify reviewed source or user data, commit, push, or post PR comments.
Focused tests and disposable reproductions outside tracked source are allowed
under Reality Check's isolation and cleanup rules. Preserve the shared worktree;
use an isolated copy for mutations. Report in chat only:
findings in the Reality Check findings format, then open questions and review
limits. Skip the next-action routing.
```
