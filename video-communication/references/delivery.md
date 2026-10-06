# Local and PR delivery

Read when a host requests a video package for a user, branch, or pull request.

## Host handoff

The handoff needs the audience, canonical evidence or its path, desired explanation, source revision, and destination. Infer these from the request and existing host output where possible. Clarify only missing information that changes the result. The caller retains its finding dispositions, plan tasks, validation claims, and approval boundaries.

For a review, explain confirmed findings with severity and limits. For a plan, say that the behavior is proposed. For a PR walkthrough, tie the story to the inspected change and show one representative before/after or failure scenario. The video does not replace code evidence or executable planning tasks.

Keep existing quizzes in the canonical Markdown or HTML artifact. An MP4 cannot capture interactive decisions; do not invent quiz answers or turn a reflective checkpoint into a narration claim. A video may accompany an HTML report when both are requested.

## Branch and PR boundaries

Use the current worktree's evidence without switching branches. If the user requests a separate delivery branch, hand that operation to the host's implementation/Git workflow after the video package is reviewable. PR publication remains a separate workflow. Do not create or push branches merely because the output explains a PR.

Keep generated video, audio, render caches, and private source notes out of the staged diff by default. Do not modify `.gitignore` just to render. If the user explicitly asks to commit reproducible video sources or media, select the requested files and check repository size/asset conventions; do not sweep the entire job directory into a commit. Planning and review records keep their existing local-only rules.

For an existing PR, use its repository and head revision explicitly. An explanation of a merged PR is still a valid local artifact; it does not authorize reopening or mutating that PR. Follow the environment's PR linking requirements for PRs actually used by the task.

## Attachments and links

Deliver the local MP4 with an absolute file link or supported inline video embed. Include the caption/script location and a short description the host can use with the attachment.

Posting in a PR requires an accessible attachment or URL. A local path cannot serve as a GitHub video URL. Use an authorized browser upload or existing storage integration only when it can attach the actual MP4 and the destination was requested. Verify the returned URL and its audience access. Do not assume that `gh pr comment` or the GitHub comments API uploads local video files.

If upload tools are unavailable, give the user the local file and copy-ready attachment text, for example:

> Video walkthrough of microphone selection and fallback in this PR, based on commit `<sha>`. The diagrams illustrate the implementation; the accompanying review records validation limits.

Do not auto-publish to public storage, alter sharing permissions, add CI, or commit a large binary to manufacture a URL. A video-delivery blocker does not change the host's conclusions or automatically block an otherwise authorized PR workflow; report the separate attachment gap.
