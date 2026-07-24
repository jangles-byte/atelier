# Engine Budgets and the Degradation Ladder

## Game-engine budgets (Unity / Godot / custom)

The same three walls exist everywhere; know which one you're hitting before
changing anything (profiler first — engines ship one):

- **CPU / draw calls:** each draw call costs driver time. Batch by material
  (atlases, sprite batching), instance repeated meshes/particles, and keep
  per-frame allocations at zero in hot loops (GC spikes read as rhythmic hitches —
  pool particles, projectiles, strings). UI counts: a naive canvas/HUD that
  rebuilds per frame (layout invalidation in Unity UGUI, `queue_redraw` storms in
  Godot) can outcost the game scene.
- **GPU fill rate / overdraw:** transparent layers stack cost — same math as
  Metal's blended-overdraw rule (≤ ~2.5× average). Mobile and integrated GPUs hit
  this wall first. Fixes in order: tighter particle textures, fewer larger
  particles over many small (or vice versa — measure), half-resolution offscreen
  for glow/smoke composited up, cap simultaneous emitters.
- **GPU vertex / scene complexity:** LODs, frustum + occlusion culling, shadow
  map resolution and cascade count. Shadows and post-processing (bloom, DoF, SSAO)
  are the expensive prestige items — they enter the ladder early.

Fixed-step simulation, interpolated rendering: simulate at a fixed dt (e.g. 60Hz),
render at display rate interpolating between states — motion stays smooth at
144Hz and correct at 40. Never step physics with raw frame dt uncapped.

## The degradation ladder

When the frame budget is blown (p95 frame time over budget after profiling), cut
in this order — it is sorted by *visual damage per millisecond recovered*,
cheapest damage first. Stop cutting as soon as you're under budget.

1. **Particle counts and secondary emitters** — halve counts; nobody counts
   particles. Dust, sparks-on-sparks, ambient motes go first.
2. **Blur radii and glow spreads** — `backdrop-filter` blur 24→12px, bloom
   iterations 5→3, shadow radius 32→12. Blur cost is per-pixel × radius; the
   aesthetic survives at half strength.
3. **Post-processing prestige effects** — DoF, film grain, chromatic aberration,
   SSAO quality steps. (Keep tone mapping/color grade — palette is design, grade
   is cheap.)
4. **Resolution of effects, not the scene** — render particles/glow/reflections
   at half res composited up; dynamic resolution on the 3D scene before anything
   in tier 5 is touched.
5. **Ambient/idle motion** — background drift, shimmer, breathing gradients:
   reduce frame-rate request (120→30), then freeze off-interaction. This tier is
   also the reduced-motion/low-power variant, so it must exist anyway.
6. **Stagger richness and secondary animation** — collapse staggers to group
   moves, drop follow-through elements (shadow settles with its parent). The
   choreography simplifies; the feedback remains.
7. **Shadow/lighting fidelity** — shadow map resolution, cascade count, real-time
   → baked where possible.

**Never cut, at any tier:** primary feedback motion (press states, hit
confirmation — cheapen it to opacity/color, never remove); text contrast or
legibility effects; loading/progress indication; hitch-free scrolling (scroll
smoothness outranks every effect on this list — a beautiful page that stutters
on scroll has already failed).

Degradation must be *designed*, not discovered: decide these tiers when building
the effect, gate them behind a quality setting or runtime heuristic (frame-time
moving average crossing budget → step down one tier, hysteresis before stepping
back up), and test the floor tier — the floor is what half your audience ships on.
