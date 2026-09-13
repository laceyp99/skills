---
name: skill-crafter
description: Create or revise a skill with a focus on communication quality. Use when building a new skill, improving routing or clarity of an existing skill, or reviewing skill prose.
---

# Skill Crafter

Skills are instructions written for a model reader. Every line exists to change what the agent does; if a sentence would not change a decision, cut it. This skill teaches the recurring sections of a skill, what good looks like for each, and how length should scale with complexity.

## Principles

- **Write for a capable agent.** State only what changes decisions: non-obvious context, real constraints, preferred outcomes. Do not restate what the agent would do anyway.
- **Match specificity to risk.** Loose, outcome-based guidance where multiple approaches are fine; fixed steps and absolute language only where deviation causes concrete harm.
- **Disclose progressively.** Name and description route; SKILL.md body instructs; references add depth only when a mode needs it. Put a one-line trigger on every reference ("read when ...").
- **Communicate, don't legislate.** Prefer a concrete example over a rule; prefer a rule over a lecture. One before/after example beats three paragraphs of explanation.

## Sections of a Skill

Most skills contain some subset of the sections below. Guidance on each is compact here; [references/writing-guide.md](references/writing-guide.md) has expanded before/after examples and the anti-pattern catalog — read it when writing or revising a skill's prose.

### Frontmatter

`name` and `description` are the only required fields, and they are read *before* the skill is loaded. The name must be lowercase hyphen-case, under 64 characters, matching the folder name. Preserve existing optional fields (`metadata`, `license`) when updating.

### Description

The description decides whether the skill gets loaded at all. It must discriminate: state what the skill does and **when to use it**, with a boundary against near-miss requests. Write it as a routing hint (ex. include trigger phrases) for a reader who has never seen the body. Don't focus on how it works; no capability lists, no catchalls. Detail lives in the body, not the description.

Syntax limits enforced by the validator: maximum 1024 characters, and no angle brackets (`<` or `>`).

### Opening Summary

The first lines after the frontmatter should orient in one or two sentences: what this skill produces and what stance it takes. Do not restate the description verbatim, and do not open with history, motivation, or a table of contents.

### Body

The body holds the task-specific instruction. Organize by what the agent must decide or produce, not by how you think about the topic. Keep shared guidance and mode selection here; move per-mode detail into references. Every instruction should be actionable without the agent guessing at intent.

### Stop Conditions

Conditional, but loud when triggered: any skill that writes files, sends requests, retries, loops, or runs multi-step without user input **must** state when to stop and what requires re-confirmation. The more autonomous and multi-step the skill, the more explicit the stop conditions need to be. This is where you can note the completion signal, the failure-handling behavior, and the point where the agent must return to the user rather than continue. Read-only advisory skills may skip this section.

### Length Calibration

Length scales with complexity, not with importance:

- **Single-mode, routine task** → ~40–90 line SKILL.md, no sub-files. If a skill fits here and you've written more, you are over-prompting.
- **Multi-mode or risky workflow** → lean SKILL.md carrying shared guidance and mode selection; per-mode detail moves to references. Each reference gets a one-line trigger.
- **Deterministic or fragile steps** → move the mechanics to a script in `scripts/`; the body describes when to run it, not how it works inside.

Each step up must be justified by the task. A harder task gets a genuinely distinct mode, or a correctness requirement. Complexity is never a reason for padding; it is a reason for structure.

## Supporting Resources

Create only resources the workflow actually needs:

- `scripts/` — executable helpers for repeated transformations or fragile operations. Run new or changed scripts to verify them.
- `references/` — documentation needed only in particular contexts (schemas, policies, format-specific procedures, substantial examples). Link each from the body with a trigger.
- `assets/` — files copied into output (templates, images, fonts). Never loaded as instructions.

Do not add a README, changelog, or duplicated quick reference.

## UI Metadata

`agents/openai.yaml` provides UI-facing metadata. Generate it with:

```bash
scripts/generate_openai_yaml.py <path/to/skill-folder> --interface key=value
```

Read [references/openai_yaml.md](references/openai_yaml.md) when creating or editing this file. Keep implicit invocation enabled unless the user explicitly requests explicit-only (`policy.allow_implicit_invocation: false`).

The generator replaces the entire file on each run. If an existing `openai.yaml` contains `policy` or `dependencies`, edit those fields in place instead of regenerating. Running the generator on that skill would silently drop them. Overriding `short_description` via `--interface` must stay within 25–64 characters.

## Creating a Skill

Respect a user-specified location; otherwise use `$CODEX_HOME/skills` (`~/.codex/skills` when unset). Scaffold with:

```bash
scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets] [--examples]
```

Request only the resource directories the skill needs; never re-initialize an existing skill. Replace all scaffold TODOs before finishing.

Then write the sections: engineer the description for routing, draft the body organized by decisions, add stop conditions if the skill mutates anything or runs autonomously, and calibrate length against the ladder above.

## Self-Review

After writing, run `scripts/quick_validate.py <path/to/skill-folder>`, then check:

1. Does the description discriminate? Would a reader route to this skill over its neighbors correctly?
2. Does every instruction in the body change behavior? Cut any that don't.
3. If the skill mutates state or runs multi-step, are stop conditions explicit and proportional to autonomy?
4. Is length on the correct rung of the calibration ladder?
5. Any anti-patterns from the writing guide present?
6. Do references each have a trigger line, and does anything duplicate reference content in the body?
7. Do scripts actually run?

Treat failures as targeted edits, not grounds for rewriting the skill.