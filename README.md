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
| `prelude` | Investigate GitHub issues, bugs, or user stories before implementation. | Useful for understanding what is actually happening before writing code or committing to a solution path. |
| `grill-me` | Relentlessly interview a user about a plan or design until the decision tree is clear. | Inspired by Matt Pocock's "grill me" skill/prompt style. Useful when a plan needs to be stress-tested before implementation. |
| `blueprint` | Create GitHub-safe and VS Code-safe project plans in a single `plan.md`. | Uses structured Markdown, task IDs, file and risk matrices, verification plans, acceptance criteria, limited Mermaid diagrams, and restricted HTML details blocks. |
| `assembly` | Execute a local plan in controlled units. | Hand holding pauses for user commits; autopilot commits the plan and uses `pr-actical` to deliver a draft PR. |
| `gauntlet` | Establish that changed behavior works through automated checks and guided human testing. | Use after or alongside code review when runtime evidence matters; maintains a local `review.md`. |
| `pr-actical` | Push a ready branch and create or update a GitHub draft PR. | Uses local `git` and `gh`; intentionally keeps PRs as drafts and avoids risky operations by default. |
| `reality-check` | Find concrete correctness and maintainability problems in a diff. | Use for static code review and prioritized engineering findings, not interactive behavioral testing. |

See [docs/skills-lifecycle.md](docs/skills-lifecycle.md) for the workflow diagram and lifecycle details.

See [docs/subagents.md](docs/subagents.md) for the shared delegation appch.

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
