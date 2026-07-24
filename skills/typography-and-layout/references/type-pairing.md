# Type Pairing With Intent

## The one-axis rule

Two faces pair when they **contrast decisively on one axis and agree on the rest**:
serif display over sans text (axis: class), a black-weight grotesque over its own
regular (axis: weight), a wide display over a normal-width text face (axis: width),
a mono over a humanist sans (axis: construction). Two similar sans faces (Inter +
Roboto) contrast on no axis — that's not a pairing, it's a version conflict. A
didone over a script contrasts on every axis — that's noise.

Strong default patterns:

| Pattern | Voice | Example pairing (all free/open) |
|---|---|---|
| High-contrast serif display / humanist sans text | editorial, authoritative | Playfair Display / Source Sans 3 |
| Chunky slab or black grotesque display / same family regular | confident, modern, single-family | Space Grotesk 700 / Space Grotesk 400 |
| Geometric sans display / serif text | contemporary essay, product story | Archivo / Source Serif 4 |
| Mono display / sans text | technical, terminal, data product | JetBrains Mono / Inter |
| Wide display / normal text | poster energy, sports, culture | Archivo Expanded / Archivo |

The single-family strategy (one variable family, extreme weight/width/optical-size
contrast) is underrated: maximum coherence, real contrast, one network request.

## Choosing the display face — this is the personality decision

The text face should be almost invisible; the display face *is* the design's voice.
Interrogate the philosophy's tone adjectives: "precise" → grotesque or mono;
"literary" → oldstyle or transitional serif; "loud" → black weights, condensed or
extended widths; "warm" → humanist sans, soft-terminal slab; "premium" → didone,
high-contrast serif, wide tracking on caps. Then apply the anti-generic test: Inter,
Roboto, Open Sans, and system-ui are *text* utilities — using one as the display
face is a decision not to have a voice (acceptable only when the philosophy
explicitly says so, e.g. brutalist system-font honesty).

## Craft details that separate senior from default

- **Tracking scales inversely with size.** Display sizes want negative tracking
  (−1% to −3%, e.g. `letter-spacing: -0.02em` at 64px); small caps and labels want
  positive (+5% to +12%). Default tracking at 96px looks amateur — the gaps read
  as holes.
- **Weight jumps of ≥ 300.** 400 vs 500 reads as rendering inconsistency; 400 vs
  700+ reads as hierarchy. Pick 2–3 weights total and make them far apart.
- **Optical sizes exist.** Variable fonts with an `opsz` axis (Source Serif 4,
  Literata, Fraunces) cut display sizes sharper and text sizes sturdier — enable
  `font-optical-sizing: auto` (on by default, but don't defeat it with fixed opsz).
- **OpenType features are free quality:** `tabular-nums` for data columns,
  `case`-sensitive forms for all-caps UI, real small caps (`font-variant-caps`),
  fractions in recipes/finance. In CSS: `font-feature-settings` /
  `font-variant-numeric`; in SwiftUI: `.monospacedDigit()`; in matplotlib: choose a
  face with tabular figures (e.g. Source Sans 3) for tick labels.
- **Hierarchy of quotation:** real quotes (“ ”), en/em dashes, and non-breaking
  spaces before units. Straight quotes in display type are a tell.

## Per-stack notes

**CSS** — self-host WOFF2 with `font-display: swap`, preload the display face only;
subset if the family is heavy. Variable font + `font-variation-settings` gives the
weight/width axes above at one file cost.

**SwiftUI / iOS** — prefer the platform voice unless the philosophy overrides: SF
Pro with `.fontDesign(.serif/.monospaced/.rounded)` covers four voices with perfect
rendering and Dynamic Type for free. Custom display faces via `UIFont` registration;
keep body text on the system face unless brand demands otherwise, and always support
Dynamic Type scaling.

**Slides / posters / charts** — display face earns its keep here most of all: titles
at genuinely poster scale (see `scale-and-space.md`), everything else in the text
face. In matplotlib set families once via `rcParams["font.family"]`; never mix the
default DejaVu with a brand face in the same figure.
