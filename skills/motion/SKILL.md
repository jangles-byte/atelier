---
name: motion
description: Build animation that feels alive — and watch it before shipping. Production recipes for interface motion (modals, drawers, toasts, tabs, lists, drag, tickers), view transitions (route changes, shared elements, scroll reveals), and procedural motion (particles, screen shake, hit-stop, springs, ambient fields), plus easing and spring mathematics usable in any language and a diagnostic for motion that "feels dead", "floaty", "janky", or "cheap". Use this skill for ANY animation work: adding or tuning a transition, hover or press state, loading state, page transition, chart animation, game juice, or generative motion. Trigger on "animate", "animation", "transition", "make it feel", "add some life", "microinteraction", "juice", "springy", "smooth", or any easing, duration, or timing decision.
---

# Motion

Motion is communication. Every animation answers one of three questions — *what just
happened?* (feedback), *where did it go?* (orientation), or *is this alive?* (character).
Animation that answers none of them is decoration on a delay; delete it rather than tune it.

The rule that makes this skill different from reading about animation: **you cannot judge
motion from source code, and you cannot judge it from a still.** Run it, capture it, watch
it. There is a script here that does exactly that.

## Workflow

1. **Name the question.** Feedback, orientation, or character — and what the motion
   temperament is (snappy or viscous, calm or nervous). One line is enough. If the project
   has a design philosophy from `design-direction`, take the temperament from there.
2. **Start from a recipe, not from scratch.** Find the pattern in the recipe files below;
   they carry tuned values, per-stack code, reduced-motion variants, and the failure mode
   for each. Adapt the values to your temperament rather than inventing timings.
3. **Implement** with curves and springs from
   [references/easing-and-springs.md](references/easing-and-springs.md).
4. **Watch it.** Capture the running animation and look at the result:
   ```bash
   ./scripts/capture-motion.py index.html --out motion.gif \
       --trigger "document.querySelector('#open').click()" --duration 1200
   ```
   It records real composited frames over the DevTools protocol, so it works for CSS,
   Web Animations, GSAP/Framer, canvas, and WebGL alike. For native or engine work,
   use the platform's own capture (simulator recording, engine profiler playback).
5. **Diagnose if it underwhelms** — work
   [references/dead-motion-diagnostic.md](references/dead-motion-diagnostic.md) in order
   before touching values, then re-capture. The first render of a fix is a hypothesis.
6. **Check the frame cost** with the `performance-craft` skill, and confirm the
   reduced-motion path is complete and calm — not merely disabled.

## Which reference to load

| Situation | Load |
|---|---|
| Modal, drawer, dropdown, toast, accordion, tabs, list reorder, drag, ticker, hover/press | `references/recipes-interface.md` |
| Route/page transitions, shared elements, scroll reveals, parallax, skeletons, progress | `references/recipes-transitions.md` |
| Particles, screen shake, hit-stop, springs in a game loop, ambient/generative fields | `references/recipes-procedural.md` |
| Choosing a curve, spring tuning, staggers, interruption | `references/easing-and-springs.md` |
| The 12 principles, duration standards, game feel, accessibility floor | `references/principles.md` |
| It exists but feels dead / floaty / cheap / janky | `references/dead-motion-diagnostic.md` |

## Non-negotiables

- Nothing moves without a reason. Name the question it answers or cut it.
- Durations from the weight scale: micro 100–150ms, small 150–250, medium 250–400,
  large 400–600. Exits ~20% faster than entrances. Nothing over 700ms without a reason.
- No linear easing on anything an eye follows. Enter fast-and-decelerate, exit
  accelerate-and-gone. Linear is honest only for machine progress (determinate bars).
- Animate compositor-friendly properties (transform, opacity, and platform equivalents).
  Layout properties — `top`, `height`, `width`, `margin` — get FLIPped, not animated.
- Every entrance has an exit, and every animation survives being interrupted mid-flight.
- Delta-time everywhere; never assume 60fps. ProMotion and 144Hz displays are common.
- `prefers-reduced-motion` (and platform equivalents) is part of done, not a follow-up:
  keep opacity and colour feedback, drop travel, scale, parallax, shake, and ambient.
- Scarcity is what makes the good animation land. One excellent motion beats six
  mediocre ones, and a still page with one great transition beats a page that breathes
  everywhere.
