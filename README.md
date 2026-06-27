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
npx skills@latest add laceyp99/skills -g -a codex --skill visual-coding-plan -y
```

To preview what is available without installing:

```bash
npx skills@latest add laceyp99/skills --list
```

## Included Skills

| Skill | Purpose | Notes |
|---|---|---|
| `branch-planner` | Turn a rough feature, fix, refactor, or chore idea into a scoped branch plan. | This is my older planning workflow. It focuses on branch names, commit sequencing, validation, risks, and a local `plan.md`. I am keeping it here for reference while moving my planning workflow toward `visual-coding-plan`. |
| `visual-coding-plan` | Create GitHub-safe and VS Code-safe visual project plans in a single `plan.md`. | This is the direction I am actively moving toward. It uses structured Markdown, task IDs, file and risk matrices, verification plans, acceptance criteria, limited Mermaid diagrams, and restricted HTML details blocks. It is still being optimized. |
| `grill-me` | Relentlessly interview a user about a plan or design until the decision tree is clear. | Inspired by Matt Pocock's "grill me" skill/prompt style. Useful when a plan needs to be stress-tested before implementation. |
| `prelude` | Investigate GitHub issues, bugs, or user stories before implementation. | Useful for understanding what is actually happening before writing code or committing to a solution path. |
| `pr-creator` | Draft a local `PR.md` for the current branch. | Reads branch scope, diffs, commits, and PR templates, then prepares a human-reviewable PR description. |
| `pr-actical` | Push a ready branch and create or update a GitHub draft PR. | Uses local `git` and `gh`; intentionally keeps PRs as drafts and avoids risky operations by default. |

## Repository Layout

```text
.
├── branch-planner/
├── grill-me/
├── pr-actical/
├── pr-creator/
├── prelude/
└── visual-coding-plan/
```

Each skill directory should be copied as a whole. The `SKILL.md` file is the entrypoint; supporting files are referenced relative to that directory.

## Installing a Skill

Copy the skill directory you want into your agent's skills directory.

For the Pi agent path I currently use:

```powershell
Copy-Item -Recurse .\visual-coding-plan $HOME\.pi\agent\skills\
```

For Codex-style local skills:

```powershell
Copy-Item -Recurse .\visual-coding-plan $HOME\.codex\skills\
```

Repeat that command for any other skill directory you want to install.

The manual copy flow is still useful when you are editing a skill locally. For normal installation from GitHub, prefer the `npx skills@latest add laceyp99/skills` quickstart above.

## Planning Workflow Notes

`branch-planner` represents my old way of planning coding work: narrow the scope, suggest branch names, break the work into commits, and write a `plan.md` that can guide implementation.

`visual-coding-plan` is my newer planning direction. Instead of focusing mainly on branch and commit structure, it tries to create a plan that is more useful to both people and coding agents: a plain Markdown artifact with stable task IDs, decision logs, matrices, stop conditions, verification, and optional simple visuals that still render safely in GitHub and VS Code.

The visual planning skill is not final. I am still optimizing the structure, the level of detail, and how much visual markup is helpful before it becomes noise.

## Provenance

This is a personal working collection. Some skills are mine, some are adapted from public ideas or community workflows, and some may be forks of prompts I found useful. Where I know the inspiration, I try to call it out in this README or the skill itself.

Before redistributing a skill outside this repo, check the source and licensing expectations for any upstream material it may have been adapted from.
