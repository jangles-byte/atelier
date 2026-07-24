# Warm Terminal

*(Design philosophy for the Driftlog example — produced by the `design-direction`
skill's workflow: interrogation → philosophy → point of view. This document was
written before `after.html`; every decision in that file traces back here.)*

**Job:** convince a developer in one viewport that Driftlog understands their
workflow, and get one click on "Start logging".
**Audience:** developers who live in terminals and distrust marketing gloss.
**Tone:** precise, warm, quietly confident. **Not:** corporate, playful, loud.

---

Driftlog is a tool for people whose day already happens in a terminal, so the page
speaks terminal as a native language — not as a costume. Its ancestors are man
pages, well-kept lab notebooks, and the amber phosphor of hardware that worked.
The design's warmth comes from light and type, never from rounded mascots or
exclamation points.

Space is structured like a log: a strict left rail of timestamps and rules, content
hung from it in asymmetric measure. The page reads top-to-bottom like output
scrolling by — dense where information lives, with one long deliberate silence
before the final prompt. Nothing is centered; centering is for posters, and this
is an instrument.

Color is a dark, warm ground — charcoal with a trace of amber in it, never pure
black — carrying ivory text and exactly one accent: amber phosphor. The accent is
rationed to what a cursor would touch: the prompt, the primary action, the live
line. Green appears once, as a status dot, meaning only "recording". Everything
else earns attention through lightness, not hue.

Type is a two-voice conversation: JetBrains Mono for everything that is *the
product* — headings, log lines, timestamps, buttons — and a quiet humanist sans
(Inter, at text sizes only, where it is a fine text face) for explanatory prose.
The mono speaks at genuinely large sizes in the hero, tracking tightened, because
confidence here means setting `$ driftlog` at 72px and not blinking.

Motion is a typewriter's temperament: instant, discrete, honest. The hero log line
types itself once; the cursor blinks; state changes snap with 120–180ms ease-out.
Nothing drifts, nothing floats, nothing parallaxes. Reduced motion gets the same
page with the line pre-typed.

**Is not:** corporate, playful, or glossy. Kills on sight: gradients, emoji
bullets, drop-shadowed cards, centered hero stacks.
**Signature move:** the page is presented as a log of itself — every section
carries a timestamped log-line header (`09:41:07 · feature/capture`), and the hero
headline is a typed command with a live cursor.
