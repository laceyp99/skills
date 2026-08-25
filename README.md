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
| `assembly` | Execute a local plan in controlled units. | Use `/assembly` for plan execution. Supports `Hand holding mode` and `autopilot mode`. |
| `gauntlet` | Establish that changed behavior works through automated checks and guided human testing. | Use after or alongside code review when runtime evidence matters; maintains a local `review.md`. |
| `grill-me` | Relentlessly interview a user about a plan or design until the decision tree is clear. | Inspired by Matt Pocock's "grill me" skill/prompt style. Useful when a plan needs to be stress-tested before implementation. |
| `prelude` | Investigate GitHub issues, bugs, or user stories before implementation. | Useful for understanding what is actually happening before writing code or committing to a solution path. |
| `pr-actical` | Push a ready branch and create or update a GitHub draft PR. | Uses local `git` and `gh`; intentionally keeps PRs as drafts and avoids risky operations by default. |
| `reality-check` | Find concrete correctness and maintainability problems in a diff. | Use for static code review and prioritized engineering findings, not interactive behavioral testing. |
| `visual-coding-plan` | Create GitHub-safe and VS Code-safe visual project plans in a single `plan.md`. | Uses structured Markdown, task IDs, file and risk matrices, verification plans, acceptance criteria, limited Mermaid diagrams, and restricted HTML details blocks. |

## Repository Layout

```text
skills/
├── assembly/
├── grill-me/
├── pr-actical/
├── prelude/
├── reality-check/
└── visual-coding-plan/
```

Each skill directory should be copied as a whole. The `SKILL.md` file is the entrypoint; supporting files are referenced relative to that directory.

## Installing a Skill

The manual copy flow is still useful when you are editing a skill locally. For normal installation from GitHub, prefer the `npx skills@latest add laceyp99/skills` quickstart above.

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

## Workflow Notes

`/assembly` is the execution path for turning a plan into controlled work units. Use it when the repo already has a plan and you want implementation to proceed in small, reviewable steps.

`gauntlet` answers **“Does the changed behavior actually work?”** It combines read-only automated checks with risk-based, human-observed testing and keeps the evidence in a local `review.md`.

`/reality-check` answers **“What is wrong or risky in this code?”** It inspects diffs, branches, and PR context with a skeptical, maintainability-first lens and returns prioritized engineering findings.

`prelude` is for investigation before implementation. It is meant to slow the agent down long enough to understand an issue, bug report, or user story before recommending a fix.

`visual-coding-plan` is the planning direction in this repo. It creates a plain Markdown `plan.md` that is useful to both people and coding agents: stable task IDs, decision logs, matrices, stop conditions, verification, and optional simple visuals that still render safely in GitHub and VS Code.

`grill-me` (from Matt Pocock) is for unresolved thinking. It asks one decision-shaping question at a time and gives a recommended answer, which helps turn a fuzzy plan into explicit choices.

`pr-actical` is for the end of a ready branch. It uses local repository state, `gh`, commits, diffs, templates, and tests to create or update a GitHub draft PR without publishing it for review.


## Provenance

This is a personal working collection. Some skills are mine, some are adapted from public ideas or community workflows, and some may be forks of prompts I found useful. Where I know the inspiration, I try to call it out in this README or the skill itself.

Before redistributing a skill outside this repo, check the source and licensing expectations for any upstream material it may have been adapted from.
