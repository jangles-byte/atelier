# Critique: `before.html` (Driftlog landing page)

*Produced by the `critique` skill's protocol: real render → inventory → rubric →
ranked changes with exact values. Philosophy on file: `DESIGN.md` ("Warm
Terminal — precise, warm, quietly confident; not corporate, playful, loud").*

## Inventory

Rendered at 1280×800. Purple-gradient hero (135°, #667eea→#764ba2) with a
centered stack: 48px/700 white headline, 18px subhead at 90% opacity, two
buttons (white solid + white outline). Below, three equal cards (white, radius
12px, shadow 0 4px 6px rgba(0,0,0,.1)), each: 40px emoji, 20px title, 15px grey
#888 body, all center-aligned. Final band #f7f7f9 with centered 32px heading and
a gradient button. Inter throughout; weights 400/600/700. Motion: `transition:
all 300ms ease`, hover = opacity 0.85. Uniform section padding 80px; card gaps
24px.

## Scores

- **Hierarchy 2** — headline, two equal-weight hero buttons, three identical
  cards, and a second 32px heading all compete; blur test shows one purple mass
  and undifferentiated white below. No single hero element.
- **Color 1** — the exact slop-list gradient (#667eea→#764ba2); no palette
  beyond it (greys are pure); card body #888 on white = 3.5:1, **fails AA**;
  hero subhead at 90% white on mid-purple ≈ 4.1:1, fails at 18px.
- **Typography 2** — Inter-only at default tracking; max jump 48px = 3× but the
  page voice is "any product"; center-aligned everything; emoji as icons.
- **Spacing & alignment 3** — consistent (80/24) but perfectly uniform: gap
  between unrelated sections equals gap inside cards' content; nothing groups.
- **Motion 2** — `transition: all` (animates properties never intended);
  opacity-only hover reads cheap; no entrance choreography, no exits.
- **Consistency 3** — one system, but two button vocabularies (white-on-purple
  and gradient-on-grey) and radius 8 vs 12 mixed.
- **Accessibility 2** — the two contrast failures above; no visible focus
  styles; emoji announced by screen readers as "rocket, sparkles, light bulb".
- **Distinctiveness 1** — fails the swap test (any SaaS logo fits), fails the
  describability test (nothing memorable), four slop-list hits (gradient hero,
  three-card row, emoji bullets, "Supercharge/Seamless" copy).

## Changes (ranked)

1. **[accessibility] Card body text:** #888 → #555 (7.4:1) — clears AA now,
   independent of the redesign.
2. **[accessibility] All interactive elements:** add `:focus-visible { outline:
   2px solid currentColor; outline-offset: 2px }` — keyboard users currently get
   the browser default on a gradient, i.e. nothing.
3. **[color] Replace the gradient system:** per DESIGN.md, ground the page in
   oklch(18% 0.015 75) charcoal-amber; text oklch(92% 0.01 75); one accent
   oklch(78% 0.14 75) reserved for the prompt, the primary CTA, and the cursor.
   Delete both gradients.
4. **[hierarchy] One CTA:** "Get Started" becomes the sole filled-accent button;
   "Learn More" demotes to an underlined mono text link; delete the duplicate
   bottom CTA band's heading (keep a single closing prompt line).
5. **[typography] Voice:** headings/buttons/labels → JetBrains Mono; hero
   command at 72px/700, tracking −2%, left-aligned; body prose stays Inter 16px
   but measure capped at 60ch.
6. **[distinctiveness] Signature move:** render the page as a log of itself —
   timestamped mono section headers (`09:41:07 · feature/capture`) replacing the
   emoji cards' titles, and a typed hero command with a blinking cursor.
7. **[spacing] Break the uniformity:** section gaps 80px → 128px; within-feature
   spacing 16px; left rail alignment replaces centering so all edges share one
   grid line.
8. **[motion] Purposeful only:** replace `transition: all 300ms` with scoped
   `transition: background-color 150ms cubic-bezier(0.22,1,0.36,1), color 150ms`;
   hero line types once at load (reduced-motion: pre-typed); cursor blinks at
   1.06s steps(1).
9. **[consistency] One radius (2px), one button height (44px), one border
   (1px oklch(32% 0.02 75))** — replacing radius 8/12 and the two button styles.

**Re-render expectation:** Hierarchy 2→4, Color 1→5, Typography 2→4,
Accessibility 2→4, Distinctiveness 1→4. Result: `after.html`.

## The iterate pass (critique of `after.html`, round 2)

The protocol requires re-rendering and re-measuring the fixed version — and it
caught a real defect in the first pass of `after.html`: the `--text-faint`
timestamp text (13px) measured **3.4:1** on the page ground and **3.22:1** inside
the log window (measured in-browser via canvas readback of the computed oklch
colors, not eyeballed). Below the 4.5:1 body-text floor.

**Change:** `--text-faint` oklch(52% 0.012 75) → oklch(66% 0.012 75).
**Re-measured:** loglines 6.02:1, window timestamps 5.69:1 — passing, with the
faint/muted/primary hierarchy preserved (6.0 < 6.5 < 14.8). This is what step 5
of the workflow is for: the first render of a fix is a hypothesis, not a result.
