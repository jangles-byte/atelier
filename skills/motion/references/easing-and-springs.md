# Easing and Spring Mathematics

Language-agnostic first: every easing function is `f(t) → progress`, both 0→1. Any
environment that can set a property per frame can use everything here.

## Choosing a curve

| Situation | Curve | Why |
|---|---|---|
| Element entering | ease-out (decelerate) | arrives fast, settles gently — feels responsive |
| Element exiting | ease-in (accelerate) | departs without lingering |
| Moving A→B on screen | ease-in-out | natural for an eye that tracks the whole path |
| Color/opacity only | ease-out or gentle in-out | no position, subtle is fine |
| Playful/physical | spring | see below |
| Anything an eye follows | **never linear** | uniform velocity reads as mechanical |
| Mechanical-on-purpose (ticks, typewriter, progress of real work) | linear or steps() | honesty about machinery |

Named cubic-béziers worth standardizing on (tokens, not sprinkled literals):

```css
--ease-out:      cubic-bezier(0.22, 1.0, 0.36, 1.0);   /* "quint-ish out": fast arrival, long settle */
--ease-in:       cubic-bezier(0.55, 0.0, 1.0, 0.45);
--ease-in-out:   cubic-bezier(0.65, 0.0, 0.35, 1.0);
--ease-overshoot:cubic-bezier(0.34, 1.56, 0.64, 1.0);  /* back-out: ~10% overshoot, playful */
```

The browser's built-in `ease` is serviceable; the default `linear` on Web Animations
API and many game tweens is the single most common cause of dead motion.

As portable code (drop into JS, Swift, Python, GDScript, GLSL alike):

```
easeOutQuint(t) = 1 - (1-t)^5        // the workhorse "snappy arrival"
easeInCubic(t)  = t^3
easeInOutCubic(t) = t<0.5 ? 4t^3 : 1 - (-2t+2)^3 / 2
easeOutBack(t)  = 1 + 2.70158*(t-1)^3 + 1.70158*(t-1)^2   // overshoot ≈ 10%
```

Game-loop usage: `value = lerp(from, to, ease(elapsed / duration))`, clamp t to
[0,1], and *never* the `pos += (target - pos) * 0.1` exponential chase for
choreographed motion — it's frame-rate dependent and never arrives. (Its correct,
frame-rate-independent form for camera-follow feels:
`pos = target + (pos - target) * exp(-k * dt)`, k ≈ 5–15.)

## Springs

Springs replace (duration, curve) with physics — they're interruptible mid-flight
with velocity preserved, which tweens can't do gracefully. The model is a damped
harmonic oscillator:

```
acceleration = -stiffness * (pos - target) - damping * velocity     (mass = 1)
```

Integrated per frame (semi-implicit Euler is fine at UI stiffness):

```
v += (-k*(x - target) - c*v) * dt
x += v * dt
```

The one number that matters is the **damping ratio** ζ = c / (2·√(k·m)):

| ζ | Behavior | Use |
|---|---|---|
| < 1 | overshoots, oscillates | playful, toy, "alive" — ζ 0.5–0.8 |
| 0.8–1 | one tiny overshoot / none | premium default — ζ ≈ 0.85 |
| = 1 | fastest no-overshoot settle | critically damped: modals, serious UIs |
| > 1 | sluggish crawl | almost never (reads as broken easing) |

Working recipes (k, c with m=1): **snappy UI** k=400, c=38 (ζ≈0.95, settles
~250ms) · **playful** k=300, c=20 (ζ≈0.58, one visible bounce) · **gentle/large
surfaces** k=120, c=20 (ζ≈0.91, ~450ms). Stiffness sets speed, ζ sets character —
tune ζ first.

Per stack: CSS `linear()` can encode a sampled spring (or use
`animation-timing-function: linear(…)` generators); JS: Framer Motion / Motion One
`spring({stiffness, damping})`, or 6 lines of the integrator above in rAF; SwiftUI:
`.spring(response: 0.35, dampingFraction: 0.85)` — `response` ≈ speed
(2π/√k), `dampingFraction` *is* ζ; Compose: `spring(dampingRatio, stiffness)`;
Unity/Godot: the integrator in `_process`, with `dt` clamped (spikes explode
springs — cap dt at ~1/30).

## Staggers

Groups animate as choreography, not as a block and not as N clones:

- Offset 20–40ms per item (list feel), 60–80ms for hero sequences. Total stagger
  window ≤ ~450ms: cap via `delay = min(i, 8) * offset` or compress the offset as
  count grows (`offset = total_window / n`).
- Direction follows meaning: top-down for lists, from-the-interaction-point
  (distance-based delay: `delay = dist(item, origin) * 0.5ms/px`) for grids —
  the ripple reads as causality.
- Exit staggers reverse order and halve the offset; often a plain group fade-out is
  better (exits explain less).

## Interruption

Every animation must handle being interrupted by its reverse (hover-out mid
hover-in, close mid open). Rules: animate from *current* rendered value, never
restart from the keyframe start; springs handle this natively (retarget, keep
velocity); CSS transitions handle it natively (tweens/JS timelines must read
current value explicitly); and toggling animations must be idempotent under rapid
toggling — test by mashing.
