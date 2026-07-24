# The Dead Motion Diagnostic

Run when animation exists but underwhelms — "feels dead / floaty / cheap / janky /
AI-generated". Work the list in order; each check names its fix. Most dead motion
fails 2–3 of the first five.

## 1. Is anything actually linear?

Grep for `linear`, default-eased Web Animations calls, raw `lerp(a, b, t)` with
unshaped `t`, engine tweens with default interpolation. Uniform velocity is the #1
killer. **Fix:** ease-out on enters, ease-in on exits (`easing-and-springs.md`).

## 2. Uniform durations?

If everything animates at one duration (the classic: `transition: all 300ms`),
motion carries no weight information — big things and small things move identically,
so nothing feels like an object. **Fix:** duration scale from `principles.md`
(micro 100–150 → large 400–600), exits ~20% faster. Also kill `transition: all`
(it eases properties you never meant to animate, and adds jank).

## 3. Does everything start and stop at once?

Simultaneous start + simultaneous stop = "PowerPoint slide arrives". No
follow-through, no overlap, no life. **Fix:** stagger group members 20–40ms;
let one secondary element (shadow, icon, underline) settle ~80ms after its parent.

## 4. Overshoot: absent (dead) or everywhere (cheap)?

Zero overshoot anywhere reads clinical-to-dead in products whose philosophy says
"alive"; bounce on *every* element reads as a toy ad. **Fix:** springs with ζ ≈
0.8–0.9 for most moves; one or two hero moments at ζ 0.55–0.7; ζ ≥ 1 for modals
and serious surfaces. Character lives in the *distribution* of bounce, not its
presence.

## 5. Floaty? Check duration × distance × easing together.

"Floaty" = too slow for its size, or ease-in-out where ease-out belongs (the slow
start reads as hesitation), or spring stiffness too low (k < ~150 on a small
element). **Fix:** drop duration one class (400→250), switch to a decisive
ease-out, raise stiffness. Elements are lighter than they look on screens; err
fast.

## 6. Is it animating the wrong property?

Opacity-only hovers read as cheap; width/height/top/left animation both janks and
mushes (see `performance-craft`). Cheap-feel often = the *change itself* is
trivial. **Fix:** compose transform + opacity (scale 1.02 + lift −2px + shadow
deepen beats any single property); FLIP layout moves onto transforms.

## 7. Missing anticipation or exit?

Things that appear from nothing and vanish instantly feel like DOM mutations, not
events. **Fix:** entrances get origin (scale from 0.96, slide from 8–16px away —
*from the direction that explains them*); exits exist at all (the most common
omission), accelerating away toward where they'd return from.

## 8. No causality?

Motion that starts nowhere: the modal fades in centered regardless of what was
clicked; the ripple ignores the pointer. **Fix:** originate motion at the
interaction point — `transform-origin` at the trigger, distance-based stagger
rippling outward, shared-element (FLIP / matchedGeometry) from the tapped item.

## 9. Interruption broken?

Mash-test: hover on/off rapidly, open/close mid-animation, spam the button. Snaps,
restarts-from-zero, or queue pileups make polished values feel broken anyway.
**Fix:** `easing-and-springs.md` § Interruption — animate from current value;
springs retarget with velocity.

## 10. Is it dead because it's janky?

Stutter reads as "cheap" before the eye can judge the choreography. Frame-time
check before value-tuning: DevTools performance panel / Xcode Instruments / engine
profiler. If frames drop, fix with `performance-craft` *first* — no easing value
rescues 40fps.

## 11. Is it dead because it shouldn't exist?

An animation answering no question (feedback / orientation / character) can't be
tuned into mattering; it's decoration on a delay. Also: ambient motion competing
with the content, or juice on insignificant events (see restraint notes in
`principles.md`). **Fix:** delete it. Motionlessness next to one excellent
animation beats six mediocre ones — scarcity is what makes the good one land.

## Output format

After diagnosis, report as: failing check numbers → concrete value changes
(property, from → to, e.g. "§2: modal 300ms→260ms, tooltip 300ms→140ms; §4: card
hover spring k=400 c=38"). Then re-render and watch it again — the diagnostic
isn't done until the re-render passes.
