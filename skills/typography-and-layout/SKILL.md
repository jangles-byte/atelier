---
name: typography-and-layout
description: Typography with intent and composition with rhythm — type pairing, modular scale systems, grids (and when to break them), negative space, and visual hierarchy. Use this skill whenever setting ANY text styles or arranging ANY elements on a surface: choosing fonts, sizing headings, building a landing page or app screen layout, laying out a slide, spacing a dashboard, composing a poster or chart, or when a design "feels cramped", "feels empty", "looks flat", or "the hierarchy is off". Trigger even when the user only says "make this look better" — type and spacing are usually why it doesn't.
---

# Typography & Layout

Typography is most of design: get type and spacing right and a screen looks designed
before it has any color or decoration. The failure mode is timidity — small scale
jumps, default tracking, uniform spacing — not bad taste.

## Workflow

1. Read the design philosophy (`design-direction`); the type *voice* comes from there.
2. Choose faces and pairings with
   [references/type-pairing.md](references/type-pairing.md) — contrast on exactly one
   axis, two families maximum.
3. Build a modular scale and spacing system with
   [references/scale-and-space.md](references/scale-and-space.md) — sizes, line
   heights, measure, and the spacing ladder, as tokens.
4. Compose with [references/composition.md](references/composition.md) — grid,
   hierarchy channels, negative space, and the sanctioned ways to break the grid.
5. Render at real size and run the `critique` skill. Type that looks right in code
   is routinely wrong on screen.

## Which reference to load

| Situation | Load |
|---|---|
| Picking fonts, pairing display + text faces, font features | `references/type-pairing.md` |
| Setting sizes, line-height, measure, spacing ladder | `references/scale-and-space.md` |
| Arranging a page/screen/slide, hierarchy problems, grids | `references/composition.md` |

## Non-negotiables

- Two font families maximum (a third only for code/data, and it counts if decorative).
- A real scale ratio, and at least one jump ≥ 3× body size somewhere in display
  contexts (heroes, slides, posters); interfaces cap lower but still need contrast.
- Body measure 45–75 characters; line-height inversely proportional to size.
- Spacing from a ladder (4/8-based), applied asymmetrically: space *groups*, not
  elements — more space between sections than inside them, always.
- Tabular numerals (`font-variant-numeric: tabular-nums` or a mono) for any column
  of numbers that can change.
