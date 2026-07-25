# Three Dimensions

Two routes, and picking the wrong one costs a rewrite. **Raymarched SDFs** need no geometry
at all — the whole image is one fragment shader, and the scene is a mathematical function.
**Rasterised geometry** (Three.js and friends) is the right call the moment you need real
models, physics, or many independent objects.

| | Raymarched SDF | Rasterised (Three.js) |
|---|---|---|
| Scene is | a distance function | meshes and instances |
| Infinite repetition | free (`mod` the domain) | costly |
| Smooth blending of forms | free (`smin`) | hard |
| Loading a model | impractical | trivial |
| Cost scales with | screen pixels × march steps | triangles × instances |
| Best at | organic, infinite, morphing | objects, scenes, particles in depth |

## Raymarching, minimally

March a ray from the camera, stepping by the distance to the nearest surface — which is
safe because the SDF guarantees nothing is closer than that.

```glsl
float map(vec3 p);                                  // the whole scene, as one function

float march(vec3 ro, vec3 rd){
  float t = 0.0;
  for (int i = 0; i < 96; i++){
    float d = map(ro + rd * t);
    if (d < 0.001 * t) break;                       // epsilon scales with distance
    if (t > 60.0) break;                            // far plane; unbounded scenes hang
    t += d * 0.9;                                   // <1 for safety with warped SDFs
  }
  return t;
}
vec3 normal(vec3 p){                                // gradient by tetrahedron sampling
  vec2 e = vec2(1.0, -1.0) * 0.0005;
  return normalize(e.xyy*map(p+e.xyy) + e.yyx*map(p+e.yyx)
                 + e.yxy*map(p+e.yxy) + e.xxx*map(p+e.xxx));
}
```

**The epsilon must scale with `t`.** A fixed `0.001` produces visible surface noise in the
distance and wasted steps up close — this is the single most common raymarching artefact.

**Step scaling below 1.0** is required as soon as you warp the domain (twisting, bending,
`sin` displacement), because those operations break the distance guarantee and a full step
will tunnel through surfaces. 0.7–0.9 is the usual range; if you see holes in the geometry,
lower it before anything else.

### Primitives and operations

```glsl
float sphere(vec3 p, float r){ return length(p) - r; }
float box(vec3 p, vec3 b){ vec3 q = abs(p)-b;
  return length(max(q,0.0)) + min(max(q.x,max(q.y,q.z)),0.0); }
float torus(vec3 p, vec2 t){ return length(vec2(length(p.xz)-t.x, p.y)) - t.y; }

float opUnion(float a, float b){ return min(a,b); }
float opSub  (float a, float b){ return max(-a,b); }
float opInter(float a, float b){ return max(a,b); }

// smooth minimum — the reason SDFs look organic, and the most useful function here
float smin(float a, float b, float k){
  float h = clamp(0.5 + 0.5*(b-a)/k, 0.0, 1.0);
  return mix(b, a, h) - k*h*(1.0-h);
}
```

`k` in `smin` is the blend radius in world units — 0.1–0.6 for most scenes. Blending two
spheres with `smin` rather than `min` is the difference between a snowman and a single
living form.

### Infinite domains, free

```glsl
vec3 q = mod(p + 0.5*c, c) - 0.5*c;                 // repeat every c units
vec3 q = p - c*clamp(round(p/c), -lim, lim);        // finite repetition, bounded
```
Domain repetition is why SDF scenes render vast structures for the same cost as one — the
map function never knows how many copies exist. Repeat *after* a slow rotation of `p` and
the grid stops reading as a grid.

### Shading that isn't flat

- **Ambient occlusion**, five short samples along the normal: cheap, and it does most of
  the work of making a shape read as solid.
- **Soft shadows** by marching toward the light and tracking the closest approach —
  `res = min(res, k*h/t)` — a fraction of the cost of a real shadow map.
- **Fog by distance**: `mix(sceneColour, fogColour, 1.0 - exp(-t*density))`. Exponential,
  not linear; linear fog reads as a wash.
- **Colour by the same rules as 2D**: earned by a property. Distance, normal direction,
  ambient occlusion, or iteration count all carry meaning. Iteration count in particular
  makes a beautiful free heat-map of scene complexity.

### Cost

Cost is `pixels × steps`, so the far plane and the step count are the two budget knobs.
Lower the step count and distant surfaces dissolve; raise the far plane and everything
slows. Render at half resolution and upscale for anything soft or foggy — SDF scenes with
fog survive it invisibly. On a 4K display, always render at a fixed internal resolution
rather than native.

## Rasterised: instancing is the whole game

For particles and objects in depth, the rule is **one draw call, many instances**. In
Three.js, `InstancedMesh` with a per-instance matrix, or `Points` with a custom shader:

```js
const mesh = new THREE.InstancedMesh(geo, mat, 50000);
mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);   // updating every frame
// per frame: write matrices into mesh.instanceMatrix.array, then
mesh.instanceMatrix.needsUpdate = true;
```

Above ~50k instances, stop writing matrices on the CPU and move the simulation to the GPU:
positions in a data texture, read in the vertex shader — the same GPGPU pattern as
[`gpu-and-shaders.md`](gpu-and-shaders.md), with the render pass drawing instanced quads
instead of points.

**Depth is the thing 2D cannot give you**, so spend it: size attenuation with distance,
fog thinning the far field, and depth-of-field or a blurred far layer. A particle system
with no depth cues is a 2D particle system that costs more.

**Additive particles in 3D need `depthWrite: false`** and no depth sorting, or they punch
holes in each other. Blending is order-dependent for alpha but not for additive, which is
one more reason additive is the default for glowing systems.

## What carries over unchanged

Everything in [`density-and-tone.md`](density-and-tone.md) and
[`post-processing.md`](post-processing.md) applies identically — arguably more, because 3D
renders naturally produce HDR values that must be tone-mapped, and bloom on an emissive 3D
scene is what sells it as light rather than as bright paint. The
[`art-direction.md`](art-direction.md) tells apply too: rainbow hue, uniform density and
one-scale-for-everything ruin a 3D piece exactly as fast.

The one addition is **camera discipline**. A slowly orbiting camera is the default and it
is nearly always wrong — it reads as a turntable product shot. Prefer a camera that drifts
along a path with slight noise, holds still during interesting moments, and never completes
a full revolution. Motion of the camera and motion of the subject compete; pick one.
