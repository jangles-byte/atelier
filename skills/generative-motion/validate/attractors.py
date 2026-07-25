#!/usr/bin/env python3
"""
attractors.py — verify that a strange-attractor parameter set is actually worth rendering.

Why this exists: most parameter sets are visually dead, and you cannot tell by looking at
the numbers. A set can converge to a fixed point, fall into a short cycle, diverge to
infinity, or fill the plane as featureless noise — and all four produce a wasted render.
Worse, interpolating between two *good* sets passes through regions where the attractor
collapses, so animating parameters needs checking along the whole path.

Three measurements decide it:
  * finite      — no NaN/inf after the transient
  * lyapunov    — largest Lyapunov exponent > 0 means chaotic (structure, not a cycle)
  * occupancy   — fraction of a 256x256 grid visited. Too low is a line or a point;
                  too high is noise with no filigree.

Usage:
  ./attractors.py                       # check the sets documented in systems.md
  ./attractors.py --search clifford 40  # hunt for new sets, print the good ones
  ./attractors.py --path clifford 0 1   # check every step between two sets (for animation)
"""
import argparse, math, sys
import numpy as np

MAPS = {
    "clifford": lambda x, y, p: (math.sin(p[0]*y) + p[2]*math.cos(p[0]*x),
                                 math.sin(p[1]*x) + p[3]*math.cos(p[1]*y)),
    "dejong":   lambda x, y, p: (math.sin(p[0]*y) - math.cos(p[1]*x),
                                 math.sin(p[2]*x) - math.cos(p[3]*y)),
}

# the sets currently documented in references/systems.md
DOCUMENTED = {
    "clifford": [(-1.4, 1.6, 1.0, 0.7), (1.7, 1.7, 0.6, 1.2), (-1.7, 1.3, -0.1, -1.21),
                 (1.5, -1.8, 1.6, 0.9)],
    "dejong":   [(1.641, 1.902, 0.316, 1.525), (-2.0, -2.0, -1.2, 2.0)],
}

def analyse(kind, p, n=60000, transient=1000, grid=256):
    f = MAPS[kind]
    x, y = 0.1, 0.1
    # a second trajectory, perturbed, for the Lyapunov estimate
    eps0 = 1e-9
    xe, ye = x + eps0, y
    lyap = 0.0
    xs = np.empty(n, dtype=np.float64)
    ys = np.empty(n, dtype=np.float64)

    for i in range(n + transient):
        x, y = f(x, y, p)
        xe, ye = f(xe, ye, p)
        if not all(map(math.isfinite, (x, y, xe, ye))):
            return {"ok": False, "reason": "diverged"}
        d = math.hypot(xe - x, ye - y)
        if d == 0:
            # trajectories merged: contracting, not chaotic
            xe, ye = x + eps0, y
        else:
            lyap += math.log(d / eps0)
            s = eps0 / d
            xe, ye = x + (xe - x)*s, y + (ye - y)*s
        if i >= transient:
            xs[i - transient] = x
            ys[i - transient] = y

    lyap /= (n + transient)
    spanx, spany = np.ptp(xs), np.ptp(ys)   # ndarray.ptp() removed in numpy 2.x
    if spanx < 1e-6 or spany < 1e-6:
        return {"ok": False, "reason": "collapsed to a point or line", "lyapunov": lyap}

    gx = ((xs - xs.min()) / spanx * (grid - 1)).astype(np.int32)
    gy = ((ys - ys.min()) / spany * (grid - 1)).astype(np.int32)
    occ = len(np.unique(gx.astype(np.int64) * grid + gy)) / (grid * grid)

    ok = lyap > 0.01 and 0.02 < occ < 0.60
    reason = ("chaotic" if ok else
              "not chaotic (cycle or fixed point)" if lyap <= 0.01 else
              "too sparse" if occ <= 0.02 else "too diffuse — noise, no structure")
    return {"ok": ok, "reason": reason, "lyapunov": round(lyap, 4),
            "occupancy": round(occ, 4), "span": (round(spanx, 2), round(spany, 2))}

def check_documented():
    bad = 0
    for kind, sets in DOCUMENTED.items():
        print(f"\n{kind}")
        for p in sets:
            r = analyse(kind, p)
            flag = "PASS" if r["ok"] else "FAIL"
            bad += 0 if r["ok"] else 1
            extra = f"λ={r.get('lyapunov')}, occ={r.get('occupancy')}"
            print(f"  {flag}  {p}  {r['reason']}  ({extra})")
    return bad

def search(kind, want, seed=0):
    rng = np.random.default_rng(seed)
    found = 0
    tries = 0
    print(f"\nsearching {kind} for {want} viable sets")
    while found < want and tries < 20000:
        tries += 1
        p = tuple(rng.uniform(-2.0, 2.0, 4).round(3))
        r = analyse(kind, p, n=8000, transient=400, grid=128)
        if r["ok"] and r["occupancy"] > 0.06:
            found += 1
            print(f"  {p}  λ={r['lyapunov']}  occ={r['occupancy']}")
    print(f"  ({tries} candidates tested — most parameter sets are dead)")

def path(kind, i, j, steps=12):
    a, b = DOCUMENTED[kind][i], DOCUMENTED[kind][j]
    print(f"\ninterpolating {kind} {a} -> {b}")
    dead = 0
    for s in range(steps + 1):
        t = s / steps
        p = tuple(round(a[k] + (b[k] - a[k]) * t, 4) for k in range(4))
        r = analyse(kind, p, n=8000, transient=400, grid=128)
        if not r["ok"]:
            dead += 1
        print(f"  t={t:4.2f}  {'ok  ' if r['ok'] else 'DEAD'}  {r['reason']}")
    if dead:
        print(f"  -> {dead}/{steps+1} steps are visually dead. Do not lerp between these;\n"
              f"     orbit a single seed instead.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", nargs=2, metavar=("KIND", "N"))
    ap.add_argument("--path", nargs=3, metavar=("KIND", "I", "J"))
    a = ap.parse_args()
    if a.search:
        search(a.search[0], int(a.search[1]))
    elif a.path:
        path(a.path[0], int(a.path[1]), int(a.path[2]))
    else:
        sys.exit(1 if check_documented() else 0)
