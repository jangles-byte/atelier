# Composition: Grids, Hierarchy, Negative Space

## Hierarchy: the channel budget

A viewer should know what to read first, second, third without deciding to. You
have six channels to say "this matters": **size, weight, color/contrast, space,
position, motion**. The discipline: each hierarchy level differs from its neighbor
by **at most two channels**. Differ by one and levels blur; differ by four and the
page shouts. A classic well-built card: title (larger + heavier), metadata (smaller
+ muted), body (default everything) — two channels, one channel, baseline.

Diagnosis by squint (or 8px Gaussian blur on a screenshot): the blur should reveal
2–4 obvious masses in a deliberate order. One undifferentiated field → no
hierarchy. Ten competing blobs → everything is emphasized, so nothing is.

**One hero per view.** Every screen, slide, and chart has exactly one element with
maximum visual mass — the thing the job (from the philosophy's purpose line) says
matters most. Two heroes is a fight; the fix is demotion, not further promotion.

## Grids

- **Columns:** 12 for full pages (divisible by 2/3/4), 4 on mobile, 8 for tools.
  The grid earns its keep only when elements *span asymmetrically*: 7+5, 8+4, 3+9.
  Equal splits (6+6, 4+4+4) everywhere means the grid is organizing nothing —
  that's the template skeleton.
- **Gutters** from the spacing ladder (16–32px); **margins** larger than gutters.
- **Baseline-ish vertical rhythm:** vertical spacing in multiples of the body
  line-height's pixel value (e.g. 8px system with 24px body leading → verticals in
  24s where text blocks meet).
- **Alignment is the cheapest quality signal.** Every element's edge should land on
  a grid line or another element's edge — the difference between "designed" and
  "assembled" is usually eight stray edges. Optical alignment overrides geometric:
  circles, triangles, and quote marks need to overhang the geometric edge (~2–6px
  or `padding-inline` compensation) to *look* aligned.

### Breaking the grid

Breaks read as intent only against an otherwise strict grid, and each break must be
one of the sanctioned moves: **bleed** (image/color field runs to viewport edge
while text holds the grid), **overlap** (element straddles two zones to bind them,
e.g. card overlapping hero into content), **rotation** (±1–3° on a single accent
element, Organic direction only), **interruption** (oversized display type or
numeral crossing column boundaries), **asymmetric void** (deliberately empty
columns — see below). One or two break types per design. Three-plus breaks = no
grid = no breaks.

## Negative space

Space is a material you spend, not what's left over. Its jobs: **isolation** (the
hero is the element with the most space around it — power = emptiness around, not
size alone), **grouping** (proximity, per `scale-and-space.md`), and **pacing**
(dense passages then a void = visual breathing; uniform density = monotone). The
asymmetric void is the strongest sophistication signal available: content occupying
7 of 12 columns with 5 genuinely empty reads as confidence; content stretched to
fill reads as fear of emptiness. Density is a *choice* per the philosophy —
Bloomberg-dense and gallery-sparse are both excellent — but even maximal density
needs one isolation zone, and even galleries need one dense anchor.

## Reading gravity

F-pattern for text-heavy interfaces, Z-pattern for heroes/posters/slides: the eye
enters top-left (LTR), and exits bottom-right — which is why terminal CTAs sit
bottom-right and why a logo bottom-left feels lost. Place the hero on the entry
path; place the action on the exit path. Against-gravity placements (right-aligned
navigation rails, bottom-anchored headlines) are legitimate signature moves *when
the philosophy claims them* — they cost a beat of viewer effort and must buy
distinctiveness with it.

## Per-stack notes

**CSS** — real CSS Grid with named lines/areas, not nested flex approximating one.
`grid-template-columns: repeat(12, 1fr)` + spans; bleeds via a full-width grid with
a constrained center track (`minmax(0,1fr) min(100% - 2*var(--margin), 72rem)
minmax(0,1fr)`).

**Slides (incl. pptx/Keynote)** — one idea per slide, hero at poster scale, 5:7-ish
asymmetric split; margins ≥ 8% of slide width; never center-stack more than three
elements.

**Charts** — hierarchy channels apply directly: the key series gets chroma and
weight, context series get grey hairlines; direct-label the endpoint instead of a
legend (position channel); title top-left on the reading path, not centered above.

**Game HUD / native screens** — safe-area margins are the grid edge; corner-anchor
groups (health top-left, currency top-right) with ladder spacing; the "one hero"
rule becomes "one unanchored element maximum" — the reticle/focus point.
