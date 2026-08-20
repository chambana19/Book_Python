# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 9 studio · Parameter sweeps and sensitivity: wwr vs. shade_m
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week09 module folder. No external data file is needed --
     energy_proxy is a provided formula, defined in cell [1] below.
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict a shape, range, or best-region before running.
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A sensitivity finding is not "done" until you can state, in one plain sentence, which
  region of the design space is best and how much better it is than the baseline -- not
  just that you produced a heatmap picture.

MILESTONE: PROJECT 2 ASSIGNED THIS WEEK
  Project 2 (Predict, Optimize, Decide) is assigned this week -- problem-area, dataset,
  and prediction/optimization pairing selection is now open. The two-variable sensitivity
  sweep you build in this file is not just practice: it is the exact Part I requirement
  Project 2 will ask you to reproduce, as supporting evidence, on your own problem later
  this semester.
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


print(round(basin(0.40, 0.30, 0.52, 0.25,
                  30.0, 0.06, 0.18), 3))


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

# TODO: Confirm the printed basin value is -3.906 and the printed baseline rounds to
# 22.076. If either differs, check the formula above against Meeting A's slide, line by
# line, before continuing -- every sweep in this studio is built on these two functions.


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

# TODO: build `looped` with an explicit for-loop over wwr_check, appending one
# energy_proxy((w, 0.30)) call per value, e.g.:
# looped = []
# for w in wwr_check:
#     looped.append(energy_proxy((w, 0.30)))
# looped = np.array(looped)
raise NotImplementedError(
    "Cell [2] incomplete: build `looped` with the required loop, then remove this gate."
)

# TODO: uncomment once `looped` is built correctly
# assert np.allclose(vectorized, looped)
print("vectorized == looped:", np.allclose(vectorized, looped))


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

# TODO: Before moving on, write one sentence: based on these two numbers alone, which
# variable looks more important?


# %% [4] The trap: re-run both sweeps from different fixed baselines
# QUESTION           Does "wwr matters more" still hold if the OTHER variable is fixed
#                    somewhere else?
# INPUTS/ASSUMPTIONS same two 9-point sweeps as cell [3], but shade_m now fixed at 0.28's
#                    partner value and wwr now fixed at 0.90's partner value
# METHOD             re-run energy_proxy with wwr fixed at 0.28 (for the shade sweep) and
#                    shade_m fixed at 0.90 (for the wwr sweep)
# CHECKS/INTERPRET   Expected shade range @ wwr=0.28: 33.996. Expected wwr range @
#                    shade=0.90: 33.182 -- both much bigger than cell [3] suggested.

# TODO: compute e_shade2 = energy_proxy((0.28, shade_vals)) and print its range
raise NotImplementedError(
    "Cell [3] incomplete: compute e_shade2 at the required fixed WWR, then remove this gate."
)
print("shade range @ wwr=0.28:", round(e_shade2.max() - e_shade2.min(), 3))

# TODO: compute e_wwr2 = energy_proxy((wwr_vals, 0.90)) and print its range
raise NotImplementedError(
    "Cell [3] incomplete: compute e_wwr2 at the required fixed shade, then remove this gate."
)
print("wwr range @ shade=0.90:", round(e_wwr2.max() - e_wwr2.min(), 3))

# TODO: write one sentence explaining why cell [3]'s conclusion was incomplete.


# %% [5] Boolean mask: flag which wwr values meet a target
# QUESTION           Of the 9 wwr values from cell [3], which ones score 15 or better?
# INPUTS/ASSUMPTIONS e_wwr and wwr_vals from cell [3]; target = 15.0
# METHOD             build a boolean mask with e_wwr <= target, then index wwr_vals
#                    with that mask
# CHECKS/INTERPRET   Expected passing values: [0.45, 0.5, 0.55, 0.6] (4 of 9).

target = 15.0
# TODO: meets_target = e_wwr <= target
raise NotImplementedError(
    "Cell [4] incomplete: build the Boolean target mask, then remove this gate."
)
print(meets_target)
print("passing wwr values:", wwr_vals[meets_target])


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

# TODO: Z = energy_proxy((WW, SS))
raise NotImplementedError(
    "Cell [5] incomplete: evaluate the full two-variable grid, then remove this gate."
)

print("grid shape:", Z.shape, "=", Z.size, "combinations")

# TODO: best = np.unravel_index(np.argmin(Z), Z.shape)
# print("grid best:", WW[best], SS[best], Z[best])

print("local basin center (direct call):", round(energy_proxy((0.52, 0.25)), 3))


# %% [7] Visualize the full surface as a heatmap
# QUESTION           What does the whole (wwr, shade_m) surface look like -- and can you
#                    see both basins at once?
# INPUTS/ASSUMPTIONS WW, SS, Z from cell [6]
# METHOD             fig, ax = plt.subplots(); ax.pcolormesh(WW, SS, Z, cmap=...);
#                    label both axes with units; add a colorbar; save the figure
# CHECKS/INTERPRET   Two distinct low-value (green, if using the suggested colormap)
#                    regions should be visible -- lower-left and lower-right of the plot.

fig, ax = plt.subplots(figsize=(7, 5))
# TODO: mesh = ax.pcolormesh(WW, SS, Z, cmap="RdYlGn_r", shading="auto")
# TODO: fig.colorbar(mesh, ax=ax, label="energy_proxy (lower is better)")
ax.set_xlabel("wwr (window-to-wall ratio)")
ax.set_ylabel("shade_m (overhang depth, m)")
ax.set_title("energy_proxy(wwr, shade_m) -- full sweep, Radley Hall south wing")
fig.savefig("radley_energy_sweep_heatmap.png", dpi=150)
print("heatmap saved")


# %% [8] Write the required one-sentence sensitivity finding
# QUESTION           State, in one sentence, which sampled region scores best on the grid
#                    and how much better it is than the baseline.
# INPUTS/ASSUMPTIONS cell [6]'s grid best (-11.135) and cell [1]'s baseline (22.076)
# METHOD             fill in sensitivity_finding as one plain-language sentence, with
#                    both numbers stated
# CHECKS/INTERPRET   The sentence must name a region (low wwr, deep shade), a number for
#                    the grid-best score, and a number for the improvement over baseline.

sensitivity_finding = "TODO: one sentence naming the best sampled region, its score, and the improvement over baseline."
print(sensitivity_finding)


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
    # TODO: add at least four specific defects
]

print(ai_sweep)
for defect in ai_defects:
    print("-", defect)


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

# TODO: Add 2-4 assert statements here, using a stricter target (-9.0) and the local
# sub-region -- NOT the better-basin sampled numbers already used in cells [6]-[8]. Example to
# complete:
# strict_mask = Z <= -9.0
# assert strict_mask.sum() == 45
# region_local = (WW >= 0.45) & (WW <= 0.60) & (SS >= 0.15) & (SS <= 0.35)
# assert abs(np.min(np.where(region_local, Z, np.inf)) - (-7.10)) < 0.05

print("Self-check cell reached")


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
1. why the one-at-a-time sweeps in cells [3]-[4] gave a misleading first read,
2. what meshgrid added that a 1-D sweep could not,
3. what the heatmap in cell [7] shows about the two basins,
4. your one-sentence sensitivity finding from cell [8], and
5. one thing this sweep cannot yet tell you about Radley Hall's actual design.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Outline a 2-D sweep for insulation thickness × glazing ratio: define ranges
# and units, generate every combination with meshgrid, evaluate one proxy, mask
# a daylight/constructability threshold, identify a promising region, and name
# one limitation. Do not report one sampled point as a universal optimum.
