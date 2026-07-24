# The Change List Format

The critique's output is a ranked change list. Every entry follows one shape:

```
N. [dimension] Location: change X from <current> to <new> — <principle it serves>
```

Requirements per entry:

- **Location** precise enough to act on without asking: a selector, component name,
  file:line, or unambiguous description ("hero CTA", ".pricing-card h3").
- **Current → new with units.** Colors as hex or oklch(), space in px/rem, time in
  ms, curves by name or cubic-bezier, font sizes in px, weights as numbers. If the
  current value is unknown (screenshot-only critique), estimate it and mark the
  estimate: "(~16px)".
- **The principle**, in a clause, so the change teaches: "…so the section gap
  exceeds 2× the in-card gap", "…to put the muted text over 4.5:1".
- **Rank by impact on the lowest rubric scores**, accessibility findings first
  regardless of dimension score.

Anti-patterns: "improve the spacing" (no value), "consider a bolder font" (no
commitment), "the colors could be more harmonious" (no location, no value, no
principle — pure vibes), bundling five changes into one entry (unactionable and
unrankable).

## Worked example

Input: screenshot of a SaaS pricing page. Philosophy on file: "Warm Terminal —
precise, calm, technical; is not: playful, corporate, dense."

---

**Inventory:** Dark page; centered hero ("Simple pricing") ~36px semibold white;
three equal pricing cards (#1e1e2e on #14141f, radius 12px, shadow 0 4px 6px), the
middle badged "Popular" in purple #8b5cf6; per-card feature list at ~14px grey
#6b7280 with green check icons; each card a full-width purple CTA; footer FAQ links
#4b5563. Fonts: Inter throughout. Motion: cards lift 4px on hover, 300ms ease,
opacity-only fade-in on scroll.

**Scores:** Hierarchy 2 — three identical cards, three identical CTAs; "Popular"
badge is the only differentiation and it's 11px. Color 2 — purple #8b5cf6 is
off-philosophy (terminal warmth called for), grey #6b7280 on #14141f is 3.9:1
(fails AA), pure-grey neutrals on a tinted-dark ground. Typography 2 — Inter-only
contradicts "terminal"; 36px max jump is 2.25×; prices (the hero datum) same size
as card titles. Spacing 4 — consistent 24px ladder, though uniform (card-gap =
in-card gap = 24px). Motion 3 — hover works; scroll fade is linear-feeling,
no exits. Consistency 4 — one system, defaults throughout. Accessibility 2 — the
3.9:1 body grey plus color-only checkmarks. Distinctiveness 1 — this is the
slop-list page verbatim.

**Changes:**

1. **[accessibility] Feature-list text:** change #6b7280 to oklch(72% 0.01 265)
   (≈ #9a9ab0) — 4.9:1 on #14141f, clearing AA.
2. **[accessibility] Feature checks:** add 500-weight "Included" semantics —
   pair the green check with text weight, not hue alone.
3. **[hierarchy] Recommended card:** make the middle card the sole hero — scale
   1.0→1.04, surface +0.04 L, border 1px oklch(78% 0.09 85); demote outer-card
   CTAs to ghost buttons (transparent bg, 1px border) so one CTA is loudest.
4. **[color] Replace the purple system:** accent #8b5cf6 → warm amber
   oklch(78% 0.13 85) per "Warm Terminal"; reserve it for the hero CTA and price
   deltas only (60-30-10).
5. **[typography] Prices:** 20px → 44px JetBrains Mono 700, tabular-nums — the
   price is the datum; make it the biggest thing on each card.
6. **[typography] Display voice:** hero + card titles Inter → JetBrains Mono
   (600, tracking −1%); keep Inter for body — one-axis pairing that delivers the
   terminal voice.
7. **[distinctiveness] Signature move:** prices render with a terminal cursor
   block that blinks once on card hover (2 frames, 120ms) — small, describable,
   on-philosophy.
8. **[spacing] Section rhythm:** hero→cards gap 24px → 64px and card-gap 24px →
   32px, so between-group > within-group (in-card stays 24px).
9. **[motion] Scroll entrance:** opacity-only 300ms → translateY(12px→0) +
   opacity, 240ms cubic-bezier(0.22,1,0.36,1), 40ms stagger per card; add
   150ms ease-in fade-out for dismissed FAQ items.

**Re-render check:** after applying, re-screenshot; expect Hierarchy 2→4,
Color 2→4, Accessibility 2→4, Distinctiveness 1→3. Remaining gap: the three-card
skeleton itself (structural; propose only if the user is open to layout surgery).

---

Note the shape of entry 7: distinctiveness findings still get exact values.
"Make it more unique" is never a finding.
