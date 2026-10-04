# Repository instructions

This is a shared skills repository used across multiple machines. It is the source of truth for skill development; global skill directories are downstream configurations that may be updated from this repository later.

Assume any mention of skills are the skills existing within this workspace, unless further specified. When creating or editing a skill, make and validate the change here, inside the current worktree or another explicitly requested in-repo path. Do not modify global skill directories such as `$CODEX_HOME/skills`, `~/.codex/skills`, `~/.agents/skills` or any other global `~/` paths during ordinary repository work. Only copy, install, or update a global skill when the user explicitly requests that separate downstream action.

## Skill catalog completion rule

Every root-level directory containing `SKILL.md` must appear exactly once in both the `README.md` Included Skills table and the `skills` array in `.claude-plugin/plugin.json` (as `./<directory-name>`).

Creating, renaming, or removing a skill includes updating both catalogs in the same change. Update the README purpose and notes when an existing skill's behavior or invocation changes. These updates are part of the requested skill work even when the conversation only discusses skill contents; complete them without asking for a separate reminder or approval. Preserve unrelated plugin metadata and README content.

Before reporting skill work complete:

1. Validate each added or edited skill with `python skill-crafter/scripts/quick_validate.py <skill-directory>`.
2. Run `python scripts/check_skill_catalog.py` from the repository root and fix any missing, stale, or duplicate entries.
3. Review the diff for accurate README descriptions and valid plugin paths. Report the validation results and any unresolved failure; do not claim completion while a required check is failing.
