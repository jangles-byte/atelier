---
name: color
description: Build perceptually coherent color systems in OKLCH — palettes, ramps, semantic tokens, dark/light theme families, and contrast discipline. Use this skill whenever choosing ANY colors for visual work: UI themes, brand palettes, data-visualization series colors, game graphics, generative art, slides, or syntax themes. Trigger on requests like "pick colors", "make a palette", "add dark mode", "this color looks off", "improve the theme", "what color should the chart series be", or whenever you are about to write a hex code into any file.
---

# Color

Color decisions in this package are made in **OKLCH** (perceptual lightness L, chroma
C, hue H), not hex or HSL, because equal numeric steps in OKLCH are equal *perceived*
steps — which is what makes ramps even, themes coherent, and contrast predictable.
Hex is only an output format.

## Workflow

1. Read the design philosophy (from `design-direction`); the palette's emotional
   register comes from there, not from this skill.
2. Construct the palette in OKLCH using
   [references/palette-construction.md](references/palette-construction.md) — anchor
   hue → neutral ramp (tinted, never pure grey) → accent ramp → semantic colors.
3. If the work has themes, build dark and light as **sibling palettes, not
   inversions**, per [references/themes.md](references/themes.md).
4. Verify every text/background pair against
   [references/contrast-and-restraint.md](references/contrast-and-restraint.md)
   before shipping; it also covers when glow/saturation is earned vs. noise.

## Which reference to load

| Situation | Load |
|---|---|
| OKLCH mechanics, converting, browser/tool support | `references/oklch-foundations.md` |
| Building a palette, ramps, data-viz series colors | `references/palette-construction.md` |
| Dark mode, theme families, elevation in dark UIs | `references/themes.md` |
| Contrast checking, WCAG/APCA, glow & saturation discipline | `references/contrast-and-restraint.md` |

## Non-negotiables

- Body text meets WCAG AA (4.5:1) minimum; UI chrome ≥ 3:1. Check, don't eyeball.
- Neutrals carry a trace of the anchor hue (C ≈ 0.005–0.02). Pure grey reads dead.
- One color is the loudest in any view. If two compete, demote one.
- Never ship a palette without rendering it in the real artifact and running the
  `critique` skill on the result.
