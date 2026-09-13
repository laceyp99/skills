# Review Thread Retrieval

Read when checking whether all blocking automated findings on a PR are handled.
Incomplete retrieval prevents claiming they are.

`gh pr view --json reviews,comments,statusCheckRollup` does not return inline
review threads. Use `gh api graphql` with the bound repository owner and name
(add `--hostname` for a nondefault host) to paginate `reviewThreads`,
collecting per thread:

- Thread ID (required for `resolveReviewThread`)
- `isResolved`, `isOutdated`, `viewerCanResolve`
- Comment bodies, authors, and URLs
- Commit / original-commit associations and review publication state

Paginate nested comment and reply connections as well as the top-level thread
connection; a partial page silently omits findings.
