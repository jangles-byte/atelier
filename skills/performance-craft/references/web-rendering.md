# Web Rendering Discipline

## The pipeline, and what each property costs

Style → Layout → Paint → Composite. A property's cost is which stages it re-runs:

| Animate | Triggers | Verdict |
|---|---|---|
| `transform`, `opacity` | composite only | free-tier; the default answer |
| `filter`, `backdrop-filter` | composite (GPU) but expensive per-pixel | budgeted; blur radius is the cost knob |
| `color`, `background-color`, `box-shadow` | paint | fine for small elements; costly full-viewport |
| `width/height/top/left/margin/padding/font-size` | **layout** (+ everything after) | never animate; FLIP it |

**FLIP** converts layout animation to transforms: measure First, apply the end
state, measure Last, Invert with a transform, Play the transform to identity. The
View Transitions API (`document.startViewTransition`) is FLIP built into the
platform — prefer it for route/DOM-state changes where supported.

Layout thrash: interleaved reads (`offsetHeight`, `getBoundingClientRect`) and
writes force synchronous layout per iteration. Batch reads, then writes; per frame,
read in one rAF phase, write after.

## Layers

`will-change: transform` (or a 3D transform) promotes an element to its own GPU
layer: cheap to move, but each layer costs VRAM (~width×height×4 bytes at DPR).
Promote the few elements that actually animate, *before* they animate (promotion
mid-animation causes the very hitch it prevents); demote (remove will-change) when
done. Blanket `will-change` on lists is a memory leak with a CSS syntax.
`backface-visibility` hacks are obsolete — use will-change. Check layer count in
DevTools Layers panel; more than ~10 active layers deserves an explanation.

## Scroll

Scroll handlers must do nothing but record; work happens in rAF or, better, via
**scroll-driven animations** (`animation-timeline: scroll()/view()`) and
`IntersectionObserver`, which keep scroll off the main thread entirely. Parallax
via JS top/left is jank-by-design; parallax via transform inside a
scroll-timeline is compositor-priced. `content-visibility: auto` on long-page
sections skips rendering off-screen content — the cheapest big win on content
sites.

## rAF loops, canvas, WebGL

- Delta-time always: `const dt = (now - last) / 1000` — at 120Hz your callback
  runs twice as often; per-frame increments (`x += 2`) double your animation
  speed on ProMotion. Physics with `dt`, springs with `dt` clamped (≤ 1/30).
- Stop idle loops: no permanent rAF that mostly does nothing. Run the loop while
  animating; cancel on settle; restart on interaction. An idle rAF loop pins a CPU
  core's wake cycle — the battery cost of "always-on" is paid here.
- Pause when hidden: `document.visibilitychange` + IntersectionObserver — ambient
  canvas animations off-screen or in background tabs must fully stop.
- Canvas 2D: batch by state (set fillStyle once, draw many), avoid shadowBlur in
  loops (per-draw Gaussian), pre-render repeated sprites to offscreen canvases,
  and size the canvas to CSS-pixels × DPR exactly (over-sized canvases pay
  quadratic fill cost).
- WebGL/WebGPU: instancing for particles (one draw call for 10k quads), keep
  per-frame uniform updates off allocation paths, and respect that mobile GPUs
  are fill-rate-limited — overdraw (stacked transparent quads) is the usual
  culprit, same math as Metal (see `apple-silicon.md`).

## Reduced motion and low power

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```

…as the blunt fallback, plus designed reduced variants for the animations that
carry meaning (opacity swaps instead of movement — see the `motion` skill).
`navigator.getBattery()` is gone/unreliable; treat reduced-motion as the low-power
signal you actually have, and make ambient effects cheap enough that you don't
need one.

## Verification

DevTools Performance panel with 4×–6× CPU throttle (a mid-range Android is your
median user); look for long tasks during interaction, purple layout blocks inside
animations, and layer explosions. `requestAnimationFrame` timestamp deltas logged
for 5s of your heaviest animation: p95 ≤ budget or the degradation ladder applies
(`budgets-and-degradation.md`).
