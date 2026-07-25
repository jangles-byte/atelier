# Post-Processing: The Layer That Makes It Look Finished

Raw simulation output looks like simulation output. The gap between a sketch and something
that reads as a photograph of a real phenomenon is mostly here — and it is the cheapest
quality per line of code in the whole discipline. Two or three of these, tuned quietly, are
usually the difference.

The discipline is restraint: each effect below is invisible when it's right and obvious
when it's overdone. If a viewer can name the effect, it is too strong.

## Order of operations

Effects are not commutative. This order is standard because each stage assumes the previous:

1. **Render the scene** to an HDR-ish buffer (`RGBA16F`), letting values exceed 1.0
2. **Bloom** — extract bright areas, blur, add back
3. **Chromatic aberration** and **distortion** — lens behaviour, applied to the composed image
4. **Tone map** — HDR → 0–1 (see [`density-and-tone.md`](density-and-tone.md))
5. **Colour grade** — lift/gamma/gain, or a gradient map
6. **Vignette**
7. **Grain** — always last, so it isn't blurred or graded and stays at pixel scale

Getting grain before tone mapping is the most common ordering mistake: the grain gets
crushed by the curve and disappears in the shadows where you wanted it most.

## Bloom

The single highest-impact effect for additive/emissive work. Real bloom is not "blur the
whole image" — it is *bright areas only*, spread wide.

```glsl
// 1. bright pass, at half resolution
vec3 c = texture(uScene, uv).rgb;
float lum = dot(c, vec3(0.2126, 0.7152, 0.0722));
o = vec4(c * smoothstep(THRESH - 0.1, THRESH + 0.1, lum), 1.0);   // THRESH ~0.7-1.0
```

Then blur that buffer and add it back: `final = scene + bloom * INTENSITY`. Intensity
0.25–0.6; above ~0.8 everything turns to fog.

**Do it as a mip chain, not one big blur.** Downsample the bright pass to 1/2, 1/4, 1/8,
1/16, blurring at each level, then upsample and accumulate. Five small blurs give a far
wider, softer, cheaper glow than one large kernel, and the wide soft falloff is what reads
as light rather than as blur. Separate each blur into horizontal and vertical passes.

**Threshold with a soft knee** (the `smoothstep` above rather than a hard `step`), or
pixels pop in and out of bloom as they cross the threshold and the image flickers.

## Chromatic aberration

Sample each channel at a slightly different radius. Real lenses disperse more toward the
edges, so scale by distance from centre — uniform aberration reads as a broken video codec.

```glsl
vec2 d = uv - 0.5;
float r2 = dot(d, d);
vec2 off = d * r2 * AMOUNT;                 // AMOUNT ~0.01-0.04
o = vec3(texture(uTex, uv + off).r,
         texture(uTex, uv      ).g,
         texture(uTex, uv - off).b);
```

Keep it below the point where you can identify colour fringes on a still. It should only be
detectable by turning it off.

## Grain

Film grain is what stops a smooth gradient from banding, and it makes synthetic images read
as captured. Two rules: it must be **animated** (static grain reads as a dirty screen), and
it must be **stronger in the midtones** than in the blacks or highlights, because that is
how film behaves.

```glsl
float n = fract(sin(dot(gl_FragCoord.xy + uTime*13.7, vec2(12.9898, 78.233))) * 43758.5453);
float lum = dot(c, vec3(0.2126,0.7152,0.0722));
float w = 4.0 * lum * (1.0 - lum);          // peaks at mid grey, zero at both ends
c += (n - 0.5) * AMOUNT * w;                // AMOUNT ~0.02-0.06
```

Grain also *masks banding for free* — if a dark gradient is stepping, adding a little grain
is a better fix than more bit depth.

## Vignette

Darken the corners so the eye stays where you want it. Subtle: the effect should not be
nameable.

```glsl
float v = smoothstep(1.0, RADIUS, length((uv - 0.5) * vec2(aspect, 1.0)));
c *= mix(1.0 - STRENGTH, 1.0, v);           // RADIUS ~0.35-0.55, STRENGTH ~0.15-0.35
```

Correct for aspect ratio or the vignette is an ellipse on wide displays. For a warmer look,
tint the darkening slightly rather than multiplying to neutral grey.

## Feedback and displacement

The most distinctive effect here, and the least used. Sample the *previous frame*, offset
by a field, and blend it with the current one:

```glsl
vec2 flow = (fbm2(uv * 3.0, uTime) - 0.5) * 0.004;   // tiny offsets only
vec3 prev = texture(uPrev, uv + flow).rgb;
o = mix(current, prev * DECAY, FEEDBACK);            // DECAY ~0.96, FEEDBACK ~0.7
```

This produces smearing, trailing and organic dissolve that no per-frame effect can. Offsets
must be very small — a few thousandths of a UV — or it becomes an obvious swirl. `DECAY`
below 1.0 is mandatory: at exactly 1.0 energy accumulates until the frame is white.

Rotational or scaling feedback (sampling the previous frame slightly rotated or zoomed)
gives infinite-tunnel and bloom-from-within effects, and is where a lot of the classic
demoscene look comes from.

## Colour grading

After tone mapping, the cheapest transformative move is a **gradient map**: take the
luminance and look up a colour ramp, then blend back toward the original by taste.

```glsl
float lum = dot(c, vec3(0.2126,0.7152,0.0722));
vec3 graded = texture(uRamp, vec2(lum, 0.5)).rgb;
c = mix(c, graded, 0.85);
```

A three- or four-stop ramp (deep shadow tint → midtone → highlight tint) applied at 70–90%
will unify an image whose colours were never quite coherent, and it is how most
"cinematic" looks are actually made. Duotone is the same trick with two stops.

Lift/gamma/gain, if you prefer working like a colourist:
`c = pow(max(c*gain + lift, 0.0), vec3(1.0/gamma))`.

## Budget

At 1080p, each fullscreen pass is ~2M fragments. A reasonable stack is:
bright-pass (½ res) + 5 blur levels (mip chain, all small) + one composite pass ≈ the cost
of about 1.5 fullscreen passes. Grain, vignette, aberration and grading should all live in
that **same final composite shader** — do not give each its own pass, it is pure bandwidth
for no benefit.

If the frame budget is blown, cut in this order: feedback → bloom levels (5→3) → aberration
→ grain. Keep the vignette and the tone map; they cost almost nothing and do the most for
legibility. This mirrors the degradation ladder in the `performance-craft` skill.
