# Palette Construction

A repeatable method: anchor → neutrals → accent ramp → semantics → data series.
Every value in OKLCH; hex is the export.

## Step 1 — Anchor hue

One hue angle, chosen from the design philosophy's emotional register:

| Register | Hue range |
|---|---|
| trust / calm / technical | 230–265 (blue–indigo) |
| growth / money / go | 140–160 (green) |
| energy / urgency / appetite | 25–45 (red–orange) |
| warmth / craft / paper | 60–90 (amber–yellow) |
| premium / night / mystery | 280–320 (violet–magenta) |
| clinical / cold | 190–210 (cyan) |

Then interrogate it: is this the *default* hue for the domain? (Fintech defaults
blue-260, health defaults teal.) Following the default is a choice the philosophy
must make consciously — often a 15–30° rotation off the default (indigo → 285
periwinkle; teal → 165 sea-green) keeps the register while escaping the template.

## Step 2 — Tinted neutral ramp

Neutrals do 90% of the interface's work. Build 8–10 steps with the anchor hue at
whisper chroma:

```
L:  0.98  0.95  0.90  0.82  0.70  0.55  0.42  0.30  0.22  0.15
C:  0.005 0.006 0.008 0.010 0.012 0.012 0.010 0.010 0.008 0.008
H:  <anchor>  (optionally drifting ±10° warm at light end, cool at dark end)
```

The even-L spacing above is intentionally *not* uniform in usage: interfaces need
many light steps (backgrounds, borders, hovers) and few mid steps. Pure-grey
(C = 0) neutrals are permitted only when the philosophy explicitly calls for
achromatic ("color is data") — and even then, test both; tinted usually wins.

## Step 3 — Accent ramp

Same L ladder, chroma following a peak curve:

```
L:  0.95  0.85  0.75  0.65  0.55  0.45  0.35
C:  0.03  0.08  0.13  0.17  0.19  0.16  0.12     (peak near L 0.55–0.65)
H:  anchor ± small drift
```

Pick the **working accent** — the step used for buttons/links — by contrast, not
vibes: it must hit ≥ 4.5:1 against the page background if it ever carries text-sized
meaning, ≥ 3:1 for large UI shapes. In light themes that's usually L 0.45–0.60; in
dark themes L 0.65–0.78.

## Step 4 — Semantic tokens

Name colors by role, never by appearance, so themes can swap under them:

```
bg, bg-elevated, bg-sunken        (surface ladder)
text, text-muted, text-faint
border, border-strong
accent, accent-hover, accent-text (text *on* accent)
danger, warning, success, info
```

Semantic hues stay conventional (danger ≈ 25, warning ≈ 75, success ≈ 150, info ≈
240) but get *tuned to the palette*: match their chroma ceiling and lightness ladder
to the accent ramp so alerts feel native, not pasted in. If the anchor is near a
semantic hue (a green brand vs. success-green), separate them by lightness and
chroma, or shift the semantic 10–15°.

## Step 5 — Data-viz series (when charts exist)

Categorical series need **equal perceived weight**: same L (±0.03), same C (±0.02),
hues ≥ 40° apart, anchored so series 1 = the brand accent. Six is the practical
ceiling before direct labeling must replace the legend.

```
series: L 0.62 C 0.15, H = anchor, anchor+55, anchor+130, anchor+190, anchor+250
```

Sequential ramps: vary L monotonically (0.90 → 0.30) with the peak-chroma curve and
≤ 40° hue drift. Diverging: two such ramps meeting at a *neutral* midpoint (C ≤
0.02) — never white unless the background is white. Check all series in a
color-blindness simulator; if two series survive only by hue, add a lightness step
between them.

## Output format

Ship the palette as tokens with OKLCH as source of truth and hex as export:

```css
--accent: oklch(65% 0.19 285);        /* #7c6cf0 */
```

```python
PALETTE = {"accent": "#7c6cf0"}  # oklch(65% 0.19 285) — regenerate via coloraide
```

A palette is not done until it has been rendered in the real artifact — colors that
work as swatches routinely fail at real proportions (a 60-30-10 dominance test:
neutral ~60%, secondary surface ~30%, accent ≤ 10% of pixels).
