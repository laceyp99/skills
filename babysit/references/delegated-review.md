# Delegated review

Start one fresh-context, read-only reviewer for the published head. Its findings
return to this thread for triage in step 4.

## Reviewer model

Default to Claude `claude-opus-5-5` at `high` effort. A provider, model, or
effort named by the user or applicable `AGENTS.md`/`CLAUDE.md` instructions
overrides the default.

## Mechanism

Use the first available option:

1. **T3 Code:** call `delegate_task` with the brief below, leaving isolation at
   its shared default so the reviewer works in this checkout:

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

   Keep watching checks while the reviewer runs; its completion wakes this
   thread.
2. **Native subagent:** spawn a fresh general-purpose subagent that supports
   the chosen model, such as Claude Code's `Agent` with
   `subagent_type: "general-purpose"`, `model: "opus"`, and `effort: "high"`.
   Never fork; a fork inherits this conversation and loses the fresh context.
3. **Neither:** report the delegated review as unavailable. Do not substitute a
   review from the current context.

Send the reviewer a follow-up only when a finding needs clarification before
triage.

## Brief

Pass only this brief, never the conversation history:

```markdown
Review PR #<number> in <owner/repo> as a read-only reviewer.

- Worktree: <absolute path>
- Base: <base-branch> at <base-sha>
- Head: <head-branch> at <head-sha>

First run `git rev-parse HEAD` in the worktree. If it does not equal <head-sha>,
stop and report the mismatch.

Run `/reality-check` on <base-sha>..<head-sha>. Read the PR title and description
with `gh pr view <number> --repo <owner/repo>` for the requested scope and claims.

Do not edit files, commit, push, or post PR comments. Report findings in chat only,
using the Reality Check findings format, followed by review limits.
```
