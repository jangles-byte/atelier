# Diagnostic: dead motion (third medium — interaction)

*Runs the `motion` skill's [dead-motion diagnostic](../skills/motion/references/dead-motion-diagnostic.md)
and the `performance-craft` rules on a real interaction. The two pages —
[`motion-before.html`](motion-before.html) and [`motion-after.html`](motion-after.html) —
have **byte-identical markup and static CSS**. Only the motion block differs, so the
static screenshots are the same and motion is the isolated variable.*

Every number below was sampled per animation frame in Chrome
(`getBoundingClientRect()` on each card, every frame, normalized 0–1), not estimated.

## Diagnosed failures in `motion-before.html`

| Check | Finding | Evidence (measured) |
|---|---|---|
| **§1 linear?** | `transition: all 300ms linear` | Progress rose in equal 0.055 steps every frame, matching `t/300` to within 0.03 at every checkpoint — a dead-straight line |
| **§2 uniform durations?** | one 300ms for hover, card entrance, and panel alike | no weight information: a 7px dot and a full panel move identically |
| **§3 start/stop together?** | no stagger | all five cards first moved at **21.1ms** — spread of **0.0ms** |
| **§4 overshoot** | none anywhere | — |
| **§6 wrong property?** | animates `top` (layout stage) and hovers on opacity alone | `top: 20px → 0` on a positioned element; `:hover { opacity: .85 }` |
| **§7 missing exit?** | panel has no exit at all | closes via `display: none` — it vanishes between frames |
| **§8 no causality?** | panel appears centered regardless of origin | no `transform-origin`, no relationship to the clicked card |
| **§11 shouldn't exist** | permanent `requestAnimationFrame` loop | **60 callbacks/second during idle**, forever, writing inline opacity to one 7px dot |

## Applied changes (exact values)

1. **§1/§2 curves and scale:** `all 300ms linear` → scoped transitions on a duration
   ladder — `--t-micro: 130ms` (hover/press), `--t-card: 260ms` (entrance),
   `--t-panel: 380ms` — with `--ease-out: cubic-bezier(0.22, 1, 0.36, 1)` on
   entrances and `--ease-in: cubic-bezier(0.55, 0, 1, 0.45)` on exits.
2. **§3 stagger:** `transition-delay: min(i, 8) * 40ms` per card.
3. **§6 properties:** `top` → `transform: translateY(14px) scale(0.985)`; hover
   composes three channels (`translateY(-2px)`, `scale(1.006)`, border-color) instead
   of dimming opacity.
4. **§4 press:** `:active { scale(0.984) }` at 90ms, released through
   `--ease-back: cubic-bezier(0.34, 1.56, 0.64, 1)` (≈10% overshoot).
5. **§7 exit:** panel gains a real closing state at `380ms × 0.8 = 304ms` with
   `ease-in`, sheet leaving on `scale(0.94) translateY(6px)`.
6. **§8 causality:** `transform-origin` computed from the clicked card's center, so
   the sheet grows out of whatever the user actually touched.
7. **§9 interruption:** the pending close timer is cancelled on reopen, so
   mash-clicking never leaves the panel stranded.
8. **§11 / performance-craft:** the permanent rAF loop → a declarative CSS
   `@keyframes pulse` the compositor owns and the browser throttles off-screen.
9. **Reduced motion:** a complete path, not a kill switch — color and opacity
   feedback survive; travel, scale, stagger and ambient pulse do not.

## Measured result

| Metric | Before | After |
|---|---|---|
| Progress at 40ms | 11% | **49%** (4.4× further) |
| Progress at 130ms | 44% | **96.5%** (visually finished) |
| Stagger spread across 5 cards | 0.0ms | **149.9ms** (~33–40ms apart) |
| rAF callbacks during 1s idle | **60** | **0** |
| Ambient driven by | JS, every frame | CSS/compositor |
| Frame time p95 during entrance | 17.9ms | 17.1ms |

The eased card is **4.4× further along at 40ms** and done by 133ms while the linear
card is still at 44%. That gap is what "snappy" is, expressed as a number rather than
an adjective — and the linear curve's perfectly equal per-frame increments are the
signature of the uniform velocity that reads as mechanical.

**One honest note on the frame times:** 17.9 → 17.1ms p95 is a real but small
improvement, because this is a five-card page on an M-series Mac — the layout-property
sin does not bite until the page is heavy or the device is weak. The unambiguous
performance win here is the idle one: 60 wake-ups per second, forever, reduced to zero.
That is the cost that shows up as battery drain rather than as jank, which is exactly
why `performance-craft` treats always-on animation as its own budget line.
