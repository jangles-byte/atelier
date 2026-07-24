# Recipes: Interface Motion

Production patterns for the interactions people actually build. Each recipe gives the
question it answers, the values, code in 2–3 stacks, the reduced-motion variant, and
the failure mode. Copy the values; they are tuned, not placeholders.

Shared tokens assumed throughout (define once):

```css
:root {
  --ease-out:   cubic-bezier(0.22, 1, 0.36, 1);
  --ease-in:    cubic-bezier(0.55, 0, 1, 0.45);
  --ease-back:  cubic-bezier(0.34, 1.56, 0.64, 1);
  --t-micro: 130ms; --t-small: 200ms; --t-medium: 300ms; --t-large: 450ms;
}
```

## Contents
1. [Press & hover](#1-press--hover) · 2. [Modal / dialog](#2-modal--dialog) ·
3. [Drawer / sheet](#3-drawer--sheet) · 4. [Dropdown / popover](#4-dropdown--popover) ·
5. [Toast stack](#5-toast-stack) · 6. [Accordion](#6-accordion) ·
7. [Tabs](#7-tabs) · 8. [List insert / remove / reorder](#8-list-insert--remove--reorder-flip) ·
9. [Drag with snap-back](#9-drag-with-snap-back) · 10. [Number ticker](#10-number-ticker)

---

## 1. Press & hover

**Answers:** *what just happened?* — the most-seen motion in any product, so it must be
fast and must not be opacity alone (dimming reads as "disabled", not "pressed").

```css
.btn {
  transition: transform var(--t-micro) var(--ease-back),
              background-color var(--t-micro) var(--ease-out),
              box-shadow var(--t-micro) var(--ease-out);
}
.btn:hover  { transform: translateY(-1px); box-shadow: 0 4px 12px rgb(0 0 0 / .18); }
.btn:active { transform: scale(0.96) translateY(0); transition-duration: 80ms; }
```

Press is *faster* than release (80ms down, 130ms back through `--ease-back`): contact
should feel instant, recovery can have personality. Compose 2–3 channels — lift +
shadow + color. Cards: `translateY(-2px) scale(1.006)` is plenty; anything over
`scale(1.02)` on a large card reads as a zoom bug.

**SwiftUI**
```swift
.scaleEffect(pressed ? 0.96 : 1)
.animation(.spring(response: 0.25, dampingFraction: 0.7), value: pressed)
```

**Reduced motion:** keep color/shadow, drop transform.
**Failure mode:** `transition: all` (animates layout properties you didn't intend) and
hover states that only change opacity.

---

## 2. Modal / dialog

**Answers:** *where did it come from?* Scale-from-origin beats a centred fade because it
explains itself.

```css
.backdrop { opacity: 0; transition: opacity var(--t-medium) var(--ease-out); }
.sheet    { opacity: 0; transform: scale(0.94) translateY(8px);
            transition: opacity var(--t-medium) var(--ease-out),
                        transform var(--t-medium) var(--ease-out); }
.open .backdrop { opacity: 1; }
.open .sheet    { opacity: 1; transform: scale(1) translateY(0); }
/* exits are ~20% faster and accelerate away */
.closing .backdrop, .closing .sheet {
  transition-duration: 240ms; transition-timing-function: var(--ease-in);
}
```

Causality: set the origin from whatever was clicked, so it grows out of the trigger.

```js
const r = trigger.getBoundingClientRect();
sheet.style.transformOrigin = `${r.left + r.width/2}px ${r.top + r.height/2}px`;
```

Use `<dialog>` for focus trapping and `::backdrop`, and remember `display` isn't
animatable — either keep the node mounted, use `@starting-style` + `transition-behavior:
allow-discrete`, or delay unmount by the exit duration.

**Damping:** modals are serious surfaces — critically damped (ζ ≥ 1, no bounce).
A bouncing dialog reads as a toy.

**Reduced motion:** opacity only, 120ms, no scale.
**Failure mode:** no exit at all (`display:none` on close) — the single most common
omission in modal code.

---

## 3. Drawer / sheet

**Answers:** *where did it go?* Edge-anchored, so it must travel from its edge.

```css
.drawer { transform: translateX(-100%);
          transition: transform var(--t-large) var(--ease-out); }
.drawer.open { transform: translateX(0); }
.drawer.closing { transition-duration: 360ms; transition-timing-function: var(--ease-in); }
```

Drag-to-dismiss: track the pointer 1:1 (no easing while the finger is down — the sheet
*is* the finger), then on release decide by **velocity, not position**: fling over
~0.5 px/ms dismisses even at 20% travel; otherwise snap to the nearer end with a spring
(k=400, c=38).

```js
const v = (y - lastY) / (now - lastT);      // px/ms
if (v > 0.5 || progress > 0.5) dismiss(); else snapBack();
```

**SwiftUI:** `.offset(y:)` + `DragGesture`, release into
`.spring(response: 0.35, dampingFraction: 0.85)`; read `value.predictedEndTranslation`
for the fling.
**Failure mode:** easing the drag itself (lag between finger and sheet destroys
direct-manipulation feel).

---

## 4. Dropdown / popover

**Answers:** *what opened, and from where?* Small, fast, anchored.

```css
.menu { opacity: 0; transform: scale(0.96) translateY(-4px);
        transform-origin: top center;      /* match the anchor edge */
        transition: opacity 150ms var(--ease-out), transform 150ms var(--ease-out); }
.menu.open { opacity: 1; transform: none; }
```

150ms, not 300 — menus are seen dozens of times per session and any weight becomes
friction. Set `transform-origin` to the anchored edge (top-left for a left-aligned
trigger, bottom for an upward menu). Stagger items only if there are ≤ 6 and the menu
is a feature surface; utility menus should arrive as one block.

**Failure mode:** staggering a 12-item menu — the last item lands 400ms after the user
already started reading.

---

## 5. Toast stack

**Answers:** *what happened?* — while never stealing the cursor.

Enter from the edge it lives on (`translateY(16px)` for bottom-anchored) over 250ms
ease-out. Exit at 200ms ease-in, **and collapse the gap**: the toasts below must move up,
which is a layout change — animate it with FLIP or `transform` on the survivors, never by
animating `height`.

```js
// FLIP the survivors after removing one
const first = [...stack.children].map(el => el.getBoundingClientRect().top);
stack.removeChild(dead);
[...stack.children].forEach((el, i) => {
  const dy = first[i + 1] - el.getBoundingClientRect().top;
  el.animate([{ transform: `translateY(${dy}px)` }, { transform: 'none' }],
             { duration: 220, easing: 'cubic-bezier(0.22,1,0.36,1)' });
});
```

Auto-dismiss pauses on hover and on focus-within. Stack ≥ 4 → collapse into a count.
**Failure mode:** the removed toast's neighbours snapping instantly — the jump is what
makes toast stacks feel cheap.

---

## 6. Accordion

**Answers:** *what expanded?* The classic `height: auto` problem.

Modern (Chrome 129+, progressive enhancement):
```css
:root { interpolate-size: allow-keywords; }
.panel { height: 0; overflow: clip; transition: height var(--t-medium) var(--ease-out); }
.panel.open { height: auto; }
```

Universally compatible today — animate grid rows instead:
```css
.panel { display: grid; grid-template-rows: 0fr;
         transition: grid-template-rows var(--t-medium) var(--ease-out); }
.panel.open { grid-template-rows: 1fr; }
.panel > div { overflow: hidden; }   /* required for the collapse to clip */
```

Duration scales with content: 200ms for a short panel, 350ms for a long one; over ~450ms
it feels broken. Rotate the chevron on the same curve (secondary action) but let it
finish ~80ms after the panel for follow-through.

**Failure mode:** measuring `scrollHeight` and animating pixel heights — it thrashes
layout every frame and breaks on resize/content change.

---

## 7. Tabs

**Answers:** *where am I now?* The indicator carries the continuity.

Slide the indicator between tabs rather than fading it — the travel is the information.

```js
const r = tab.getBoundingClientRect(), p = list.getBoundingClientRect();
indicator.style.transform = `translateX(${r.left - p.left}px) scaleX(${r.width / 100})`;
// indicator is 100px wide at rest; transition transform 250ms var(--ease-out)
```

Content swap: cross-fade at 150ms with a 40% overlap, or slide horizontally in the
direction of travel (right-to-left when moving to a later tab) at 200ms. Never both.

**SwiftUI:** `matchedGeometryEffect` on the indicator across tab views.
**Failure mode:** animating the indicator's `left`/`width` (layout) instead of
`transform`/`scaleX`.

---

## 8. List insert / remove / reorder (FLIP)

**Answers:** *what changed?* Layout animation, done the only cheap way.

FLIP = First, Last, Invert, Play. Measure before, mutate, measure after, apply the
inverse transform, animate it away.

```js
function flip(items, mutate, { duration = 300 } = {}) {
  const first = new Map(items.map(el => [el, el.getBoundingClientRect()]));
  mutate();
  for (const el of items) {
    const a = first.get(el), b = el.getBoundingClientRect();
    const dx = a.left - b.left, dy = a.top - b.top;
    if (!dx && !dy) continue;
    el.animate([{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'none' }],
               { duration, easing: 'cubic-bezier(0.22,1,0.36,1)' });
  }
}
```

Entrances stagger 20–40ms (cap the window at ~450ms: `delay = min(i, 8) * 40`);
removals do not stagger — they leave together at 200ms ease-in, then survivors FLIP into
place. Reorder: 300ms, no stagger, everything moves at once so the swap reads as one event.

**Failure mode:** animating `top`/`margin` for reflow, and staggering removals (which
makes deletion feel slow and uncertain).

---

## 9. Drag with snap-back

**Answers:** *is this alive?* Direct manipulation must be 1:1, and release must be physical.

Follow the pointer with no easing. On release, hand the *current velocity* to a spring —
this is the case tweens genuinely cannot do well.

```js
let v = 0, x = 0, target = 0;                       // px, px/frame
function frame(dt) {                                 // dt in seconds
  const k = 400, c = 38;                             // ζ≈0.95, settles ~250ms
  v += (-k * (x - target) - c * v) * dt;
  x += v * dt;
}
```

Rubber-banding past a boundary: `overshoot = pow(raw, 0.55)` — resistance grows with
distance, matching the iOS feel. Add `touch-action: none` on the drag surface and use
Pointer Events (not mouse/touch pairs).

**Failure mode:** applying easing during the drag, and dropping the release velocity so
the element stops dead.

---

## 10. Number ticker

**Answers:** *what changed?* — for dashboards, counters, prices.

```js
const el = document.querySelector('#value');
function tickTo(to, from = +el.dataset.v || 0, dur = 600) {
  const t0 = performance.now();
  (function step(now) {
    const t = Math.min(1, (now - t0) / dur);
    const e = 1 - Math.pow(1 - t, 5);                 // easeOutQuint
    el.textContent = Math.round(from + (to - from) * e).toLocaleString();
    if (t < 1) requestAnimationFrame(step); else el.dataset.v = to;
  })(performance.now());
}
```

Requires `font-variant-numeric: tabular-nums` or the whole row jitters as glyph widths
change. Pair with a 120ms colour pulse in the direction of change (up/down) — that pulse
is often the only motion a serious data product needs. Cap duration at 600ms and never
animate a number that changes more than ~twice a second.

**Failure mode:** proportional figures (layout shifts every frame), and counting up on
every poll so the number is never readable.
