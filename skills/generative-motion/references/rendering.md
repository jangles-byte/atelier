# Rendering: Trails, Blending, Colour, Scale

The algorithm decides what moves. This decides whether it looks like a screensaver or a
photograph of something real.

## Trails — the accumulation buffer

Do not clear the canvas. Fade it:

```js
ctx.globalCompositeOperation = 'source-over';
ctx.fillStyle = 'rgba(6, 5, 10, 0.055)';     // the ground colour, low alpha
ctx.fillRect(0, 0, W, H);
```

The alpha *is* the trail length: 0.02 gives long smoky tails, 0.10 short comet heads, 0.3
is nearly no trail. This is the highest-leverage single number in the whole piece — tune
it before anything else.

**Two cautions.** First, the fade colour must be the exact ground colour or the frame
drifts to a tint over a minute. Second, with very low alpha, 8-bit rounding means dark
trails never quite reach zero and the frame slowly greys out — if you need alpha below
~0.02, render to a float texture or periodically hard-clear.

Draw *segments*, not points: `moveTo(prevX, prevY); lineTo(x, y)`. Points at speed become
dotted lines; segments stay continuous at any velocity.

## Blending

- **`lighter` (additive)** — overlapping strokes accumulate to white-hot. This is what
  makes dense regions glow without any blur, and it is nearly always the right choice on
  dark grounds. Keep per-stroke alpha low (0.02–0.15) so accumulation does the work.
- **`screen`** — softer additive, saturates less harshly.
- **`multiply`** — for ink-on-paper pieces on light grounds; the inverse aesthetic and
  badly under-used.
- **`destination-out`** — erasing brushes, for carving negative space.

Additive on a *light* ground does nothing (everything is already bright), so pick ground
and blend mode together, not separately.

## Colour that means something

Map colour to a property the system actually has, and use OKLCH so steps are perceptual:

| Property | Reads as |
|---|---|
| speed / velocity magnitude | heat — fast is bright and hot |
| age / lifetime | embers cooling, or ink drying |
| curvature or turn rate | stress, tension in the structure |
| local density / neighbour count | mass, glow where things gather |
| field divergence or curl magnitude | turbulence |

```js
const L = 32 + speed*52, C = 0.10 + speed*0.085, H = 22 + speed*58;
ctx.strokeStyle = `oklch(${L}% ${C} ${H} / ${alpha})`;
```

Note that **chroma rises with lightness** here — a common mistake is holding chroma
constant, which makes bright regions look chalky. Keep the hue span narrow (40–70°); a
full hue rotation is the single loudest "student work" signal in generative art. Two
hues plus the ground is usually the whole palette.

## Envelopes — nothing pops

Every particle needs a fade in and out, or spawns and deaths flicker:

```js
const age = life / maxLife;
const env = Math.min(1, age*5) * Math.min(1, (1-age)*3);   // fast in, slower out
```

Stagger initial ages at startup (`life = random()*maxLife`) or the whole population dies
simultaneously and the piece pulses.

## Scale and performance

- **Canvas 2D** handles ~3–10k stroked segments per frame comfortably. Beyond that, batch
  by colour bucket (group strokes into 8–16 colour bins and issue one path each) — the
  per-`stroke()` overhead dominates, not the pixels.
- **Typed arrays, not objects.** `Float32Array` with a stride (x, y, px, py, life, max) is
  several times faster than an array of objects and produces no GC pressure.
- **WebGL** for 100k+ agents: particles as a texture (position/velocity in RG/BA channels),
  update in a fragment shader, render as points. Physarum and reaction-diffusion belong
  here — they are per-pixel by nature.
- **Half-resolution + upscale** works remarkably well for glow-heavy fields: render the
  particle layer at 0.5×, draw it up with smoothing. Detail loss is invisible; cost is
  quartered.
- **DPR**: cap at 2. A retina flow field at DPR 3 is 2.25× the fill cost for no visible
  gain.

Always `dt`-clamp (`min(dt, 1/30)`), and stop the loop when the page is hidden — see the
`performance-craft` skill.

## Export

For stills, render at 2–4× and downsample: antialiasing for free, and the piece survives
being printed. For loops, drive the animation from a phase variable that returns to its
start (`t = (frame / totalFrames) * TAU`), so the loop is seamless by construction rather
than by cross-fade.
