# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 9 studio · INSTRUCTOR SOLUTIONS
Parameter sweeps and sensitivity: wwr vs. shade_m
Syracuse University · School of Architecture · Fall 2026

MILESTONE: PROJECT 2 ASSIGNED THIS WEEK
  Project 2 (Predict, Optimize, Decide) is assigned this week -- problem-area, dataset,
  and prediction/optimization pairing selection is now open. The two-variable sensitivity
  sweep below is not just practice: it is the exact Part I requirement Project 2 will ask
  students to reproduce, as supporting evidence, on their own problem later this semester.
"""

# %% [0] Environment and working-folder check
# QUESTION           Confirm your Python version, executable, and working folder.
# INPUTS/ASSUMPTIONS no inputs; Spyder is installed and this file is open
# METHOD             run the cell and read the three printed environment lines
# CHECKS/INTERPRET   You should see a Python version, an executable path, and a folder
#                    path with no error.

from pathlib import Path
import sys

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())


# %% [1] The provided formula, and one baseline call
# QUESTION           What does Radley Hall's new south wing score at a plausible
#                    baseline design -- wwr=0.40, shade_m=0.30?
# INPUTS/ASSUMPTIONS energy_proxy is PROVIDED -- a fictional energy-use-intensity-like
#                    score to MINIMIZE, bounded wwr in [0.20, 0.60], shade_m in [0.0, 1.2]
# METHOD             define basin, check it alone, then define and call
#                    energy_proxy((wwr, shade_m)) once at the baseline
# CHECKS/INTERPRET   Expected basin value: -3.906. Expected baseline score: 22.076.

import numpy as np
import matplotlib.pyplot as plt


def basin(x: np.ndarray, y: np.ndarray, cx: float,
          cy: float, depth: float, wx: float,
          wy: float) -> np.ndarray:
    """Gaussian dip of depth, centered at (cx, cy)."""
    dx = ((x - cx) ** 2) / (2 * wx ** 2)
    dy = ((y - cy) ** 2) / (2 * wy ** 2)
    return -depth * np.exp(-(dx + dy))


# One dip on its own, at the baseline design: expected -3.906.
print(round(basin(0.40, 0.30, 0.52, 0.25,
                  30.0, 0.06, 0.18), 3))
# WHY THIS MATTERS: basin is the single helper energy_proxy is built from. It is deepest
# (-depth) exactly at (cx, cy) and fades toward 0 away from it, so a design scores well
# only by sitting near a deep dip. Confirming -3.906 here isolates a retyping error in
# basin BEFORE it silently propagates into all 4,941 grid points later in this studio.


def energy_proxy(v: tuple[float, float]) -> float:
    """Provided proxy to MINIMIZE; v=(wwr, shade_m)."""
    w, s = v
    base = 20.0
    b1 = basin(w, s, 0.52, 0.25, 30.0, 0.06, 0.18)
    b2 = basin(w, s, 0.28, 0.90, 34.0, 0.06, 0.18)
    ridge = 6.0 * np.exp(-((w - 0.40) ** 2) / 0.02)
    return base + b1 + b2 + ridge


baseline = energy_proxy((0.40, 0.30))
print(f"baseline energy_proxy: {baseline:.3f}")
# WHY THIS MATTERS: energy_proxy takes ONE packed input v=(wwr, shade_m), not two separate
# arguments. That exact shape is not an arbitrary style choice -- Week 11 hands this
# identical function to scipy.optimize.minimize, which requires a single-array-argument
# objective function. Calling it correctly now is a rehearsal for Week 11, not busywork.
# COMMON ERROR: writing energy_proxy(0.40, 0.30) with two separate arguments raises a
# TypeError -- energy_proxy takes exactly one argument, v, which is then unpacked inside.


# %% [2] Required check: vectorized call vs. an explicit loop
# QUESTION           Does calling energy_proxy on a whole ndarray at once give the exact
#                    same numbers as calling it once per value in a loop?
# INPUTS/ASSUMPTIONS 21 wwr values, shade_m fixed at 0.30
# METHOD             compute once with a vectorized ndarray call, once with a Python
#                    for-loop, then assert they match
# CHECKS/INTERPRET   Both arrays must be identical (np.allclose). This is this week's
#                    REQUIRED assert-verified vectorized-vs-loop equivalence check.

wwr_check = np.linspace(0.20, 0.60, 21)

vectorized = energy_proxy((wwr_check, 0.30))

looped = []
for w in wwr_check:
    looped.append(energy_proxy((w, 0.30)))
looped = np.array(looped)

assert np.allclose(vectorized, looped)
print("vectorized == looped:", np.allclose(vectorized, looped))
# WHY THIS MATTERS: this assert is the graded proof that vectorization is not a shortcut
# that changes the answer -- it is the identical arithmetic, applied to every element at
# once instead of one at a time. Every sweep for the rest of this studio depends on that
# equivalence actually holding.
# COMMON ERROR: comparing with == instead of np.allclose. Floating-point arithmetic can
# differ in the last bit between a loop and a vectorized path on some machines; allclose
# checks "close enough," which is the correct standard for numeric equivalence.


# %% [3] Sweep one variable at a time -- first read
# QUESTION           Which variable, swept alone, appears to move the score more?
# INPUTS/ASSUMPTIONS 9-point linspace sweeps; shade_m fixed at 0.30 for the wwr sweep,
#                    wwr fixed at 0.40 for the shade_m sweep
# METHOD             np.linspace for each swept variable; one vectorized call per sweep;
#                    range = array.max() - array.min()
# CHECKS/INTERPRET   Expected wwr range: 28.373. Expected shade_m range: 3.46.

wwr_vals = np.linspace(0.20, 0.60, 9)
shade_vals = np.linspace(0.0, 1.2, 9)

e_wwr = energy_proxy((wwr_vals, 0.30))
e_shade = energy_proxy((0.40, shade_vals))

print("wwr sweep:", np.round(e_wwr, 3), "range:", round(e_wwr.max() - e_wwr.min(), 3))
print("shade sweep:", np.round(e_shade, 3), "range:", round(e_shade.max() - e_shade.min(), 3))
# WHY THIS MATTERS: 28.373 vs. 3.46 looks like a clean, confident answer -- "wwr matters,
# shade_m doesn't." Cell [4] exists specifically to test whether that conclusion survives
# a different choice of which variable gets held fixed.
# COMMON ERROR: stopping here and reporting "wwr is the important variable" as a final
# answer. Both numbers came from ONE arbitrarily chosen fixed value of the other variable
# -- that is not yet a full sensitivity analysis.


# %% [4] The trap: re-run both sweeps from different fixed baselines
# QUESTION           Does "wwr matters more" still hold if the OTHER variable is fixed
#                    somewhere else?
# INPUTS/ASSUMPTIONS same two 9-point sweeps as cell [3], but wwr now fixed at 0.28 (for
#                    the shade sweep) and shade_m now fixed at 0.90 (for the wwr sweep)
# METHOD             re-run energy_proxy with wwr fixed at 0.28 and shade_m fixed at 0.90
# CHECKS/INTERPRET   Expected shade range @ wwr=0.28: 33.996. Expected wwr range @
#                    shade=0.90: 33.182 -- both much bigger than cell [3] suggested.

e_shade2 = energy_proxy((0.28, shade_vals))
print("shade range @ wwr=0.28:", round(e_shade2.max() - e_shade2.min(), 3))

e_wwr2 = energy_proxy((wwr_vals, 0.90))
print("wwr range @ shade=0.90:", round(e_wwr2.max() - e_wwr2.min(), 3))
# WHY THIS MATTERS: fixed at wwr=0.28 instead of 0.40, shade_m's own range jumps from 3.46
# to 33.996 -- bigger than wwr's original 28.373. "shade_m doesn't matter" was never a
# fact about the formula; it was an artifact of where the other variable happened to sit.
# This is exactly why cell [6] evaluates every (wwr, shade_m) pair together with meshgrid,
# instead of trusting any single 1-D slice.
# COMMON ERROR: treating this as a special case unique to this one formula. Any real
# nonlinear design formula can have this property -- one-at-a-time testing against
# whatever baseline is already on the table is a common, real analysis mistake.


# %% [5] Boolean mask: flag which wwr values meet a target
# QUESTION           Of the 9 wwr values from cell [3], which ones score 15 or better?
# INPUTS/ASSUMPTIONS e_wwr and wwr_vals from cell [3]; target = 15.0
# METHOD             build a boolean mask with e_wwr <= target, then index wwr_vals
#                    with that mask
# CHECKS/INTERPRET   Expected passing values: [0.45, 0.5, 0.55, 0.6] (4 of 9).

target = 15.0
meets_target = e_wwr <= target
print(meets_target)
print("passing wwr values:", wwr_vals[meets_target])
# WHY THIS MATTERS: meets_target has the same shape (9,) as e_wwr and wwr_vals -- that
# shared shape is what lets one array's True/False values select matching positions from
# a completely different array. This is the exact mechanism Week 5's Boolean pandas
# filtering (df[mask]) was built on, one level closer to the raw array.
# COMMON ERROR: writing e_wwr <= target as an if statement (if e_wwr <= target:) -- e_wwr
# is an array of 9 values, not one number; Python raises "truth value of an array is
# ambiguous" because it cannot collapse 9 comparisons into one True/False on its own.


# %% [6] Sweep both variables together with meshgrid
# QUESTION           What is the best sampled (wwr, shade_m) combination on this finite
#                    grid, found by evaluating every sampled pair together?
# INPUTS/ASSUMPTIONS an 81x61 grid: np.linspace(0.20, 0.60, 81) x np.linspace(0.0, 1.2, 61)
# METHOD             np.meshgrid the two linspace arrays, call energy_proxy once on the
#                    full grid, then np.argmin + np.unravel_index to find the best cell
# CHECKS/INTERPRET   Expected grid best: wwr=0.275, shade_m=0.9, energy_proxy=-11.135.
#                    Expected local-basin center value (direct call, not grid): -7.08 at
#                    (wwr=0.52, shade_m=0.25).
#                    The dense 81x61 grid corroborates the better sampled region; it does
#                    not prove the continuous global optimum.

wwr_fine = np.linspace(0.20, 0.60, 81)
shade_fine = np.linspace(0.0, 1.2, 61)
WW, SS = np.meshgrid(wwr_fine, shade_fine)

Z = energy_proxy((WW, SS))
print("grid shape:", Z.shape, "=", Z.size, "combinations")

best = np.unravel_index(np.argmin(Z), Z.shape)
print("grid best:", WW[best], SS[best], round(Z[best], 3))
print("local basin center (direct call):", round(energy_proxy((0.52, 0.25)), 3))
# WHY THIS MATTERS: 4,941 combinations, evaluated in one vectorized line -- the same
# meshgrid technique from Meeting A's coarse 63-point demo, just with much finer linspace
# arrays. No new tool was needed to go from a rough read to a precise one, only more
# points per array.
# COMMON ERROR: calling np.meshgrid(wwr_fine, shade_fine) and then forgetting that WW and
# SS, not wwr_fine and shade_fine, are what energy_proxy needs -- passing the original 1-D
# arrays here would silently repeat cell [9]'s AI-audit bug (only 61 elementwise pairs,
# not 4,941 full combinations, and a shape mismatch besides since 81 != 61).


# %% [7] Visualize the full surface as a heatmap
# QUESTION           What does the whole (wwr, shade_m) surface look like -- and can you
#                    see both basins at once?
# INPUTS/ASSUMPTIONS WW, SS, Z from cell [6]
# METHOD             fig, ax = plt.subplots(); ax.pcolormesh(WW, SS, Z, cmap=...);
#                    label both axes with units; add a colorbar; save the figure
# CHECKS/INTERPRET   Two distinct low-value (green, using the suggested colormap) regions
#                    should be visible -- lower-left and lower-right of the plot.

fig, ax = plt.subplots(figsize=(7, 5))
mesh = ax.pcolormesh(WW, SS, Z, cmap="RdYlGn_r", shading="auto")
fig.colorbar(mesh, ax=ax, label="energy_proxy (lower is better)")
ax.set_xlabel("wwr (window-to-wall ratio)")
ax.set_ylabel("shade_m (overhang depth, m)")
ax.set_title("energy_proxy(wwr, shade_m) -- full sweep, Radley Hall south wing")
fig.savefig("radley_energy_sweep_heatmap.png", dpi=150)
print("heatmap saved")
# WHY THIS MATTERS: this is the required heatmap deliverable. Per course policy, a
# plotting call produces no fabricated console text here -- inspect the saved PNG in
# Spyder's Plots pane or Files pane. Verified by rendering it: a deep green pocket sits
# near the lower-left (low wwr, high shade_m -- the better sampled basin) and a shallower green
# pocket sits near the lower-right (mid-high wwr, low shade_m -- the local basin), with a
# red ridge running between them near wwr=0.40.
# COMMON ERROR: choosing a sequential colormap (like "viridis") instead of a diverging one
# for a "lower is better" quantity -- RdYlGn_r (reversed red-yellow-green) makes "good"
# read as green and "bad" read as red, matching intuitive traffic-light expectations.


# %% [8] Write the required one-sentence sensitivity finding
# QUESTION           State, in one sentence, which sampled region scores best on the grid
#                    and how much better it is than the baseline.
# INPUTS/ASSUMPTIONS cell [6]'s grid best (-11.135) and cell [1]'s baseline (22.076)
# METHOD             fill in sensitivity_finding as one plain-language sentence, with
#                    both numbers stated
# CHECKS/INTERPRET   The sentence must name a region (low wwr, deep shade), a number for
#                    the grid-best score, and a number for the improvement over baseline.

sensitivity_finding = (
    "Moving toward a low window-to-wall ratio (about 0.275) with deep shading (about "
    "0.90 m) drives energy_proxy down to about -11.1, roughly 33.2 points better than "
    "the 22.076 baseline design -- clearly beating the smaller, shallower improvement "
    "available near the higher-wwr, shallow-shading region (about -7.08, 29.2 points "
    "better than baseline)."
)
print(sensitivity_finding)
# WHY THIS MATTERS: this sentence is the actual graded weekly-assignment artifact --
# not the heatmap image alone. A picture without a stated, numeric finding does not yet
# answer the sensitivity question this whole studio was built to answer.


# %% [9] AI-generated sweep script audit
# QUESTION           Would you accept this AI-suggested sensitivity script as-is?
# INPUTS/ASSUMPTIONS ai_sweep as shown text
# METHOD             list at least four specific defects, then compare with your own
#                    pipeline from cells [3]-[6]
# CHECKS/INTERPRET   A defensible list names the shape defect and the flawed-comparison
#                    defect -- not merely that the code "looks wrong."

ai_sweep = """
import numpy as np
from typing import Callable

def ai_sweep_and_compare(energy_proxy: Callable) -> None:
    \"\"\"Audit target: two seeded defects -- no meshgrid, mismatched baselines.\"\"\"
    wwr_vals = np.linspace(0.20, 0.60, 9)
    shade_vals = np.linspace(0.0, 1.2, 9)

    # "sweep both variables together"
    combined = energy_proxy((wwr_vals, shade_vals))
    print("combined shape:", combined.shape)

    wwr_range = energy_proxy((wwr_vals, 0.30)).max() - energy_proxy((wwr_vals, 0.30)).min()
    shade_range = energy_proxy((0.60, shade_vals)).max() - energy_proxy((0.60, shade_vals)).min()
    print(f"wwr range: {wwr_range:.3f}, shade range: {shade_range:.3f}")
    if wwr_range > shade_range:
        print("Conclusion: wwr is the more important variable.")
"""

ai_defects = [
    "Missing meshgrid: energy_proxy((wwr_vals, shade_vals)) with two 9-element 1-D "
    "arrays does NOT sweep 'both variables together' -- NumPy broadcasts them "
    "elementwise, pairing wwr_vals[0] only with shade_vals[0], wwr_vals[1] only with "
    "shade_vals[1], and so on. combined.shape prints (9,), 9 pairs, not the 81 "
    "combinations the comment claims.",
    "Mismatched baselines: wwr_range is measured at shade_m=0.30, while shade_range is "
    "measured at a DIFFERENT, arbitrarily chosen wwr=0.60 -- an unfair comparison, "
    "exactly the trap cell [4] demonstrated. Fixing wwr at 0.28 instead of 0.60 would "
    "have given shade_range=33.996, reversing the conclusion entirely.",
    "Overclaimed conclusion: 'wwr is the more important variable' is stated as a general "
    "fact about the formula, when it is only true for these two specific, mismatched "
    "fixed values -- cell [4] already proved this exact claim is not stable.",
    "No full-grid evidence: the script never builds a meshgrid or evaluates the full "
    "(wwr, shade_m) surface, so it has no basis for comparing the two variables' actual "
    "combined effect at all -- only two incommensurable 1-D slices.",
]

print(ai_sweep)
for defect in ai_defects:
    print("-", defect)
# WHY THIS MATTERS: every one of these four defects is individually plausible and easy to
# miss under time pressure -- especially because the code runs without raising an error.
# An AI suggestion that "runs" and "looks reasonable" is never sufficient evidence it
# answers the actual sensitivity question correctly.


# %% [10] Self-check: a different threshold and a different region
# QUESTION           Does your pipeline hold up on a scenario you have not hand-checked
#                    yet -- a stricter target, and a different sub-region of the grid?
# INPUTS/ASSUMPTIONS Z, WW, SS from cell [6]; a stricter target of -9.0 (not the 15.0
#                    used in cell [5]); the local-basin sub-region (wwr 0.45-0.60,
#                    shade_m 0.15-0.35), NOT the better sampled sub-region already discussed
# METHOD             write 2-4 assert statements checking the stricter mask's count and
#                    the local sub-region's grid minimum
# CHECKS/INTERPRET   Expected count meeting target <=-9.0: 45 of 4,941 cells, all inside
#                    the better sampled region (wwr 0.255-0.295). Expected local sub-region grid
#                    minimum: about -7.10, near (wwr=0.525, shade_m=0.26).

strict_mask = Z <= -9.0
assert strict_mask.sum() == 45

region_local = (WW >= 0.45) & (WW <= 0.60) & (SS >= 0.15) & (SS <= 0.35)
local_region_min = np.min(np.where(region_local, Z, np.inf))
assert abs(local_region_min - (-7.10)) < 0.05

assert WW[strict_mask].min() >= 0.25 and WW[strict_mask].max() <= 0.30
assert SS[strict_mask].min() >= 0.80 and SS[strict_mask].max() <= 1.00

print("Self-check passed: strict-mask count =", strict_mask.sum(),
      "| local sub-region min =", round(local_region_min, 3))
# WHY THIS MATTERS: cell [5] used target=15.0 and the better sampled sub-region was never
# isolated on its own; this cell tests the SAME mask-and-region technique on a stricter,
# previously unused target and the OTHER basin's sub-region. It is one useful transfer
# check, not proof that the technique generalizes to every target or region.


# %% [11] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished sweep in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five
#                    required points listed below
# METHOD             fill in the AI-use record honestly, then write the exit
#                    explanation addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing
#                    the sweep cannot tell you.

ai_use_record = """
Tool/model: Example assistant
Prompt: Write a NumPy script that sweeps two design variables against energy_proxy and
tells me which one matters more.
Suggestion received: A script computing energy_proxy((wwr_vals, shade_vals)) directly on
two 1-D arrays (no meshgrid) and comparing ranges measured at two different fixed
baselines, concluding wwr is more important.
What I accepted: The general shape -- sweep each variable, compare ranges, then build a
full grid.
What I modified and why: Added np.meshgrid so every (wwr, shade_m) combination is
evaluated together, not just 9 elementwise pairs; re-measured both 1-D ranges at matched,
stated fixed baselines instead of mismatched ones; added the boolean-mask target check
and the fine 81x61 grid to get a precise, not just directional, answer.
What I rejected and why: The claim that wwr is "the more important variable" in general --
cell [4] showed this flips depending on where the other variable is fixed, so no single
variable can be named "more important" without stating the full 2-D picture.
How I tested it: Asserted the vectorized-vs-loop equivalence in cell [2], and ran the
self-check in cell [10] on a stricter target and the other basin's sub-region, neither of
which were used in the earlier worked cells.
One limitation I found: This sweep says which (wwr, shade_m) combination scores best on
THIS fictional proxy formula -- it says nothing about cost, daylighting, or structural
feasibility, which a real design decision would also need to weigh.
"""

exit_explanation = """
The one-at-a-time sweeps in cells [3]-[4] gave a misleading first read: fixed at
shade_m=0.30, wwr looked 8 times more important than shade_m fixed at wwr=0.40 -- but
re-fixing wwr at 0.28 made shade_m's own range jump to 33.996, bigger than wwr's original
28.373. meshgrid added what no 1-D sweep could: every one of 4,941 (wwr, shade_m) pairs
evaluated together, not one slice. The heatmap in cell [7] shows two separated low-score
basins -- a deep one near low wwr, deep shading, a shallower one near mid-high wwr,
shallow shading -- with a high ridge between them. Finding: aim near wwr=0.275,
shade_m=0.90, about 33.2 points better than the 22.076 baseline. This sweep cannot say if
that design is affordable or buildable.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Expected workflow for insulation thickness × glazing ratio: stated ranges and
# units → meshgrid → vectorized proxy → feasibility mask → promising region →
# limitation. Accept omitted cost, simplified climate/geometry, discrete product
# sizes, and proxy validity as limitations; reject a single-point universal claim.
