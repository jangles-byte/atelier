# OKLCH Foundations

## The model

`oklch(L C H)`:

- **L — lightness, 0–1** (written as 0–100% in CSS). Perceptually uniform: a ramp
  with L = 0.95, 0.85, 0.75… *looks* evenly stepped. This is the property HSL lacks —
  in HSL, yellow at 50% lightness is blindingly bright while blue at 50% is dark, so
  HSL ramps are visually lumpy and HSL-derived "same lightness" pairs aren't.
- **C — chroma, 0–~0.4.** Colorfulness. 0 is achromatic. Usable ceilings vary by hue
  and lightness (sRGB can express far more chroma in mid-lightness greens than in
  light blues). There is no fixed max — clip-aware tools matter.
- **H — hue angle, 0–360.** Roughly: 30 red, 90 yellow, 145 green, 195 cyan, 260
  blue, 320 magenta. Perceptually spaced: +20° is a similar-feeling hue step
  anywhere on the wheel, unlike HSL's crowded greens.

Two consequences worth internalizing:

1. **Contrast is (mostly) a lightness story.** Perceived text contrast tracks ΔL far
   more than ΔC or ΔH. A rule of thumb that works: body text needs ΔL ≥ ~0.55 from
   its background; large display text can drop to ~0.40. Always confirm with a real
   checker (see `contrast-and-restraint.md`) — but *design* in L, and contrast
   mostly takes care of itself.
2. **Chroma is not free.** As L approaches 0 or 1, available chroma collapses. Dark
   themes that keep light-theme chroma values produce neon smearing; light pastels
   that keep mid-tone chroma clip to grey. Ramps need a chroma *curve*, not a chroma
   constant (peak chroma near L 0.55–0.65, tapering toward both ends).

## Gamut and clipping

sRGB cannot display all OKLCH values. When a color clips, browsers/tools gamut-map it
— usually by desaturating — so two colors you defined as "same chroma" may render
differently. Discipline: keep UI chroma ≤ 0.15 for broad safety, ≤ 0.25 when
targeting Display-P3, and spot-check ramp endpoints. `color(display-p3 …)` and
`@media (color-gamut: p3)` unlock wider accents on modern screens; always define the
sRGB fallback first.

## Using it per stack

**CSS** — native, all modern browsers (2023+):

```css
:root {
  --ink:    oklch(20% 0.01 260);
  --paper:  oklch(97% 0.005 260);
  --accent: oklch(65% 0.19 145);
  --accent-hover: oklch(from var(--accent) calc(l - 0.07) c h); /* relative color */
}
```

`oklch(from …)` (relative color syntax) derives hover/active/disabled states from one
token — the pattern that keeps systems coherent.

**Swift / Kotlin / game engines** — no native OKLCH type; convert at design time, ship
sRGB/Display-P3 values, and keep the OKLCH source as the palette's source of truth
in a comment or design-token file:

```swift
// oklch(65% 0.19 145)
static let accent = Color(red: 0.204, green: 0.678, blue: 0.416)
```

For runtime interpolation (gradients, animated color), interpolate in OKLab — the
rectangular form of the same space — to avoid the grey dead zone that RGB lerps
produce between complementary colors. OKLab↔sRGB is ~20 lines of math (Björn
Ottosson's reference implementation) and worth vendoring into any engine that
animates color.

**Python / data viz** — the `coloraide` package speaks OKLCH directly:

```python
from coloraide import Color
ramp = [Color("oklch", [l, 0.14 * (1 - abs(l - 0.6) * 1.6), 260]).convert("srgb").to_string(hex=True)
        for l in (0.30, 0.45, 0.60, 0.75, 0.90)]  # chroma tapers off mid-peak
```

Matplotlib/plotly accept the resulting hex; the ramp will be perceptually even where
a `Blues` slice or HSL sweep is not.

## Quick vocabulary for palette work

- **Ramp / scale:** one hue at many lightnesses (the "blue-100…blue-900" family).
- **Tinted neutral:** grey with C 0.005–0.02 at the anchor hue. All Atelier neutrals
  are tinted.
- **Hue drift:** intentionally shifting H a few degrees across a ramp (e.g. shadows
  drift cool, highlights drift warm) — small drift (≤15°) makes ramps feel organic
  rather than mechanical.
