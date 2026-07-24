# Contrast Discipline, Glow, and Saturation Restraint

## Contrast: the floors

WCAG 2.x ratios are the legal/compat floor — compute them, never eyeball:

| Content | Minimum |
|---|---|
| Body text (< ~24px / < 19px bold) | **4.5:1** (AA) |
| Large text (≥ ~24px / ≥ 19px bold) | 3:1 |
| UI components, icons, focus rings, chart marks | 3:1 |
| Decorative / disabled | exempt, but keep disabled ≥ ~2.5:1 findable |

Compute in code rather than by eye. In a browser context, a ~15-line function
suffices (WCAG relative luminance):

```js
const lum = c => { const [r,g,b] = c.map(v => { v/=255;
  return v <= .03928 ? v/12.92 : ((v+.055)/1.055)**2.4 });
  return .2126*r + .7152*g + .0722*b };
const ratio = (a,b) => { const [x,y] = [lum(a),lum(b)].sort((p,q)=>q-p);
  return (x+.05)/(y+.05) };   // pass [r,g,b] arrays 0–255
```

Python: `wcag-contrast-ratio` or ten lines of the same math. Run it over every
(text, background) token pair as a loop, not per-color ad hoc — a palette change
should re-verify the whole matrix.

**Know WCAG's blind spot:** the formula over-rewards dark-on-mid pairs and
under-rewards light-on-dark; APCA (the draft WCAG 3 model) tracks perception better,
especially in dark themes. Practical stance: WCAG AA is the shipping gate; when a
pair passes WCAG but looks weak in a dark theme, trust your rendered screenshot and
add lightness distance anyway. Designing with ΔL ≥ 0.55 (OKLCH) between text and
ground clears both models nearly always.

Beyond the floors: **contrast is hierarchy budget.** Give maximum contrast to the
one thing that matters most and *deliberately less* to everything else. A screen
where every element passes AAA is often a screen with no hierarchy at all — muted
(but passing) secondary text is what makes primary text loud.

## Never encode meaning in hue alone

Red/green deltas, chart series, form errors: pair every hue signal with a second
channel — icon, weight, label, position, or lightness step. ~4% of users won't see
the hue; everyone benefits from redundancy in sunlight.

## Glow: rules of engagement

Glow (outer bloom, text-shadow halos, neon edges) is the most abused effect in
dark-theme design. It works by simulating overexposure — which is precisely why it
only works when rare:

1. **Glow is a spotlight, not a material.** Maximum one or two glowing elements per
   view: the primary action, the live datum, the active state. If everything glows,
   the screen reads as a smeared photo.
2. **Glow must inherit its element's hue** (same H, higher L, low C, blurred).
   White glow on colored elements looks like a rendering bug.
3. **Radius small, opacity low:** start `0 0 12px` at 25–40% opacity and tune down.
   If the glow is visible as a shape rather than felt as light, halve it.
4. **Glow implies energy — animate it only if the energy is real** (recording,
   live, processing). A pulsing glow on a static feature is a lie the user learns
   to ignore.
5. Light themes almost never earn glow; use shadow and chroma instead.

## Saturation restraint

- **The 60-30-10 dominance rule:** ~60% of pixels neutral ground, ~30% secondary
  surfaces/muted color, ≤ 10% full-chroma accent. Accents get their power from
  scarcity — a screen that is 40% accent-colored has no accent.
- **One loudest color per view.** When adding a second saturated hue, ask what it
  *means*. Color without assigned meaning is noise; users try to read it anyway.
- **High chroma + large area = fatigue.** Full-bleed saturated backgrounds work for
  posters and hero moments (seconds of viewing), not work surfaces (hours). For
  sustained UIs, cap large-area chroma near 0.04–0.06 and spend full chroma on
  small elements.
- **Text on saturated grounds:** prefer near-white or near-black derived from the
  ground hue (`accent-text` token), never a second saturated color.
