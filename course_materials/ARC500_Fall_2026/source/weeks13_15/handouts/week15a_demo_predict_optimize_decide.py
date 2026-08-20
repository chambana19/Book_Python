# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 15a REFERENCE DEMO · Predict-optimize-decide, worked end to end
Syracuse University · School of Architecture · Fall 2026

THIS IS A REFERENCE DEMO, NOT AN ASSIGNMENT.
  There is no Meeting B this week (Dec 9 is a reading day) and no separate graded
  weekly assignment -- this week's deliverable IS Project 2 itself. This script is a
  complete, runnable, instructor-narrated walkthrough of the exact integration pattern
  Project 2 Part IV requires: take a fitted model from Week 13 or Week 14, and use it
  as the objective (or a constraint) inside scipy.optimize.minimize -- the same tool
  Week 11 used, with a fitted model standing in for Week 9/11's analytic energy_proxy
  formula. Nothing here is scaffolded with # TODO: gaps; every cell already runs top to
  bottom. Students may keep this file to adapt for their own Project 2 pipeline.

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week15 module folder, with radley_portfolio_envelope.csv
     inside a data/ subfolder next to it (data/radley_portfolio_envelope.csv).
  2. Click inside one # %% cell and press Ctrl+Enter -- same workflow as every prior
     week's handout.
  3. Read each QUESTION before running its cell; compare the printed output against the
     CHECKS/INTERPRET line before moving on.
  4. Restart the kernel and run from the top at least once, to confirm the whole demo
     is reproducible end to end (random_state=42 everywhere a split occurs).

COURSE RULE, CARRIED FORWARD FROM WEEK 13
  A predicted number is not a decision. Every optimization result below is reported
  with a separately calibrated split-conformal range and its training-domain limits.
  The optimized candidate is then checked with independent reference evidence. It is
  still a bounded recommendation to investigate, not a guaranteed building result.
"""

# %% [0] Environment and working-folder check
# QUESTION           Run the cell and confirm your Python version, executable, and working
#                    folder, and that a data/ subfolder holding
#                    radley_portfolio_envelope.csv sits next to this script.
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


# %% [1] Fit a separate Week 15 demonstration surrogate with Week 14's four features
# QUESTION           What does the fitted surrogate model -- the one this whole demo
#                    optimizes against -- actually look like?
# INPUTS/ASSUMPTIONS data/radley_portfolio_envelope.csv (n=140); features
#                    [wwr, shade_m, glazing_shgc, compactness]; target eui_kwh_m2yr;
#                    an untouched 25% final test set plus a 30-row calibration set drawn
#                    only from the remaining training pool
# METHOD             fit LinearRegression on 75 rows, use 30 separate rows to calibrate a
#                    90% split-conformal interval, and open the 35-row final test only for
#                    the final performance audit; this demo is self-contained
# CHECKS/INTERPRET   Expected coef_ (wwr, shade_m, glazing_shgc, compactness):
#                    [17.0805, -2.7740, 5.2417, 6.0549], intercept 13.8918.
#                    Expected final-test MAE=2.0272, RMSE=2.5312, R2=0.5599 and a
#                    90% split-conformal half-width q_hat=5.3388 kWh/m2/yr.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = Path("data") / "radley_portfolio_envelope.csv"
portfolio = pd.read_csv(DATA_PATH)

FEATURES = ["wwr", "shade_m", "glazing_shgc", "compactness"]
TARGET = "eui_kwh_m2yr"

X = portfolio[FEATURES].values
y = portfolio[TARGET].values

# Reserve the final test first. It is never used to fit the model or choose an interval.
X_train_pool, X_test, y_train_pool, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
X_fit, X_cal, y_fit, y_cal = train_test_split(
    X_train_pool, y_train_pool, test_size=30, random_state=42
)
assert len(X_fit) == 75 and len(X_cal) == 30 and len(X_test) == 35

surrogate = LinearRegression().fit(X_fit, y_fit)
pred_cal = surrogate.predict(X_cal)
pred_test = surrogate.predict(X_test)

# Finite-sample split-conformal quantile for nominal 90% marginal coverage.
# The "higher" rule prevents interpolation to an anticonservative cutoff.
CONFORMAL_ALPHA = 0.10
calibration_errors = np.abs(y_cal - pred_cal)
conformal_level = min(
    1.0,
    np.ceil((len(calibration_errors) + 1) * (1 - CONFORMAL_ALPHA))
    / len(calibration_errors),
)
q_hat = float(np.quantile(calibration_errors, conformal_level, method="higher"))

mae = mean_absolute_error(y_test, pred_test)
rmse = np.sqrt(mean_squared_error(y_test, pred_test))
r2 = r2_score(y_test, pred_test)

print("coef_ (wwr, shade_m, glazing_shgc, compactness):", surrogate.coef_.round(4))
print("intercept_:", round(surrogate.intercept_, 4))
print(f"fit/calibration/final-test rows: {len(X_fit)}/{len(X_cal)}/{len(X_test)}")
print(f"final-test MAE={mae:.4f}  RMSE={rmse:.4f}  R2={r2:.4f}")
print(f"90% split-conformal half-width q_hat={q_hat:.4f} kWh/m2/yr")

assert np.allclose(surrogate.coef_.round(4), [17.0805, -2.7740, 5.2417, 6.0549], atol=1e-3)
assert round(surrogate.intercept_, 4) == 13.8918
assert round(q_hat, 4) == 5.3388


# %% [2] Baseline design and its predicted EUI
# QUESTION           Held at a plausible "as-designed" starting point, what does the
#                    surrogate model predict?
# INPUTS/ASSUMPTIONS baseline design, held fixed except where the optimizer is
#                    explicitly allowed to move it: wwr=0.50, shade_m=0.20,
#                    glazing_shgc=0.45, compactness=1.10, orientation=S (orientation is
#                    not a numeric input to this 4-feature model; it is part of the
#                    scenario's narrative, not the regression, exactly as in Week 14)
# METHOD             surrogate.predict() on a single-row array built from the baseline
#                    dict
# CHECKS/INTERPRET   Expected baseline predicted EUI: 30.8964 kWh/m2/yr.

BASELINE = {"wwr": 0.50, "shade_m": 0.20, "glazing_shgc": 0.45, "compactness": 1.10,
            "orientation": "S"}

def row_from(wwr: float, shade_m: float, glazing_shgc: float, compactness: float) -> np.ndarray:
    """One design point, in FEATURES order, ready for surrogate.predict()."""
    return np.array([[wwr, shade_m, glazing_shgc, compactness]])

baseline_pred = surrogate.predict(
    row_from(BASELINE["wwr"], BASELINE["shade_m"], BASELINE["glazing_shgc"], BASELINE["compactness"])
)[0]
print("Baseline design:", BASELINE)
print("Baseline predicted EUI:", round(baseline_pred, 4))

assert round(baseline_pred, 4) == 30.8964


# %% [2b] FIGURE 1 (PREDICT) -- predicted vs. actual on the held-out test rows
# QUESTION           Is this surrogate accurate enough to be worth optimizing against?
#                    Cell [1] printed R2=0.5599 as a number; what does that number LOOK
#                    like as evidence a reviewer can read?
# INPUTS/ASSUMPTIONS y_test (35 untouched final-test rows), pred_test, and q_hat calibrated
#                    on a separate 30-row calibration set; nothing is refit here
# METHOD             scatter actual (x) against predicted (y) for the test rows; add the
#                    1:1 GRAY dashed reference line and the calibrated 90% split-conformal
#                    band; annotate final-test metrics and empirical interval coverage
#                    with fig.savefig()
# CHECKS/INTERPRET   Expected: q_hat=5.3388 and 34/35 final-test rows inside the nominal
#                    90% interval in this deterministic course split. Empirical coverage
#                    on 35 rows is descriptive, not a new tuning signal.

import matplotlib.pyplot as plt

# Course figure palette -- cells [6b] and [7b] reuse these same names.
BLUE = "#2E74B5"     # the optimized / recommended case
AMBER = "#B5731A"    # the baseline / "before" case
GREEN = "#2E7D5B"    # the accepted, verified answer
GRAY = "#5A5F66"     # reference lines and annotations
GRAY_LT = "#B8BCC4"  # the uncertainty band, gridlines

inside_band = int(np.sum(np.abs(y_test - pred_test) <= q_hat))
print(f"test rows={len(y_test)}  R2={r2:.4f}  MAE={mae:.4f}  RMSE={rmse:.4f}  "
      f"inside nominal 90% split-conformal interval: {inside_band} of {len(y_test)} "
      f"({inside_band / len(y_test) * 100:.1f}%)")

lo = min(y_test.min(), pred_test.min()) - 1.5
hi = max(y_test.max(), pred_test.max()) + 1.5
line = np.array([lo, hi])

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.fill_between(line, line - q_hat, line + q_hat, color=GRAY_LT, alpha=0.45,
                label=f"90% split-conformal band (+/-{q_hat:.2f} kWh/m2/yr)")
ax.plot(line, line, color=GRAY, linestyle="--", linewidth=1.4,
        label="1:1 line (perfect prediction)")
ax.scatter(y_test, pred_test, color=BLUE, s=45, alpha=0.85, edgecolor="white",
           linewidth=0.6, label=f"held-out test rows (n={len(y_test)})")
ax.annotate(f"final-test R2 = {r2:.4f}\nMAE = {mae:.4f} kWh/m2/yr\n"
            f"RMSE = {rmse:.4f} kWh/m2/yr\n"
            f"{inside_band}/{len(y_test)} inside nominal 90% interval",
            xy=(0.03, 0.97), xycoords="axes fraction", va="top", ha="left",
            fontsize=10, color=GRAY,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=GRAY_LT))
ax.set_title("Is the surrogate accurate enough to optimize against?")
ax.set_xlabel("actual EUI (kWh/m2/yr)")
ax.set_ylabel("surrogate-predicted EUI (kWh/m2/yr)")
ax.set_xlim(lo, hi)
ax.set_ylim(lo, hi)
ax.grid(alpha=0.3, color=GRAY_LT)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="lower right", fontsize=9)
fig.tight_layout()
fig.savefig("week15_predict_vs_actual.png", dpi=150)
print("saved week15_predict_vs_actual.png")
# WHY THIS MATTERS: RMSE remains an average error metric; it is not an interval. q_hat was
# calibrated on different rows and therefore has a valid split-conformal interpretation:
# under exchangeability, a new ordinary design has 90% marginal coverage. An optimizer's
# adaptively selected winner is not an ordinary pre-specified design, so even this interval
# is a diagnostic rather than permission to skip the post-optimization simulation in [7c].
# COMMON ERROR: plotting predicted vs. actual on the TRAINING rows instead of y_test /
# pred_test. The training scatter always hugs the diagonal more tightly, so the figure
# looks better and silently invalidates the final audit.


# %% [3] The integration move: wrap the fitted model as a minimize() objective
# QUESTION           Surrogate model, defined: a fitted model used as a fast stand-in
#                    for an expensive or unavailable simulation, so an optimizer can
#                    search against it directly. How do we hand THIS surrogate to
#                    scipy.optimize.minimize the same way Week 11 handed it
#                    energy_proxy(wwr, shade_m)?
# INPUTS/ASSUMPTIONS surrogate from cell [1]; BASELINE from cell [2]; the optimizer is
#                    only allowed to move (wwr, shade_m) -- glazing_shgc, compactness,
#                    and orientation stay fixed at baseline, exactly as Week 15's plan
#                    specifies
# METHOD             one small Python function of (wwr, shade_m) only, which builds the
#                    full 4-feature row (holding the other two features at BASELINE) and
#                    calls surrogate.predict() -- this is the ENTIRE integration: same
#                    minimize() call site as Week 11, a different function inside it
# CHECKS/INTERPRET   Calling this function at the baseline (wwr, shade_m) must reproduce
#                    cell [2]'s baseline predicted EUI exactly.

def surrogate_eui(design_vars: tuple) -> float:
    """Predicted EUI (kWh/m2/yr) as a function of (wwr, shade_m) alone.

    glazing_shgc and compactness are held at BASELINE -- this is exactly the same
    minimize() objective shape as Week 11's energy_proxy(v), except the formula inside
    it is now a FITTED model instead of a hand-written analytic function.
    """
    wwr, shade_m = design_vars
    row = row_from(wwr, shade_m, BASELINE["glazing_shgc"], BASELINE["compactness"])
    return surrogate.predict(row)[0]

check_value = surrogate_eui((BASELINE["wwr"], BASELINE["shade_m"]))
print("surrogate_eui at baseline (wwr, shade_m):", round(check_value, 4))

assert round(check_value, 4) == round(baseline_pred, 4)


# %% [4] DEMO 1 -- minimize() from a plausible starting guess
# QUESTION           Starting the search at the baseline design itself, where does
#                    minimize() land?
# INPUTS/ASSUMPTIONS bounds=[(0.20, 0.60), (0.0, 1.2)] -- the SAME wwr/shade_m bounds as
#                    Weeks 9 and 11, unchanged; x0=(0.50, 0.20), the baseline design
#                    point
# METHOD             from scipy.optimize import minimize; call minimize(surrogate_eui,
#                     x0=..., bounds=...), exactly Week 11's call shape
# CHECKS/INTERPRET   Expected result.x = [0.20, 1.20] (both variables at a BOUND, not an
#                    interior point), result.fun = 22.9983, result.success = True.

from scipy.optimize import minimize

BOUNDS = [(0.20, 0.60), (0.0, 1.2)]

result_1 = minimize(surrogate_eui, x0=(0.50, 0.20), bounds=BOUNDS)
if not result_1.success:
    raise RuntimeError(f"DEMO 1 optimizer failed: {result_1.message}")
print("DEMO 1 -- x0=(0.50, 0.20)")
print("  x:", result_1.x.round(4))
print("  predicted EUI:", round(result_1.fun, 4))
print("  success:", result_1.success)

assert np.allclose(result_1.x.round(2), [0.20, 1.20])
assert round(result_1.fun, 4) == 22.9983


# %% [5] DEMO 2 -- only x0 changes; does the answer change too?
# QUESTION           Week 11 taught us NOT to trust a single starting guess on a
#                    nonlinear objective. Does that same warning apply to THIS
#                    surrogate?
# INPUTS/ASSUMPTIONS same surrogate_eui and bounds; a deliberately very different
#                    starting guess, x0=(0.22, 1.10), close to where Week 11's demo
#                    landed for its GLOBAL optimum on the unrelated energy_proxy problem
# METHOD             same minimize() call, only x0 changed
# CHECKS/INTERPRET   Expected: converges to the IDENTICAL x=[0.20, 1.20],
#                    predicted EUI=22.9983 -- agreement with DEMO 1, not disagreement.

result_2 = minimize(surrogate_eui, x0=(0.22, 1.10), bounds=BOUNDS)
if not result_2.success:
    raise RuntimeError(f"DEMO 2 optimizer failed: {result_2.message}")
print("DEMO 2 -- x0=(0.22, 1.10)")
print("  x:", result_2.x.round(4))
print("  predicted EUI:", round(result_2.fun, 4))
print("  success:", result_2.success)

assert np.allclose(result_1.x.round(4), result_2.x.round(4))
assert round(result_1.fun, 4) == round(result_2.fun, 4)
print("Two very different starting guesses agree exactly -- unlike Week 11's two-basin demo.")


# %% [6] Why there is no local trap here: sweep each axis and look at the shape
# QUESTION           Week 11's energy_proxy had two real basins; 5 of 8 starting
#                    guesses landed in the wrong one. Why does THIS surrogate never do
#                    that?
# INPUTS/ASSUMPTIONS same surrogate_eui; sweep wwr across its full bound with shade_m
#                    held at baseline, then sweep shade_m across its full bound with wwr
#                    held at baseline
# METHOD             evaluate surrogate_eui at 5 evenly spaced points across each
#                    variable's own bounds and print the sequence
# CHECKS/INTERPRET   Both sequences must be MONOTONIC (strictly increasing for wwr,
#                    strictly decreasing for shade_m) with no bend and no interior dip --
#                    that is what "linear in wwr and shade_m" looks like in practice, and
#                    it is exactly why the optimizer always pushes to a bound instead of
#                    settling into an interior valley.

fractions = np.array([0.0, 0.25, 0.5, 0.75, 1.0])

wwr_sweep = 0.20 + fractions * (0.60 - 0.20)
eui_over_wwr = []
for w in wwr_sweep:
    eui_over_wwr.append(round(surrogate_eui((w, BASELINE["shade_m"])), 4))
print("wwr sweep (shade_m fixed at baseline 0.20):")
for w, e in zip(wwr_sweep.round(3), eui_over_wwr):
    print(f"  wwr={w:.3f} -> predicted EUI={e}")

shade_sweep = 0.0 + fractions * (1.2 - 0.0)
eui_over_shade = []
for s in shade_sweep:
    eui_over_shade.append(round(surrogate_eui((BASELINE["wwr"], s)), 4))
print("shade_m sweep (wwr fixed at baseline 0.50):")
for s, e in zip(shade_sweep.round(3), eui_over_shade):
    print(f"  shade_m={s:.3f} -> predicted EUI={e}")

diffs_wwr = np.diff(eui_over_wwr)
diffs_shade = np.diff(eui_over_shade)
assert np.all(diffs_wwr > 0), "expected predicted EUI to rise monotonically with wwr"
assert np.all(diffs_shade < 0), "expected predicted EUI to fall monotonically with shade_m"
print("Both sweeps are monotonic: a straight line has no interior valley to trap a search in.")
# WHY THIS MATTERS: this is a property of THIS surrogate's own shape (LinearRegression
# is linear in wwr and shade_m by construction, holding the other two features fixed) --
# it is not a general guarantee about every fitted model. A model with polynomial
# features, or a tree-based model, could reintroduce real local optima, exactly like
# Week 11's energy_proxy.


# %% [6b] FIGURE 2 (OPTIMIZE) -- the surrogate's own design space, and where the search went
# QUESTION           Cells [4]-[6] argued in numbers that minimize() slides straight to a
#                    corner of the bounded box. What does that search look like drawn on
#                    the surrogate's own surface?
# INPUTS/ASSUMPTIONS surrogate_eui from cell [3]; BOUNDS from cell [4]; baseline_pred from
#                    cell [2]; result_1 from cell [4]. glazing_shgc and compactness stay
#                    fixed at BASELINE, exactly as the objective defines them
# METHOD             np.meshgrid over the two bounded variables (the same technique as Week
#                    9's heatmap), evaluate surrogate_eui at every grid point, draw it with
#                    ax.contourf(cmap="RdYlGn_r", lower-is-better) plus a labeled colorbar;
#                    re-run the SAME minimize() call through a logging wrapper so the
#                    search's real effort (evaluations, distinct designs visited) can be
#                    counted and reported on the figure; mark baseline in AMBER and the
#                    optimum in BLUE, joined by a dashed arrow showing the move
# CHECKS/INTERPRET   Expected: "logged 6 objective evaluations over 1 iteration(s), at 2
#                    distinct (wwr, shade_m) points",
#                    "logged optimum: wwr=0.20, shade_m=1.20, predicted EUI=22.9983" --
#                    identical to cell [4] (the wrapper only records, it does not change
#                    the search), and "surface range: 22.9983 to 33.1592 kWh/m2/yr" (the
#                    best and worst corners of the bounded box: the optimum found, and
#                    wwr=0.60 with no shading at all).

wwr_grid = np.linspace(BOUNDS[0][0], BOUNDS[0][1], 61)
shade_grid = np.linspace(BOUNDS[1][0], BOUNDS[1][1], 61)
WWR, SHADE = np.meshgrid(wwr_grid, shade_grid)
EUI_SURFACE = np.array([[surrogate_eui((w, s)) for w in wwr_grid] for s in shade_grid])
print(f"surface range: {EUI_SURFACE.min():.4f} to {EUI_SURFACE.max():.4f} kWh/m2/yr")

eval_log = []  # the demo never keeps the search path, so record it here, once

def surrogate_eui_logged(design_vars: tuple) -> float:
    """surrogate_eui(), plus a record of every point the optimizer asks about."""
    value = surrogate_eui(design_vars)
    eval_log.append((design_vars[0], design_vars[1], value))
    return value

result_traced = minimize(surrogate_eui_logged, x0=(0.50, 0.20), bounds=BOUNDS)
path = np.array(eval_log)
n_distinct = len(np.unique(path[:, :2].round(4), axis=0))
print(f"logged {len(eval_log)} objective evaluations over {result_traced.nit} iteration(s), "
      f"at {n_distinct} distinct (wwr, shade_m) points")
print(f"logged optimum: wwr={result_traced.x[0]:.2f}, shade_m={result_traced.x[1]:.2f}, "
      f"predicted EUI={result_traced.fun:.4f}")

assert np.allclose(result_traced.x, result_1.x), "logging wrapper must not change the search"
assert round(result_traced.fun, 4) == round(result_1.fun, 4)

fig, ax = plt.subplots(figsize=(9, 5.5))
surface = ax.contourf(WWR, SHADE, EUI_SURFACE, levels=18, cmap="RdYlGn_r")
fig.colorbar(surface, ax=ax,
             label="surrogate-predicted EUI (kWh/m2/yr) -- lower is better")
ax.annotate("", xy=(result_1.x[0], result_1.x[1]),
            xytext=(BASELINE["wwr"], BASELINE["shade_m"]),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.8, linestyle="--",
                            shrinkA=9, shrinkB=11))
ax.scatter([BASELINE["wwr"]], [BASELINE["shade_m"]], s=170, color=AMBER,
           edgecolor="white", linewidth=1.2, zorder=5,
           label=f"baseline: {baseline_pred:.4f} kWh/m2/yr")
ax.scatter([result_1.x[0]], [result_1.x[1]], s=330, marker="*", color=BLUE,
           edgecolor="white", linewidth=1.2, zorder=5,
           label=f"optimized: {result_1.fun:.4f} kWh/m2/yr")
ax.annotate(f"baseline\nwwr=0.50, shade_m=0.20\n{baseline_pred:.4f} kWh/m2/yr",
            xy=(BASELINE["wwr"], BASELINE["shade_m"]),
            xytext=(0.605, 0.33), fontsize=9, color=AMBER, ha="right",
            arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.4),
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=AMBER))
ax.annotate(f"optimized -- ON a bound, not an interior point\n"
            f"wwr=0.20, shade_m=1.20\n{result_1.fun:.4f} kWh/m2/yr",
            xy=(result_1.x[0], result_1.x[1]), xytext=(0.607, 1.06), fontsize=9,
            color=BLUE, ha="right",
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.4),
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=BLUE))
ax.annotate(f"the search moved DOWNHILL by\n"
            f"{baseline_pred - result_1.fun:.4f} kWh/m2/yr "
            f"({(baseline_pred - result_1.fun) / baseline_pred * 100:.2f}% of baseline)\n"
            f"in {result_traced.nit} iteration: {len(path)} evaluations,\n"
            f"only {n_distinct} distinct designs (start, then the corner)",
            xy=(0.605, 0.75), fontsize=9, color=GREEN, ha="right",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=GREEN))
ax.set_title("Where did minimize() search, and how far downhill did it move the design?")
ax.set_xlabel("wwr (window-to-wall ratio, dimensionless)")
ax.set_ylabel("shade_m (overhang depth, m)")
ax.set_xlim(BOUNDS[0][0] - 0.015, BOUNDS[0][1] + 0.015)
ax.set_ylim(BOUNDS[1][0] - 0.045, BOUNDS[1][1] + 0.075)
ax.grid(alpha=0.3, color=GRAY_LT)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="lower left", fontsize=9, framealpha=0.95)
fig.tight_layout()
fig.savefig("week15_optimize_search_path.png", dpi=150)
print("saved week15_optimize_search_path.png")
# WHY THIS MATTERS: this is the same picture Week 9 drew for the hand-written
# energy_proxy(wwr, shade_m) formula -- except the surface here is a FITTED MODEL. The
# colors tilt smoothly in one direction with no valley anywhere inside the box, which is
# cell [6]'s monotonicity result made visible: the answer had to land on a corner. Seeing
# the surface is also how you catch the opposite case -- if a reviewer asks "did the
# optimizer just stop early?", a picture of where it searched answers that, two numbers
# cannot.
# COMMON ERROR: reading the corner star as "the best possible building." It is the best
# point INSIDE the bounds you typed in cell [4]. Widen BOUNDS and the star moves; the
# surface only exists where the model was asked to predict, and pushing wwr or shade_m
# past the training range is Week 13's silent extrapolation all over again.


# %% [7] Baseline vs. optimized: state the improvement, then frame the decision
# QUESTION           How much does the optimizer's recommended design improve on the
#                    baseline, and how should that improvement be reported?
# INPUTS/ASSUMPTIONS baseline_pred from cell [2]; result_1 from cell [4]
# METHOD             improvement = baseline_pred - result_1.fun; percent = improvement /
#                    baseline_pred * 100
# CHECKS/INTERPRET   Expected predicted improvement=7.8981 kWh/m2/yr, about 25.56%.

improvement = baseline_pred - result_1.fun
improvement_pct = improvement / baseline_pred * 100

print(f"{'design':<12}{'wwr':>8}{'shade_m':>10}{'predicted EUI':>16}")
print(f"{'baseline':<12}{BASELINE['wwr']:>8.2f}{BASELINE['shade_m']:>10.2f}{baseline_pred:>16.4f}")
print(f"{'optimized':<12}{result_1.x[0]:>8.2f}{result_1.x[1]:>10.2f}{result_1.fun:>16.4f}")
print(f"Improvement: {improvement:.4f} kWh/m2/yr ({improvement_pct:.2f}%)")

assert round(improvement, 4) == 7.8981
assert round(improvement_pct, 2) == 25.56

decision_sentence = (
    "The surrogate model predicts an EUI reduction of about 7.9 kWh/m2/yr (about 26%) "
    "at wwr=0.20, shade_m=1.20, holding glazing_shgc/compactness/orientation fixed at "
    f"baseline. A separately calibrated nominal 90% interval has half-width {q_hat:.2f} "
    "kWh/m2/yr, but marginal split-conformal coverage does not certify an adaptively "
    "optimized winner. The result is a candidate for an independent high-fidelity run, "
    "not a guaranteed performance claim."
)
print("\nDECISION FRAMING:\n" + decision_sentence)


# %% [7b] FIGURE 3 (DECIDE) -- prediction intervals are context, not a decision test
# QUESTION           This is the figure that goes in the review: what exactly changes
#                    between the baseline and recommended design, and what uncertainty
#                    must travel with the predicted values?
# INPUTS/ASSUMPTIONS BASELINE and baseline_pred from cell [2]; result_1 from cell [4];
#                    improvement/improvement_pct from cell [7]; q_hat calibrated on the
#                    separate calibration rows in cell [1]
# METHOD             three panels sharing one question: the two design variables the
#                    optimizer was allowed to move (wwr, shade_m) and the predicted
#                    performance; AMBER bars for baseline, BLUE for recommended; exact
#                    values and nominal 90% marginal conformal ranges are shown
# CHECKS/INTERPRET   The two point predictions differ, but interval overlap/non-overlap is
#                    explicitly NOT used as a hypothesis test or acceptance rule. Cell
#                    [7c] performs the independent post-optimization confirmation.

rec = {"wwr": result_1.x[0], "shade_m": result_1.x[1], "eui": result_1.fun}
base_interval = (baseline_pred - q_hat, baseline_pred + q_hat)
rec_interval = (rec["eui"] - q_hat, rec["eui"] + q_hat)
intervals_overlap = bool(rec_interval[1] >= base_interval[0])

print(f"predicted improvement: {improvement:.4f} kWh/m2/yr")
print(f"baseline nominal 90% marginal interval: {base_interval[0]:.4f}-"
      f"{base_interval[1]:.4f} kWh/m2/yr")
print(f"recommended nominal 90% marginal interval: {rec_interval[0]:.4f}-"
      f"{rec_interval[1]:.4f} kWh/m2/yr")
print(f"intervals overlap: {intervals_overlap} (descriptive only; not a decision test)")
assert q_hat > 0 and base_interval[0] < base_interval[1]
assert rec_interval[0] < rec_interval[1]

labels = ["baseline", "recommended"]
colors = [AMBER, BLUE]
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12.5, 5.5),
                                    gridspec_kw={"width_ratios": [1, 1, 1.5]})

def draw_variable_panel(ax, values, ylabel, panel_title, top):
    """One design variable, baseline (AMBER) then recommended (BLUE), values labeled."""
    ax.bar(labels, values, color=colors, width=0.6, edgecolor="white")
    for i, v in enumerate(values):
        ax.text(i, v + top * 0.03, f"{v:.2f}", ha="center", fontsize=11,
                color=colors[i], fontweight="bold")
    ax.set_ylim(0, top)
    ax.set_ylabel(ylabel)
    ax.set_title(panel_title, fontsize=11)
    ax.grid(alpha=0.3, color=GRAY_LT, axis="y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

draw_variable_panel(ax1, [BASELINE["wwr"], rec["wwr"]],
                    "wwr (window-to-wall ratio, dimensionless)",
                    "design variable 1: wwr", 0.72)
draw_variable_panel(ax2, [BASELINE["shade_m"], rec["shade_m"]],
                    "shade_m (overhang depth, m)",
                    "design variable 2: shade_m", 1.62)

ax1.annotate(f"{rec['wwr'] - BASELINE['wwr']:+.2f} "
             f"({(rec['wwr'] / BASELINE['wwr'] - 1) * 100:+.0f}%)",
             xy=(0.5, 0.60), ha="center", fontsize=10, color=GRAY)
ax2.annotate(f"{rec['shade_m'] - BASELINE['shade_m']:+.2f} m "
             f"({(rec['shade_m'] / BASELINE['shade_m'] - 1) * 100:+.0f}%)",
             xy=(0.5, 1.38), ha="center", fontsize=10, color=GRAY)

eui_values = [baseline_pred, rec["eui"]]
ax3.bar(labels, eui_values, color=colors, width=0.6, edgecolor="white",
        yerr=q_hat, capsize=10, error_kw=dict(ecolor=GRAY, elinewidth=1.8, capthick=1.8))
for i, v in enumerate(eui_values):
    ax3.text(i, v + q_hat + 0.9, f"{v:.4f}", ha="center", fontsize=11, color=colors[i],
             fontweight="bold")
ax3.hlines(baseline_pred, 0, 1.30, color=GRAY_LT, linestyle=":", linewidth=1.4)
ax3.annotate("", xy=(1.30, rec["eui"]), xytext=(1.30, baseline_pred),
             arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.0))
ax3.annotate(f"{-improvement:.4f} kWh/m2/yr\n({-improvement_pct:.2f}%)",
             xy=(1.30, baseline_pred + 2.0), ha="center", va="bottom",
             fontsize=10, color=GREEN, fontweight="bold")
ax3.annotate(f"error bars = nominal 90% split-conformal marginal ranges\n"
             f"(+/-{q_hat:.4f} kWh/m2/yr, calibrated before final testing)\n"
             f"overlap is not an acceptance test; run the reference simulation",
             xy=(-0.45, 47.5), ha="left", va="top", fontsize=9, color=GRAY,
             bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=GRAY_LT))
ax3.set_ylim(0, 48)
ax3.set_xlim(-0.6, 1.75)
ax3.set_ylabel("surrogate-predicted EUI (kWh/m2/yr)")
ax3.set_title("predicted performance, with calibrated ranges", fontsize=11)
ax3.grid(alpha=0.3, color=GRAY_LT, axis="y")
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)

fig.suptitle("Baseline vs. recommended: prediction ranges travel with the decision",
             fontsize=14)
fig.tight_layout()
fig.savefig("week15_decide_baseline_vs_recommended.png", dpi=150)
print("saved week15_decide_baseline_vs_recommended.png")
# WHY THIS MATTERS: RMSE is reported as a metric, while the interval comes from held-back
# calibration residuals. Neither interval overlap nor a ratio to RMSE decides whether the
# design works. The optimizer deliberately selected an extreme prediction, so cell [7c]
# checks that candidate with evidence the surrogate never saw.
# COMMON ERROR: calling q_hat a confidence interval for the mean, or claiming that a
# candidate is validated because two marginal intervals do not overlap. Split conformal
# offers marginal prediction coverage under exchangeability; adaptive optimization makes
# independent confirmation especially important.


# %% [7c] REQUIRED POST-OPTIMIZATION CONFIRMATION -- query evidence outside the surrogate
# QUESTION           Does the optimized candidate still beat the baseline when evaluated
#                    by an independent, higher-fidelity source that was never optimized?
# INPUTS/ASSUMPTIONS the baseline and recommended dictionaries; a deterministic course-only
#                    reference simulator standing in for EnergyPlus, measurement, or an
#                    instructor-provided high-fidelity run
# METHOD             evaluate both designs with the independent source, compare the true
#                    contrast, save an audit table, and refuse to call the candidate
#                    confirmed unless the external result is finite and improves on baseline
# CHECKS/INTERPRET   Expected reference results: baseline=31.3550, recommended=23.1700,
#                    confirmed reduction=8.1850 kWh/m2/yr. In a real project, replace this
#                    demonstration function with an actual simulation/measurement result.

def course_reference_simulation(design: dict) -> float:
    """Course-only high-fidelity oracle; replace with real independent evidence."""
    required = {"wwr", "shade_m", "glazing_shgc", "compactness", "orientation"}
    if set(design) != required:
        raise ValueError(f"reference design must contain exactly {sorted(required)}")
    wwr = float(design["wwr"])
    shade_m = float(design["shade_m"])
    shgc = float(design["glazing_shgc"])
    compactness = float(design["compactness"])
    values = np.array([wwr, shade_m, shgc, compactness], dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("reference design contains NaN or infinity")
    orientation_penalty = {"N": 0.8, "E": 0.5, "S": 0.0, "W": 0.7}
    if design["orientation"] not in orientation_penalty:
        raise ValueError("orientation must be one of N/E/S/W")
    return float(
        14.0
        + 17.0 * wwr
        - 2.8 * shade_m
        + 4.0 * shgc
        + 6.0 * compactness
        + 4.0 * (wwr - 0.40) ** 2
        + 1.2 * (shade_m - 0.70) ** 2
        + 3.0 * wwr * shgc
        + orientation_penalty[design["orientation"]]
    )

RECOMMENDED = {
    **BASELINE,
    "wwr": float(result_1.x[0]),
    "shade_m": float(result_1.x[1]),
}
baseline_reference = course_reference_simulation(BASELINE)
recommended_reference = course_reference_simulation(RECOMMENDED)
confirmed_improvement = baseline_reference - recommended_reference
recommended_in_interval = bool(
    rec_interval[0] <= recommended_reference <= rec_interval[1]
)

confirmation = pd.DataFrame(
    {
        "design": ["baseline", "recommended"],
        "surrogate_prediction_kwh_m2yr": [baseline_pred, rec["eui"]],
        "conformal_low_kwh_m2yr": [base_interval[0], rec_interval[0]],
        "conformal_high_kwh_m2yr": [base_interval[1], rec_interval[1]],
        "independent_reference_kwh_m2yr": [baseline_reference, recommended_reference],
    }
)
print("\nPOST-OPTIMIZATION CONFIRMATION (course demonstration):")
print(confirmation.round(4).to_string(index=False))
print(f"confirmed reduction: {confirmed_improvement:.4f} kWh/m2/yr")
print(f"recommended reference result inside nominal interval: {recommended_in_interval}")

if not np.isfinite([baseline_reference, recommended_reference]).all():
    raise RuntimeError("independent confirmation returned a non-finite result")
if confirmed_improvement <= 0:
    raise RuntimeError("independent evidence did not confirm improvement; do not recommend")
assert round(baseline_reference, 4) == 31.3550
assert round(recommended_reference, 4) == 23.1700
assert round(confirmed_improvement, 4) == 8.1850
confirmation.to_csv("week15_post_optimization_confirmation.csv", index=False)
print("saved week15_post_optimization_confirmation.csv")
print("Decision status: conditionally supported by the independent course reference run; "
      "real projects must substitute simulation, measurement, or expert-reviewed evidence.")


# %% [8] Conceptual note -- Track A's constraint pattern (no separate numeric demo)
# QUESTION           Track A students (go/no-go framing) do not have a continuous EUI
#                    surrogate to minimize -- they have Week 14's classifier. How does
#                    predict-optimize-decide apply to THEIR model instead?
# INPUTS/ASSUMPTIONS Week 14 Track A's LogisticRegression, its predict_proba(...)[:, 1]
#                    output (a probability-like score unless calibration was assessed),
#                    and its operating threshold selected on validation/out-of-fold rows
#                    from the false-positive-is-dangerous consequences argument
# METHOD             this cell is CONCEPTUAL ONLY, printed as a comment/explanation, not
#                    a second full numeric optimization -- keeping this single
#                    single 80-minute session focused, per the current pacing plan
# CHECKS/INTERPRET   Read the printed explanation; no numeric assertion needed for this
#                    cell.

track_a_pattern = """
Track A (go/no-go) integration pattern, described, not re-solved here:

  Track B (this demo):  minimize( surrogate_eui(wwr, shade_m) )       <- model IS the objective
  Track A (conceptual):  minimize( some_other_objective(wwr, shade_m) )
                          subject to:
                          classifier.predict_proba([[wwr, shade_m, shgc, compactness]])[:, 1]
                              >= FROZEN_VALIDATION_SELECTED_THRESHOLD
                                                                        <- model becomes a CONSTRAINT

  Same predict-optimize-decide pattern as this whole demo -- a fitted model feeding
  minimize -- just used to BOUND the feasible region (only designs the classifier is
  allowed by the frozen operating rule) instead of being the quantity minimized. Reuse
  Week 14 Track A's validation-selected threshold and report calibration status; never
  tune the threshold again on final-test or optimization outcomes.
"""
print(track_a_pattern)


# %% [9] Self-generated transfer check: a different fixed-feature scenario
# QUESTION           Does the optimizer's recommended (wwr, shade_m) -- and the SIZE of
#                    the improvement -- depend on which glazing_shgc/compactness values
#                    happen to be held fixed?
# INPUTS/ASSUMPTIONS a DIFFERENT scenario than the one worked through above:
#                    glazing_shgc=0.55, compactness=0.90 (baseline used 0.45 and 1.10)
# METHOD             rebuild the objective function with the new fixed values, re-run
#                    minimize from the same two starting guesses as DEMO 1/DEMO 2, and
#                    compare
# CHECKS/INTERPRET   Expected: the optimizer still lands on x=[0.20, 1.20] -- same
#                    corner of the bounded box -- because wwr and shade_m's coefficients
#                    do not depend on the other two features' values; only the absolute
#                    predicted EUI shifts by a constant offset. The IMPROVEMENT
#                    (baseline minus optimized, both under the SAME fixed scenario)
#                    should still come out to 7.8981 kWh/m2/yr -- identical to cell [7],
#                    because a constant offset cancels out of a difference.

ALT_SHGC = 0.55
ALT_COMPACTNESS = 0.90

def surrogate_eui_alt(design_vars: tuple) -> float:
    wwr, shade_m = design_vars
    row = row_from(wwr, shade_m, ALT_SHGC, ALT_COMPACTNESS)
    return surrogate.predict(row)[0]

alt_baseline_pred = surrogate_eui_alt((BASELINE["wwr"], BASELINE["shade_m"]))
alt_result_1 = minimize(surrogate_eui_alt, x0=(0.50, 0.20), bounds=BOUNDS)
alt_result_2 = minimize(surrogate_eui_alt, x0=(0.22, 1.10), bounds=BOUNDS)
alt_improvement = alt_baseline_pred - alt_result_1.fun

print("Transfer scenario: glazing_shgc=0.55, compactness=0.90 (not the baseline values)")
print("  alt baseline predicted EUI:", round(alt_baseline_pred, 4))
print("  alt optimized x:", alt_result_1.x.round(4), " predicted EUI:", round(alt_result_1.fun, 4))
print("  alt improvement:", round(alt_improvement, 4))

assert np.allclose(alt_result_1.x.round(2), [0.20, 1.20])
assert np.allclose(alt_result_1.x.round(4), alt_result_2.x.round(4)), "two starts should still agree"
assert round(alt_improvement, 4) == 7.8981, "improvement should be invariant to the fixed features here"
print("Confirmed: the recommended corner and the SIZE of the improvement transfer to a new scenario.")
