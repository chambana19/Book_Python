# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 13 studio · INSTRUCTOR SOLUTIONS
Evaluated prediction (regression): baseline, metrics, leakage audit
Syracuse University · School of Architecture · Fall 2026
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


# %% [1] Load the Radley Hall portfolio and confirm its shape
# QUESTION           Load radley_portfolio_envelope.csv and confirm it has the size you
#                    expect: 140 explored design variants, one row each.
# INPUTS/ASSUMPTIONS DATA_PATH points to data/radley_portfolio_envelope.csv; sep="," is
#                    the column separator, named explicitly as a keyword argument
# METHOD             pd.read_csv(DATA_PATH, sep=","), then print portfolio.shape,
#                    portfolio.dtypes, and portfolio.head()
# CHECKS/INTERPRET   Expected shape: (140, 9). eui_kwh_m2yr is the TARGET (the number we
#                    predict); est_annual_cost_index is reporting-only -- never a feature
#                    (see cell [9]).

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = Path("data") / "radley_portfolio_envelope.csv"
portfolio = pd.read_csv(DATA_PATH, sep=",")
print(portfolio.shape)
print(portfolio.dtypes)
print(portfolio.head())
# WHY THIS MATTERS: "feature, defined" -- a FEATURE is an input column a model is allowed
# to use to predict (here: wwr, shade_m, glazing_shgc). "target, defined" -- the TARGET is
# the column being predicted (here: eui_kwh_m2yr, kWh/m2/yr). Radley Hall's design team
# explored these 140 envelope variants during schematic design; this is fictional data,
# same convention as every prior week's Radley Hall material.


# %% [2] Verify the split
# QUESTION           train_test_split claims to hold out 25% of the data for testing --
#                    does it actually, and does any row leak between the two sets?
# INPUTS/ASSUMPTIONS FEATURES3 = [wwr, shade_m, glazing_shgc] (compactness and
#                    orientation are deliberately left out this week); target eui_kwh_m2yr;
#                    test_size=0.25, random_state=42 (fixed seed, same as every split
#                    this block, for reproducibility)
# METHOD             call train_test_split, print the four resulting shapes, then verify
#                    with two asserts: sizes sum to 140, and no row index appears in both
#                    the train set and the test set
# CHECKS/INTERPRET   Expected: X_train (105, 3), X_test (35, 3), y_train (105,),
#                    y_test (35,). Both asserts must pass silently.

FEATURES3 = ["wwr", "shade_m", "glazing_shgc"]
X = portfolio[FEATURES3]
y = portfolio["eui_kwh_m2yr"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
print("X_train:", X_train.shape, " X_test:", X_test.shape)
print("y_train:", y_train.shape, " y_test:", y_test.shape)

assert len(X_train) + len(X_test) == len(portfolio) == 140
assert set(X_train.index).isdisjoint(set(X_test.index))
print("Split verified: 105 train + 35 test = 140, and no row is in both sets.")
# WHY THIS MATTERS: "set / isdisjoint(), defined" -- a set is a collection with no
# duplicates and no order: {1,2,3}.isdisjoint({4,5}) is True (nothing shared),
# {1,2,3}.isdisjoint({3,4}) is False. Converting each index to a set and calling
# .isdisjoint() asks exactly one question: does ANY row-index number appear in both
# train and test?
# WHY THIS MATTERS: "train_test_split, recalled" -- it randomly holds out a fraction of
# rows (test_size=0.25 here) so the model is EVALUATED on rows it never saw while
# fitting. random_state=42 makes the "random" split reproducible: everyone in this course
# gets the exact same 105/35 split, every time the cell reruns.
# COMMON ERROR: checking only the printed shapes and stopping there. Two sets can each
# have the right SIZE while still overlapping if code elsewhere accidentally re-samples
# or re-indexes the data -- the isdisjoint() assert is what actually proves no leakage
# between train and test rows (a DIFFERENT kind of leakage than cell [9]'s feature
# leakage -- this one is about which ROWS a model sees, not which COLUMNS).


# %% [3] One documented helper, then the naive baseline
# QUESTION           Four different models in this handout (baseline, 3-feature,
#                    AI-drafted, fixed) all need the same three metrics. Write the scoring
#                    ONCE, then answer: how good is "just guess the average"?
# INPUTS/ASSUMPTIONS X_train/X_test/y_train/y_test from cell [2]
# METHOD             define report_metrics(y_true, y_pred, label) -> dict, following the
#                    course convention required on every function since Week 4 (one-line
#                    docstring in triple quotes + type hints); then
#                    DummyRegressor(strategy="mean").fit(X_train, y_train), predict on
#                    X_test, and score through the helper
# CHECKS/INTERPRET   Expected: constant prediction 28.0836 (the TRAINING mean) for every
#                    test row; MAE=2.8906, RMSE=3.8154, R2 approx 0.0 (about -0.00003).
#                    The helper prints R2 to 5 decimals on purpose -- 4 decimals would
#                    flatten -0.00003 to -0.0000 and hide the point.


def report_metrics(y_true, y_pred, label: str) -> dict:
    """Print and return MAE, RMSE and R2 for one set of predictions."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    line = f"MAE={mae:.4f} RMSE={rmse:.4f} R2={r2:.5f}"
    print(label + ":", line)
    return {"MAE": mae, "RMSE": rmse, "R2": r2}


baseline = DummyRegressor(strategy="mean")
baseline.fit(X_train, y_train)
pred_baseline = baseline.predict(X_test)

print("baseline predicts every row as:", round(baseline.constant_[0][0], 4))
base = report_metrics(y_test, pred_baseline, "baseline")

assert round(base["MAE"], 4) == 2.8906
assert round(base["RMSE"], 4) == 3.8154
# WHY THIS MATTERS: "docstring + type hints, recalled" -- label: str states that label must
# be text, -> dict states that a dictionary comes back, and the triple-quoted first line
# says what the function does. This is the same convention every function in Project 2
# must follow, and it is why the three later cells can reuse this function without anyone
# re-reading its body.
# WHY THIS MATTERS: writing the scoring arithmetic once, instead of four times, removes
# four chances to score two models differently and then compare them as if they matched.
# WHY THIS MATTERS: "naive baseline, defined" -- a model that always predicts the TRAINING
# mean, with no design variables at all. R2=0.0 is not "a bad score" here -- it is the
# DEFINITION of "no better than guessing the average." Every real model this week is
# judged against this number, not against zero error.
# COMMON ERROR: computing the baseline's R2 and being surprised it isn't exactly 0.0.
# DummyRegressor is fit on the TRAINING mean, then scored against the TEST set's own
# mean-centered variance -- the two are close but not numerically identical, so a tiny
# negative R2 (about -0.00003) is the expected, correct answer, not a bug.


# %% [4] AI-scaffolded LinearRegression -- three honest design features
# QUESTION           Scaffolded quickly with an AI coding assistant: does a real
#                    3-feature regression beat the naive baseline?
# INPUTS/ASSUMPTIONS X_train/X_test/y_train/y_test from cell [2] (FEATURES3 only --
#                    compactness and orientation are NOT included yet, on purpose;
#                    Week 14 adds compactness back in as its own studio task)
# METHOD             LinearRegression().fit(X_train, y_train); predict on X_test; score
#                    through the SAME report_metrics helper as cell [3], so the two models
#                    are guaranteed to be measured identically
# CHECKS/INTERPRET   Expected coef_ (wwr, shade_m, glazing_shgc) = [17.6545, -3.3915,
#                    3.4181], intercept_=21.6211, MAE=2.2680, RMSE=2.7146, R2=0.49374
#                    (0.4937 rounded to 4 decimals, the way the slides write it).

model3 = LinearRegression()
model3.fit(X_train, y_train)
pred_model3 = model3.predict(X_test)

print("coef_ [wwr, shade_m, glazing_shgc]:", model3.coef_.round(4))
print("intercept_:", round(model3.intercept_, 4))
m3 = report_metrics(y_test, pred_model3, "3-feature")

assert round(m3["MAE"], 4) == 2.2680
assert round(m3["R2"], 4) == 0.4937
# WHY THIS MATTERS: the SAME helper scored both models, so "MAE dropped from 2.8906 to
# 2.2680" is an exact comparison, not an approximate one. Two hand-typed metric blocks
# that differ by a single argument (say, squared=True somewhere) would silently produce
# two numbers that cannot be compared at all.
# WHY THIS MATTERS: this is exactly the kind of pipeline an AI assistant scaffolds in
# seconds -- import, split (already done), .fit(), .predict(), three metric calls. The
# plan's intent is that you spend the TIME saved on cells [5]-[10]: does it beat the
# baseline, where does it fail, and is every feature legitimate. Every coefficient's
# SIGN is physically sensible: more window area (wwr) raises EUI (+17.65), more shading
# (shade_m) lowers it (-3.39), a higher solar heat gain glazing (glazing_shgc) raises it
# (+3.42).
# COMMON ERROR: reporting R2=0.4937 as "the model failed" because it is far from 1.0. R2
# near 0.5 with real, physically-sensible coefficients, beating a naive baseline of
# R2 approx 0, is a genuinely useful model -- it is honestly imperfect because two real
# effects (compactness, orientation) are not in it yet, not because linear regression
# is broken.


# %% [5] Baseline vs. model: the comparison table the studio task requires
# QUESTION           By how much does the 3-feature model beat the naive baseline?
# INPUTS/ASSUMPTIONS the base dictionary from cell [3] and the m3 dictionary from cell
#                    [4] -- both returned by the same report_metrics helper
# METHOD             build a small comparison DataFrame straight out of the two
#                    dictionaries; compute the MAE improvement as a percentage:
#                    (base["MAE"] - m3["MAE"]) / base["MAE"] * 100
# CHECKS/INTERPRET   Expected: MAE improvement approx 21.5%; R2 rises from approx 0.0 to
#                    0.4937. The model beats the baseline -- if it had NOT, that would be
#                    equally real and equally worth reporting.

comparison = pd.DataFrame(
    {
        "MAE": [base["MAE"], m3["MAE"]],
        "RMSE": [base["RMSE"], m3["RMSE"]],
        "R2": [base["R2"], m3["R2"]],
    },
    index=["naive baseline (mean)", "3-feature LinearRegression"],
)
mae_improvement_pct = (base["MAE"] - m3["MAE"]) / base["MAE"] * 100
print(comparison.round(4))
print(f"MAE improvement over baseline: {mae_improvement_pct:.1f}%")

assert m3["MAE"] < base["MAE"], "model did not beat the naive baseline on MAE"
# WHY THIS MATTERS: "beat the baseline" is not a figure of speech -- it is this exact
# assert. A model that cannot pass it has told you something real (the features you
# chose carry no signal), and that is a legitimate, reportable studio finding, not a
# failure to hide.
# COMMON ERROR: comparing R2 values only and ignoring MAE/RMSE. R2 is a single-number
# summary of the SAME comparison MAE/RMSE already show in the units EUI is actually
# measured in (kWh/m2/yr) -- report all three, since a client or reviewer thinks in the
# original units, not in R2.


# %% [6] Calculate a metric manually -- MAE from its own definition
# QUESTION           MAE is defined as "the average of the absolute residuals." Does that
#                    formula, computed with plain arithmetic (no sklearn function call),
#                    actually reproduce the sklearn MAE from cell [4]?
# INPUTS/ASSUMPTIONS X_test/y_test from cell [2]; pred_model3 from cell [4]
# METHOD             build a small comparison table of variant_id/actual/predicted/
#                    residual; hand-add the first 8 printed rows on paper or a calculator
#                    and divide by 8 (a genuinely by-hand moment); THEN, in code, compute
#                    manual_mae = mean(|residual|) over the FULL 35-row test set using
#                    only np.abs/np.mean (no mean_absolute_error call) and assert it
#                    matches the sklearn MAE to 2 decimals
# CHECKS/INTERPRET   The first 8 printed rows' hand-computed mean should be approximately
#                    1.82 (a smaller subset, not the full-sample MAE). manual_mae over
#                    all 35 rows must equal 2.2680, matching cell [4] exactly.

residual_table = pd.DataFrame(
    {
        "variant_id": portfolio.loc[X_test.index, "variant_id"].values,
        "actual": y_test.values,
        "predicted": pred_model3.round(4),
        "residual": (y_test.values - pred_model3).round(4),
    }
)
print(residual_table.head(8))

by_hand_subset = residual_table.head(8)["residual"]
by_hand_mae = by_hand_subset.abs().sum() / len(by_hand_subset)
print("hand-added mean |residual| of the first 8 printed rows:", round(by_hand_mae, 4))

manual_mae = np.mean(np.abs(residual_table["residual"]))
print("manual MAE (full 35-row test set, formula only, no sklearn call):",
      round(manual_mae, 4))
print("sklearn MAE from cell [4]:", round(m3["MAE"], 4))

assert round(manual_mae, 2) == round(m3["MAE"], 2)
print("Manual MAE matches sklearn's mean_absolute_error to 2 decimals.")
# WHY THIS MATTERS: MAE is not a mysterious sklearn output -- it is "add up how wrong
# every prediction was (ignoring direction), divide by how many predictions there were."
# Computing it from the definition, on both a small hand-countable subset AND the full
# test set, is what makes that concrete rather than a black box.
# COMMON ERROR: forgetting the absolute value and computing mean(residual) instead of
# mean(|residual|). Positive and negative residuals would then cancel out, hiding real
# error -- this is exactly why RMSE also squares first (cell [7]'s worst residual is
# NEGATIVE; without abs()/squaring it would partially cancel smaller positive residuals
# elsewhere in the sum).


# %% [7] Diagnose the largest residual
# QUESTION           Which test-set design does this model miss the worst -- and why,
#                    specifically, does it miss that one so badly?
# INPUTS/ASSUMPTIONS residual_table from cell [6]; portfolio's compactness and
#                    orientation columns (NOT used as features this week, but still
#                    readable for diagnosis)
# METHOD             sort residual_table by |residual| descending; look up the worst
#                    row's compactness and orientation from portfolio (joined by
#                    variant_id); reason about what the 3-feature model cannot see
# CHECKS/INTERPRET   Expected worst residual: variant V037, actual=20.43,
#                    predicted approx 26.77, residual approx -6.34 (the model
#                    OVER-predicts -- thinks the design performs worse than it does).

residual_table_sorted = residual_table.reindex(
    residual_table["residual"].abs().sort_values(ascending=False).index
)
print(residual_table_sorted.head(3))

worst_id = residual_table_sorted.iloc[0]["variant_id"]
worst_row = portfolio.loc[portfolio["variant_id"] == worst_id].iloc[0]
print(worst_row[["variant_id", "wwr", "shade_m", "glazing_shgc",
                  "compactness", "orientation"]])

diagnosis_v037 = (
    "V037's model over-predicts EUI by about 6.34 kWh/m2/yr -- the single worst miss in "
    "the test set. Its shade_m is 0.917, among the deepest overhangs in the whole "
    "portfolio, and its orientation is North, the coolest/lowest-gain offset in the "
    "generating process. Both are REAL effects: deep shading and a north orientation "
    "both genuinely lower EUI. The 3-feature model sees shade_m (so it captures PART of "
    "the shading benefit) but cannot see orientation at all -- it is not a numeric "
    "feature in this model yet -- so it under-credits how well this specific design "
    "actually performs. This is a genuine, honest gap, not a coding mistake."
)
print(diagnosis_v037)
# WHY THIS MATTERS: "reindex(), defined" -- reindex() here simply reorders an existing
# DataFrame's rows into a NEW row order (here, largest-to-smallest |residual|); it does
# not add, remove, or recompute any values -- a less common use than reindex()'s more
# typical job of aligning to new or missing labels.
# WHY THIS MATTERS: "residual, defined" -- actual minus predicted, per row. A large
# residual is not automatically a bug in the code; here it is evidence of a real,
# nameable missing feature (orientation), which is exactly what motivates Week 14's
# refinement. Compare: cell [9]'s problem is the OPPOSITE failure mode -- a feature that
# should never have been included at all.
# COMMON ERROR: diagnosing the worst residual by staring at wwr/shade_m/glazing_shgc
# alone (the three features actually in the model) and concluding "nothing explains
# this." The explanation lives in the columns the model was NOT given -- you have to go
# back to the full portfolio table, not just the model's own inputs, to find it.


# %% [7b] Predicted vs. actual, with the 1:1 line
# QUESTION           Distance from the 1:1 line IS the prediction error. Do the 35 held-out
#                    predictions sit on that line, or drift off it at one end of the range?
# INPUTS/ASSUMPTIONS residual_table from cell [6]; m3["R2"] and m3["MAE"] from cell [4];
#                    the course figure palette defined below and reused in cell [8]
# METHOD             draw the GRAY dashed 1:1 diagonal across the FULL data range first,
#                    then scatter actual (x) against predicted (y) on top of it; print, then
#                    annotate, R2, MAE, and the mean residual at each end of the range;
#                    label V037, the worst miss diagnosed in cell [7]
# CHECKS/INTERPRET   Expected: the 1:1 line spans 19.25 to 38.19 kWh/m2/yr; R2=0.4937 and
#                    MAE=2.2680 (cell [4]'s own numbers); mean residual of the 12
#                    LOWEST-EUI test designs = -2.7634 (predicted too high, so those points
#                    sit ABOVE the line), of the 12 HIGHEST-EUI designs = +1.0754
#                    (predicted too low, BELOW the line). Saves week13_pred_vs_actual.png.

# The course figure palette -- these five hex values are used in every ARC 500 figure.
BLUE = "#2E74B5"   # the main series
AMBER = "#B5731A"  # the flagged case / a warning
GREEN = "#2E7D5B"  # the confirmed reference value
GRAY = "#5A5F66"   # reference lines and annotation text

low_end_bias = residual_table.nsmallest(12, "actual")["residual"].mean()
high_end_bias = residual_table.nlargest(12, "actual")["residual"].mean()
line_lo = min(residual_table["actual"].min(), residual_table["predicted"].min()) - 1
line_hi = max(residual_table["actual"].max(), residual_table["predicted"].max()) + 1

print("1:1 line spans:", round(line_lo, 2), "to", round(line_hi, 2), "kWh/m2/yr")
print("mean residual, 12 lowest-EUI test designs:", round(low_end_bias, 4))
print("mean residual, 12 highest-EUI test designs:", round(high_end_bias, 4))

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot([line_lo, line_hi], [line_lo, line_hi], color=GRAY, linestyle="--", linewidth=1.6,
        label="perfect prediction (1:1 line)")
ax.scatter(residual_table["actual"], residual_table["predicted"], color=BLUE, s=42,
           alpha=0.85, label="35 held-out test designs")

v037 = residual_table.loc[residual_table["variant_id"] == "V037"].iloc[0]
ax.annotate(f"V037: actual {v037['actual']:.2f}, predicted {v037['predicted']:.2f}\n"
            f"= {abs(v037['residual']):.2f} kWh/m2/yr ABOVE the 1:1 line",
            xy=(v037["actual"], v037["predicted"]),
            xytext=(line_lo + 0.7, line_hi - 4.0),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4),
            fontsize=9.5, color=AMBER)
ax.annotate(f"R2 = {m3['R2']:.4f}   MAE = {m3['MAE']:.4f} kWh/m2/yr\n"
            f"12 lowest-EUI: mean residual {low_end_bias:+.2f} (over-predicted)\n"
            f"12 highest-EUI: mean residual {high_end_bias:+.2f} (under-predicted)",
            xy=(0.03, 0.98), xycoords="axes fraction", va="top", ha="left",
            fontsize=9, color=GRAY)

ax.set_title("Do the 35 held-out predictions land on the 1:1 line, or drift off it at one end?")
ax.set_xlabel("actual eui_kwh_m2yr (kWh/m2/yr)")
ax.set_ylabel("predicted eui_kwh_m2yr (kWh/m2/yr)")
ax.set_xlim(line_lo, line_hi)
ax.set_ylim(line_lo, line_hi)
ax.set_aspect("equal")  # equal scales, so the 1:1 line really is a 45-degree diagonal
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig("week13_pred_vs_actual.png", dpi=150)
print("saved week13_pred_vs_actual.png")
# WHY THIS MATTERS: the VERTICAL distance from a point to the dashed line is that design's
# residual -- a point sitting ON the line was predicted exactly. This is the same MAE=2.2680
# from cell [4], now drawn per design instead of averaged into one number.
# WHY THIS MATTERS: R2=0.4937 is one number for all 35 designs at once, so it cannot tell
# you WHERE the model is wrong. The picture can: at the low-EUI end the points sit
# systematically ABOVE the line (mean residual -2.76 -- the model over-predicts the
# best-performing designs, exactly V037's failure), and at the high-EUI end they sit BELOW
# it (+1.08 -- it under-predicts the worst performers). That range-dependent bias is
# invisible in R2 and MAE, and it is the honest reason a client should not read a single
# predicted EUI as equally trustworthy everywhere.
# COMMON ERROR: drawing the diagonal only across the PREDICTED range (23.82-33.33) instead
# of the full data range. The line then stops short of the lowest and highest actual
# designs -- precisely the two ends where the bias above lives -- so the figure hides the
# very pattern it exists to show.
# COMMON ERROR: fitting a second regression line through the scatter and reading it as the
# 1:1 line. The 1:1 line is not fitted to anything: it is y = x, the line every point would
# sit on if the model were perfect.


# %% [8] Residual plot: the shape test
# QUESTION           Do the model's errors look like random scatter around zero, or do they
#                    form a SHAPE -- a funnel or a curve?
# INPUTS/ASSUMPTIONS residual_table from cell [6]; residual_table_sorted from cell [7];
#                    m3["MAE"]/m3["RMSE"] from cell [4]; the palette from cell [7b]
# METHOD             fig, ax = plt.subplots(figsize=(9, 5.5)); a GREEN dashed reference line
#                    at residual=0; scatter predicted (x) against residual (y); label the
#                    largest-|residual| variant by its identifier, reusing cell [7]'s sort
#                    rather than re-sorting
# CHECKS/INTERPRET   Expected: 16 of the 35 residuals above the zero line, 19 below;
#                    residuals span -6.3373 to +4.2250 kWh/m2/yr; the labelled worst miss is
#                    V037, at predicted 26.7673, residual -6.3373. Saves
#                    week13_residual_plot.png.

worst_row = residual_table_sorted.iloc[0]  # cell [7] already sorted by |residual|
above_zero = (residual_table["residual"] > 0).sum()
below_zero = (residual_table["residual"] < 0).sum()

print("residuals above the zero line:", above_zero, " below:", below_zero)
print("residual range:", round(residual_table["residual"].min(), 4), "to",
      round(residual_table["residual"].max(), 4), "kWh/m2/yr")
print("largest miss:", worst_row["variant_id"], "at predicted",
      round(worst_row["predicted"], 4), "residual", round(worst_row["residual"], 4))

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.axhline(0, color=GREEN, linestyle="--", linewidth=1.6,
           label="zero error (residual = 0)")
ax.scatter(residual_table["predicted"], residual_table["residual"], color=BLUE, s=42,
           alpha=0.85, label="35 held-out test designs")

ax.annotate(f"{worst_row['variant_id']}: residual {worst_row['residual']:.2f} kWh/m2/yr\n"
            f"(largest miss in the test set)",
            xy=(worst_row["predicted"], worst_row["residual"]),
            xytext=(worst_row["predicted"] + 1.8, worst_row["residual"] - 0.6),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4),
            fontsize=9.5, color=AMBER)
ax.annotate(f"MAE = {m3['MAE']:.4f} kWh/m2/yr   RMSE = {m3['RMSE']:.4f} kWh/m2/yr\n"
            f"{above_zero} points above the line, {below_zero} below -- no funnel, no curve",
            xy=(0.03, 0.03), xycoords="axes fraction", va="bottom", ha="left",
            fontsize=9.5, color=GRAY)

ax.set_ylim(-8.2, 6.4)
ax.set_title("Are the errors random scatter around zero, or do they form a shape?")
ax.set_xlabel("predicted eui_kwh_m2yr (kWh/m2/yr)")
ax.set_ylabel("residual, actual - predicted (kWh/m2/yr)")
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig("week13_residual_plot.png", dpi=150)
print("saved week13_residual_plot.png")
# WHY THIS MATTERS: this is the SHAPE TEST, and it is a different question from "is MAE
# small?" Random scatter above and below zero, with roughly constant spread and no slope --
# what this figure shows, 16 above and 19 below -- means the linear model's assumptions
# hold: its error does not grow with the predicted value. A FUNNEL (spread widening to the
# right) or a CURVE (residuals arcing above zero in the middle and below at both ends)
# would mean they do NOT hold, no matter how good MAE=2.2680 looked, because the model's
# shape itself would be wrong rather than merely imprecise. This is the same healthy-vs-
# funnel comparison from Meeting A, now built from your own 35 residuals.
# WHY THIS MATTERS: individual outliers are not the same as a bad shape. V037 (-6.3373)
# sits far below the line while the overall scatter stays healthy -- one nameable missing
# feature (orientation, cell [7]), not a broken model.
# COMMON ERROR: reading this plot as "does the model work" and stopping there -- that is
# cell [7b]'s job, near the 1:1 line. Predicted-vs-residual exists to reveal PATTERNS in
# the error: slope, funnel, curve.
# COMMON ERROR: plotting residual against ACTUAL instead of against PREDICTED. Residuals
# are correlated with actual by construction (actual appears in both axes), so that version
# always tilts upward and looks like a pattern even when nothing is wrong.


# %% [9] AI-drafted leakage audit -- find the bug
# QUESTION           An AI assistant drafted a "better" version of this same regression,
#                    adding a fourth feature: est_annual_cost_index, reasoning that "cost
#                    is a design-relevant variable too." Should you accept it?
# INPUTS/ASSUMPTIONS FEATURES_LEAK = [wwr, shade_m, glazing_shgc, est_annual_cost_index];
#                    same split settings (test_size=0.25, random_state=42)
# METHOD             refit LinearRegression on FEATURES_LEAK; compare its R2 against
#                    cell [4]'s honest R2=0.4937; compute the correlation between
#                    est_annual_cost_index and the target itself
# CHECKS/INTERPRET   Expected leak-version coef_=[0.3310, 0.0374, 0.3054, 7.1264],
#                    MAE=0.2852, RMSE=0.3342, R2=0.9923 -- suspiciously close to 1.0 for a
#                    noisy, real-world-style target. corr(est_annual_cost_index,
#                    eui_kwh_m2yr) = 0.995574.

# AI ASSISTANT'S DRAFT, AS RECEIVED (paraphrased prompt/response):
# "Add est_annual_cost_index as a fourth feature -- cost is a design-relevant variable
#  too, and including it should only help the model."
FEATURES_LEAK = ["wwr", "shade_m", "glazing_shgc", "est_annual_cost_index"]
X_leak = portfolio[FEATURES_LEAK]
Xtr_leak, Xte_leak, ytr_leak, yte_leak = train_test_split(
    X_leak, y, test_size=0.25, random_state=42
)
model_leak = LinearRegression()
model_leak.fit(Xtr_leak, ytr_leak)
pred_leak = model_leak.predict(Xte_leak)

print("leak-version coef_ [wwr, shade_m, glazing_shgc, est_annual_cost_index]:",
      model_leak.coef_.round(4))
leak = report_metrics(yte_leak, pred_leak, "leaking")

corr_leak_target = portfolio["est_annual_cost_index"].corr(portfolio["eui_kwh_m2yr"])
print("corr(est_annual_cost_index, eui_kwh_m2yr):", round(corr_leak_target, 6))


def leakage_scan(features: list, target: str) -> list:
    """List features whose correlation with the target is suspiciously high."""
    suspects = []
    for col in features:
        r = portfolio[col].corr(portfolio[target])
        print(f"  {col:<22} corr={r:+.4f}")
        if abs(r) > 0.9:
            suspects.append(col)
    return suspects


TARGET = "eui_kwh_m2yr"

print("leakage scan -- the AI-drafted 4-feature list:")
suspects = leakage_scan(FEATURES_LEAK, TARGET)
print("suspects:", suspects)
for col in suspects:
    print("DROP:", col, "- derived from the target, not measured independently")

print("leakage scan -- the honest 3-feature list:")
clean = leakage_scan(FEATURES3, TARGET)
print("suspects:", clean)

assert suspects == ["est_annual_cost_index"]
assert clean == []
# WHY THIS MATTERS: the one-off correlation check above becomes a REUSABLE tool the moment
# it is wrapped in a documented function. Run leakage_scan on your own Project 2 feature
# list before you fit anything -- it costs one line and catches the single most expensive
# mistake in this whole block. The 0.9 cutoff is a stated judgement, not a law: no honest
# design variable in this portfolio comes close to it (wwr +0.5740, shade_m -0.3481,
# glazing_shgc +0.0128), while est_annual_cost_index sits at +0.9956.
# COMMON ERROR: treating a HIGH correlation with the target as automatically good news --
# "this feature is very predictive!" For an independently measured design variable it
# would be; for a column computed FROM the target it is the signature of leakage. The
# question is never how strong the correlation is, it is where the column came from.

leakage_diagnosis = (
    "R2=0.9923 is the 'too good to be true' signal itself, before reading a single line "
    "of code: no real, noisy, simulated building-performance target is this predictable "
    "from four envelope variables. The correlation check confirms it -- "
    "est_annual_cost_index correlates with the TARGET at 0.995574, because it is "
    "DERIVED from the target (est_annual_cost_index = eui_kwh_m2yr * 0.14 + small "
    "noise). It is a reporting-only OUTPUT column, dressed up as a predictive feature: "
    "the model is not predicting EUI from design variables at all, it is mostly just "
    "reading the answer back off a rescaled copy of itself. This is DATA LEAKAGE: "
    "information that would not be available at prediction time (you cannot know the "
    "annual cost of a design before you know its EUI) has leaked into the feature set."
)
print(leakage_diagnosis)
# WHY THIS MATTERS: "correlation, defined" -- correlation ranges from -1 to 1 and measures
# how closely two variables move together; 0.995574 means these two columns move almost
# in lockstep -- near-perfect, which is itself suspicious for two supposedly independent
# measurements.
# WHY THIS MATTERS: "data leakage, defined" -- when a feature carries information that is
# derived from, or only available after, the target itself, so the model's apparent
# accuracy is inflated by information it should never have had at prediction time. THE
# most reliable leakage detector is not reading code line by line looking for a bug -- it
# is being suspicious of a suspiciously perfect metric FIRST, then checking correlations
# to confirm.
# COMMON ERROR: accepting the AI's stated reasoning ("cost is a design-relevant variable
# too") at face value because it sounds plausible. Plausible-SOUNDING is not the same as
# legitimate -- est_annual_cost_index is a real column in this dataset, but it is a
# reporting output, never a predictor, and no restating of "cost matters to design"
# changes that.


# %% [10] THE FIX -- remove the leaking feature, refit, confirm
# QUESTION           Once est_annual_cost_index is removed, does the model return to the
#                    honest cell [4] numbers?
# INPUTS/ASSUMPTIONS FEATURES3 from cell [2]; the m3 metrics dictionary from
#                    cell [4]
# METHOD             refit LinearRegression on FEATURES3 only (dropping
#                    est_annual_cost_index entirely -- not just down-weighting it);
#                    assert the resulting metrics equal cell [4]'s honest numbers
# CHECKS/INTERPRET   Fixed-model MAE/RMSE/R2 must equal cell [4]'s 2.2680/2.7146/0.4937
#                    exactly (same features, same split -- it IS the same model).

FEATURES_FIXED = [f for f in FEATURES3]  # est_annual_cost_index deliberately excluded
assert "est_annual_cost_index" not in FEATURES_FIXED

X_fixed = portfolio[FEATURES_FIXED]
Xtr_fixed, Xte_fixed, ytr_fixed, yte_fixed = train_test_split(
    X_fixed, y, test_size=0.25, random_state=42
)
model_fixed = LinearRegression()
model_fixed.fit(Xtr_fixed, ytr_fixed)
pred_fixed = model_fixed.predict(Xte_fixed)

fixed = report_metrics(yte_fixed, pred_fixed, "fixed")
assert leakage_scan(FEATURES_FIXED, TARGET) == []

assert round(fixed["MAE"], 4) == round(m3["MAE"], 4)
assert round(fixed["RMSE"], 4) == round(m3["RMSE"], 4)
assert round(fixed["R2"], 4) == round(m3["R2"], 4)
print("Fix confirmed: metrics return exactly to the honest 3-feature numbers.")

fix_explanation = (
    "THE FIX is to drop est_annual_cost_index from the feature list entirely, not to "
    "keep it with a smaller weight or 'trust it less.' It is a legitimate column in "
    "this dataset for REPORTING utility-cost estimates to a client, but it must never "
    "be a predictive feature, because it is computed FROM the target. Once removed, "
    "the model's honest MAE/RMSE/R2 (2.2680 / 2.7146 / 0.4937) are exactly what cell "
    "[4] already reported -- this IS that same model, confirmed by refitting it "
    "independently here."
)
print(fix_explanation)
# WHY THIS MATTERS: this is the entire graded studio task in one cell: find the leakage
# bug, then FIX it by removing the feature, then PROVE the fix by showing the metrics
# return to the honest, defensible numbers -- not just asserting the fix "should" work.
# COMMON ERROR: "fixing" leakage by keeping the feature but noting its coefficient is
# large in a code comment. A flagged bug is still a bug -- the feature must be removed
# from the feature list, refit, and re-evaluated, exactly as done here.


# %% [11] Self-check: prove the audit generalizes -- a different metric, a different row
# QUESTION           Does this studio's method hold up on a metric and a variant you have
#                    not hand-checked yet -- not just MAE and V037, used live above?
# INPUTS/ASSUMPTIONS residual_table_sorted from cell [7]; m3["RMSE"] from cell [4];
#                    FEATURES_FIXED from cell [10]
# METHOD             manually compute RMSE (not MAE) over the full 35-row test set using
#                    only np.sqrt/np.mean (no sklearn call); identify the SECOND-worst
#                    residual (not V037); write 2-4 assert statements
# CHECKS/INTERPRET   If every assertion holds, the cell prints its confirmation message
#                    with no error. Expected second-worst variant: V133, residual
#                    approx -4.89.

manual_rmse = np.sqrt(np.mean(residual_table["residual"] ** 2))
second_worst = residual_table_sorted.iloc[1]

assert round(manual_rmse, 2) == round(m3["RMSE"], 2)
assert second_worst["variant_id"] == "V133"
assert round(second_worst["residual"], 2) == -4.89
assert "est_annual_cost_index" not in FEATURES_FIXED

print("Self-check passed: manual RMSE =", round(manual_rmse, 4),
      "| second-worst residual =", second_worst["variant_id"],
      round(second_worst["residual"], 2))
# WHY THIS MATTERS: cells [6] and [7] worked through MAE and V037 live, with the answer
# already known. Recomputing a DIFFERENT metric (RMSE, which squares before averaging,
# so it penalizes large residuals more than MAE does) on a DIFFERENT row (V133, the
# second-worst miss) proves the method -- not just the one memorized answer -- actually
# generalizes. This is this week's required transfer check.


# %% [12] AI-use record and exit reflection
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished audit in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five
#                    required points listed below
# METHOD             fill in the AI-use record honestly, then write the exit
#                    explanation addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing this
#                    audit cannot tell you.

ai_use_record = """
Tool/model: Example assistant
Prompt: Fit a LinearRegression model predicting eui_kwh_m2yr from the design variables
in radley_portfolio_envelope.csv, including any variable that seems design-relevant.
Suggestion received: A 4-feature model adding est_annual_cost_index alongside wwr,
shade_m, and glazing_shgc, reasoning that "cost is a design-relevant variable too."
What I accepted: The overall pipeline shape -- split, fit, predict, score -- and the
three legitimate features (wwr, shade_m, glazing_shgc).
What I modified and why: Removed est_annual_cost_index entirely after the R2=0.9923
result and the 0.995574 correlation check showed it is derived from the target, not an
independent design input.
What I rejected and why: The claim that est_annual_cost_index is "design-relevant" in
the way wwr/shade_m/glazing_shgc are -- it is a reporting output computed FROM
eui_kwh_m2yr, so using it as a predictor is data leakage, not a design insight.
How I tested it: Refit the model with the feature removed and asserted the metrics
returned exactly to the honest 3-feature numbers (cell [10]); also hand-verified MAE
and RMSE from their definitions and diagnosed the two largest test-set residuals.
One limitation I found: This 3-feature model does not yet include compactness or
orientation, both of which explain part of why V037 and V133 are missed so badly --
Week 14 adds compactness back in.
"""

exit_explanation = """
The naive baseline predicts the training mean (28.0836), R2 approx 0, MAE=2.8906 -- no
better than guessing the average. The 3-feature LinearRegression (wwr, shade_m,
glazing_shgc) beats it: MAE=2.2680 (about 21.5% lower), R2=0.4937, honestly imperfect
since compactness and orientation are missing. Its worst miss, V037, is over-predicted
by 6.34 because the model cannot see V037's north orientation. The AI-drafted
"improved" version added est_annual_cost_index and reached R2=0.9923 -- too good to be
true, confirmed by a 0.995574 correlation with the target: that column is computed
FROM eui_kwh_m2yr, so it is leakage, not a real predictor. Removing it restored the
honest numbers exactly. This audit cannot yet tell you whether wwr=0.85, far outside
the training range, would predict safely.
"""

print(ai_use_record)
print(exit_explanation)
