# Contributing

Contributions welcome — especially new stack translations, sharper values, and
counter-examples.

## Ground rules

1. **Principle first, code second.** Every reference file teaches the
   medium-agnostic rule before showing stack-specific code. A PR that adds a
   framework recipe without the principle it serves will be asked to add it.
2. **Exact values or it didn't happen.** "Use generous spacing" is not teachable;
   "between-group gap ≥ 2× within-group gap" is. Claims should be checkable.
3. **Keep SKILL.md files short.** They are routers (frontmatter + workflow + a
   load table). Depth goes in `references/`. If a SKILL.md approaches 100 lines,
   move content down.
4. **Descriptions are triggers.** The frontmatter `description` is what makes a
   skill fire — when editing one, keep both halves: what it does *and* the
   phrasings that should trigger it.
5. **No lock-in.** Examples land in 2–3 different stacks (web, native/GPU, and a
   plotting/game context). Adding a stack is great; replacing the others isn't.

## Testing changes

Copy (or symlink) `skills/*` into `~/.claude/skills/`, start a fresh Claude Code
session, and confirm the edited skill still triggers on its description's
phrasings and that its references resolve. For substantive changes, run the
package's own acceptance test: build a small deliberately-mediocre artifact, run
the full workflow (direction → implement → render → critique → iterate), and
include the before/after in the PR.

## Releases

Semver. Reference-file improvements are patches, new references or skills are
minor versions, format/structure changes are major.
