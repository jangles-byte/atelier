# The Eight-Dimension Rubric

Score each 1–5 against the anchors. 5 requires the *senior tell*, not just absence of
problems. Cite on-screen evidence for every score — a score without evidence is a
vibe with a number.

## 1. Hierarchy

Does the eye know where to go first, second, third? Blur-test the screenshot (or
squint): 2–4 masses in deliberate order.
**1** — uniform field, no entry point. **3** — hero identifiable but competing
siblings (two CTAs styled equally, three same-size headings). **5** — unmistakable
first read; each level differs from the next by ≤ 2 channels (size/weight/color/
space/position/motion); one hero per view.

## 2. Color

Palette coherence, contrast discipline, chroma restraint.
**1** — default-blue accent, pure greys, contrast failures. **3** — pleasant but
undisciplined: 2+ competing saturated hues, dead greys, dark mode as inversion.
**5** — tinted neutrals; one loudest color with assigned meaning; 60-30-10
dominance; every text pair passes 4.5:1 (checked, not assumed); semantic colors
tuned to the palette.

## 3. Typography

Voice, scale, and craft.
**1** — one family/one size, default tracking everywhere, orphan display type.
**3** — competent but timid: safe pairing, ≤ 3× max scale jump, body measure off
(< 40ch or > 90ch), display type at body line-height. **5** — display face with a
voice matching the philosophy; real modular scale with a brave top end; tracking
tightened at display sizes; tabular numerals where numbers move; measure 45–75ch.

## 4. Spacing & Alignment

The grid, the ladder, the edges.
**1** — random values, misaligned edges, elements touching container walls.
**3** — consistent but uniform: same gap everywhere, so grouping is invisible; grid
present but only equal columns. **5** — spacing from a ladder with proximity logic
(between-group ≥ 2× within-group); every edge on a grid line or shared edge;
asymmetry used deliberately; at least one confident void.

## 5. Motion (score n/a for stills)

Purpose, physics, interruption.
**1** — none where feedback demands it, or linear/uniform motion everywhere.
**3** — animations present, defaults unexamined: `all 300ms ease`, no exits, no
stagger, breaks under mash-testing. **5** — every animation answers a named
question; durations follow the weight scale; springs/easing consistent
(one motion character); interruptible; reduced-motion path exists and is complete.

## 6. Consistency

Is the design one system? Radii, shadows, icon stroke weights, control heights,
easing curves, capitalization, empty/loading/error states as designed states.
**1** — three radii, two shadow styles, mixed icon sets. **3** — mostly one system,
with orphans (one odd button, an unstyled scrollbar/focus ring/select).
**5** — token-driven throughout; the odd one out doesn't exist; states (hover,
focus, disabled, empty, error) all look like they were designed on purpose.

## 7. Accessibility

The floor, checked not vibed.
**1** — contrast failures on body text, color-only meaning, no focus indicators,
motion ignores reduced-motion. **3** — main text passes but muted text/placeholders
fail; focus visible but default; hit targets < 44px present. **5** — full pair
matrix ≥ AA; hue never the sole channel; visible designed focus states; targets ≥
44×44 (touch) / 24×24 (pointer); reduced-motion complete; zoom to 200% doesn't
break layout.

## 8. Distinctiveness

The anti-generic dimension.
**1** — indistinguishable from a template; multiple slop-list hits (purple
gradient, three feature cards, Inter-at-defaults, emoji bullets). **3** — clean and
professional but anonymous: passes the swap test (any logo fits), fails the
describability test (nothing memorable). **5** — a signature move a viewer could
describe tomorrow; the design could only belong to this product; restraint
elsewhere makes the move read as intent.

## Scoring discipline

- Evidence per score, one line minimum ("Hierarchy 2: nav, hero headline, and
  banner all compete at ~32px bold within one viewport").
- The **lowest two dimensions** define the critique's focus; do not spend change-
  list slots polishing 4s while 2s exist.
- Accessibility caps the total: no render with Accessibility ≤ 2 may be called
  finished, regardless of other scores.
- Re-render after applying changes and re-score. Movement of the lowest scores —
  not the average — is the progress metric.
