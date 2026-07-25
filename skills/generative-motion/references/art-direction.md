# Art Direction for Generative Work

The checklist that separates a piece from a screensaver. Run it before shipping; most
failures are on this list, not in the maths.

## The eight tells of tutorial work

1. **Rainbow hue.** Colour cycling through the spectrum over time or angle. It encodes
   nothing and it is the loudest possible signal that no decision was made. Narrow the
   hue span to 40–70° and map it to a real property.
2. **Uniform density.** Particles spread evenly edge to edge. Real compositions have
   crowds and voids — mask the spawn field.
3. **Pure black ground.** `#000` is flat and makes everything on it look like clip art.
   Use a dark tinted ground (L 10–18%, C 0.01–0.03) so the frame has a temperature.
4. **Everything at one scale.** One particle size, one stroke width, one speed. Vary size,
   speed and lifetime across the population — variation is what reads as organic.
5. **Too fast.** The field evolves at a rate that's exciting to the person tuning it and
   frantic to everyone else. Halve it twice.
6. **Full-frame wallpaper.** No focal point, no crop, nothing to look at first.
7. **Centred symmetry.** A perfectly centred radial system is inert. Offset the centre,
   or crop asymmetrically.
8. **No end state.** It looks great for six seconds then saturates to a grey mat, or dies
   to an empty frame. Run it for a minute before you believe it.

## The five decisions that make it a piece

**One idea.** A flow field *or* an attractor *or* reaction-diffusion. Two systems stacked
is almost always worse than either alone — the eye cannot find the structure.

**A named intent.** "Embers on a thermal." "Ink dropped in still water." "A colony finding
food." The metaphor decides colour, speed and density far more reliably than parameter
fiddling. Write it before you tune.

**A property that earns colour.** Pick it explicitly and say it out loud: *brightness
means velocity*. Then a viewer can read the image, even without knowing the rule.

**A composition, not a frame.** Decide where the density sits and what stays empty. Crop
in. Off-centre. Generative work is usually improved by zooming in past the point that
feels safe.

**A pace.** Slow enough to be hypnotic, with variety over time so it isn't static.
Ambient pieces want 20–60 second cycles; the eye should never see it repeat.

## Tuning order

Parameters interact, so tune them in this order — going out of order means re-tuning
everything each time:

1. **Field scale** (feature size) — sets the whole composition.
2. **Speed** — sets the character: languid or turbulent.
3. **Trail alpha** — sets whether it's smoke, filament, or dots.
4. **Population** — density and therefore glow.
5. **Colour ramp endpoints** — last, once structure is settled. Tuning colour first wastes
   all of it, because the structure changes what the ramp does.
6. **Evolution rate** — last of all, and slower than you think.

## The tests

- **The still test.** Pause on any frame. Is it a good image on its own? Generative motion
  that only works in motion is usually hiding weak structure.
- **The minute test.** Run 60 seconds. Trails saturate, particles pool in basins, energy
  dies or explodes. Almost every failure appears between second 10 and second 60.
- **The thumbnail test.** Shrink to 200px. Does it still have a structure, or is it grey
  fuzz? Fuzz at thumbnail size means the piece has detail but no composition.
- **The description test.** Can you describe it in one sentence that isn't the algorithm's
  name? "Gold filaments braiding through dark" is a piece. "A curl noise flow field" is
  a sketch.
