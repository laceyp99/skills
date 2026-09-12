---
name: babysit
description: >-
  Use when the user asks to push a branch, post a ready-for-review PR, and watch
  it until automated verification checks pass, fixing and pushing follow-up
  commits when checks fail. Trigger phrases include "post the PR and babysit it",
  "watch CI until it passes", "get the checks green", and "post and babysit this
  branch". Do not use for reviewing a change without publication
  (reality-check), or for ordinary PR posting without check-watching (pr-actical).
---

# babysit

## Purpose

Turn the current local branch into a ready-for-review pull request, watch its
automated verification checks, and push focused corrective commits until all
checks pass and any currently visible blocking automated comments are resolved.
Human approvals are not part of the green-state requirement.

Invocation authorizes ordinary `git push`, `gh` PR operations, check inspection,
and small corrective commits needed to make checks pass. It never authorizes
force-pushes, rebases, or rewriting pushed history.

## Safety and stop conditions

- Use `git` for repository state and `gh` for GitHub operations. Stop if
  `gh auth status` fails or the repository is not reachable.
- Never force-push, including `--force`, `--force-with-lease`, or
  `--force-if-includes`. If a push is rejected as non-fast-forward, stop.
- Never rebase, reset, amend pushed commits, or otherwise rewrite outgoing
  history. Stop if the branch diverged from its remote, is behind its base,
  has conflicts, or requires other non-straightforward synchronization.
- Stop if the current branch is `main`, `master`, the repository default branch,
  or cannot be determined; if the base branch cannot be determined; if staged
  changes exist; if the PR is closed; or if the base changes unexpectedly.
- Stop when a failure cannot be confidently fixed because it is caused by
  infrastructure, a runner or dependency outage, suspected flakiness, required
  secrets, an environment-specific setup, or an unclear cause. Do not patch
  unrelated flaky tests or CI infrastructure. One failed job rerun may be used
  to confirm suspected flakiness and does not count as a fix attempt.
- Stop after three failed check-watch cycles. A cycle is failure → fix → push →
  re-watch. Do not push blind variations when the same failure returns unchanged.
- Ignore unrelated unstaged or untracked files, but mention them in the final
  report. Stop if such files are required for correctness.
- Treat `plan.md`, `decisions.md`, `review.md`, `review-findings.md`, and similar
  planning or review artifacts as local-only. Never stage, commit, or publish
  them. Stop if any is already in the outgoing diff and ask the user to remove it.
- Do not manage labels, reviewers, assignees, projects, milestones, or other PR
  metadata beyond the title, body, and incremental comments needed here.
- Before every push, verify the current branch, PR head, intended diff, and
  working-tree status. Stage files by name; never stage all changes blindly.

## Workflow

### 1. Inspect state and determine the base

Run:

```bash
git status --short --branch
git branch --show-current
gh auth status
gh repo view --json defaultBranchRef,nameWithOwner,url
```

Determine the base in this order: user argument, clear upstream/tracking
configuration, then GitHub’s default branch. Refuse if still unclear or if the
current branch is the default branch. Fetch the base and verify the branch is
not behind or diverged without modifying history:

```bash
git fetch --quiet origin <base>
git rev-list --left-right --count HEAD...origin/<base>
```

### 2. Run checks and publish or update the PR

Inspect repository tooling and run obvious local checks corresponding to the
project and CI. If a local check fails, fix it only when the cause is clear and
within scope; commit the focused fix, then continue. Otherwise stop and report.

Detect an existing PR:

```bash
gh pr list --head "$(git branch --show-current)" --state all \
  --json number,state,isDraft,title,url,headRefOid,body
```

- No PR: push with `git push -u origin HEAD`, then create a ready-for-review PR
  with `gh pr create --base <base> --head <branch> --title <title> --body-file <tempfile>`.
- Existing draft PR: push and update its title/body to describe the full current
  branch. Preserve useful existing content unless replacement is necessary.
- Existing open ready-for-review PR: save its remote head SHA, push, and add an
  incremental comment describing only the newly pushed changes.
- Closed PR: stop.

Compose titles, bodies, and comments from observed repository facts, applicable
PR templates, and relevant local intent artifacts. Do not claim checks or
validation that were not observed. Use a temporary file when supplying PR body
or comment content; delete it after successful use and preserve/report its path
if the operation fails.

### 3. Watch checks and automated comments

Watch verification checks with:

```bash
gh pr checks <number> --watch
```

If watch mode is unavailable or times out, poll until all checks complete. Checks
are first-order: diagnose and fix failed checks before addressing comments.

Also inspect:

```bash
gh pr view <number> --json reviews,comments,statusCheckRollup
```

Act only on published comments and submitted reviews. Ignore pending or
unpublished review comments until they are published. Check whether each
comment applies to the current PR `HEAD`; treat comments tied to an older head
as stale unless the underlying concern still exists.

Checks are first-order: diagnose and fix failed checks before addressing
comments. Never fix a comment blindly. Classify each published automated
comment as valid, invalid, stale, already addressed, or unclear. Fix valid
findings; explain invalid findings without changing code; verify stale findings
against the current code; and resolve each handled thread where GitHub permits.
Stop for unclear findings.

When all checks pass and the PR head remains unchanged, wait up to three minutes
for newly published automated comments. Resolve applicable blocking automated
comments that appear during that window, then re-run relevant checks if needed.
Any push or rerun restarts the checks-first loop and begins a fresh three-minute
post-green window. Do not wait for human approvals or non-blocking comments.

### 4. Fix loop

For each failed check or applicable blocking automated finding:

1. Inspect the actual failure and logs, not only the job name.
2. Reproduce the failing check locally when possible, then diagnose the root
   cause and make the smallest correct fix.
3. Re-run the failing command locally until it passes, when possible.
4. Verify the current branch, PR head, working tree, and intended named-file
   diff; then commit with a focused message and push normally.
5. Add a brief PR comment describing the failure and corrective commit.
6. Re-watch the same PR. Count each failure → fix → push → re-watch as one
   failed cycle, up to the three-cycle limit.

### 5. Green state

Green means all verification checks pass and currently observed blocking
automated comments are resolved. It does not require human approval. Leave the
PR ready for review and report the URL, final check summary, watch cycles, fix
commits, non-blocking comments, and warnings.

## Final response

On success:

- `Ready-for-review PR is green:` followed by the URL.
- Report the final check summary, total cycles, pushed fix commits, and any
  non-blocking comments or ignored local files.

On a stop or refusal:

- `Babysit stopped:` followed by the PR URL when one exists and the reason.
- Include the exact relevant state or command output, current blocking failure
  and best diagnosis, attempted commits, preserved temp-file path, and safest
  next user action.
