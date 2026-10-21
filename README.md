# Skills

This repo is a shared collection of AI agent skills I use in my own workflow. Some are original, some are adapted from patterns or prompts I found useful elsewhere, and some are experiments that are still being tuned.

The intent is practical sharing: each folder is a standalone skill directory with a `SKILL.md` entrypoint and, where needed, supporting `references/` or `agents/` files. Skill metadata omits default prompts; invocation guidance lives in `SKILL.md`.

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
| `prelude` | Investigate GitHub issues, bugs, or user stories before implementation. | Understand behavior before choosing a solution; requested reports use the user-specified communication style. |
| `grill-me` | Relentlessly interview a user about a plan or design until the decision tree is clear. | Inspired by Matt Pocock's "grill me" skill/prompt style. The **default mode** goes one question at a time, but **batch mode** will group up to 5 connected questions. |
| `blueprint` | Create GitHub-safe and VS Code-safe project plans in a single `plan.md`. | Uses structured Markdown, Mermaid diagrams, and HTML details blocks; requested companion reports use the user's chosen medium while preserving the canonical plan. |
| `assembly` | Execute a local plan in controlled units. | **Hand holding mode** pauses for user commits; **autopilot mode** commits the plan and uses `babysit` to publish and verify the PR. |
| `babysit` | Canonical PR workflow: publish ready-for-review, get CI green, then run a delegated `reality-check` review alongside any review bots and fix clear findings. | Inspired by Theo Browne's "babysit" skill/prompt style. Writes reviewer-friendly PR bodies with visual evidence, upload limits, and brief exemptions when visuals add no value. Caps post-push repair cycles at 1. Never force-pushes. |
| `gauntlet` | Establish that changed behavior works through automated checks and guided human testing. | Maintains local `review.md`; requested reports use the user-specified communication style. |
| `reality-check` | Explain concrete problems in a diff, their consequences, fix complexity, and decisions needed. | Static code review with concise, actionable findings; expand for meaningful uncertainty or trade-offs. Requested reports use the user-specified communication style. |
| `rigging` | Review agent sessions to infer useful collaboration insights and guide harness improvements. | Starts with a brief intent interview when needed and presents four visual report variations in one local HTML file; chat closeout links to the report for user review, with existing planning and authoring skills available for requested follow-up. |
| `checkpoint-quiz` | Define short artifact-based quiz contracts for verification checkpoints and reflective reports. | Host skills own placement and question sources; HTML mechanics use `html-communication`. No scoring or required chat answers. |
| `html-communication` | Create portable HTML reports and inline visual explanations when selected. | Choose layouts and requested variations to suit the evidence; preview before T3 rendering and distinguish parsing, syntax, layout, and interaction checks. Not for planning artifacts or ordinary prose. |
| `video-communication` | Create narrated technical explanations on Windows with Manim and ElevenLabs. | Invoked directly or by planning, investigation, and review skills when video is requested. Uses Eric narration, cached audio, and a shared renderer outside worktrees. Checks prerequisites and requests missing setup. The MP4 is primary, with working files accessible. |
| `skill-crafter` | Draft or edit a skill for optimal agent instruction. | Use for prompt engineering a skill with the focus of concise detail and effectiveness. |

See [docs/skills-lifecycle.md](docs/skills-lifecycle.md) for the workflow diagram and lifecycle details.

Session artifacts default to ignored, untracked repository-root `artifacts/`: `plan.md`, `decisions.md`, `review.md`, `review-findings.md`, and standalone `quiz.md`. HTML reports use `artifacts/reports/`. Ignored artifacts persist only in the local checkout; preserve them separately before removing a worktree.

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

## Contributing Skills

Create and edit skills in this repository following [AGENTS.md](AGENTS.md). Every skill must be listed in both the Included Skills table above and [.claude-plugin/plugin.json](.claude-plugin/plugin.json); add, rename, or remove those entries in the same change as the skill. Keep descriptions current when behavior changes.

Before finishing, validate each changed skill and check the complete catalog:

```bash
python skill-crafter/scripts/quick_validate.py <skill-directory>
python scripts/check_skill_catalog.py
```

The catalog check also runs on pushes and pull requests in GitHub Actions.
