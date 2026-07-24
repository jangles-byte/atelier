---
name: performance-craft
description: Design that holds its frame rate — because janky motion is failed design, not a separate engineering concern. Per-platform rendering discipline: compositor-friendly CSS and GPU layers on the web; ProMotion/adaptive-refresh timing, Metal particle/overdraw budgets, and efficiency-core scheduling on Apple platforms; draw-call and fill-rate budgets in game engines. Includes the graceful-degradation ladder — what to cut first when the frame budget is blown. Use this skill whenever animation stutters, scrolling janks, "feels laggy", fans spin up, battery drains from an always-on animation, before shipping ANY continuous animation (particles, ambient motion, canvas/WebGL scenes), or when choosing which properties/effects to animate.
---

# Performance Craft

A dropped frame is a design defect the user feels before they can name it. This
skill treats the frame budget as a design material: know the budget, spend it on
what the philosophy values, and degrade in the order that does the least visual
damage.

## The budget

Frame time = 1000 / refresh rate: **8.3ms at 120Hz, 16.6ms at 60Hz** — minus the
platform's own compositing overhead. Design for the *display the audience has*:
ProMotion phones and most gaming displays are 120Hz; never hardcode 60. Measure
before and after any motion work — profilers, not vibes (DevTools Performance /
Instruments' Animation Hitches / engine profilers).

## Which reference to load

| Situation | Load |
|---|---|
| Web: CSS/JS/canvas/WebGL animation, scroll jank, layout thrash | `references/web-rendering.md` |
| Apple: SwiftUI/UIKit hitches, Metal, ProMotion, battery/thermals | `references/apple-silicon.md` |
| Game engines, particles at scale, and the degradation ladder | `references/budgets-and-degradation.md` |

## Non-negotiables

- Animate compositor-friendly properties (transform, opacity — and their platform
  equivalents) unless a measured reason says otherwise.
- Timing from delta-time or the platform's frame callback, never a hardcoded
  1/60 assumption.
- Always-on ambient animation must be provably cheap: paused off-screen, GPU-only,
  and off the performance cores / not preventing CPU idle.
- `prefers-reduced-motion` (and platform equivalents) is also the low-power path —
  wire them together.
- When the budget is blown, cut by the degradation ladder — never ship the stutter,
  and never fix it by cutting the design's primary feedback motion first.
