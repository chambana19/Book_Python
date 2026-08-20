# Shared, pre-verified scenarios for Weeks 9-12 (Optimization block)

All three scenarios below are fictional teaching problems (say so on slide,
same convention as Radley Hall in Weeks 4-8) but every number was verified in
the pinned course environment (numpy 2.4.6, scipy 1.17.1). Do not recompute or alter these numbers — cite them
exactly, or re-run the exact scripts below yourself if you need a value not
listed here.

Continuity: Radley Hall (Weeks 4-8's fictional building) is a fine framing
device to reuse here ("Radley Hall's new south wing," "Radley Hall's roof")
for narrative continuity across the whole semester, even though these
weeks' scenarios are otherwise independent formulas/problems, not derived
from `building_rooms.csv`.

## Week 9 (sweep) + Week 11 (optimize) — SAME nonlinear objective

A fictional "annual energy use intensity proxy" (kWh/m2/yr-like units, to
MINIMIZE) for a new wing, as a function of two design variables: window-to-
wall ratio `wwr` (bounds 0.20-0.60) and shading overhang depth in meters
`shade_m` (bounds 0.0-1.2). Deliberately constructed with TWO basins of
comparable depth, well separated, so a gradient-based optimizer's answer
genuinely depends on its starting guess (Week 11's core teaching point) -
this is not accidental structure, it is the intended lesson.

```python
import numpy as np

def basin(x, y, cx, cy, depth, wx, wy):
    return -depth * np.exp(-(((x-cx)**2)/(2*wx**2) + ((y-cy)**2)/(2*wy**2)))

def energy_proxy(v):
    w, s = v
    base = 20.0
    b1 = basin(w, s, 0.52, 0.25, 30.0, 0.06, 0.18)   # local minimum (shallower)
    b2 = basin(w, s, 0.28, 0.90, 34.0, 0.06, 0.18)   # GLOBAL minimum (deeper)
    ridge = 6.0 * np.exp(-((w-0.40)**2)/0.02)         # soft wall near wwr=0.40
    return base + b1 + b2 + ridge
```

**Verified facts (Week 9 sweep):** grid search over 81x61 points confirms the
true global minimum sits at wwr=0.275, shade=0.900, value=-11.135. The local
basin's center (0.52, 0.25) evaluates to -7.08 — clearly worse, but a real,
comparable "trap."

**Verified facts (Week 11 optimize, `scipy.optimize.minimize` with
`bounds=[(0.20,0.60),(0.0,1.2)]`, default method):**
| starting guess (wwr, shade) | converges to (wwr, shade) | value | which basin |
|---|---|---|---|
| (0.55, 0.20) | (0.5241, 0.2500) | -7.1521 | LOCAL (wrong) |
| (0.50, 0.30) | (0.5241, 0.2500) | -7.1521 | LOCAL (wrong) |
| (0.40, 0.55) | (0.5241, 0.2500) | -7.1521 | LOCAL (wrong) |
| (0.45, 0.60) | (0.5241, 0.2500) | -7.1521 | LOCAL (wrong) |
| (0.60, 0.10) | (0.5241, 0.2500) | -7.1521 | LOCAL (wrong) |
| (0.20, 1.00) | (0.2763, 0.9000) | -11.1437 | GLOBAL (right) |
| (0.30, 0.85) | (0.2763, 0.9000) | -11.1437 | GLOBAL (right) |
| (0.22, 1.15) | (0.2763, 0.9000) | -11.1437 | GLOBAL (right) |

Use this table directly: 5 of 8 plausible starting guesses land in the WORSE
local optimum. Recommended teaching flow: Week 9 sweeps and visualizes the
full surface (a heatmap clearly shows two low-value regions); Week 11 asks
"let the computer find the minimum" via `minimize`, picks a starting guess
that lands in the local trap, and only by trying a second, different
starting guess (e.g., one from the "GLOBAL" rows above) does the true
optimum reveal itself — this is a real, not manufactured, demonstration of
why Week 11's whole lesson (initial guess matters) is true.

## Week 10 — linear programming (exact/linear optimization family)

Radley Hall's roof: allocate 200 m2 total between solar panels (`x1`, $/m2
install cost 400, annual benefit 60/m2/yr) and a green roof (`x2`, install
cost 150/m2, annual benefit 25/m2/yr). Maximize annual benefit subject to a
total-area limit, a total-budget limit, and a structural cap on solar area.

```python
from scipy.optimize import linprog
c = [-60, -25]                      # maximize 60x1+25x2 -> minimize the negative
A_ub = [[1, 1], [400, 150]]         # area <= 200 ; cost <= 50000
b_ub = [200, 50000]
bounds = [(0, 120), (0, None)]      # solar structurally capped at 120 m2
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
```

**Verified result:** `x1=80.0` m2 solar, `x2=120.0` m2 green roof, total
benefit = **$7,800/yr**. BOTH constraints bind exactly at the optimum
(80+120=200 area used exactly; 400*80+150*120=50,000 budget used exactly) -
an excellent real example for "verify every constraint by hand."

**Verified comparison to naive (non-optimized) strategies** - use this to
motivate WHY formulate-and-solve beats intuition:
- All-solar (structurally capped at 120 m2, 80 m2 of roof unused): **$7,200/yr** (worse)
- All-green (200 m2 green, no solar): **$5,000/yr** (much worse)
- Optimal mixed allocation above: **$7,800/yr** (best - neither obvious "pure" strategy wins)

## Week 12 — discrete/combinatorial heuristic search (genetic algorithm)

Radley Hall's south facade: 6 bays, each assigned exactly ONE of 6 distinct
panel types (a permutation problem - genuinely combinatorial, NOT solvable
by `linprog` or `minimize`). Each bay has an "ideal transmittance" (from its
sun exposure); each panel type has a fixed transmittance. Cost = sum of
squared mismatch between assigned panel and each bay's ideal value.

```python
position_ideal = [0.15, 0.25, 0.45, 0.55, 0.35, 0.20]        # bay 1..6
panel_transmittance = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60]   # 6 distinct panels
def cost(perm):  # perm[i] = which panel index is assigned to bay i
    return sum((panel_transmittance[p]-position_ideal[i])**2 for i,p in enumerate(perm))
```

**Verified brute-force baseline** (all 720 permutations checked): true
optimum permutation `(0, 2, 4, 5, 3, 1)` (bay1<-panel0, bay2<-panel2, ...),
cost = **0.0125**. Worst permutation cost: 0.5825. Mean cost: 0.2975.

**Verified genetic algorithm** (permutation GA: order crossover + swap
mutation, population 12, 5 survivors kept per generation, mutation rate
0.35, run for up to 30 generations) reliably finds the SAME true optimum
(cost 0.0125, confirmed identical to brute force) across all 7 tested random
seeds. **Use `random.seed(1)` for the primary in-class/handout demo** - it
reaches the true optimum by generation 9, with a clean, visible improvement
curve: generation 0 best cost 0.1025 -> gen 5: 0.0225 -> gen 9: 0.0125
(already at the true optimum) -> stays 0.0125 thereafter. Total individuals
evaluated by the GA to reach this: about 12 + 9*7 = 75, versus 720 for
brute force - a real, honest efficiency comparison (note for discussion: at
N=6 brute force is still entirely feasible; the real-world case for
heuristics is when N grows - e.g. 12 panels would be 12! ~= 479 million
permutations, making brute force infeasible, which is the actual motivating
scenario worth naming even though this teaching example keeps N small
enough to verify by brute force for grading purposes).

NOTE (corrected after audit): seed=1 is NOT the fastest of the 7 tested
seeds to reach the true optimum - re-verified per-seed generations-to-reach
0.0125: seed 1 -> gen 9, seed 2 -> gen 9, seed 3 -> gen 4, seed 4 -> gen 13,
seed 5 -> gen 20, seed 6 -> gen 6, seed 7 -> gen 15. Seeds 3 and 6 both
reach the optimum faster than seed 1. Seed=1 remains the recommended
primary demo seed for its clean, clearly-staged improvement curve (0.1025
-> 0.0925 -> 0.0525 -> 0.0225 -> 0.0125), not because it is fastest - do
not describe seed=1 as "fastest" anywhere.
