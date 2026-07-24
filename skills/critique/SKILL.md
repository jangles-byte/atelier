---
name: critique
description: A structured design-critique protocol that turns "looks off" into ranked, concrete changes with exact values (px, ms, curves, colors) — never vibes. Use this skill whenever evaluating any rendered visual: reviewing a screenshot, judging your own just-built UI/chart/slide/game screen before shipping, responding to "does this look good?", "review this design", "why does this feel off?", "roast my landing page", or comparing two design options. ALWAYS run this skill as the final step of any visual work, on a real render — it is the package's quality gate.
---

# Critique

A critique is an ordered list of changes with exact values, produced by evaluating a
**real render** against a fixed rubric. "Feels unbalanced" is not critique;
"increase section gap 32px→64px so the pricing table separates from the hero" is.

## Workflow

1. **Get a real render.** Screenshot the running artifact (browser preview, simulator,
   plot output, game capture) — never critique source code or imagination. For motion,
   interact with it (hover, open/close, mash) before judging.
2. **Inventory** — one paragraph of what is objectively on screen (elements, reading
   order as encountered, palette, faces in use). Forces looking before judging.
3. **Score the rubric** — eight dimensions, 1–5 each, using
   [references/rubric.md](references/rubric.md). Cite evidence per score.
4. **Write the change list** — every scored weakness becomes a change in the exact
   format of [references/change-format.md](references/change-format.md): ranked by
   impact, each with location, current value → new value, and the principle it serves.
   3 changes minimum, 10 maximum; past 10, ship the top 10 and re-critique after.
5. **Apply and re-render.** A critique that isn't applied and re-verified is a memo.
   Iterate until the weakest rubric dimension scores ≥ 4 or the user stops you.

## Which reference to load

| Situation | Load |
|---|---|
| Scoring any render; the eight dimensions with anchors | `references/rubric.md` |
| Writing the output; worked example of a full critique | `references/change-format.md` |

## Rules

- Judge against the design philosophy first (does it keep its own promises?), the
  rubric second. If no philosophy exists, write a one-line inferred intent and say so.
- Diagnose over prescribe when uncertain of intent — but never emit a finding without
  a proposed exact value. Uncertainty goes in a parenthetical, not in vagueness.
- Strengths get one sentence, findings get the rest. Flattery is not calibration.
- Accessibility findings (contrast, motion, hit targets) always rank above aesthetic
  findings, whatever their scores.
