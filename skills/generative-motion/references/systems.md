# Systems Worth Building

Each entry: what it *is*, the maths, parameter ranges that actually look good (the ones
tutorials omit), what to map colour to, and the failure mode. All are engine-agnostic —
they need a loop, an array, and somewhere to draw.

**The numeric claims here are checked, not remembered.** `validate/attractors.py` measures
every attractor seed for chaos (Lyapunov exponent) and structure (grid occupancy);
`validate/gray_scott.py` runs every reaction–diffusion pair and classifies the result.
Both are CPU-only and take seconds. Run them after editing any number in this file — a
wrong parameter here costs a reader a render and their confidence, and in both these
systems a value slightly outside the viable band produces *nothing at all* rather than
something worse.

## Contents
[Physarum](#physarum-slime-mould) · [Strange attractors](#strange-attractors) ·
[Boids](#boids-flocking) · [Reaction-diffusion](#reaction-diffusion) ·
[Differential growth](#differential-growth) · [N-body & orbits](#n-body--orbital-motion) ·
[Metaballs](#metaballs) · [Interference & moiré](#interference--moiré) ·
[Cellular automata](#cellular-automata)

---

## Physarum (slime mould)

The single most striking system per line of code. Agents deposit trail, sense it ahead,
and steer toward it; the feedback builds transport networks that look alive and organic.

```
for each agent:
  F  = sense(x + cos(θ)·dist,        y + sin(θ)·dist)          # sensor distance 9–14px
  FL = sense(x + cos(θ-α)·dist,      y + sin(θ-α)·dist)        # sensor angle α ≈ 22–35°
  FR = sense(x + cos(θ+α)·dist,      y + sin(θ+α)·dist)
  if      F > FL and F > FR: θ += 0
  else if FL > FR:           θ -= turn·random()                # turn ≈ 25–45°/step
  else if FR > FL:           θ += turn·random()
  else:                      θ += (random()-0.5)·2·turn
  x += cos(θ)·speed·dt ; y += sin(θ)·speed·dt                  # speed 30–90 px/s
  deposit(x, y, 5)                                             # then wrap at edges
# each frame, on the trail map:
blur(trail, 1px) ; trail *= decay                              # decay 0.90–0.97 / frame
```

**Ranges that matter:** decay is the whole piece — 0.97 gives dense lace, 0.90 gives sparse
filaments. Sensor distance far exceeds step size (agents look further than they move) or
no network forms. 100k–1M agents on GPU, 20k–80k is plenty on canvas.

**Colour:** trail concentration, through a two-stop ramp. **Failure mode:** uniform grey
mat — decay too high or too many agents; and initialising agents in a uniform random
field gives a boring even mesh, so seed them in a disc or ring and let the network grow
outward.

---

## Strange attractors

Deterministic chaos: iterate a point through a map and plot where it lands. Millions of
points reveal delicate filigree structure. No physics, no time step — just iteration.

**Clifford:** `x' = sin(a·y) + c·cos(a·x)` , `y' = sin(b·x) + d·cos(b·y)`
with a ∈ [−2, 2], b ∈ [−2, 2], c ∈ [−2, 2], d ∈ [−2, 2]. Good seeds: (−1.4, 1.6, 1.0, 0.7),
(1.7, 1.7, 0.6, 1.2), (−1.7, 1.3, −0.1, −1.21).

**De Jong:** `x' = sin(a·y) − cos(b·x)` , `y' = sin(c·x) − cos(d·y)`.
Try (1.641, 1.902, 0.316, 1.525) or (−2.0, −2.0, −1.2, 2.0).

**Lorenz (3D):** `dx = σ(y−x)`, `dy = x(ρ−z) − y`, `dz = xy − βz`, with σ=10, ρ=28,
β=8/3, `dt` = 0.005–0.01. Project to 2D and rotate slowly.

Animate by **orbiting one seed**, not by travelling between two (see the measurement
below). Plot with very low alpha (0.02–0.06) and let density accumulate — the filigree is
built from millions of overlapping faint points, not from bright ones.

**Colour:** step index (age along the orbit), or local velocity `|p' − p|`.
**Failure mode:** most parameter sets are visually dead. `validate/attractors.py --search
clifford 10` hunts for viable ones and reports how many candidates it rejected on the way.

**Do not interpolate between two good seeds.** Measured on the first two Clifford sets
above, **8 of 13 steps along the straight line between them are non-chaotic** — the orbit
collapses to a fixed point or a short cycle, and the render goes empty mid-animation. To
animate, *orbit* one seed instead: `a + 0.2·sin(t·0.117)` per parameter keeps you inside
the viable region. Check any path you do want with `--path`.

---

## Boids (flocking)

Three rules over neighbours within a radius — separation, alignment, cohesion — produce
murmurations.

```
sep = Σ (p − q)/|p − q|²   for q within  ~18px      weight 1.5
ali = avg(v_q)             for q within  ~40px      weight 1.0
coh = avg(p_q) − p         for q within  ~55px      weight 0.9
v += (sep·1.5 + ali·1.0 + coh·0.9)·dt ; clamp |v| to [minSpeed, maxSpeed]
```

**Ranges:** separation radius must be well under alignment radius or the flock explodes.
Clamp speed to a *band* (e.g. 60–140 px/s) — birds never stop. 400–2,000 agents. Use a
spatial hash above ~800 or it's O(n²).

**Colour:** heading (hue from `atan2(vy, vx)` is the one defensible use of hue-over-angle),
or local neighbour count, which makes dense knots glow.
**Failure mode:** a single blob orbiting the centre — cohesion too strong, or no boundary
handling. Wrap edges rather than bouncing; bouncing reads as a container.

---

## Reaction-diffusion (Gray–Scott)

Two chemicals; one feeds, one kills. Produces coral, spots, stripes, mitosis.

```
A' = A + (Da·∇²A − A·B² + f·(1−A))·dt
B' = B + (Db·∇²B + A·B² − (k+f)·B)·dt
Da = 1.0, Db = 0.5, dt = 1.0, ∇² via a 3×3 laplacian (0.05 corners, 0.2 edges, −1 centre)
```

**The whole piece is (f, k)** — all five verified to produce structure at 180², 9,000 steps:

| name | f | k | features formed |
|---|---|---|---|
| mitosis | 0.0367 | 0.0649 | 131 |
| coral | 0.0545 | 0.0620 | 495 (densest) |
| spots | 0.0300 | 0.0620 | 141 |
| worms | 0.0780 | 0.0610 | 56 (sparsest — needs longer to fill) |
| waves | 0.0140 | 0.0470 | 184 |

Seed with a few random blobs of B in a field of A=1, plus a little noise for symmetry
breaking — a perfectly symmetric seed grows a perfectly symmetric and rather dull result.
`validate/gray_scott.py --scan` maps the viable band if you want pairs of your own.

**Colour:** B concentration, ramped. **Failure mode:** running it at screen resolution on
CPU (it's a per-pixel loop — use a small grid, 200–400², and upscale, or do it in a
shader). Also: (f, k) outside the narrow viable band gives a blank field within seconds.

---

## Differential growth

A closed chain of nodes that repel locally, stay linked, and *insert new nodes* when
segments stretch. Produces coral, brain folds, ruffled edges.

```
each node: repel from neighbours within r (≈12px), attract to its two chain links,
           add a little noise-driven outward push
if |n[i] − n[i+1]| > maxLen: insert midpoint      # this is the growth
if |n[i] − n[i+1]| < minLen: remove node
```

**Ranges:** repulsion radius ≈ 1.5× maxLen. Grow slowly — a few insertions per frame, not
hundreds. **Colour:** node index, or curvature. **Failure mode:** self-intersection
(needs a spatial hash for repulsion) and runaway node counts; cap the chain.

---

## N-body & orbital motion

Attractors with inverse-square pull. Elegant, and trivially beautiful with trails.

```
for each particle: for each attractor:
  d = a.pos − p.pos ; r² = max(|d|², softening)      # softening 400–2000 prevents blowups
  p.v += normalize(d) · (G·a.mass / r²) · dt
```

**Ranges:** softening is mandatory — without it, particles that pass close to an attractor
slingshot to infinity and the piece dies. 2–4 attractors, slowly moving, is far more
interesting than one. **Colour:** speed (fast = hot near periapsis) — physically motivated
and it reads instantly. **Failure mode:** everything collapses into the attractor; add
mild drag and give particles initial tangential velocity so they *orbit*.

---

## Metaballs

Sum of radial falloffs, thresholded — organic blobs that merge and split.

`f(p) = Σ rᵢ² / |p − cᵢ|²` , surface where `f = 1`. Render with marching squares on a
coarse grid (cell 6–12px) for crisp edges, or as a shader threshold for speed. Move the
centres on noise or orbits. **Colour:** field strength just inside the threshold, so edges
glow. **Failure mode:** blobby-lava-lamp cliché — escape it by thresholding *thin*
(render only the isoline band) or by using many small balls rather than six big ones.

---

## Interference & moiré

Two or more periodic fields overlaid, beating against each other. Nearly free, and
capable of extraordinary depth.

`v = sin(k·(x·cosθ₁ + y·sinθ₁) + φ₁) + sin(k·(x·cosθ₂ + y·sinθ₂) + φ₂)`

Animate φ slowly, or rotate θ by fractions of a degree. Concentric variants:
`sin(|p − a| · k₁) + sin(|p − b| · k₂)` gives classic two-source interference.
**Colour:** threshold or posterise `v` into 2–4 bands; smooth gradients kill the effect.
**Failure mode:** aliasing — supersample, or keep spatial frequency well below the pixel
grid.

---

## Cellular automata

Discrete rules on a grid. Beyond Life: **cyclic CA** (a cell adopts the next colour in a
cycle if enough neighbours already have it) produces spiral waves and is far more
beautiful than Life; **Langton-style turmites** draw structured paths.

**Colour:** the cycle index, mapped through a ramp, not to a rainbow.
**Failure mode:** rendering at 1 cell = 1 pixel, so structure is invisible. Use 3–8px cells
and let the pattern read.
