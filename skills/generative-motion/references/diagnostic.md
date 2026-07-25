# The Generative Diagnostic

Run this when a piece is built but wrong. Work the symptom you actually see, in the order
given — each check is cheaper than the one after it, and most failures are found in the
first two.

The governing principle: **separate simulation failures from rendering failures before
tuning anything.** They look identical on screen and have opposite fixes. The one-line test
is to render the raw field with no colour treatment (`o = vec4(vec3(field * 0.01), 1.0)`,
adjusting the multiplier by orders of magnitude). If structure appears, the simulation is
fine and every subsequent change belongs in tone and colour.

---

## "It's a black frame"

1. **Did anything throw?** A shader that failed to compile, or an exception during init,
   leaves a canvas that never paints. Check the console; check `COMPILE_STATUS` and
   `LINK_STATUS` explicitly, because a failed program draws silently.
2. **Is the field actually zero?** Raw-field test above. If the field has values but the
   screen is black, it's tone — jump to the next section.
3. **On GPU: is blending on a float target?** Writes are silently discarded without
   `EXT_float_blend`. Use `R16F`/`RGBA16F` for accumulation. See
   [`gpu-and-shaders.md`](gpu-and-shaders.md).
4. **On GPU: `checkFramebufferStatus`.** Anything but `FRAMEBUFFER_COMPLETE` means the
   format isn't renderable — a missing float extension almost every time.
5. **Are particles off-screen?** Print the first few positions. Seeding in normalised 0–1
   coordinates while drawing in pixels puts the whole population in one corner pixel.

## "It saturates to flat white"

Your tone curve has no floor, so the field average already exceeds the ceiling. This is a
mapping failure, not a simulation failure — the structure is there, you just can't see
inside it. Subtract a floor before scaling; see
[`density-and-tone.md`](density-and-tone.md). Reducing deposit instead is the tempting fix
and usually the wrong one: it weakens the feedback the system needs and changes the
structure rather than revealing it.

## "It's a few thin outlines on black"

The opposite: the floor is too high and is eating the body of the structure. Also check for
an over-aggressive `pow()` or a `smoothstep` band that's too narrow.

## "It dies to an empty frame"

- **Decay exceeds deposit.** Equilibrium is `deposit × elements_per_cell / (1 − decay)`; if
  that's below your visible threshold the field never establishes.
- **Everything escaped.** Particles left the viewport and were never recycled. Wrap or
  respawn, and count live elements every second while debugging.
- **N-body without softening.** Close passes produce near-infinite forces and eject
  everything. `r² = max(r², softening)` with softening 400–2000 is mandatory.
- **Energy drained.** Drag applied per frame instead of per second: `v *= 0.98` runs twice
  as fast at 120Hz. Use `v *= pow(0.98, dt*60)`.

## "It explodes / goes to infinity"

- **`dt` not clamped.** A tab-switch or a slow first frame integrates a multi-second step.
  `dt = min(dt, 1/30)` everywhere, and reset the timestamp on resume.
- **Spring stiffness too high for the step.** Semi-implicit Euler is stable only up to
  roughly `dt < 2/√k`. Either lower `k`, substep the integration, or move to Verlet.
- **Feedback loop at gain ≥ 1.** Any accumulation buffer needs decay strictly below 1.0.

## "Everything clumps into a few thick strands"

The system is over-converging. In trail-following systems this specifically means:

- **Occupancy too high.** Agent count per cell above ~40% fuses the network into trunks.
  Raise grid resolution or lower population — physarum wants ~10–15%.
- **Step size under one cell per frame.** An agent that doesn't leave its cell deposits into
  it repeatedly, over-saturating locally. Target ~1px per frame.
- **Diffusion too weak.** Counter-intuitively, *more* blur produces *finer* networks: the
  blur is what lets agents sense trails at range and connect to them. Partial diffusion
  keeps trails narrow, so agents lock onto their own path and form isolated worms.
- **No exploration.** Fully deterministic steering collapses; keep a random component in
  the turn.

## "It looks like a tutorial"

Not a bug — a direction failure. Run the checklist in
[`art-direction.md`](art-direction.md). The usual four: rainbow hue, uniform density, pure
black ground, everything at one scale.

## "It runs at 4fps"

- **Count passes × pixels**, not objects. Four fullscreen passes at 1080p is 8.3M fragment
  invocations before anything else.
- **Are you reading back?** `readPixels`/`getImageData` per frame stalls on the GPU
  finishing. Move it to once a second or eliminate it.
- **Per-object draw calls.** Thousands of `stroke()` calls dominate over the pixels they
  cover; batch into colour buckets, or move to GPU.
- **Blur kernels.** Separate into 1D horizontal + vertical passes; run glow chains at half
  resolution.
- **O(n²) neighbour queries.** Boids above ~800 agents needs a spatial hash.

## "It flickers or strobes"

- **Reading and writing the same texture in one pass.** Undefined; ping-pong properly.
- **No spawn envelope.** Particles popping in and out at full opacity. Fade both ends.
- **Whole population sharing a lifetime.** Stagger initial ages at startup or everything
  dies at once and the piece pulses.
- **Bloom threshold too hard.** Pixels crossing it pop; use a soft knee.

## "It's beautiful for ten seconds, then grey mush"

The most common late failure, and the reason to run the **minute test** before shipping.
Trails saturate as the field reaches equilibrium; particles pool in attractor basins;
networks consolidate. Fixes: adaptive normalisation so tone tracks the field, a slow
parameter drift so the system never settles, periodic partial resets, or simply choosing
the phase you want and looping there. A piece that only looks right in its first eight
seconds is a piece with an eight-second loop, and that is a legitimate answer.
