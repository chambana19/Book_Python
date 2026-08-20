# data/README.md -- energy_proxy(v) and the Week 11 multi-start table

Week 11's optimization studio does not use a CSV. Instead, Week 9 provided one
formula -- `energy_proxy(v)` -- as a fictional annual energy-use-intensity-like
score for a new wing, over two design variables packed into `v = (wwr, shade_m)`:
window-to-wall ratio (unitless, bounds [0.20, 0.60]) and overhang shade depth
(meters, bounds [0.0, 1.2]). Lower is better. Week 11's cells [1]-[11] cite this
file so that the exact formula and the exact eight-start table both live in one
place, instead of being retyped by hand and quietly drifting from Week 9's
original.

## 1. energy_proxy(v), copied verbatim from Week 9's instructor file

This is pasted unchanged from `ARC500_Week09B_Instructor.py` cell [1]. It is
the same two-basin surface swept there with a grid and re-used here as a
`scipy.optimize.minimize` objective -- only the tool changes, not the formula.

```python
def basin(x: np.ndarray, y: np.ndarray, cx: float,
          cy: float, depth: float, wx: float,
          wy: float) -> np.ndarray:
    """Gaussian dip of depth, centered at (cx, cy)."""
    dx = ((x - cx) ** 2) / (2 * wx ** 2)
    dy = ((y - cy) ** 2) / (2 * wy ** 2)
    return -depth * np.exp(-(dx + dy))


def energy_proxy(v: tuple[float, float]) -> float:
    """Provided proxy to MINIMIZE; v=(wwr, shade_m)."""
    w, s = v
    base = 20.0
    b1 = basin(w, s, 0.52, 0.25, 30.0, 0.06, 0.18)
    b2 = basin(w, s, 0.28, 0.90, 34.0, 0.06, 0.18)
    ridge = 6.0 * np.exp(-((w - 0.40) ** 2) / 0.02)
    return base + b1 + b2 + ridge
```

Bounds used everywhere in Week 11: `BOUNDS = [(0.20, 0.60), (0.0, 1.2)]`
(wwr min/max, then shade_m min/max).

## 2. The eight starting-guess table (Week 11 cell [4]), verified by running it

Reproduced by running `ARC500_Week11B_Instructor.py` fresh, top to bottom, with
`scipy.optimize.minimize(energy_proxy, x0=(start_wwr, start_shade), bounds=BOUNDS)`
called once per row. All eight rows converge with `success = True`.

| start_wwr | start_shade | final_wwr | final_shade | value    | basin  |
|-----------|-------------|-----------|--------------|----------|--------|
| 0.55      | 0.20        | 0.5241    | 0.2500       | -7.1521  | LOCAL  |
| 0.50      | 0.30        | 0.5241    | 0.2500       | -7.1521  | LOCAL  |
| 0.40      | 0.55        | 0.5241    | 0.2500       | -7.1521  | LOCAL  |
| 0.45      | 0.60        | 0.5241    | 0.2500       | -7.1521  | LOCAL  |
| 0.60      | 0.10        | 0.5241    | 0.2500       | -7.1521  | LOCAL  |
| 0.20      | 1.00        | 0.2763    | 0.9000       | -11.1437 | GLOBAL |
| 0.30      | 0.85        | 0.2763    | 0.9000       | -11.1437 | GLOBAL |
| 0.22      | 1.15        | 0.2763    | 0.9000       | -11.1437 | GLOBAL |

Count: 5 LOCAL, 3 GLOBAL. This matches Demo A (x0 = (0.55, 0.20) -> the LOCAL
row above, value -7.1521) and Demo B (x0 = (0.20, 1.00) -> the GLOBAL row
above, value -11.1437) from Week 11 cells [2]-[3], and it matches the two
self-check transfer starts in cell [9]: (0.35, 0.75) lands GLOBAL (-11.1437)
and (0.58, 0.15) lands LOCAL (-7.1521).

## 3. Why this file exists

Week 11 hands `energy_proxy` to `minimize` instead of sweeping it on a grid
like Week 9 did, and a `minimize` result only ever reports what the local
slope looked like from its own starting guess -- it cannot see a deeper basin
sitting somewhere else in bounds, which is exactly why this handout keeps one
verified copy of the formula and one verified copy of the eight-start table
for every citation in Week 11 to point back to.
