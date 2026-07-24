---
name: motion
description: Animation that feels alive — Disney's 12 principles translated for UI transitions, procedural/particle effects, and game feel; easing and spring mathematics usable in any language; duration standards; and a diagnostic for animation that "feels dead", "feels floaty", "feels janky", or "feels cheap". Use this skill whenever adding, tuning, or reviewing ANY animation or transition: hover states, page/route transitions, modals, list reordering, loading states, chart transitions, game juice (hit effects, screen shake), or generative/procedural motion. Trigger on "animate", "transition", "make it feel", "add some life", "microinteractions", or any easing/duration/spring decision.
---

# Motion

Motion is communication, not decoration. Every animation answers one of three
questions — *what just happened?* (feedback), *where did it go?* (orientation), or
*is this alive?* (character) — and an animation that answers none of them is
subtracted, not tuned.

## Workflow

1. Read the philosophy's motion temperament (`design-direction`): snappy or viscous,
   calm or nervous, and which question (feedback / orientation / character) is
   primary for this product.
2. Design transitions with [references/principles.md](references/principles.md) —
   the 12 principles mapped to interface and game work, plus duration standards.
3. Implement with [references/easing-and-springs.md](references/easing-and-springs.md)
   — curve selection, spring math, and stagger rules, in CSS / JS / Swift / game-loop
   forms.
4. If it's a game or toy, add juice via the game-feel section of
   [references/principles.md](references/principles.md) (hit-stop, shake, particles).
5. Run the artifact and watch it. If any animation underwhelms, run
   [references/dead-motion-diagnostic.md](references/dead-motion-diagnostic.md)
   before touching values.
6. Verify `prefers-reduced-motion` (or platform equivalent) yields a complete,
   calm experience — and check frame cost with the `performance-craft` skill.

## Which reference to load

| Situation | Load |
|---|---|
| Designing any transition; durations; game juice | `references/principles.md` |
| Choosing/implementing curves, springs, staggers | `references/easing-and-springs.md` |
| Animation exists but feels dead/floaty/cheap/janky | `references/dead-motion-diagnostic.md` |

## Non-negotiables

- Nothing moves without a reason (feedback, orientation, or character — name it).
- Durations from the standard scale (micro 100–150ms … large 400–600ms); nothing
  over 700ms without a stated reason.
- No linear easing on anything an eye follows. Enter fast-and-decelerate; exit
  accelerate-and-gone.
- Every entrance has an exit. Every animation is interruptible.
- Reduced-motion support is part of the definition of done, not a follow-up.
