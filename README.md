# Skills

This repo is a shared collection of AI agent skills I use in my own workflow. Some are original, some are adapted from patterns or prompts I found useful elsewhere, and some are experiments that are still being tuned.

The intent is practical sharing: each folder is a standalone skill directory with a `SKILL.md` entrypoint and, where needed, supporting `references/` or `agents/` files.

## Quickstart

Install interactively with the open `skills` CLI:

```bash
npx skills@latest add laceyp99/skills
```

That command will fetch this GitHub repo, show the available skills, and let you choose which agent or agents to install them into.

To install every skill globally without prompts:

```bash
npx skills@latest add laceyp99/skills -g --skill '*' --agent '*' -y
```

To install one skill for Codex:

```bash
npx skills@latest add laceyp99/skills -g -a codex --skill blueprint -y
```

To preview what is available without installing:

```bash
npx skills@latest add laceyp99/skills --list
```

## Included Skills

| Skill | Purpose | Notes |
|---|---|---|
| `assembly` | Execute a local plan in controlled units. | **Hand holding mode** pauses for user commits; **autopilot mode** commits the plan and uses `pr-actical` to deliver a draft PR. |
| `babysit` | Watch PR verification; fix checks or publish a ready PR when requested. | Inspired by Theo Browne's "babysit" skill/prompt style. Caps corrective pushes at 3. Never force-pushes. |
| `blueprint` | Create GitHub-safe and VS Code-safe project plans in a single `plan.md`. | Uses structured Markdown, Mermaid diagrams, and HTML details blocks to better visualize proposed plans. |
| `gauntlet` | Establish that changed behavior works through automated checks and guided human testing. | Use after or alongside code review when runtime evidence matters; maintains a local `review.md`. |
| `grill-me` | Relentlessly interview a user about a plan or design until the decision tree is clear. | Inspired by Matt Pocock's "grill me" skill/prompt style. The **default mode** goes one question at a time, but **batch mode** will group up to 5 connected questions. |
| `html-communication` | Create readable local HTML communication artifacts. | Use for internal reports, comparisons, summaries, and insight briefs; not for planning artifacts or ordinary prose. |
| `prelude` | Investigate GitHub issues, bugs, or user stories before implementation. | Useful for understanding what is actually happening before writing code or committing to a solution path. |
| `pr-actical` | Push a ready branch and create or update a GitHub draft PR. | Uses local `git` and `gh`; intentionally keeps PRs as drafts and avoids risky operations by default. |
| `reality-check` | Find concrete correctness and maintainability problems in a diff. | Use for static code review and prioritized engineering findings, not interactive behavioral testing. |
| `skill-crafter` | Draft or edit a skill for optimal agent instruction. | Use for prompt engineering a skill with the focus of concise detail and effectiveness. |

See [docs/skills-lifecycle.md](docs/skills-lifecycle.md) for the workflow diagram and lifecycle details.

See [docs/subagents.md](docs/subagents.md) for the shared delegation approach.

## Installing a Skill

The manual copy flow is still useful when you are editing a skill locally. For normal installation from GitHub, prefer the `npx skills@latest add laceyp99/skills` quickstart above.

Copy the skill directory you want into your agent's skills directory.

For the Pi agent path I currently use:

```powershell
Copy-Item -Recurse .\blueprint $HOME\.pi\agent\skills\
```

For Codex-style local skills:

```powershell
Copy-Item -Recurse .\blueprint $HOME\.codex\skills\
```

Repeat that command for any other skill directory you want to install.
