# The Anti-Generic Checklist

Genericism is not one bad decision; it is the *absence* of decisions — every choice
defaulting to the statistical center of the training data. This file catalogs the
tells. Check drafts against it; treat two or more hits as a failed direction step.

## Default-AI tells (the slop list)

Layout:
- Hero with centered headline + subhead + two buttons, then three feature cards in a
  row, then alternating image/text bands. (The single most common AI page skeleton.)
- Every section the same width, same padding, same card treatment — no rhythm.
- Border-radius 8–16px on everything, drop shadow `0 4px 6px rgba(0,0,0,0.1)`.
- 12-column grid used only as three or four equal columns.

Color:
- Purple/indigo gradient (`#667eea → #764ba2` and family) on hero or buttons.
- Blue-500 as accent because nothing chose otherwise.
- Dark mode as pure `#000`/`#111` with the light palette's saturated colors unchanged.
- Glassmorphism (blur + translucency) applied to cards that hover over nothing.

Type:
- Inter/Roboto/Open Sans at 16px body, 48px hero, weight 400/700 only, no size jumps
  bigger than 3×, tracking untouched.
- Title Case On Every Heading, emoji as section bullets (🚀 ✨ 💡).

Copy & content:
- "Empower", "Seamless", "Supercharge", "Unlock", "Effortless" in headings.
- Lorem-shaped feature triads ("Fast. Secure. Scalable.").

Motion:
- Everything fades up on scroll with the same duration and delay.
- Hover states that only change opacity.
- Pulsing gradient blobs in the hero background.

Data viz:
- Category-10 default palette, legends instead of direct labels, gridlines at full
  opacity, 3D or donut charts for two values.

## Why it happens

Each default is individually defensible — that's what makes them defaults. Genericism
is the *conjunction*: when every axis (layout, color, type, motion, copy) sits at its
default simultaneously, the result is a template regardless of technical quality.

## The countermeasure

You do not need to deviate everywhere. Pick 1–3 axes where the philosophy demands
deviation, and execute the rest with disciplined restraint:

1. **One structural decision** the template version wouldn't make (asymmetric grid,
   vertical nav rail, oversized index numbers, exposed rule lines).
2. **One color decision** that requires defending (an off-palette accent, achromatic
   UI with color reserved for data, a tinted—not grey—neutral ramp).
3. **One type decision** with contrast (a display face with actual character, a 6×+
   scale jump, a mono for all numerals).

Restraint elsewhere is what makes the deviations read as intent instead of noise.

## Litmus tests

- **The describability test:** could a viewer describe one thing about this design
  from memory tomorrow? If not, no signature move exists.
- **The swap test:** swap the logo for a competitor's. Does the design still fit
  perfectly? Then it belongs to no one.
- **The screenshot test:** in a folder of twenty screenshots of similar products,
  would this one be findable in under three seconds?
- **The default audit:** list five visual decisions and ask of each, "did the
  philosophy choose this, or did it choose itself?" More than three self-chosen
  defaults → return to the philosophy.
