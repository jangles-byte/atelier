# GPU: When, and How Without Losing a Day

Most generative systems die on the CPU not because the algorithm is wrong but because the
population is too small to express it. Physarum needs a million agents before it branches;
reaction–diffusion is per-pixel by definition; fluid is a grid solve. On the GPU these run
at 60fps. In JavaScript they do not run at all.

## The decision rule

Go GPU when any of these is true:

- **Per-element work × element count > ~5M operations per frame.** 50k agents doing three
  texture samples each is already at the edge in JS.
- **The system is per-pixel**: reaction–diffusion, fluid, domain-warped noise at full
  resolution, cellular automata, feedback effects.
- **The population is the aesthetic.** Physarum at 30k agents is a different (worse) piece
  than physarum at 1M, not the same piece running slower. Lace requires the count.

Stay on CPU when the element count is under ~10k, the logic is branchy or needs neighbour
queries with a spatial hash (boids), or the piece needs to run everywhere without WebGL2.

## The architecture: state lives in textures

There is one pattern and everything uses it. **Ping-pong**: read from texture A, write to
texture B, swap. Never read and write the same texture in one pass — it's undefined and
produces feedback garbage.

For an agent system, agent state is a square float texture: a 1024×1024 RGBA32F texture is
1,048,576 agents with four floats each (x, y, heading, spare). Passes per frame:

1. **Move** — fullscreen quad over the *agent* texture; each fragment is one agent. Read
   state from A, sample the environment, write new state to B. Swap.
2. **Deposit** — draw `gl.POINTS`, one vertex per agent, into the environment texture with
   additive blending. The vertex shader reads the agent's position by `gl_VertexID`.
3. **Diffuse/decay** — fullscreen quad over the environment texture, blur and multiply.
4. **Present** — fullscreen quad to the default framebuffer, mapping the field to colour.

Four passes, no vertex buffers, no CPU readback. Readback (`readPixels`) is what kills GPU
pipelines — it stalls until the GPU finishes. Never do it per frame.

### Attribute-less drawing

You do not need vertex buffers for any of this. A fullscreen triangle from `gl_VertexID`:

```glsl
#version 300 es
void main(){ vec2 p = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);
             gl_Position = vec4(p * 2.0 - 1.0, 0, 1); }
```
`gl.drawArrays(gl.TRIANGLES, 0, 3)` — one triangle covering the viewport, cheaper than two
(no diagonal seam, better quad utilisation).

And one point per agent, positions fetched from the state texture:

```glsl
#version 300 es
uniform sampler2D uAgents; uniform vec2 uRes; uniform int uSide;
void main(){
  ivec2 id = ivec2(gl_VertexID % uSide, gl_VertexID / uSide);
  vec2 p = texelFetch(uAgents, id, 0).xy;
  gl_Position = vec4(p / uRes * 2.0 - 1.0, 0, 1);
  gl_PointSize = 1.0;
}
```
`gl.drawArrays(gl.POINTS, 0, agentCount)` with an empty VAO bound. Use `texelFetch`, not
`texture` — it takes integer coordinates and ignores filtering, which is what you want for
state.

## The extension minefield

This is where the day disappears, because **the failures are silent**. Request these up
front and check them:

| Extension | Without it |
|---|---|
| `EXT_color_buffer_float` | Float textures are not renderable; framebuffers are incomplete |
| **`EXT_float_blend`** | **Blending into a 32-bit float target silently writes nothing** |
| `OES_texture_float_linear` | `LINEAR` filtering on float textures fails; samples read black |

The middle one cost me an afternoon: the deposit pass ran, the draw call succeeded, no
error was raised, and the trail map stayed empty. **Prefer half-float (`R16F`/`RGBA16F`)
for accumulation buffers** — it is renderable *and* blendable in core WebGL2, and 16 bits
is ample for a trail map or a density field. Reserve 32-bit for agent state, where position
precision actually matters.

```js
const gl = canvas.getContext('webgl2', { antialias:false, alpha:false });
if (!gl.getExtension('EXT_color_buffer_float')) throw new Error('no float targets');
gl.getExtension('OES_texture_float_linear');
gl.getExtension('EXT_float_blend');
```

## Debugging, in the order that finds it fastest

A black frame has about five causes. Check them in this order — each is one line:

1. **`gl.getError()`** immediately after each pass. `1286` (`INVALID_FRAMEBUFFER_OPERATION`)
   means you drew to an incomplete framebuffer; `1281` (`INVALID_VALUE`) is usually a
   texture format/type mismatch.
2. **`gl.checkFramebufferStatus(gl.FRAMEBUFFER)`** after attaching. Anything other than
   `FRAMEBUFFER_COMPLETE` (36053) means the format isn't renderable — almost always a
   missing float extension.
3. **Shader compile and link logs.** Always check `COMPILE_STATUS` and `LINK_STATUS` and
   throw the info log; a silently failed program draws nothing.
4. **Is blending on a float target?** See above. This raises no error.
5. **Is the tone map clipping to zero?** Render the raw field as `vec3(t)` with no curve.
   If you see structure, the field is fine and the problem is colour — see
   [`density-and-tone.md`](density-and-tone.md).

Uniform locations are per-program: call `getUniformLocation` *after* `useProgram`, and set
uniforms after binding the program, not before.

## Fragment-shader systems

Some systems have no agents at all — the texture *is* the state, and one shader advances it.

**Reaction–diffusion** (Gray–Scott) is the canonical case. A and B in two channels of a
half-float texture, one pass per step, 5–15 steps per frame because the simulation runs far
faster than 60Hz needs:

```glsl
vec2 lap = -uv * 1.0
  + (n + s + e + w) * 0.2 + (ne + nw + se + sw) * 0.05;   // 3x3 laplacian
float A = uv.x, B = uv.y, r = A*B*B;
o = vec4(A + (Da*lap.x - r + f*(1.0-A)) * dt,
         B + (Db*lap.y + r - (k+f)*B)   * dt, 0, 1);
```
Run it at 256²–512², not screen resolution, and upsample on present; the patterns have no
high-frequency detail to lose and it's 10× cheaper.

**Fluid** (stable fluids) is advect → diffuse → project → advect-dye, each its own pass,
with the pressure projection needing 20–40 Jacobi iterations. It is the heaviest thing in
this file and the most rewarding; budget six-plus passes per frame.

**Domain warping and SDF raymarching** are single-pass — the whole image is one fragment
shader with no state at all. These are the cheapest way to get something beautiful on
screen, and the easiest to iterate on because there is no simulation to settle.

## Precision

Declare `precision highp float;` in every fragment shader. `mediump` is 16-bit on many
mobile GPUs and destroys position accuracy and noise quality — the symptom is banding or
agents snapping to a grid. Use `highp` for positions and accumulators, and note that
`half`/`mediump` is fine for colour work if you are optimising for a phone.

Integer division in GLSL ES 300 is exact for `int`, which is what makes the
`gl_VertexID % side` addressing above reliable.

## Cost model

Think in **passes × pixels**, not in objects. A 4-pass pipeline at 1920×1080 is ~8.3M
fragment invocations per frame before any agents — that is the floor. Then:

- Agent passes cost `agentCount` fragments (the state texture), which at 1M agents is
  comparable to one fullscreen pass at 1080p. Cheap.
- The deposit pass costs `agentCount` point rasterisations. Also cheap, but **additive
  blending is bandwidth-bound**: every point is a read-modify-write.
- Blur passes are the expensive ones. A 3×3 blur is nine samples per pixel; separate it
  into two 1D passes (3+3) when the kernel grows past 5 taps.

Halve the resolution of anything that isn't the final image. Simulation grids, glow
buffers, and blur chains all survive it invisibly.

## Always pause when hidden

An unattended generative sketch will pin a GPU indefinitely and drain a laptop. Every piece
needs this, and it is the single most common omission (including in this package's own
first six sketches):

```js
document.addEventListener('visibilitychange', () => {
  running = !document.hidden;
  if (running) { last = performance.now(); requestAnimationFrame(frame); }
});
```
Gate the `requestAnimationFrame` call on `running`, and reset your `last` timestamp on
resume or the first frame after waking integrates a multi-minute `dt`.
