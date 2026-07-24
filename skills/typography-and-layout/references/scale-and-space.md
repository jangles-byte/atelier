# Scale Systems and the Spacing Ladder

## Modular type scale

Sizes come from a ratio, not from taste-per-element. Pick the ratio by medium:

| Ratio | Name | Character | Best for |
|---|---|---|---|
| 1.2 | minor third | quiet, dense | dashboards, tools, docs |
| 1.25 | major third | balanced default | product UI, marketing |
| 1.333 | perfect fourth | editorial confidence | content sites, blogs |
| 1.5–1.618 | fifth / golden | dramatic | posters, slides, heroes |

Generate from a 16–18px base, round to sensible pixels, and **name the steps**
(`text-sm/base/lg/xl/2xl…` or `caption/body/h3/h2/h1/display`). Two scales can
coexist deliberately: a tight ratio for the interface plus a dramatic ratio for
display moments — what looks broken is *one* scale applied timidly.

The senior tell is the top end. Templates stop at ~3× body. Editorial and hero
contexts want 4–8× (64–128px+ desktop), with the drop in tracking and line-height
that size demands. If the philosophy calls for impact and the largest text is 40px,
the scale is failing the philosophy.

**Fluid scale (web):** interpolate between a phone size and a desktop size instead
of breakpoint jumps:

```css
--step-5: clamp(2.5rem, 1.5rem + 4.5vw, 5rem);   /* display: 40px → 80px */
--step-0: clamp(1rem, 0.95rem + 0.25vw, 1.125rem); /* body: 16px → 18px */
```

Fluid steps should use a *larger* ratio at desktop than mobile (viewport-relative
term bigger on high steps) — big screens earn more drama.

## Line-height: inverse to size

| Context | Line-height |
|---|---|
| Display ≥ 48px | 0.95–1.1 |
| Headings 24–48px | 1.1–1.25 |
| Body 14–18px | 1.4–1.6 |
| Captions/labels ≤ 13px | 1.3–1.4 |
| Data tables | 1.2–1.35 + row padding doing the breathing |

Multi-line display type at body line-height (the default) is the most common
amateur tell — `line-height: 1` on a 96px headline is usually *still too loose*.

## Measure

Body text: **45–75 characters per line** (~ `max-width: 65ch`). Under 40ch chops
rhythm; over 90ch loses the return sweep. Wide layouts don't justify wide text —
use columns, a narrower text block placed asymmetrically, or larger type. Headlines
tolerate 8–20ch. Center-aligned text: 3 lines maximum, then left-align.

## The spacing ladder

All space from one geometric-ish ladder, 4px base:

```
4  8  12  16  24  32  48  64  96  128  (192 for section breaks)
```

Tokens, not raw numbers (`--space-1…--space-10`). The ladder's power is the *gaps*
in it: because 20 and 40 don't exist, near-miss inconsistencies can't creep in.

**Proximity beats quantity.** Space encodes grouping: the gap between unrelated
groups must be ≥ 2× the gap inside a group. A label sits closer to its field than
to the previous field; a heading sits closer to its paragraph than to the section
above (e.g. `margin-top: 48px; margin-bottom: 16px`). Uniform spacing everywhere is
how layouts read as "flat" even when every individual value is reasonable.

**Padding proportionality:** container padding scales with container size — cards
16–24, modals 24–32, page sections 64–128 vertical. Small padding on large surfaces
reads as cramped; huge padding on small elements reads as lost.

## Per-stack notes

**CSS** — tokens as custom properties; `gap` over margins where flex/grid allows
(margins leak, gaps don't); logical properties (`margin-block-start`) if RTL is
plausible.

**SwiftUI** — mirror the ladder in a `Spacing` enum; use it in `VStack(spacing:)`
and `.padding()`; let the type scale ride on Dynamic Type text styles
(`.largeTitle`…`.caption2`) re-weighted to your ratio via custom `Font` extensions.

**Matplotlib / plotting** — the same ideas map directly: `rcParams` for a real
scale (`axes.titlesize` ≥ 1.5× `axes.labelsize` ≥ 1.2× `xtick.labelsize`),
`constrained_layout` for spacing, and title padding (`axes.titlepad`) larger than
tick padding — a chart whose title crowds its axes reads as flat exactly like a
heading at uniform spacing.
