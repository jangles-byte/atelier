# Density and Tone: Getting an Unbounded Field onto a Screen

This is the most common way a technically-correct generative piece looks wrong, and it is
almost never discussed. Accumulation buffers, visit counts, trail maps and particle density
are **unbounded** — values grow until decay balances deposit, and that equilibrium depends
on population, resolution and frame rate. Displays are bounded to 0–1. The map between them
is a design decision, and getting it wrong produces exactly two failure images:

- **A flat white blob** — the field average lands above your curve's ceiling, so every
  structure clips to the same value and all internal detail is destroyed.
- **A few thin outlines on black** — the floor is too high, so only the extreme cores
  survive and the body of the structure vanishes.

Both look like the *algorithm* failed. Neither is an algorithm problem.

## Why the naive curve fails

The instinct is `v = log(1 + t) * k`. It fails because it has no floor. If the quiet field
sits at t≈30 and the routes at t≈600, then `log(31)=3.4` and `log(601)=6.4` — the entire
interesting range is compressed into the top half of the curve while the background is
already at 50% brightness. You get a grey wash with slightly brighter noodles.

**Subtract a floor before scaling:**

```glsl
float v = clamp((log(1.0 + t) - FLOOR) * SCALE, 0.0, 1.0);
```

`FLOOR` is roughly `log(1 + background_level)` and `SCALE` is `1.0 / (log(1 + peak) -
FLOOR)`. For the example above: FLOOR ≈ 3.4, SCALE ≈ 1/3.0 ≈ 0.33. The background goes to
zero, the routes span the full range, and the structure appears.

## Finding the floor and scale without guessing

Guessing costs a render each time. Three better options, cheapest first:

**Reason it out.** Equilibrium for a deposit/decay field is
`deposit × elements_per_cell / (1 − decay)`. With 1M agents on 350k pixels, deposit 0.42
and decay 0.955: average ≈ `0.42 × 3 / 0.045` ≈ 28, and routes run 10–30× the average, so
peak ≈ 300–800. That gets you within one iteration.

**Render the raw field first.** Output `vec3(t * 0.01)` and look. If you see structure at
some multiplier, you know the magnitude. This also tells you instantly whether a black
frame is a tone problem or a simulation problem — a distinction worth thirty seconds.

**Normalise adaptively.** Track a running maximum with a slow follow so it can't be spiked
by one hot pixel, and divide by it:

```js
peak += (frameMax - peak) * 0.02;         // seconds-scale adaptation
```
This is what makes a piece robust across resolutions and populations — the composition
survives when someone opens it on a 4K display, where per-pixel density is a quarter of
what you tuned at. **Any piece whose tone constants were tuned at one resolution will look
wrong at another** unless it normalises or scales deposit by pixel area.

## Choosing the curve, not just its range

The curve shape decides what the image is *about*:

| Curve | Behaviour | Use for |
|---|---|---|
| `log(1+t)` | compresses highs hard | huge dynamic range: attractors, visit counts |
| `pow(t, 1/2.2)` | gentle, film-like | trail maps, moderate range |
| `t / (1 + t)` (Reinhard) | asymptotic, never clips | additive glow, HDR-ish accumulation |
| ACES / filmic | S-curve, shoulder + toe | anything that should look photographic |
| `smoothstep(a, b, t)` | hard band | isolating a specific density band |

Reinhard and ACES matter for additive rendering, where overlapping strokes push far past
1.0. They roll the highlights off instead of clipping them, which is the difference between
"glowing" and "blown out". A cheap ACES approximation, worth having in every shader:

```glsl
vec3 aces(vec3 x){ return clamp((x*(2.51*x+0.03))/(x*(2.43*x+0.59)+0.14), 0.0, 1.0); }
```

## Percentile mapping, for when it must be right

For stills and print, map by *distribution* rather than by extremes: build a 256-bin
histogram of the field, find the 1st and 99.5th percentile, and map that range to 0–1. This
is immune to a single hot pixel dragging the whole image dark, and it is how the fractal
flame renderer gets its tonality. On the GPU, compute it once every N frames rather than
every frame — the readback stall is fine at 1Hz, fatal at 60.

## Colour on top of the curve

Only after tone is right should colour go on, because the ramp's shape depends on where
values land. Two rules that carry most of the quality:

**Chroma should rise with lightness, then fall at the very top.** Holding chroma constant
makes bright regions look chalky and washed. `C = 0.02 + v*0.13*(1.0 - v*0.55)` gives a
saturated midtone and a clean near-white core — the shape of real emission.

**Keep the hue span to 40–70°** and let it track the same `v`. A full hue rotation is the
loudest possible signal that no decision was made. In OKLCH, hue in radians in a shader:

```glsl
float L = 0.06 + v*0.90;
float C = 0.02 + v*0.13*(1.0 - v*0.55);
float H = radians(300.0 - v*230.0);       // violet in the quiet field, gold on the routes
```

## The checks

- **Sample the histogram, not the picture.** If more than ~5% of pixels are at exactly 1.0,
  you are clipping; if more than ~90% are at 0.0, your floor is eating the piece.
- **Check it after a minute.** Fields drift toward equilibrium slowly; a curve tuned at
  five seconds is often wrong at sixty, because the field is still filling.
- **Check it at two resolutions.** If the piece looks different at 2× size, your tone
  constants are load-bearing and should be normalised instead.
