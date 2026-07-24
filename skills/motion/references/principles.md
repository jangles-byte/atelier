# The 12 Principles, Translated

Disney's principles (Johnston & Thomas) are physics-of-attention rules. Translation
table first, then the ones that do the heaviest interface lifting, then durations
and game feel.

| Principle | Interface / procedural translation |
|---|---|
| Squash & stretch | Scale overshoot on appear (1 → 1.03 → 1), button press compress (0.97), drag-release jelly. Volume conserved: stretch X while squashing Y. |
| Anticipation | Pre-gesture before the main move: button dips before the card flies, drawer nudges before opening from swipe, chart clears before re-drawing. |
| Staging | One motion at a time owns attention. Dim/still everything else while the hero moves. |
| Straight-ahead vs pose-to-pose | Simulate (springs/particles: straight-ahead) vs interpolate (transitions: pose-to-pose). Know which you're writing; mixing them mid-element reads as glitch. |
| Follow-through & overlap | Parts stop at different times: panel lands, its shadow settles a beat later; list arrives, items overlap-stagger. Nothing complex stops all at once. |
| Slow in / slow out | Easing. The most load-bearing principle — see `easing-and-springs.md`. |
| Arcs | Elements moving in 2D travel on slight curves, not L-paths. FLIP-animate position via a single transform so the browser interpolates a straight diagonal — then bend it with a mid-keyframe if the move is large. |
| Secondary action | A supporting motion that enriches without competing: icon rotates *while* the accordion opens, confetti *behind* the headline. Cut it first when budget is tight. |
| Timing | Duration = weight. Small/light = fast; large/heavy = slower. A modal at 120ms feels weightless; a tooltip at 500ms feels broken. |
| Exaggeration | Push 10–20% past real physics so the eye registers intent at UI speeds (real physics reads as accident at 200ms). Overshoot, oversized shadows mid-drag. |
| Solid drawing | Consistent light/space logic: shadows agree on one light source; things that occlude also elevate; scale implies depth consistently. |
| Appeal | Character without noise — the motion equivalent of the signature move: one distinctive, repeated motion trait (everything settles with the same spring; state changes ripple from the interaction point). |

## Durations (the scale)

| Class | Duration | Examples |
|---|---|---|
| Micro | 100–150ms | hover, press, toggle, color/opacity |
| Small | 150–250ms | tooltip, dropdown, tab underline, icon morph |
| Medium | 250–400ms | modal, drawer, card expand, list insert |
| Large | 400–600ms | route/page transition, full-screen |
| Ambient | 2–20s | background drift, gradients, idle loops |

Modifiers: exits ~20% faster than entrances (leaving needs less explanation than
arriving); distance adds time (same element moving 800px gets ~1.3× its 200px
duration); frequency subtracts (an animation seen 50×/day belongs at the fast edge
or opacity-only). Desktop ~10–20% faster than mobile (smaller distances, pointer
precision).

## Orientation transitions (the "where did it go?" toolkit)

Shared-element continuity beats fade-through: the tapped card *becomes* the detail
view (FLIP on the web, `matchedGeometryEffect` in SwiftUI, shared-element
transitions on Android). Spatial consistency: things exit toward where they'd
return from; hierarchies slide consistently (drill-in leftward, back rightward).
Cross-fade is the fallback when no spatial relationship exists — at 200–300ms with
a 30–50% temporal overlap, never a full fade-to-blank.

## Game feel (juice)

Feedback cranked to eleven, for media where character is the point:

- **Hit-stop:** freeze the simulation 40–80ms on significant impact (scale with
  damage). The pause *is* the punch. Skip camera/UI — freeze the actors only.
- **Screen shake:** drive with a decaying trauma value; shake amplitude ∝ trauma²
  (or ³) so small hits whisper and big hits slam. Use Perlin-noise offsets, not
  random jitter — noise reads as force, jitter reads as bug. Rotational shake
  (±0.5–2°) sells more than translation at lower cost. Always cap amplitude and
  offer a reduce toggle.
- **Particles on state change:** bursts (impact), trails (speed), lingerers
  (damage). Particle count is a performance budget item — see `performance-craft`.
- **Tween everything that changes:** numbers count up, bars drain with a
  chasing-ghost second bar, pickups arc toward the HUD counter. In a game loop
  that's one `ease(t)` call per property — the easing functions in
  `easing-and-springs.md` are engine-agnostic.
- **Anticipation & recovery frames:** even 2-frame windup + 3-frame recovery makes
  procedural attacks read. Squash on land (Y 0.85 for 60ms), stretch on jump.

Juice restraint: effects stack multiplicatively on *feel* but also on *noise* —
tie every juice element to game-state significance, and let quiet moments stay
quiet or the loud ones stop landing.

## Ambient motion

Idle/background animation (drift, shimmer, breathing gradients) is a *character*
answer, so it obeys character rules: sub-perceptual speed (movement you notice only
when told), zero interaction with reading (never behind body text), paused when
off-screen or reduced-motion, and cheap (compositor/GPU only — see
`performance-craft`). One ambient system per view.

## Accessibility floor

`prefers-reduced-motion` (CSS), `UIAccessibility.isReduceMotionEnabled` (Apple),
`Settings.Global.ANIMATOR_DURATION_SCALE` (Android), an options toggle (games).
Reduced ≠ removed: keep opacity fades and color feedback (still answer "what
happened?"), drop translation/scale/parallax/shake/ambient. Autoplaying motion
over 5s must be pausable; nothing flashes more than 3×/second, ever.
