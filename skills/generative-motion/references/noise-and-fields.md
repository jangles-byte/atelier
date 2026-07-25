# Noise, Fields and Flow

Most beautiful generative motion is a **field being sampled**: at every point in space
there is a direction or a value, and things move according to it. Get the field right and
the motion is right.

## Noise: which one, and why it matters

- **Value noise** — cheap, blocky, fine for slow drift. Interpolate with smoothstep, never
  linearly (linear gives visible diamond artefacts).
- **Perlin (gradient) noise** — the default. Smooth, isotropic, mildly grid-aligned.
- **Simplex/OpenSimplex** — fewer directional artefacts, scales better to 3D/4D. Prefer it
  when the grid alignment of Perlin starts showing as horizontal/vertical banding.
- **Worley/cellular** — distance to feature points; gives cracks, scales, cells. `F2 − F1`
  is the classic edge look.

**Use one more dimension than your space.** For 2D motion, sample 3D noise with time as
the third axis: `noise(x·s, y·s, t)`. This makes the field *evolve* instead of *scroll* —
scrolling reads as a moving texture, evolving reads as weather. The distinction is the
single biggest quality tell in flow-field work.

## fbm — where the detail comes from

One octave of noise is a smooth blob field. Fractal Brownian motion sums octaves at
doubling frequency and halving amplitude:

```
fbm(p) = Σᵢ₌₀ⁿ⁻¹  amp·noise(p · freq) ,  freq *= lacunarity (≈2.0) , amp *= gain (≈0.5)
```

**Ranges:** 2 octaves for flow fields (more makes the motion jittery rather than
detailed), 4–6 for textures and heightfields. Gain above 0.5 gets noisy; below 0.4 the
detail vanishes. Vary lacunarity slightly off 2.0 (1.93, 2.07) to break repeating
alignment.

## Domain warping — the single best trick

Feed noise into the *coordinates* of more noise. This is what makes fields look like
marble, smoke, or ink rather than clouds:

```
q = ( fbm(p),                fbm(p + (5.2, 1.3)) )
r = ( fbm(p + 4·q + (1.7, 9.2)),  fbm(p + 4·q + (8.3, 2.8)) )
value = fbm(p + 4·r)
```

The offsets are arbitrary decorrelation constants; the `4·` factors are warp strength —
1–2 is subtle, 4 is the classic look, 8+ turns to chaos. Two levels of warp (q then r) is
almost always enough. Animate by evolving the innermost noise's time axis only: the
structure then *breathes* instead of sliding.

## Turning a field into motion

**Angle field (reliable, what most flow fields use):**
```
θ = fbm(x·s, y·s, t·e) · TAU · k        # s ≈ 0.001–0.004, k ≈ 1.5–3, e ≈ 0.03–0.08
v = (cos θ, sin θ) · speed
```
Spatial scale `s` sets feature size — the most important knob. At 0.001 you get long
sweeping rivers; at 0.006, turbulent detail. `k > 3` makes neighbouring points point
opposite ways and the flow shreds.

**Curl noise (divergence-free — no sources or sinks, so particles never pool):**
```
ε = 0.5 / s                              # epsilon in the SAME units the noise is sampled in
curl = ( (n(x, y+ε) − n(x, y−ε)) / (2ε),  −(n(x+ε, y) − n(x−ε, y)) / (2ε) )
```
The classic bug is choosing ε in pixels while sampling at `p·0.001`, which makes the
derivative vanish and the field read as motionless. Scale ε to the noise domain, then
normalise the result before applying speed.

Curl looks like smoke; angle fields look like currents. Curl is better when you want
particles to keep moving forever without clumping.

**Gradient descent/ascent:** move along `∇f` for growth, cracks, and river-like branching.

## Making a field a composition, not a texture

A field sampled uniformly across the frame is wallpaper. To make a *piece*:

- **Vary density.** Spawn more particles where the field is interesting — high curl
  magnitude, high gradient — and fewer elsewhere. Uniform spawn is the default that makes
  everything look the same.
- **Mask the field.** Multiply speed or spawn probability by a large-scale, slow shape
  (a radial falloff, a soft band, a second very-low-frequency noise). This is what creates
  negative space, and negative space is what makes it read as designed.
- **Crop in.** The interesting region of a field is usually smaller than the frame. Zoom
  until structure fills it.
- **Layer two scales.** A slow, large-scale field for overall drift plus a fast, fine field
  for local detail, at different opacities, gives depth a single field never has.

## Seeding

Always seed the PRNG and the noise permutation table, and print the seed. A generative
piece you cannot reproduce is a piece you cannot iterate on.

```js
const mulberry32 = a => () => { a |= 0; a = a + 0x6D2B79F5 | 0;
  let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
  return ((t ^ t >>> 14) >>> 0) / 4294967296; };
```
Build the noise permutation from that PRNG, not `Math.random()`, or the field changes on
every reload while the particles don't.
