# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 11 studio · INSTRUCTOR SOLUTIONS
Nonlinear optimization with scipy.optimize.minimize
Syracuse University · School of Architecture · Fall 2026
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
#                    rounds to -11.08 -- about 4 points lower. Dense-grid plus multistart
#                    evidence corroborates this candidate; it does not prove globality.

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
# COMMON ERROR: retyping energy_proxy from memory instead of pasting it exactly from
# Week 9 / data/README.md. A single changed width (wx, wy) or depth value quietly moves
# both basins and invalidates every verified number in this handout.


# %% [2] DEMO A -- a plausible starting guess
# QUESTION           Where does minimize land if you start at wwr=0.55, shade=0.20?
# INPUTS/ASSUMPTIONS energy_proxy and BOUNDS from cell [1]
# METHOD             minimize(energy_proxy, x0=(0.55, 0.20), bounds=BOUNDS)
# CHECKS/INTERPRET   Expected: x = [0.5241, 0.2500], value = -7.1521, success = True

result_a = minimize(energy_proxy, x0=(0.55, 0.20), bounds=BOUNDS)
print("x:", result_a.x.round(4))
print("value:", round(result_a.fun, 4))
print("success:", result_a.success)
# WHY THIS MATTERS: success is True here, and the answer LOOKS complete -- a clean x, a
# clean value, no error. Nothing about this printed output signals that a better design
# exists. That is exactly why a single minimize call is never enough on its own.


# %% [3] DEMO B -- a different starting guess, same function, same bounds
# QUESTION           Does a different x0 change the answer?
# INPUTS/ASSUMPTIONS energy_proxy and BOUNDS from cell [1]; only x0 differs from cell [2]
# METHOD             minimize(energy_proxy, x0=(0.20, 1.00), bounds=BOUNDS)
# CHECKS/INTERPRET   Expected: x = [0.2763, 0.9000], value = -11.1437, success = True

result_b = minimize(energy_proxy, x0=(0.20, 1.00), bounds=BOUNDS)
print("x:", result_b.x.round(4))
print("value:", round(result_b.fun, 4))
print("success:", result_b.success)

print("improvement over Demo A:", round(result_b.fun - result_a.fun, 2))
# COMMON ERROR: assuming that because Demo A "succeeded," rerunning with the same x0 a
# second time will somehow find something better. It will not -- minimize is
# deterministic given the same function, bounds, and x0. Only a genuinely DIFFERENT x0
# can change the answer, which is the entire point of Demo B.
# WHY THIS MATTERS: -11.1437 vs. -7.1521 is roughly a 4-point gap in this energy proxy --
# a real, material difference in a real building-performance metric, not a rounding
# artifact.


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
    res = minimize(energy_proxy, x0=(wwr0, shade0), bounds=BOUNDS)
    records.append({
        "start_wwr": wwr0, "start_shade": shade0,
        "final_wwr": round(res.x[0], 4), "final_shade": round(res.x[1], 4),
        "value": round(res.fun, 4),
    })

multi_start = pd.DataFrame(records)
print(multi_start)
# WHY THIS MATTERS: pd.DataFrame(records) is a genuinely new construction, not a repeat of
# Week 4. Week 4 always built a DataFrame from a dict of whole COLUMNS, e.g.
# pd.DataFrame({"area_m2": [35.0, 62.5, 44.2]}). Here, records is a LIST OF DICTS -- one
# dict per starting guess, each dict is one ROW -- and pandas reads the dicts' shared keys
# as column names. Same function, opposite shape; know which one you are building.
# COMMON ERROR: writing "for wwr0, shade0 in starting_guesses" then calling
# minimize(energy_proxy, x0=starting_guesses, ...) outside the loop by mistake -- passing
# the whole list instead of one (wwr0, shade0) tuple raises a shape error inside scipy.
# Always call minimize once per iteration, using that iteration's own wwr0/shade0.


# %% [5] Classify each run into a basin, then count
# QUESTION           How many of the eight starts land in the worse local optimum?
# INPUTS/ASSUMPTIONS multi_start from cell [4], with 8 filled rows
# METHOD             np.where(multi_start["value"] < -9, "LOWER", "LOCAL"), then
#                    value_counts()
# CHECKS/INTERPRET   Expected counts: LOCAL 5, LOWER 3. LOWER is descriptive, not proof.

multi_start["basin"] = np.where(multi_start["value"] < -9, "LOWER", "LOCAL")
print(multi_start[["start_wwr", "start_shade", "value", "basin"]])
print(multi_start["basin"].value_counts())

assert (multi_start["basin"] == "LOCAL").sum() == 5
assert (multi_start["basin"] == "LOWER").sum() == 3

sensitivity_finding = (
    "5 of 8 plausible starting guesses (62.5%) converge to the worse local optimum "
    "(-7.1521) instead of the lower basin / best result found in this multi-start plus "
    "dense-grid check (-11.1437); a single minimize run, "
    "with no second starting guess to compare against, would very likely report the "
    "wrong answer as final."
)
print(sensitivity_finding)
# WHY THIS MATTERS: -9 is a threshold picked deliberately between the two known optimum
# values (-7.15 and -11.14) -- it is a labeling convenience for THIS verified problem,
# not a general rule for classifying basins on a different objective function.
# COMMON ERROR: computing the LOCAL/LOWER split by eye from the printed table instead of
# with value_counts() -- easy to miscount by one row under time pressure; let pandas count.


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
    "Single starting guess presented as THE answer: only x0=(0.55, 0.20) is tried, yet "
    "the docstring-free function name ai_find_best_design() and the print label 'Best "
    "design' both claim global optimality. Cells [2]-[4] show this exact start lands in "
    "the LOCAL trap (-7.1521), not the lower best-corroborated basin (-11.1437).",
    "No bounds= argument at all: physically nonsensical designs (negative wwr, wwr>1) "
    "are not excluded. This particular start happens to converge inside the sensible "
    "range by coincidence, but nothing in the code guarantees that in general -- see "
    "Meeting A's unbounded demo, where starts from (0.0, 0.0) and (1.0, 1.0) return "
    "wwr=-0.1974 and wwr=1.0.",
    "result.success is never checked or printed: the function trusts result.x/result.fun "
    "unconditionally. A failed or stalled optimization would be reported with exactly "
    "the same confidence as a converged one.",
    "'Minimum energy proxy' is a factually overreaching label: result.fun is only the "
    "minimum found FROM THIS ONE STARTING GUESS, not the minimum of the function. "
    "Conflating a local result with the global minimum is this week's central, named "
    "pitfall, not an edge case.",
]

for defect in ai_defects:
    print("-", defect)
# WHY THIS MATTERS: every one of these four defects is individually plausible and easy to
# accept under time pressure -- especially the mislabeling, since the code runs cleanly
# and prints a confident-looking result. This is exactly why an AI-suggested optimizer
# call gets audited against a multi-start comparison, never accepted on a single run.


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

assert abs(res_transfer_1.fun - (-11.1437)) < 0.01
assert abs(res_transfer_2.fun - (-7.1521)) < 0.01
assert res_transfer_1.fun < res_transfer_2.fun

print("Self-check passed: transfer starts confirm the same two-basin pattern.")
# WHY THIS MATTERS: (0.35, 0.75) and (0.58, 0.15) were never run live in cells [2]-[4] --
# asserting on them, not the eight already-seen starts, is this week's required transfer
# check: corroboration that the local/lower pattern persists on new starts, not proof that
# -11.1437 is the continuous global optimum.


# %% [8] Required write-up: multi-start comparison
# QUESTION           In 60-100 words, what does today's multi-start comparison show?
# INPUTS/ASSUMPTIONS results from cells [2]-[5]
# METHOD             write multi_start_writeup addressing the four required points below
# CHECKS/INTERPRET   60-100 words, all four required points present.

multi_start_writeup = (
    "Eight starting guesses were tried on the identical energy_proxy(wwr, shade_m) "
    "objective with identical bounds: five converged to the local optimum "
    "(wwr=0.5241, shade=0.2500, value=-7.1521), and three converged to the lower basin "
    "(wwr=0.2763, shade=0.9000, value=-11.1437), the best-known result corroborated by "
    "this multi-start plus finite dense-grid check, not proof of globality, and a real "
    "4-point improvement. "
    "This happens because scipy.optimize.minimize follows only the local slope from its "
    "starting point; it cannot see a deeper basin elsewhere in bounds the way Week 9's "
    "full grid sweep could. Going forward, every nonlinear optimization in Project 2 "
    "will be run from at least two well-separated starting guesses before its result is "
    "trusted, exactly as Part II requires."
)
print(multi_start_writeup)
print(len(multi_start_writeup.split()), "words")
# WHY THIS MATTERS: this write-up IS the Week 11 nonlinear-formulation checkpoint named
# in the semester plan -- graded as this week's ordinary studio task, not an additional
# artifact layered on top.


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
Tool/model: Example assistant
Prompt: Write a function that finds the best window-to-wall ratio and shading depth to
minimize energy_proxy using scipy.optimize.minimize.
Suggestion received: ai_find_best_design(), exactly as shown in cell [6] -- one
minimize() call, one starting guess, no bounds argument, no success check, labeled
"Best design" and "Minimum energy proxy" in the print statements.
What I accepted: The general call pattern -- minimize(function, x0=...) -- and the idea
of wrapping it in a small function.
What I modified and why: Added bounds=BOUNDS to keep every candidate physically
buildable; ran a second, well-separated starting guess (and then a full eight-start
sweep) instead of trusting one result; checked result.success explicitly; renamed the
output so it reports a LOCAL result unless verified otherwise.
What I rejected and why: The claim, implicit in the print label "Best design," that a
single minimize() call from one starting guess proves the global optimum -- contradicted
by cells [2]-[5], where 5 of 8 starts land in a real, measurably worse local trap.
How I tested it: Ran the full eight-start sweep from data/README.md's verified table
(cell [4]-[5]), then re-verified the pattern on two entirely new starting guesses not
used anywhere above (cell [7]), with passing assert statements on both.
One limitation I found: This script confirms which optimum minimize reaches from a given
start; it does not prove -11.1437 is the global minimum everywhere in bounds. Week 9's
finite dense-grid sweep corroborates the same region but still cannot prove the
continuous claim between sampled points.
"""

exit_explanation = """
Demo A, from wwr=0.55/shade=0.20, converged to a local optimum: wwr=0.5241, shade=0.2500,
value=-7.1521. Demo B, from wwr=0.20/shade=1.00 with the identical function and bounds,
converged instead to the lower basin: wwr=0.2763, shade=0.9000, value=-11.1437,
the best result found in this multi-start plus dense-grid check and a real 4-point
improvement. Across all eight tested starts, 5 landed in the local trap and only 3
reached the lower basin, because minimize follows only the slope visible
from wherever it stands and cannot see a deeper basin elsewhere. The AI-drafted
ai_find_best_design() function got this wrong: one starting guess, no bounds, no success
check, yet still labeled its local result "Best design." This script cannot prove that
-11.1437 is the global minimum everywhere in bounds. A finer sweep could strengthen the
corroboration, but a finite sweep still would not prove globality.
"""

print(ai_use_record)
print(exit_explanation)
print(len(exit_explanation.split()), "words")

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Expected evidence for courtyard width × opening ratio: at least three spread-
# out starts; identical function/bounds; success, variables, and objective value
# in one comparison table; explicit feasibility checks. Agreement reassures but
# does not prove global optimality; disagreement is a reportable design finding.
