# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 11 studio · Nonlinear optimization with scipy.optimize.minimize
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week11 module folder. No data file is needed today --
     the objective function is defined directly in this script.
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict a result BEFORE running each cell -- especially cells [2] and [3].
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A minimize result is not trustworthy on its own, no matter how clean result.success
  looks. Every nonlinear optimization in this course is verified with AT LEAST two
  different starting guesses before its result is reported as "the" answer.
"""

# %% [0] Environment check
# QUESTION           Run the cell and confirm your Python version, executable, and working
#                    folder.
# INPUTS/ASSUMPTIONS no inputs; Spyder is installed and this file is open
# METHOD             run the cell and read the three printed environment lines in the
#                    console
# CHECKS/INTERPRET   You should see a Python version, an executable path, and a folder
#                    path with no error.

from pathlib import Path
import sys

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())


# %% [1] The objective function and bounds -- recall Week 9
# QUESTION           Is this the exact same energy_proxy surface swept in Week 9?
# INPUTS/ASSUMPTIONS same two-basin construction: local basin near (0.52, 0.25), lower
#                    best-known basin near (0.28, 0.90); bounds wwr in [0.20, 0.60], shade_m in
#                    [0.0, 1.2]
# METHOD             paste in energy_proxy(v) unchanged from Week 9 / data/README.md,
#                    then evaluate it at both basin centers
# CHECKS/INTERPRET   Expected: local basin center rounds to -7.08; lower basin center
#                    rounds to -11.08 -- about 4 points lower. This numerical evidence
#                    corroborates a candidate; it does not prove globality.

import numpy as np
import pandas as pd
from scipy.optimize import minimize

def basin(x: float, y: float, cx: float, cy: float,
          depth: float, wx: float, wy: float) -> float:
    """One Gaussian dip in the surface, centered at (cx, cy), 'depth' deep."""
    return -depth * np.exp(-(((x - cx) ** 2) / (2 * wx ** 2)
                             + ((y - cy) ** 2) / (2 * wy ** 2)))

def energy_proxy(v: tuple) -> float:
    """Two-basin annual energy-use-intensity proxy for a new wing, over (wwr, shade_m)."""
    w, s = v
    base = 20.0
    b1 = basin(w, s, 0.52, 0.25, 30.0, 0.06, 0.18)   # local minimum (shallower)
    b2 = basin(w, s, 0.28, 0.90, 34.0, 0.06, 0.18)   # deeper basin (best known)
    ridge = 6.0 * np.exp(-((w - 0.40) ** 2) / 0.02)   # soft wall near wwr=0.40
    return base + b1 + b2 + ridge

BOUNDS = [(0.20, 0.60), (0.0, 1.2)]   # (wwr min, wwr max), (shade_m min, shade_m max)

print("local basin center:", round(energy_proxy((0.52, 0.25)), 2))
print("lower basin center:", round(energy_proxy((0.28, 0.90)), 2))

# TODO: Confirm both printed values match -7.08 and -11.08 before continuing. If they
# do not, you have not copied energy_proxy exactly -- fix this before cell [2].


# %% [2] DEMO A -- a plausible starting guess
# QUESTION           Where does minimize land if you start at wwr=0.55, shade=0.20?
# INPUTS/ASSUMPTIONS energy_proxy and BOUNDS from cell [1]
# METHOD             minimize(energy_proxy, x0=(0.55, 0.20), bounds=BOUNDS)
# CHECKS/INTERPRET   Expected: x = [0.5241, 0.2500], value = -7.1521, success = True

# TODO: call minimize and store the result as result_a, e.g.
# result_a = minimize(energy_proxy, x0=(0.55, 0.20), bounds=BOUNDS)
raise NotImplementedError(
    "Cell [2] incomplete: run the first bounded minimize call, then remove this gate."
)

print("x:", result_a.x.round(4) if result_a is not None else "TODO")
print("value:", round(result_a.fun, 4) if result_a is not None else "TODO")
print("success:", result_a.success if result_a is not None else "TODO")

# TODO: This should converge cleanly (success True) -- but is -7.1521 actually the BEST
# possible value in bounds? Compare against cell [1]'s lower basin center before answering.


# %% [3] DEMO B -- a different starting guess, same function, same bounds
# QUESTION           Does a different x0 change the answer?
# INPUTS/ASSUMPTIONS energy_proxy and BOUNDS from cell [1]; only x0 differs from cell [2]
# METHOD             minimize(energy_proxy, x0=(0.20, 1.00), bounds=BOUNDS)
# CHECKS/INTERPRET   Expected: x = [0.2763, 0.9000], value = -11.1437, success = True

# TODO: call minimize from the new starting guess and store the result as result_b, e.g.
# result_b = minimize(energy_proxy, x0=(0.20, 1.00), bounds=BOUNDS)
raise NotImplementedError(
    "Cell [3] incomplete: run the second bounded minimize call, then remove this gate."
)

print("x:", result_b.x.round(4) if result_b is not None else "TODO")
print("value:", round(result_b.fun, 4) if result_b is not None else "TODO")
print("success:", result_b.success if result_b is not None else "TODO")

# TODO: once result_a and result_b are both real, print round(result_b.fun - result_a.fun, 2)
# -- this is how much lower (better) the best-known basin is than Demo A's local trap.


# %% [4] Multi-start sweep -- eight starting guesses, one table
# QUESTION           Across a range of plausible starting guesses, how many land in each
#                    basin?
# INPUTS/ASSUMPTIONS the eight (wwr, shade) starting guesses below, verified in
#                    data/README.md
# METHOD             loop over the list, call minimize from each, build one dict of
#                    results per start, append it to a list, then pd.DataFrame(records)
#                    turns that LIST OF DICTS into a table -- new here: each dict is one
#                    ROW, a different shape from Week 4's dict-of-whole-COLUMNS DataFrame
# CHECKS/INTERPRET   Expected: 8 rows; five rows converge to (0.5241, 0.2500); three rows
#                    converge to (0.2763, 0.9000).

starting_guesses = [
    (0.55, 0.20), (0.50, 0.30), (0.40, 0.55), (0.45, 0.60),
    (0.60, 0.10), (0.20, 1.00), (0.30, 0.85), (0.22, 1.15),
]

records = []
for wwr0, shade0 in starting_guesses:
    # TODO: call minimize(energy_proxy, x0=(wwr0, shade0), bounds=BOUNDS) and append one
    # dict per start to records, e.g.
    # res = minimize(energy_proxy, x0=(wwr0, shade0), bounds=BOUNDS)
    # records.append({
    #     "start_wwr": wwr0, "start_shade": shade0,
    #     "final_wwr": round(res.x[0], 4), "final_shade": round(res.x[1], 4),
    #     "value": round(res.fun, 4),
    # })
    raise NotImplementedError(
        "Cell [4] incomplete: append one checked result row for every starting guess."
    )

multi_start = pd.DataFrame(records)
print(multi_start)

# TODO: Confirm multi_start has 8 rows once the loop above is filled in.


# %% [5] Classify each run into a basin, then count
# QUESTION           How many of the eight starts land in the worse local optimum?
# INPUTS/ASSUMPTIONS multi_start from cell [4], with 8 filled rows
# METHOD             np.where(multi_start["value"] < -9, "LOWER", "LOCAL"), then
#                    value_counts()
# CHECKS/INTERPRET   Expected counts: LOCAL 5, LOWER 3. LOWER is descriptive, not proof.

# TODO: uncomment once multi_start has real rows
# multi_start["basin"] = np.where(multi_start["value"] < -9, "LOWER", "LOCAL")
# print(multi_start[["start_wwr", "start_shade", "value", "basin"]])
# print(multi_start["basin"].value_counts())

sensitivity_finding = (
    "TODO: one sentence stating what fraction of starting guesses landed in the wrong "
    "(local) optimum, and what this implies about trusting a single minimize run."
)
print(sensitivity_finding)


# %% [6] AI-generated code audit
# QUESTION           Would you accept this AI-suggested "find the best design" function
#                    as-is?
# INPUTS/ASSUMPTIONS ai_find_best_design as shown
# METHOD             list at least four specific defects, then compare with your own
#                    cells [2]-[4]
# CHECKS/INTERPRET   A defensible list names the single-start, missing-bounds, and
#                    unchecked-success defects -- not merely that the code "looks wrong."

def ai_find_best_design():
    result = minimize(energy_proxy, x0=(0.55, 0.20))
    print(f"Best design: wwr={result.x[0]:.4f}, shade={result.x[1]:.4f}")
    print(f"Minimum energy proxy: {result.fun:.4f}")
    return result.x

best = ai_find_best_design()

ai_defects = [
    # TODO: add at least four specific defects
]

for defect in ai_defects:
    print("-", defect)


# %% [7] Self-check: two new starting guesses, not used above
# QUESTION           Does the same local/lower pattern hold for starting guesses you
#                    have not seen run yet?
# INPUTS/ASSUMPTIONS energy_proxy, BOUNDS from cell [1]; two NEW starts, (0.35, 0.75) and
#                    (0.58, 0.15) -- neither appears in cell [4]'s table
# METHOD             run minimize from each, then assert which basin each lands in
# CHECKS/INTERPRET   Expected: (0.35, 0.75) -> LOWER (value near -11.1437); (0.58, 0.15)
#                    -> LOCAL (value near -7.1521).

res_transfer_1 = minimize(energy_proxy, x0=(0.35, 0.75), bounds=BOUNDS)
res_transfer_2 = minimize(energy_proxy, x0=(0.58, 0.15), bounds=BOUNDS)

print("transfer 1 (0.35, 0.75):", res_transfer_1.x.round(4), round(res_transfer_1.fun, 4))
print("transfer 2 (0.58, 0.15):", res_transfer_2.x.round(4), round(res_transfer_2.fun, 4))

# TODO: Add 2-4 assert statements confirming res_transfer_1.fun is close to -11.1437
# (lower/best known) and res_transfer_2.fun is close to -7.1521 (local). Example:
# assert abs(res_transfer_1.fun - (-11.1437)) < 0.01


# %% [8] Required write-up: multi-start comparison
# QUESTION           In 60-100 words, what does today's multi-start comparison show?
# INPUTS/ASSUMPTIONS results from cells [2]-[5]
# METHOD             write multi_start_writeup addressing the four required points below
# CHECKS/INTERPRET   60-100 words, all four required points present.

multi_start_writeup = """
TODO: in 60-100 words, state:
1. how many of the 8 starting guesses (cell [4]) landed in the local vs. lower basin,
2. the two numeric values (-7.1521 and -11.1437) and which is actually better,
3. why the starting guess -- not a bug -- causes this, referencing what minimize can and
   cannot see, and
4. one practical rule you will follow before trusting a minimize result on your own
   Project 2 problem.
"""

print(multi_start_writeup)


# %% [9] AI-use record and exit reflection
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished multi-start comparison in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing this
#                    script cannot tell you.

ai_use_record = """
Tool/model:
Prompt:
Suggestion received:
What I accepted:
What I modified and why:
What I rejected and why:
How I tested it:
One limitation I found:
"""

exit_explanation = """
In 80-120 words, explain:
1. what Demo A and Demo B found (the two different optima, with their values),
2. what fraction of the 8 multi-start runs landed in each basin,
3. why the same function and bounds can produce two different answers,
4. what the ai_find_best_design() function got wrong, and
5. why dense-grid plus multistart agreement corroborates the lower basin but does not
   prove a continuous global optimum for a real design decision.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# For a courtyard-width × opening-ratio comfort/daylight proxy, choose three
# physically different starting guesses under identical bounds. Specify the
# multistart table columns, the bound/success checks, and how agreement versus
# disagreement would change the architectural interpretation.
