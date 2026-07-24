# Apple Silicon & Apple Platforms

## Timing: ProMotion changes the contract

iPhone Pro, iPad Pro, and MacBook Pro displays run adaptive 10–120Hz. Consequences:

- **Never hardcode 1/60** (or 1/120). Use `CADisplayLink` and its `targetTimestamp
  - timestamp` as dt; SwiftUI/Core Animation handle it when you animate via their
  APIs rather than stepping values yourself.
- Declare your needs: `CAFrameRateRange(minimum:preferred:maximum:)` on the display
  link (and `.preferredFrameRateRange` on CA layers). Ambient/secondary animation
  should *request less* (e.g. 30–60) — the display then ramps down and saves real
  battery; requesting 120 for a background shimmer is a thermal tax on nothing.
  Games: `CAMetalLayer` + `preferredFramesPerSecond` on MTKView.
- Match work to cadence: a 120Hz callback has **8.3ms**, and Core Animation's
  compositor takes its slice first. If your per-frame work fits 16ms but not 8,
  you'll hitch only on ProMotion devices — test on one, or set a max of 60 and
  own the choice.

## Hitches over FPS

Apple's metric is the **hitch** (a frame presented late), measured in Instruments
(Animation Hitches template) and MetricKit. Budget: hitch time ratio < 5 ms/s.
The usual suspects: layout during scroll (Auto Layout churn, SwiftUI body
re-evaluation storms), image decode on the main thread (use `UIImage.byPreparing
ForDisplay` / `.task` decode off-main), shadow paths unset (`layer.shadowPath`
turns a per-frame mask render into a cached one), and offscreen rendering
(masks + corner radius + shadow stacking — Instruments' Core Animation "color
offscreen-rendered" flag).

SwiftUI specifics: keep `body` cheap and value-typed (hitches correlate with
dependency-graph churn — use `Observable` granularity, `EquatableView`/`.id`
discipline); prefer `.animation`/`withAnimation` (runs in the render server, off
your process's critical path) over Timer-driven state mutation at 120Hz, and
`TimelineView(.animation)` + `Canvas` for procedural drawing rather than
per-frame `@State` invalidation of view trees.

## Metal budgets

- **Overdraw / fill rate is the budget that blows first.** TBDR GPUs make opaque
  overdraw nearly free (hidden surface removal) but **blended** overdraw is paid
  in full — every additive/alpha particle layer re-reads and re-writes the tile.
  Rule: average blended overdraw ≤ ~2.5× screen; measure with Xcode's GPU
  counters ("fragments shaded / pixels"). Shrink particle quads (tight textures,
  not 256px quads of mostly-transparent glow), and render dense particle fields
  at half resolution into an offscreen target composited up — glow survives
  upsampling perfectly.
- **Additive blending** is the same cost as alpha but stacks brightness — visually
  you can often halve particle count and double intensity for identical glow at
  half the fill cost. Cap particles per emitter; budget total on-screen particles
  (phone: low thousands as sprites, tens of thousands only via instanced
  half-res); pool and reuse, never allocate per-spawn.
- **Half precision:** `half` in shaders for color/UV math doubles ALU throughput
  and halves register pressure on Apple GPUs; keep positions/accumulators
  `float`. Textures: prefer 16-bit float render targets over 32 when HDR-ish
  accumulation is needed at all.
- **Unified memory** means no PCIe copy: use `storageModeShared` buffers and write
  vertex/particle data directly; the win is architectural (skip staging buffers),
  not free bandwidth — bandwidth is still the constraint, so pack vertex data
  small (half/unorm formats).

## Efficiency cores and battery

Always-on animation must not camp on P-cores. Anything that isn't the user's
primary interaction — ambient shaders, background particle sims, progress
spinners' timers — belongs at `.utility`/`.background` QoS (GCD/`Task(priority:)`),
which the scheduler routes to E-cores. The pattern: simulate at low QoS, render
via the system's vsync'd pipeline. Combine with reduced frame-rate requests above
and `ProcessInfo.processInfo.isLowPowerModeEnabled` (+ its notification) to switch
ambient effects to their reduced-motion variants. Respect
`UIAccessibility.isReduceMotionEnabled` identically — one code path, two triggers.

## Verification

Instruments: Animation Hitches (scrolls/transitions), Metal System Trace + GPU
counters (fill/ALU/bandwidth), Energy Log for the always-on effects. Test on the
oldest supported device *and* a ProMotion device — they fail differently (thermal
vs. cadence). A demo that's smooth on an M-series Mac has proven nothing about an
iPhone 12.
