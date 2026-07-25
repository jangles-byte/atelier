# Atelier

**A generative animation toolkit for Claude Code — with the parameters actually verified,
and the ability to watch what it built.**

Claude can write a flow field. What it can't normally do is *see* one, know that physarum
fuses into trunks outside a narrow occupancy band, or know that the attractor seed it just
picked collapses to a single point. Atelier supplies the knowledge that isn't in the
tutorials, machine-checks the numbers it quotes, and ships a capture script so the work gets
judged by watching it.

![Editorial hero: a didone headline rising behind a mask over a burning ember field](https://github.com/jangles-byte/atelier/releases/download/media/hero.gif)

Flow field, masked line-by-line reveal, type and palette — all from these skills, recorded
with the capture script. Source: [`hero.html`](examples/hero.html).

---

## Pieces

> ### → [Browse the generative gallery](examples/generative/)

| | |
|---|---|
| ![mycelium](https://github.com/jangles-byte/atelier/releases/download/media/physarum.gif) | ![clifford](https://github.com/jangles-byte/atelier/releases/download/media/gen-attractor.gif) |
| **Mycelium** — 1,048,576 physarum agents on the GPU, four shader passes. The network is a consequence of a million agents agreeing. | **Clifford** — deterministic chaos, 420,000 points a frame. Brightness is visit density, log-scaled. |
| ![murmuration](https://github.com/jangles-byte/atelier/releases/download/media/gen-boids.gif) | ![strata](https://github.com/jangles-byte/atelier/releases/download/media/gen-warp.gif) |
| **Murmuration** — three local rules, no leader. Brightness is local flock density. | **Strata** — noise fed into the coordinates of noise, twice. Only the inner layer evolves, so it breathes. |
| ![perihelion](https://github.com/jangles-byte/atelier/releases/download/media/gen-orbits.gif) | ![ember](https://github.com/jangles-byte/atelier/releases/download/media/gen-ember.gif) |
| **Perihelion** — bodies falling around three slow masses; they brighten at perihelion and cool at apoapsis. | **Ember** — a flow field where oxblood is calm and gold is fast. |

The rule every piece follows: **colour is earned.** It maps to a property the system
actually has — velocity, density, visit count, age — never to a rainbow of hue over time.
Colour that encodes nothing is the loudest signal that no decision was made.

## The generative-motion skill

| Reference | What's in it |
|---|---|
| **systems.md** | Nine systems with verified parameter ranges and each failure mode: physarum, strange attractors, boids, reaction–diffusion, differential growth, n-body, metaballs, interference, cellular automata |
| **noise-and-fields.md** | Which noise and why, fbm, domain warping, curl vs angle fields, and turning a field into a composition rather than wallpaper |
| **gpu-and-shaders.md** | When to go GPU (architectural, not an optimisation), WebGL2 GPGPU with ping-pong state textures, attribute-less drawing, the silent-failure extension minefield, debugging in the order that finds it fastest |
| **three-dimensional.md** | Raymarched SDFs, smooth-minimum blending, free infinite domains, instancing at scale, and camera discipline |
| **density-and-tone.md** | Mapping an unbounded accumulation buffer onto a display — the most common way a correct piece looks wrong, and how to find the floor without guessing |
| **post-processing.md** | Bloom as a mip chain, grain weighted to the midtones, aberration, feedback, gradient-map grading, and the order these must run in |
| **rendering.md** | Accumulation trails, blending modes, envelopes, batching and scale |
| **art-direction.md** | The eight tells of tutorial work, the five decisions that make it a piece, and the tuning order |
| **diagnostic.md** | Black frame, saturating, dying, exploding, clumping, 4fps, beautiful-then-grey-mush — worked by symptom |

### The numbers are checked, not remembered

A parameter just outside the viable band doesn't produce a worse image — it produces
**nothing**, and you can't tell by looking at the value. So the quoted values are verified
by scripts that ship with the skill, CPU-only, in seconds:

```bash
skills/generative-motion/validate/attractors.py     # Lyapunov + occupancy per seed
skills/generative-motion/validate/gray_scott.py     # runs each (f,k), classifies the result
```

This caught a real error in this repo's own documentation. The reference used to advise
animating an attractor by interpolating between two good seeds — measuring it showed
**8 of 13 steps along that path are non-chaotic**, collapsing the render mid-animation. The
advice is now to orbit a single seed, and `--path` will check any route you want to take.

Both scripts also search: `attractors.py --search clifford 10` finds new viable seeds and
reports how many candidates it rejected on the way; `gray_scott.py --scan` maps the viable
band so you can pick your own pairs.

## Watch your own work

```bash
skills/motion/scripts/capture-motion.py sketch.html --out piece.gif --duration 2400
```

Drives headless Chrome over the DevTools protocol and records real composited frames, so it
works for canvas, WebGL, CSS and JS animation libraries alike. *Needs only Chrome and
ffmpeg — no pip installs; the WebSocket client is stdlib.*

## Also in the box

Interface motion, for when the animation serves a UI rather than being the artwork.

| Skill | Role |
|---|---|
| **motion** | Production recipes with tuned values and failure modes — modals, drawers, toasts, FLIP reordering, view transitions, drag, springs, game feel — plus an 11-point diagnostic for motion that feels dead. [20 running demos](examples/recipes/). |
| **performance-craft** | Compositor discipline on the web; ProMotion timing, Metal overdraw and particle budgets on Apple silicon; engine budgets; and a degradation ladder ordered by visual damage. |
| **critique** | Capture the real thing, score an 8-dimension rubric with evidence, output ranked changes with exact values. Accessibility findings outrank aesthetics. |
| **design-direction** · **color** · **typography-and-layout** | Aesthetic point of view, OKLCH palettes and contrast discipline, type and grid. |

## Install

```
/plugin marketplace add jangles-byte/atelier
```
```
/plugin install atelier@atelier
```

Or as plain skills:

```bash
git clone https://github.com/jangles-byte/atelier.git
cp -r atelier/skills/* ~/.claude/skills/
```

Skills auto-trigger on relevant work — "make something generative", "a flow field",
"why is my shader black", "animate this". Each SKILL.md is a short router; depth lives in
`references/` that load only when needed, so context stays light.

## Contributing & license

PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Principle first, exact values,
verified numbers, no stack lock-in. MIT.
