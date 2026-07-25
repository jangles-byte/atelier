# Generative gallery

Pieces, not sketches. Each is a single self-contained file with a stated intent, a seeded
PRNG so the composition is reproducible, and one property that earns colour — the rule the
`generative-motion` skill insists on, because colour that encodes nothing is what makes
algorithmic work read as a demo.

All recorded with the package's own capture script.

---

## Ember — flow field

Embers on a thermal. A two-octave noise field sampled as an angle; colour is earned by
velocity, so deep oxblood is calm and gold is fast. Brightness is a reading of the field,
not a decoration on it.

![ember](https://github.com/jangles-byte/atelier/releases/download/media/gen-ember.gif) · [source](ember.html)

## Mycelium — physarum, 1,048,576 agents

A colony finding food. Agents lay trail, sense it ahead, and steer toward what they smell;
the feedback builds transport networks. Nothing here is drawn — the structure is a
consequence of a million agents agreeing.

**This piece is why the skill covers GPU work.** The CPU version failed: at 200,000 agents
in JavaScript the network fused into a handful of thick trunks no matter how the occupancy,
sensor distance, diffusion or step size were tuned. The fix wasn't a parameter, it was the
architecture — agent state lives in a 1024² float texture and every stage is a shader, four
passes per frame: move, deposit, diffuse, present.

![mycelium](https://github.com/jangles-byte/atelier/releases/download/media/physarum.gif) · [source](physarum.html)

## Strata — domain-warped noise

Ink held in glass. Noise fed into the coordinates of more noise, twice — the trick that
turns clouds into marble. Only the innermost layer evolves, so the structure breathes
instead of sliding. Rendered at a third scale and upsampled, which costs nothing because
the field has no high-frequency detail to lose.

![strata](https://github.com/jangles-byte/atelier/releases/download/media/gen-warp.gif) · [source](warp.html)

## Clifford — deterministic chaos

`x' = sin(a·y) + c·cos(a·x)`. One point, iterated 420,000 times a frame. No physics and no
randomness: the filigree is simply where the orbit chooses to spend its time, and
brightness is visit density on a log scale so the faint structure survives beside the
dense core.

The parameters **orbit** a known-chaotic seed rather than interpolating between two of
them — a straight lerp between two chaotic sets passes through non-chaotic parameter space
where the whole attractor collapses to a single point.

![clifford](https://github.com/jangles-byte/atelier/releases/download/media/gen-attractor.gif) · [source](attractor.html)

## Perihelion — n-body with trails

A sky of small bodies falling around three slow masses. Colour is earned by speed, which
here is what heat physically is: bodies brighten at perihelion and cool at apoapsis, so the
image reads as orbits rather than scribble. Softening in the force law is mandatory —
without it, close passes slingshot to infinity and the piece empties itself.

![perihelion](https://github.com/jangles-byte/atelier/releases/download/media/gen-orbits.gif) · [source](orbits.html)

## Murmuration — boids

A flock at dusk. Three local rules, no leader, no path; the shape of the whole is an
accident of everyone watching their neighbours. Colour is earned by local density, so knots
glow and stragglers go dark. Speed is clamped to a *band* rather than a maximum, because
birds do not hover.

![murmuration](https://github.com/jangles-byte/atelier/releases/download/media/gen-boids.gif) · [source](boids.html)

---

## What isn't here

Documented in the skill but not yet built here: reaction–diffusion, differential growth, metaballs,
interference/moiré, and cyclic cellular automata.
