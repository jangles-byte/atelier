---
name: generative-motion
description: Make beautiful algorithmic animation — flow fields, particle systems with trails, strange attractors, slime-mold and boid simulations, reaction-diffusion, domain-warped noise, and shader-driven motion. Use this skill for generative art, creative coding, ambient backdrops, music visualisers, hero backgrounds, screensavers, generative wallpaper, data-driven art, or any request for a "cool animation", "something generative", "abstract motion", "particle effect", "flow field", "noise animation", or work referencing p5.js, Three.js, canvas, WebGL, GLSL, Processing, openFrameworks, TouchDesigner, or shaders. Trigger whenever motion is the artwork rather than the interface.
---

# Generative Motion

The gap between a generative sketch and a generative *artwork* is almost never the
algorithm — the algorithms are public and short. It is art direction: what the colour
means, where the density sits, how slowly it evolves, and what you left out.

A tutorial renders the algorithm. A piece renders a decision.

## Workflow

1. **Write the intent first**, in two or three sentences: what the system *is* (embers on
   a thermal, ink in water, a colony finding food), what the viewer should feel, and the
   one property that earns colour. Skipping this is what produces rainbow noise.
   The `design-direction` skill's philosophy format applies directly.
2. **Pick the system** from [references/systems.md](references/systems.md) — each entry
   has the equations, the parameter ranges that actually look good, and its failure mode.
3. **Build the field and the motion** with
   [references/noise-and-fields.md](references/noise-and-fields.md) — noise, fbm, domain
   warping, curl. Most beautiful motion is a field being sampled.
4. **Decide CPU or GPU early** with [references/gpu-and-shaders.md](references/gpu-and-shaders.md).
   This is architectural, not an optimisation — some systems simply do not express
   themselves below a population the CPU cannot reach, and porting later means rewriting.
5. **Render it well** with [references/rendering.md](references/rendering.md) — trails via
   accumulation, additive blending, envelopes so nothing pops.
6. **Map the field to the screen** with [references/density-and-tone.md](references/density-and-tone.md).
   Accumulation buffers are unbounded and displays are not; this mapping is where
   technically-correct pieces most often look wrong.
7. **Finish it** with [references/post-processing.md](references/post-processing.md) — bloom,
   grain, vignette, grading. The cheapest quality per line of code in the discipline.
8. **Art-direct it** against [references/art-direction.md](references/art-direction.md) —
   the checklist that separates a piece from a screensaver.
9. **Watch it.** Record with `../motion/scripts/capture-motion.py` and look at the result
   over a long run, not one frame. Generative work fails slowly: it looks great at 4
   seconds and turns to grey mush at 60. When something is wrong, work
   [references/diagnostic.md](references/diagnostic.md) rather than tuning at random.

## Which reference to load

| Situation | Load |
|---|---|
| Choosing a system; attractors, boids, physarum, reaction-diffusion, differential growth | `references/systems.md` |
| Noise, fbm, domain warping, curl fields, flow fields | `references/noise-and-fields.md` |
| Trails, blending, buffers, performance at scale | `references/rendering.md` |
| Going GPU: WebGL2 GPGPU, ping-pong, the float-extension minefield, shader systems | `references/gpu-and-shaders.md` |
| Flat white, thin outlines, or any density-to-colour mapping | `references/density-and-tone.md` |
| Bloom, grain, vignette, aberration, feedback, colour grading | `references/post-processing.md` |
| It runs but looks like a tutorial | `references/art-direction.md` |
| It's black / saturating / dying / clumping / 4fps / grey mush | `references/diagnostic.md` |

## Non-negotiables

- **Colour is earned.** Map it to a property the system actually has — velocity,
  curvature, age, density, divergence — never to a rainbow of hue over time. If colour
  encodes nothing, the piece reads as a demo.
- **Seed the randomness.** A composition you like must be recoverable; ship the seed.
- **Delta-time everything**, clamped. A field that runs at double speed on a 120Hz display
  is a broken piece, not a fast one.
- **Evolve slower than feels right.** Field evolution that reads as "alive" in the editor
  usually reads as "busy" on the wall. Halve it, then halve it again.
- **Density needs negative space.** A frame at uniform particle density is noise. Vary it,
  or crop into it.
- **Long-run test.** Run it for a minute before shipping — trails saturate, particles
  clump in attractor basins, and energy either dies or explodes.
