# Recipes: Transitions Between Views

Motion whose job is *orientation* — keeping the user's mental model intact while the
screen changes. The governing rule: **carry something across the boundary.** A transition
where nothing persists is just two screens with a fade between them.

Every recipe below has a runnable demo and a recorded GIF in the
[gallery](https://github.com/jangles-byte/atelier/tree/main/examples/recipes).

## Contents
1. [Route / page transition](#1-route--page-transition) ·
2. [Shared element / hero](#2-shared-element--hero) ·
3. [Scroll-driven reveal](#3-scroll-driven-reveal) ·
4. [Parallax that doesn't jank](#4-parallax-that-doesnt-jank) ·
5. [Skeleton → content](#5-skeleton--content) ·
6. [Progress & pending states](#6-progress--pending-states)

---

## 1. Route / page transition

**Answers:** *where did I go?*

The View Transitions API does the hard part (snapshotting old and new states) natively:

```js
if (!document.startViewTransition) return update();     // graceful fallback
document.startViewTransition(() => update());
```

```css
::view-transition-old(root) { animation: 180ms var(--ease-in) both fade-out; }
::view-transition-new(root) { animation: 260ms var(--ease-out) both fade-in; }
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root), ::view-transition-new(root) { animation-duration: 1ms; }
}
```

Direction encodes hierarchy: drilling **in** slides content leftward (new page enters
from the right); **back** reverses it. Getting this backwards is disorienting in a way
users feel but can't name — always derive direction from navigation depth, not from
which link was clicked.

Cross-document transitions (MPA) need `@view-transition { navigation: auto; }` in both
documents. Durations: 250–400ms; over 500ms the app feels slow on every single click.

**Failure mode:** transitioning on *every* state change, including back-forward cache
restores, so the app feels like it's constantly re-animating itself.

---

## 2. Shared element / hero

**Answers:** *where did it go?* — the strongest orientation tool available. The tapped
card *becomes* the detail view.

**Web (View Transitions):** give both the source and destination element the same name.
```css
.card-image        { view-transition-name: hero; }   /* on the list page  */
.detail-image      { view-transition-name: hero; }   /* on the detail page */
```
Only one element per name may be visible at a time, so assign the name dynamically to
the clicked card just before the transition and clear it after.

**Web (manual FLIP)** when you need control or lack API support: measure the thumbnail,
measure the destination, apply the inverse transform to the destination and animate it to
identity over 350–400ms `--ease-out`. Non-matching aspect ratios need
`object-fit: cover` on both, or the image visibly squashes mid-flight.

**SwiftUI:** `@Namespace` + `.matchedGeometryEffect(id:in:)` on both views, animated with
`.spring(response: 0.4, dampingFraction: 0.85)`.
**Android:** `SharedTransitionLayout` + `Modifier.sharedElement()`.

Duration 350–450ms — longer than a normal transition, because the eye is *tracking an
object* and needs time to follow it. This is the one place 450ms is right.

**Failure mode:** animating the container while the image inside re-lays-out, so the
content jumps at the end. Freeze the inner layout for the duration of the flight.

---

## 3. Scroll-driven reveal

**Answers:** *is this alive?* — the most overused effect on the web, so the rules are
mostly about restraint.

Modern, off the main thread entirely:
```css
.reveal {
  animation: rise linear both;
  animation-timeline: view();
  animation-range: entry 10% cover 32%;   /* done well before centre-screen */
}
@keyframes rise { from { opacity: 0; transform: translateY(16px); } }
```

Compatible fallback — `IntersectionObserver`, which fires once and then stops observing:
```js
const io = new IntersectionObserver((es) => es.forEach(e => {
  if (!e.isIntersecting) return;
  e.target.classList.add('in'); io.unobserve(e.target);       // never re-animate
}), { rootMargin: '0px 0px -12% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```

Discipline: travel ≤ 16px (bigger reads as a slide show), finish before the element
reaches reading position, **animate once** — elements that re-animate on scroll-up feel
broken — and never reveal body text the user is trying to read. Stagger siblings 40ms,
never more than one group in view.

**Failure mode:** every section fading up with identical duration and delay — the single
most recognisable "template" motion signature. If everything reveals, nothing is revealed;
pick the 2–3 moments that deserve it.

---

## 4. Parallax that doesn't jank

Parallax is a scroll-linked *transform*, never a scroll handler writing `top`.

```css
.layer-back { animation: drift linear both; animation-timeline: scroll(root block); }
@keyframes drift { to { transform: translateY(-15%); } }
```

Depth budget: 2–3 layers, back layer moving 10–20% of scroll distance. More layers or
larger offsets produce a seasick effect and multiply compositing cost. Never parallax
text. Disable entirely under reduced motion — parallax is a common migraine and nausea
trigger, which makes this one of the few places where "reduced" genuinely means "off".

**Failure mode:** `window.onscroll` + `element.style.top` — guaranteed jank because
scroll events fire off the compositor's rhythm (see `performance-craft`).

---

## 5. Skeleton → content

**Answers:** *is it working?*

Skeletons must match the final layout's geometry, or their replacement causes a reflow
jump that costs more comprehension than the skeleton bought. Shimmer travels across the
skeleton at 1.2–1.6s per sweep with a 600ms gap — faster reads as anxious.

```css
.skeleton { background: linear-gradient(90deg, var(--bg-2) 25%, var(--bg-3) 37%, var(--bg-2) 63%);
            background-size: 400% 100%; animation: sweep 1.4s ease-in-out infinite; }
@keyframes sweep { to { background-position: -135% 0; } }
```

Swap with a 150ms cross-fade — instant swaps flash. **Only show a skeleton after ~200ms
of waiting** (below that, nothing should appear at all: a skeleton that flashes for 80ms
is pure noise), and only when you expect > 600ms. Under reduced motion, use a static
placeholder tint with no sweep.

**Failure mode:** generic grey boxes that don't match the content shape, and skeletons on
instant cache hits.

---

## 6. Progress & pending states

**Answers:** *is it working, and for how long?*

- **Known duration →** determinate bar, `transform: scaleX()` from a `transform-origin:
  left`, linear easing. This is the rare correct use of linear: the machine really is
  progressing uniformly, and easing it would be a lie.
- **Unknown duration →** indeterminate. Loop 1–1.5s; never fake a percentage.
- **Under ~300ms →** show nothing. A spinner that appears and vanishes is worse than a
  brief pause.
- **Optimistic UI →** commit the change immediately with a subtle pending treatment
  (85% opacity), and reserve motion for the *failure* path, where a 200ms shake plus
  revert genuinely informs.

Buttons that trigger work should keep their width while swapping label for spinner —
a resizing button shifts everything around it.

**Failure mode:** a spinner as the answer to every wait, including 60ms ones; and
progress bars that reach 90% and stop, which trains users to distrust all of them.
