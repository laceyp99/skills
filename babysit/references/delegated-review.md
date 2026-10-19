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

   The task's completion wakes this thread. Check `task_status` about every 15
   minutes while waiting; if two checks in a row show no progress, report the
   review as timed out and continue without it.
2. **Native subagent:** spawn a fresh general-purpose subagent with the
   harness's own tool, such as Claude Code's `Agent` with
   `subagent_type: "general-purpose"`, `model: "opus"`, and `effort: "high"`.
   Wait for its reply without a time limit. Never fork; a fork inherits this conversation and loses
   the fresh context.
3. **Neither:** report the delegated review as unavailable. Do not substitute a
   review from the current context.

Otherwise, treat the review as failed only when the task reports an error or
cancellation.
Send the reviewer a follow-up only when a finding needs clarification before
triage.

## Brief

Pass only this brief, never the conversation history:

```markdown
Review PR #<number> in <owner/repo> as a read-only reviewer.

- Worktree: <absolute path>
- Base: <base-branch> at <base-sha>
- Head: <head-branch> at <head-sha> (may include check repairs not yet pushed)

First run `git rev-parse HEAD` in the worktree. If it does not equal <head-sha>,
stop and report the mismatch.

Use the reality-check skill to review <base-sha>..<head-sha>, invoked the way
your harness runs skills (for example `/reality-check` in Claude Code or
`$reality-check` in Codex). If the skill is unavailable, stop and say so. Read
the PR title and description with `gh pr view <number> --repo <owner/repo>`
for the requested scope and claims.

Do not edit files, commit, push, or post PR comments. Report in chat only:
findings in the Reality Check findings format, then open questions and review
limits. Skip the next-action routing.
```
