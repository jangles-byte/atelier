# The Design Philosophy Document

A design philosophy is a short prose document written *before* implementation. It is
the single highest-leverage artifact in this package: implementation that follows a
written philosophy converges; implementation without one wanders toward the training-
data mean. The format is adapted from Anthropic's `algorithmic-art` and
`canvas-design` skills, generalized to every medium.

## Format

```markdown
# <Direction Name>

<4–6 paragraphs, ~40–80 words each>

**Is not:** <three anti-adjectives / rejected directions>
**Signature move:** <the one describable decision>
```

### 1. Name the direction (1–2 words)

Naming forces commitment. "Ledger Brutalism", "Warm Terminal", "Museum Label",
"Cartographic", "Midnight Editorial". A name you'd be embarrassed to defend is a name
that will produce embarrassing output — pick one you can argue for.

### 2. The paragraphs

Cover, in prose, not bullets:

- **Worldview** — what this design believes. ("Data is the hero; chrome is theft.
  Every pixel that isn't information must justify itself as structure.")
- **Space & structure** — how the composition breathes. Dense or airy, symmetric or
  tension-based, grid-locked or grid-breaking, and *why the job demands it*.
- **Color & material** — the emotional register of the palette, what surfaces feel
  like (paper, glass, phosphor, ink), where the single loudest accent lives.
- **Type voice** — what the typography sounds like if read aloud: clipped and
  technical, warm and bookish, loud and editorial.
- **Motion temperament** (if the medium moves) — nervous or calm, snappy or viscous,
  and what motion is *for* here (feedback, orientation, delight — pick a primary).

Write with conviction. Hedged philosophy ("clean and modern, with a touch of
personality") produces hedged design. Specific philosophy produces specific design.

### 3. "Is not"

The negative space of the direction. Three rejections, at least one of which must be
tempting — rejecting only strawmen ("is not: ugly, cluttered, broken") is a dodge.
Good example: "Is not: playful, glassy, or dense. Kills on sight: gradient meshes,
emoji in UI copy, cards with drop shadows."

### 4. Signature move

One sentence. The decision a viewer could describe from memory a day later. "All
numbers render in a monospaced slab at 2× body size." "Navigation is a single
vertical rail of rotated text." "Every state change propagates as a 300ms wave from
the point of interaction."

## Worked example

```markdown
# Ledger Brutalism

This interface believes a trading dashboard is an instrument, not a brochure. Its
ancestors are Bloomberg terminals and paper ledgers: information at maximum density
with zero decoration, where the design's beauty comes from the rigor of its alignment
rather than from ornament.

Space is rationed, not lavished. Columns lock to a strict tabular grid; the only
generous whitespace sits above the single number that matters most, isolating it the
way a ledger isolates a balance. Nothing floats — every element is anchored to a rule
line or a column edge.

Color is ink-on-paper inverted: near-black surfaces, off-white text, and exactly one
accent — a phosphor green reserved for positive deltas and calls to action. Red
appears only for losses. Nothing else in the interface is allowed to be colorful, so
that color itself becomes data.

Type is a single monospaced family at three sizes. Its voice is a telegraph operator:
terse, fixed-pitch, all signal. Hierarchy comes from weight and rule lines, never
from decorative size jumps.

Motion is nearly absent, which makes the exceptions land: numbers tick with a 120ms
color pulse when they change, and that is the only animation in the product.

**Is not:** friendly, glassy, or spacious. Kills on sight: gradients, rounded cards,
skeleton shimmer.
**Signature move:** color is reserved exclusively for data direction — the UI itself
is achromatic.
```

## Rules of use

- Keep it under a page. A philosophy that needs scrolling won't be followed.
- Write it into the project (`DESIGN.md`) when there is a project; otherwise state it
  in full in conversation before implementing.
- When a later decision is hard, the philosophy decides it. When the philosophy can't
  decide it, the philosophy is missing a sentence — add it.
- On revision requests ("make it pop more"), update the philosophy first, then the
  artifact. Drift begins when the artifact leads.
