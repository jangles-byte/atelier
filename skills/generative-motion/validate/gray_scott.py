#!/usr/bin/env python3
"""
gray_scott.py — verify that a reaction–diffusion (f, k) pair actually produces its pattern.

Why this exists: the viable region of Gray–Scott is a narrow curved band in (f, k) space.
A pair a little outside it does not produce a worse pattern — it produces *nothing*, within
a few hundred steps, and you cannot tell which side of the line you are on by looking at
the numbers. Every named pattern quoted in a reference should be run before it is quoted.

Classification is deliberately crude but decisive:
  dead     — B washes out; the field returns to A=1 everywhere
  saturated— B floods; no structure, the whole field is reacting
  uniform  — B survives but with no spatial variation
  pattern  — B survives with structure, and we count the features

Usage:
  ./gray_scott.py                 # check the pairs documented in systems.md
  ./gray_scott.py --scan          # map the viable band, to find new pairs
"""
import argparse
import numpy as np

DOCUMENTED = {
    "mitosis": (0.0367, 0.0649),
    "coral":   (0.0545, 0.0620),
    "spots":   (0.0300, 0.0620),
    "worms":   (0.0780, 0.0610),
    "waves":   (0.0140, 0.0470),
}

def laplace(x):
    return (-x
            + 0.20 * (np.roll(x, 1, 0) + np.roll(x, -1, 0) + np.roll(x, 1, 1) + np.roll(x, -1, 1))
            + 0.05 * (np.roll(np.roll(x, 1, 0), 1, 1) + np.roll(np.roll(x, 1, 0), -1, 1)
                    + np.roll(np.roll(x, -1, 0), 1, 1) + np.roll(np.roll(x, -1, 0), -1, 1)))

def run(f, k, n=180, steps=9000, Da=1.0, Db=0.5, dt=1.0, seed=3):
    rng = np.random.default_rng(seed)
    A = np.ones((n, n), dtype=np.float64)
    B = np.zeros((n, n), dtype=np.float64)
    r = n // 12
    c = n // 2
    B[c-r:c+r, c-r:c+r] = 1.0
    A[c-r:c+r, c-r:c+r] = 0.0
    B += rng.random((n, n)) * 0.02            # symmetry breaking
    for _ in range(steps):
        r2 = A * B * B
        A += (Da * laplace(A) - r2 + f * (1.0 - A)) * dt
        B += (Db * laplace(B) + r2 - (k + f) * B) * dt
        np.clip(A, 0.0, 1.0, out=A)
        np.clip(B, 0.0, 1.0, out=B)
        if not np.isfinite(B).all():
            return None, "diverged"
    return B, None

def features(B):
    """count local maxima above half-max — a crude but stable feature count"""
    t = B.max() * 0.5
    m = (B > t)
    if not m.any():
        return 0
    peak = ((B >= np.roll(B, 1, 0)) & (B >= np.roll(B, -1, 0)) &
            (B >= np.roll(B, 1, 1)) & (B >= np.roll(B, -1, 1)) & m)
    return int(peak.sum())

def classify(B):
    mean, std, mx = B.mean(), B.std(), B.max()
    if mx < 0.05:                 return "dead", mean, std, 0
    frac = (B > 0.2).mean()
    if frac > 0.85:               return "saturated", mean, std, 0
    if std < 0.02:                return "uniform", mean, std, 0
    return "pattern", mean, std, features(B)

def check():
    bad = 0
    print(f"{'name':10s} {'f':>7s} {'k':>7s}  {'result':10s} {'meanB':>7s} {'sd':>6s} {'features':>8s}")
    for name, (f, k) in DOCUMENTED.items():
        B, err = run(f, k)
        if err:
            print(f"{name:10s} {f:7.4f} {k:7.4f}  {err}")
            bad += 1
            continue
        kind, mean, std, nf = classify(B)
        flag = "" if kind == "pattern" else "   <-- NOT A PATTERN"
        bad += 0 if kind == "pattern" else 1
        print(f"{name:10s} {f:7.4f} {k:7.4f}  {kind:10s} {mean:7.4f} {std:6.3f} {nf:8d}{flag}")
    return bad

def scan():
    print("viable band (f down, k across) — '#' is a pattern, '.' dead/uniform")
    ks = np.arange(0.045, 0.070, 0.0025)
    fs = np.arange(0.010, 0.090, 0.005)
    print("        " + "".join(f"{k:.3f} "[2:] for k in ks))
    for f in fs:
        row = ""
        for k in ks:
            B, err = run(f, k, n=96, steps=4000)
            row += "  .  " if err else ("  #  " if classify(B)[0] == "pattern" else "  .  ")
        print(f" f={f:.3f} {row}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--scan", action="store_true")
    a = ap.parse_args()
    raise SystemExit(scan() if a.scan else (1 if check() else 0))
