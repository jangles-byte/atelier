---
name: design-direction
description: Establish a deliberate aesthetic point of view before building anything visual. Use this skill FIRST whenever starting any visual work — a website, landing page, app UI, dashboard, data visualization, slide deck, game screen, generative art piece, poster, or component library — even if the user only says "make it look good", "build me a page", or "design a UI". Also use it when the user complains that a design looks generic, bland, "AI-generated", or like a template. This skill produces a short written design philosophy that every other design decision follows.
---

# Design Direction

Generic output happens when implementation starts before intent exists. This skill
forces the intent step: a short, written design philosophy that commits to one
aesthetic point of view — and names what it is *not* — before a single pixel exists.

## Workflow

1. **Interrogate the brief** — answer the five questions in
   [references/interrogation.md](references/interrogation.md). If the user's request
   doesn't answer them, infer defensible answers from context and state your
   assumptions; do not stall on questions when the user isn't available.
2. **Write the philosophy** — a named direction plus 4–6 tight paragraphs, using the
   format in [references/philosophy-format.md](references/philosophy-format.md).
   Write it into the project (e.g. `DESIGN.md`) or state it in full before implementing.
3. **Pick a point of view** — choose or blend a direction from
   [references/aesthetic-vocabularies.md](references/aesthetic-vocabularies.md), and
   check the result against [references/anti-generic.md](references/anti-generic.md)
   (the catalog of default-AI tells to avoid).
4. **Then implement** — loading the other Atelier skills (`color`,
   `typography-and-layout`, `motion`) as the work requires them.
5. **Render, critique, iterate** — never ship a visual without rendering the real
   result and running the `critique` skill on it.

## Which reference to load

| Situation | Load |
|---|---|
| Starting any visual work | `references/interrogation.md` then `references/philosophy-format.md` |
| Choosing/naming an aesthetic | `references/aesthetic-vocabularies.md` |
| Work is drifting generic, or reviewing for genericism | `references/anti-generic.md` |

## The one rule

Every project gets **one signature move** — a single distinctive decision (a color no
template uses, an unusual type pairing, a bold grid break, a characteristic motion) that
someone could describe from memory. If nothing about the design is describable, the
direction step failed. Go back to step 2.
