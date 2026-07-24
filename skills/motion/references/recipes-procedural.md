# Recipes: Procedural & Generative Motion

Motion that is *simulated* rather than interpolated — particles, physics, shake, ambient
fields, game juice. The distinction matters: interpolation asks "where should this be at
time t?", simulation asks "what forces act on this, and what happens next?" Simulation is
interruptible, reactive, and endless; use it when motion must respond to unpredictable
input, and use tweens when the path is known.

Everything here is engine-agnostic — the loop is `update(dt)` whether that's `rAF`,
`_process`, `Update()`, or a `CADisplayLink`.

## Contents
1. [The loop & delta time](#1-the-loop--delta-time) · 2. [Spring integrator](#2-spring-integrator) ·
3. [Particles](#3-particles) · 4. [Screen shake](#4-screen-shake) ·
5. [Hit-stop](#5-hit-stop) · 6. [Ambient fields](#6-ambient-fields) ·
7. [Chase cameras & follow](#7-chase-cameras--follow)

---

## 1. The loop & delta time

Every value below assumes seconds. The two rules that prevent 90% of procedural bugs:

```js
let last = performance.now();
function frame(now) {
  let dt = (now - last) / 1000; last = now;
  dt = Math.min(dt, 1 / 30);          // clamp: a tab-switch spike explodes springs
  update(dt);
  requestAnimationFrame(frame);
}
```

1. **Clamp `dt`.** A 2-second stall must not integrate as 2 seconds of force.
2. **Never assume 60fps.** `x += 2` doubles in speed on a 120Hz ProMotion display;
   `x += 120 * dt` does not. This is the single most common cross-device motion bug.

For deterministic physics, run a **fixed timestep** and interpolate rendering:
accumulate `dt`, step the simulation in fixed 1/60 slices, then render at
`alpha = accumulator / step` between the last two states. Smooth at 144Hz, correct at 40.

---

## 2. Spring integrator

The workhorse. Semi-implicit Euler is stable enough at UI stiffness and is ~4 lines:

```js
function spring(s, target, dt, k = 400, c = 38) {   // ζ = c / (2√k) ≈ 0.95
  s.v += (-k * (s.x - target) - c * s.v) * dt;
  s.x += s.v * dt;
  return s.x;
}
```

Tune **ζ first** (character), then `k` (speed). ζ < 1 overshoots and feels alive; ζ = 1
is the fastest settle without bounce; ζ > 1 crawls. Recipes: snappy UI k=400 c=38
(ζ≈0.95) · playful k=300 c=20 (ζ≈0.58, one visible bounce) · heavy panel k=120 c=20.

Springs shine on **interruption**: retarget mid-flight and velocity carries through, so a
grabbed-and-thrown element never snaps. That is why drag-release, cursor-followers, and
anything user-driven should be sprung rather than tweened.

Settle test: stop the spring when `|x - target| < 0.1 && |v| < 0.1` — otherwise it runs
forever burning frames (see `performance-craft`).

---

## 3. Particles

**Answers:** *something significant happened.*

Pool everything. Allocation in a hot loop is the classic cause of rhythmic hitching as GC
runs.

```js
const P = Array.from({length: 512}, () => ({alive: false, x:0, y:0, vx:0, vy:0, life:0, max:1}));
function emit(x, y, n = 24) {
  for (const p of P) {
    if (n <= 0) break;
    if (p.alive) continue;
    const a = Math.random() * Math.PI * 2, sp = 60 + Math.random() * 180;
    Object.assign(p, { alive: true, x, y, vx: Math.cos(a)*sp, vy: Math.sin(a)*sp,
                       life: 0, max: 0.4 + Math.random() * 0.5 });
    n--;
  }
}
function update(dt) {
  for (const p of P) {
    if (!p.alive) continue;
    p.life += dt;
    if (p.life >= p.max) { p.alive = false; continue; }
    p.vy += 900 * dt;                       // gravity
    p.vx *= Math.pow(0.12, dt);             // frame-rate-independent drag
    p.x += p.vx * dt; p.y += p.vy * dt;
  }
}
```

Craft notes: **vary everything** — a burst where all particles share speed, size and
lifetime reads as a machine. Fade *and* shrink over life (`1 - t²` for alpha reads better
than linear). Bursts of 15–30 for UI feedback, hundreds only for game impacts. Emit in a
cone toward the impact normal rather than a full circle when there's a direction to
express.

Budget: particle cost is **fill rate**, not count — 50 large soft-glow quads cost more
than 500 tight ones. Half-resolution offscreen rendering for dense glow fields composites
up almost losslessly (see `performance-craft`).

---

## 4. Screen shake

**Answers:** *that hit hard.* The most effective juice per line of code, and the easiest
to overdo.

Drive everything from a single decaying **trauma** value, and raise it to a power so
small hits whisper and big ones slam:

```js
let trauma = 0;
const addTrauma = a => trauma = Math.min(1, trauma + a);   // 0.2 light … 0.8 heavy
function shake(dt, t) {
  trauma = Math.max(0, trauma - dt * 1.4);                 // ~0.7s to decay from 1
  const s = trauma * trauma;                               // squared: perceptual falloff
  return {
    x: (noise(t * 25.0) * 2 - 1) * 18 * s,
    y: (noise(t * 25.0 + 100) * 2 - 1) * 18 * s,
    rot: (noise(t * 25.0 + 200) * 2 - 1) * 1.6 * s,        // degrees
  };
}
```

Use **smooth noise, not `Math.random()`** — random jitter reads as a rendering bug,
coherent noise reads as force. Rotational shake sells impact more than translation at a
fraction of the visual cost; ±1–2° is plenty. Always cap amplitude, never shake the UI
layer (only the world/camera), and ship a "reduce screen shake" toggle — this is a
frequent motion-sickness trigger and reduced-motion must zero it.

---

## 5. Hit-stop

**Answers:** *that connected.* The pause **is** the punch.

```js
let freeze = 0;
const hitStop = ms => freeze = Math.max(freeze, ms / 1000);
function update(dt) {
  if (freeze > 0) { freeze -= dt; dt *= 0.05; }   // near-freeze, not a true stop
  world.step(dt);
}
```

40–80ms scaled by significance: 40ms for a light hit, 80–120ms for a kill. Freeze the
*actors*, not the camera, particles, or UI — a fully frozen frame reads as a stutter,
while a frozen combatant with a still-moving camera reads as impact. Slowing to 5% rather
than 0% keeps it feeling alive.

Pair with: shake trauma, a 1–2 frame white flash on the struck entity, and particle
emission at the contact point. Those four together are most of "game feel".

---

## 6. Ambient fields

**Answers:** *is this alive?* Background motion — drift, breathing, flow fields.

Rules that keep ambient from becoming noise: **sub-perceptual speed** (the viewer should
notice it only when told), one ambient system per view, never behind body text, and
provably cheap.

Flow-field drift, the general-purpose generative motion:
```js
// angle from smooth noise; particles inherit the field's direction
const a = noise(p.x * 0.0025, p.y * 0.0025, t * 0.08) * Math.PI * 4;
p.vx += Math.cos(a) * 22 * dt;
p.vy += Math.sin(a) * 22 * dt;
p.vx *= Math.pow(0.5, dt); p.vy *= Math.pow(0.5, dt);   // damping keeps it coherent
```

Breathing/pulse: prefer a declarative CSS keyframe over a JS loop so the compositor owns
it and the browser throttles it off-screen. Where JS is required, **stop the loop when
idle or hidden** — a permanent `requestAnimationFrame` for one pulsing dot wakes the CPU
60×/second forever, which is battery cost with no visual return.

Seed generative work so it's reproducible: a seeded PRNG (mulberry32 or similar) means a
composition you like can be recovered exactly.

---

## 7. Chase cameras & follow

**Answers:** *what should I be looking at?*

The naive `pos += (target - pos) * 0.1` is frame-rate dependent (twice as fast at 120Hz)
and never actually arrives. The correct exponential smoothing:

```js
pos = target + (pos - target) * Math.exp(-k * dt);    // k ≈ 5 loose, 15 tight
```

Add a **dead zone** so small movements don't drag the camera, and clamp maximum follow
speed so teleports don't whip. Look-ahead — offsetting the camera in the direction of
travel, itself smoothed — is what makes platformer cameras feel authored rather than
reactive. For cursor-followers and magnetic buttons, use a spring (§2) instead so the
release has momentum.

**Failure mode:** camera logic in the physics step rather than after it, producing
one-frame-late jitter that reads as a bad framerate even at 120fps.
