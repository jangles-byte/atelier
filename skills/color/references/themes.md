# Theme Families: Dark and Light as Siblings

A dark theme is not an inverted light theme. Inversion breaks three ways: mid-tone
chroma turns neon on dark grounds, shadows stop working (they need light to occlude),
and pure-black backgrounds make halation (light text smearing) worse for astigmatic
users — roughly half the population. Build the dark theme as a sibling: same anchor
hue, same token names, re-derived values.

## Dark theme construction rules

1. **Ground is dark, not black.** Base surface L 0.14–0.22, tinted with the anchor
   (C 0.008–0.02). Reserve L < 0.10 for OLED-first media UIs where battery and
   letterboxing matter.
2. **Elevation = lightness, not shadow.** Dark UIs communicate "raised" by lightening
   the surface (+0.03–0.05 L per level, 3 levels max). Shadows may remain but as a
   supporting cue only.
3. **Drop text below white.** Primary text L 0.90–0.93 (not 1.0) to reduce halation;
   muted text ~0.65; faint ~0.50. Check muted text still clears 4.5:1 — it is the
   most common dark-mode contrast failure.
4. **Desaturate and lighten accents.** The light theme's working accent (say L 0.55
   C 0.19) becomes roughly L 0.70–0.75, C 0.12–0.15 in dark. Saturated mid-tones on
   dark grounds vibrate; lightened, gently de-chroma'd versions read as the same
   brand color without the buzz.
5. **Semantic colors follow the same shift.** Dark-theme danger/success/warning are
   lighter and calmer than their light-theme selves, and their *tints* (alert
   backgrounds) become dark tinted surfaces (L ~0.25, C ~0.04) rather than pastels.
6. **Images and glow.** Media keeps its own color; UI around it gets quieter in dark
   themes. Glow effects (see `contrast-and-restraint.md`) are dark-theme currency —
   which is exactly why they must stay rationed.

## Symmetric token derivation

Both themes derive from one source table — hue and role are shared; L and C are
per-theme:

| token | light (L / C) | dark (L / C) |
|---|---|---|
| bg | 0.97 / 0.005 | 0.16 / 0.012 |
| bg-elevated | 1.00 / 0 | 0.20 / 0.012 |
| bg-sunken | 0.94 / 0.008 | 0.13 / 0.010 |
| text | 0.20 / 0.01 | 0.92 / 0.008 |
| text-muted | 0.45 / 0.01 | 0.65 / 0.008 |
| border | 0.88 / 0.01 | 0.28 / 0.012 |
| accent | 0.55 / 0.19 | 0.72 / 0.14 |
| accent-text | 0.98 / 0.01 | 0.15 / 0.02 |

(Hue = anchor throughout. Values are starting points; contrast-check after tuning.)

## Per-stack wiring

**CSS** — tokens once, themes as custom-property swaps; respect the OS and allow
override:

```css
:root          { --bg: oklch(97% 0.005 260); --text: oklch(20% 0.01 260); }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --bg: oklch(16% 0.012 260); --text: oklch(92% 0.008 260); }
}
:root[data-theme="dark"] { /* same dark values — explicit user choice wins */ }
```

Set `color-scheme: light dark` on `:root` so form controls and scrollbars follow.

**SwiftUI / Compose** — use the platform's semantic system (Asset Catalog
"Any/Dark", `MaterialTheme` light/dark color schemes) and populate it from the same
table; never branch on theme in view code — views read roles only.

**Data viz / plotting** — a dark chart theme changes more than the background:
gridlines drop to ~0.30 L hairlines, series colors lighten (+0.10–0.15 L) and
de-chroma slightly, and white is banned as a series color. Matplotlib: keep two
style sheets generated from the same token table rather than hand-editing both.

## Testing a theme pair

Render the same real screen in both themes side by side and check: same hierarchy
order (what reads first/second/third must not change), all text pairs pass 4.5:1,
elevated surfaces distinguishable in both, brand accent recognizably "the same
color", and no element that is loud in one theme and invisible in the other. Then
run the `critique` skill on each.
