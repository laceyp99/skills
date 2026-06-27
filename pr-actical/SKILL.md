---
name: pr-actical
description: create or update github draft pull requests from the current ready branch using git and the github cli. use when the user wants to push the current non-default branch, create a draft pr, update an existing draft pr, or add an update comment to an already published pr. inspect branch state, commits, diff, ./plan.md, pr templates, tests, and existing prs. assume invocation authorizes normal push and gh pr create/edit/comment operations, but refuse on unsafe states such as default branches, staged changes, closed prs, missing gh auth, unclear base branch, non-fast-forward push needs, or required sync unless explicitly requested.
---

# pr-actical

## Purpose

Turn the current local branch into a GitHub draft pull request using `git` and `gh`. Invocation is treated as approval to run ordinary push and PR commands, but not as approval to publish a PR, force-push, change PR metadata, commit edits, or perform risky history/base synchronization.

Use [references/pr-writing.md](references/pr-writing.md) when composing PR titles, bodies, and update comments.

## Operating Policy

- Always create new PRs as drafts. Never create or convert a PR to ready-for-review, even if the user asks for a normal PR. Explain that this skill only produces human-reviewable drafts.
- Use `gh` for GitHub operations and `git` for repository state. Refuse if `gh auth status` fails.
- Assume the user intended side effects when this skill is invoked: ordinary `git push -u origin HEAD`, `gh pr create --draft`, `gh pr edit`, and `gh pr comment` do not require a second confirmation.
- Never use `git push --force` or `git push --force-with-lease` unless the user explicitly requested force-with-lease in the current message. Plain `--force` is never allowed.
- Never create commits. If this skill makes or would need to make any tracked local file changes, stop and ask the user to review and commit them.
- Do not manage labels, reviewers, assignees, projects, or milestones.
- Use a temporary file for PR body/comment content. Delete it after successful PR creation, edit, or comment. Preserve it on refusal or failure and report its path.
- Do not write `PR.md`.

## Refusal Conditions

Refuse before pushing or changing a PR when any of these are true:

- The current branch is `main`, `master`, the repo default branch, or the current branch cannot be determined.
- The base branch cannot be determined from a user argument, current branch tracking config, or repository data.
- `gh auth status` fails or the repository is not a GitHub repository reachable by `gh`.
- There are staged but uncommitted changes.
- There are merge conflicts, and resolving them requires local file changes. If conflicts are already present, report them and stop.
- The branch is behind its base branch and the user did not explicitly ask to sync, merge, or rebase.
- An existing PR for the branch is closed.
- A push is rejected as non-fast-forward or would require force/force-with-lease not explicitly authorized.
- Required tests fail and fixing them would require local file changes. Stop with the failing command and key output.

Unstaged or untracked files are not automatically part of the PR. If they are unrelated, ignore them and mention them in the final response. If they appear required for tests or PR correctness, stop and ask the user to review/commit them.

## Workflow

### 1. Inspect repository and branch state

Run safe inspection commands first:

```bash
git status --short --branch
git branch --show-current
gh auth status
gh repo view --json defaultBranchRef,nameWithOwner,url
```

Determine the base branch in this order:

1. User-provided argument.
2. Current branch tracking/upstream configuration when it clearly implies the intended base.
3. GitHub default branch from `gh repo view`.

Do not proceed if base is still unclear. Refuse if current branch equals `main`, `master`, or the GitHub default branch.

Check whether the branch is behind base without modifying history:

```bash
git fetch --quiet origin <base>
git rev-list --left-right --count HEAD...origin/<base>
```

If the branch is behind base and the user did not explicitly request sync, refuse. Do not merge or rebase by default.

### 2. Detect existing PR

Check for an existing PR for the current branch:

```bash
gh pr list --head "$(git branch --show-current)" --state all --json number,state,isDraft,title,url,headRefOid,body
```

Use the result as follows:

- No PR: create a new draft PR after tests pass and branch pushes successfully.
- Draft PR: push latest commits and edit the PR title/body to represent the full current branch state.
- Open non-draft PR: push latest commits and add a comment summarizing only the new changes since the last pushed commit visible on the PR before this run. Do not rewrite the published PR body unless the user explicitly asks.
- Closed PR: refuse.

Before pushing an existing PR, save the current remote PR head SHA (`headRefOid`) so the update comment can summarize the incremental range after push.

### 3. Gather context for writing

Use observed repository facts as the source of truth:

```bash
git log --oneline --decorate --no-merges origin/<base>..HEAD
git diff --stat origin/<base>...HEAD
git diff --name-status origin/<base>...HEAD
git diff origin/<base>...HEAD
```

For incremental comments on an already published PR, summarize from the saved pre-push PR head SHA to the current local `HEAD`:

```bash
git log --oneline <saved-head-sha>..HEAD
git diff --stat <saved-head-sha>..HEAD
git diff --name-status <saved-head-sha>..HEAD
git diff <saved-head-sha>..HEAD
```

Read `./plan.md` only when it exists. Use it for intended goals, acceptance criteria, and risk context. Prefer the observed code diff over `./plan.md` when they conflict, and mention meaningful mismatches in the final response or PR text. Do not quote private scratchpad-like plan content verbatim.

Find PR templates in:

- `.github/pull_request_template.md`
- `.github/PULL_REQUEST_TEMPLATE/*`

If multiple templates exist, pick the closest based on branch name, changed files, diff themes, and template filename. Do not ask the user unless no reasonable choice exists. Preserve useful headings/checklists when practical, but do not get stuck on strict adherence and do not check boxes unless verified.

### 4. Infer and run tests

Inspect project files and GitHub Actions workflows to infer appropriate local checks:

- `.github/workflows/*.yml` and `.github/workflows/*.yaml`
- `package.json`, lockfiles, and package manager files
- `pyproject.toml`, `pytest.ini`, `tox.ini`, `requirements*.txt`
- `go.mod`, `Cargo.toml`, `Gemfile`, `Makefile`, or similar tooling files

Run obvious lightweight commands that correspond to repo tooling or CI, such as `npm test`, `pnpm test`, `pytest`, `go test ./...`, `cargo test`, `bundle exec rspec`, or `make test`. Prefer the repository's documented commands when available.

If a test or lint command fails, inspect the failure. If fixing it would require local file changes, stop and ask the user to review/commit the needed fix. Do not commit. If no appropriate local tests can be inferred, continue and say tests were not run because no clear local command was found.

Only include a Testing section in PR text when a command was actually run or a prior passing result was directly observed in the current session.

### 5. Push safely

Push the branch normally:

```bash
git push -u origin HEAD
```

If push fails because the remote rejected it as non-fast-forward, stop and report that manual sync or explicit force-with-lease authorization is needed. Do not force-push.

### 6. Create, edit, or comment on the PR

Write the PR body or comment to a temporary file, then invoke `gh`.

For a new PR:

```bash
gh pr create --draft --base <base> --head <branch> --title <title> --body-file <tempfile>
```

For an existing draft PR:

```bash
gh pr edit <number> --title <title> --body-file <tempfile>
```

For an existing open non-draft PR:

```bash
gh pr comment <number> --body-file <tempfile>
```

After success, delete the temporary file and fetch/display the PR URL:

```bash
gh pr view <number-or-branch> --json url,title,isDraft,state
```

## Final Response

For a new or draft PR, include:

- `Draft PR created:` or `Draft PR updated:` followed by the URL.
- Base branch and head branch.
- Tests run and result, or why tests were not run.
- Any warnings, skipped checks, ignored local files, template selected, or `./plan.md` mismatches.

For an already published PR, include:

- `PR updated:` followed by the URL.
- Whether a comment was added.
- Pushed commit count or range summarized.
- Tests run and result, or why tests were not run.
- Any warnings or skipped checks.

For refusal, include:

- The refusal reason.
- The exact state or command output that caused the refusal.
- The next safest user action.
- The temp file path if a body/comment file was created and intentionally preserved.
