# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 13 studio · Evaluated prediction (regression): baseline, metrics, leakage audit
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week13 module folder, with radley_portfolio_envelope.csv
     inside a data/ subfolder next to it (data/radley_portfolio_envelope.csv).
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict a shape, coefficient, or metric before running.
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A model is not "done" the moment .fit() runs without an error. It is done only after
  you have beaten (or honestly failed to beat) a naive baseline, verified your split,
  hand-checked at least one metric, and audited every feature for leakage. This studio
  is that audit, applied to a real "AI-drafted" regression -- the leakage bug you find
  and fix in cells [9]-[10] IS this week's graded assignment.
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

# TODO: If your shape does not print (140, 9), check DATA_PATH before anything else.


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
#                    y_test (35,). Both asserts must pass silently. SET / ISDISJOINT(),
#                    DEFINED: a set is a collection with no duplicates and no order --
#                    {1,2,3}.isdisjoint({4,5}) is True (nothing shared),
#                    {1,2,3}.isdisjoint({3,4}) is False. Converting each index to a set
#                    and calling .isdisjoint() asks exactly one question: does ANY
#                    row-index number appear in both train and test?

FEATURES3 = ["wwr", "shade_m", "glazing_shgc"]
X = portfolio[FEATURES3]
y = portfolio["eui_kwh_m2yr"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
print("X_train:", X_train.shape, " X_test:", X_test.shape)
print("y_train:", y_train.shape, " y_test:", y_test.shape)

# TODO: uncomment and complete the two verification asserts below.
# assert len(X_train) + len(X_test) == len(portfolio) == 140
# assert set(X_train.index).isdisjoint(set(X_test.index))
print("Split verification cell reached")


# %% [3] One documented helper, then the naive baseline
# QUESTION           Four different models in this handout (baseline, 3-feature,
#                    AI-drafted, fixed) all need the same three metrics. Write the scoring
#                    ONCE, then answer: how good is "just guess the average"?
# INPUTS/ASSUMPTIONS X_train/X_test/y_train/y_test from cell [2]
# METHOD             report_metrics(y_true, y_pred, label) -> dict is written out for you
#                    below as the model of the course convention required on every
#                    function since Week 4: a one-line docstring in triple quotes, plus
#                    type hints (label: str, -> dict). Read it, then use it -- do not
#                    retype the three metric calls anywhere else in this file.
# CHECKS/INTERPRET   Expected once the TODOs are done: constant prediction 28.0836 (the
#                    TRAINING mean) for every test row; MAE=2.8906, RMSE=3.8154, R2 approx
#                    0.0 (about -0.00003). The helper prints R2 to 5 decimals on purpose --
#                    4 decimals would flatten -0.00003 to -0.0000 and hide the point.


def report_metrics(y_true, y_pred, label: str) -> dict:
    """Print and return MAE, RMSE and R2 for one set of predictions."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    line = f"MAE={mae:.4f} RMSE={rmse:.4f} R2={r2:.5f}"
    print(label + ":", line)
    return {"MAE": mae, "RMSE": rmse, "R2": r2}


baseline = DummyRegressor(strategy="mean")
# TODO: baseline.fit(X_train, y_train)
# TODO: pred_baseline = baseline.predict(X_test)
raise NotImplementedError(
    "Cell [3] incomplete: fit the baseline and create real test predictions."
)

# TODO: print("baseline predicts every row as:", round(baseline.constant_[0][0], 4))
base = report_metrics(y_test, pred_baseline, "baseline")

# TODO: Once fit/predict are uncommented, confirm MAE=2.8906, RMSE=3.8154,
# R2 approx -0.00003 -- not the placeholder numbers above. Then add two asserts of your
# own here, checking base["MAE"] and base["RMSE"] against those expected values.


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
# TODO: model3.fit(X_train, y_train)
# TODO: pred_model3 = model3.predict(X_test)
raise NotImplementedError(
    "Cell [4] incomplete: fit the three-feature model and predict the test rows."
)

m3 = report_metrics(y_test, pred_model3, "3-feature")

# TODO: After fit/predict are uncommented, print model3.coef_.round(4) and
# round(model3.intercept_, 4); confirm they match the expected values above.
# TODO: add an assert of your own that m3["MAE"] rounds to 2.2680.


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
print(comparison.round(4))

# TODO: mae_improvement_pct = (base["MAE"] - m3["MAE"]) / base["MAE"] * 100
# TODO: print(f"MAE improvement over baseline: {mae_improvement_pct:.1f}%")

# TODO: uncomment once cells [3]-[4] are complete:
# assert m3["MAE"] < base["MAE"], "model did not beat the naive baseline on MAE"


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

# TODO: by_hand_subset = residual_table.head(8)["residual"]
# TODO: by_hand_mae = by_hand_subset.abs().sum() / len(by_hand_subset)
# TODO: print("hand-added mean |residual| of the first 8 printed rows:",
#             round(by_hand_mae, 4))

# TODO: manual_mae = np.mean(np.abs(residual_table["residual"]))
# TODO: print("manual MAE (full 35-row test set):", round(manual_mae, 4))
# TODO: assert round(manual_mae, 2) == round(m3["MAE"], 2)
print("Manual metric cell reached")


# %% [7] Diagnose the largest residual
# QUESTION           Which test-set design does this model miss the worst -- and why,
#                    specifically, does it miss that one so badly?
# INPUTS/ASSUMPTIONS residual_table from cell [6]; portfolio's compactness and
#                    orientation columns (NOT used as features this week, but still
#                    readable for diagnosis)
# METHOD             sort residual_table by |residual| descending; look up the worst
#                    row's compactness and orientation from portfolio (joined by
#                    variant_id); reason about what the 3-feature model cannot see.
#                    REINDEX(), DEFINED: it simply reorders residual_table's EXISTING
#                    rows into a new order (here, largest-to-smallest |residual|) --
#                    it does not add, remove, or recompute any value
# CHECKS/INTERPRET   Expected worst residual: variant V037, actual=20.43,
#                    predicted approx 26.77, residual approx -6.34 (the model
#                    OVER-predicts -- thinks the design performs worse than it does).

# TODO: residual_table_sorted = residual_table.reindex(
#     residual_table["residual"].abs().sort_values(ascending=False).index
# )
# TODO: print(residual_table_sorted.head(3))

# TODO: worst_id = residual_table_sorted.iloc[0]["variant_id"]
# TODO: worst_row = portfolio.loc[portfolio["variant_id"] == worst_id].iloc[0]
# TODO: print(worst_row[["variant_id", "wwr", "shade_m", "glazing_shgc",
#                         "compactness", "orientation"]])

diagnosis_v037 = "TODO: in 2-3 sentences, name which design variable(s) the 3-feature model CANNOT see that would explain V037's -6.34 residual, using the compactness/orientation values you just printed."
print(diagnosis_v037)


# %% [7b] Predicted vs. actual, with the 1:1 line
# QUESTION           Distance from the 1:1 line IS the prediction error. Do the 35 held-out
#                    predictions sit on that line, or drift off it at one end of the range?
# INPUTS/ASSUMPTIONS residual_table from cell [6]; m3["R2"] and m3["MAE"] from cell [4];
#                    the course figure palette defined below and reused in cell [8]
# METHOD             draw the GRAY dashed 1:1 diagonal across the FULL data range first,
#                    then scatter actual (x) against predicted (y) on top of it; print, then
#                    annotate, R2, MAE, and the mean residual at each end of the range;
#                    label V037, the worst miss diagnosed in cell [7]
# CHECKS/INTERPRET   Expected once cell [4]'s fit/predict TODOs are done (the completion
#                    gate now stops execution instead of drawing zero predictions): the
#                    1:1 line spans 19.25 to 38.19 kWh/m2/yr; R2=0.4937 and
#                    MAE=2.2680 (cell [4]'s own numbers); mean residual of the 12
#                    LOWEST-EUI test designs = -2.7634 (predicted too high, so those points
#                    sit ABOVE the line), of the 12 HIGHEST-EUI designs = +1.0754
#                    (predicted too low, BELOW the line). Saves week13_pred_vs_actual.png.

# The course figure palette -- these five hex values are used in every ARC 500 figure.
BLUE = "#2E74B5"   # the main series
AMBER = "#B5731A"  # the flagged case / a warning
GREEN = "#2E7D5B"  # the confirmed reference value
GRAY = "#5A5F66"   # reference lines and annotation text

# TODO: compute the bias at each end of the range. Use residual_table.nsmallest(12, "actual")
# and .nlargest(12, "actual"), taking the mean of each one's "residual" column. Assign them to
# low_end_bias and high_end_bias, then check both against CHECKS/INTERPRET above.
low_end_bias = residual_table.nsmallest(12, "actual")["residual"].mean()
high_end_bias = residual_table.nlargest(12, "actual")["residual"].mean()

# The 1:1 line must span the FULL data range -- actual AND predicted, both ends.
line_lo = min(residual_table["actual"].min(), residual_table["predicted"].min()) - 1
line_hi = max(residual_table["actual"].max(), residual_table["predicted"].max()) + 1

print("1:1 line spans:", round(line_lo, 2), "to", round(line_hi, 2), "kWh/m2/yr")
print("mean residual, 12 lowest-EUI test designs:", round(low_end_bias, 4))
print("mean residual, 12 highest-EUI test designs:", round(high_end_bias, 4))

fig, ax = plt.subplots(figsize=(9, 5.5))
# TODO: draw the 1:1 line FIRST, so the scatter sits on top of it:
# ax.plot([line_lo, line_hi], [line_lo, line_hi], color=GRAY, linestyle="--", linewidth=1.6,
#         label="perfect prediction (1:1 line)")
# TODO: then scatter actual on x against predicted on y:
# ax.scatter(residual_table["actual"], residual_table["predicted"], color=BLUE, s=42,
#            alpha=0.85, label="35 held-out test designs")

# TODO: label V037, the worst miss you diagnosed in cell [7]. Pull its row out with
# residual_table.loc[residual_table["variant_id"] == "V037"].iloc[0], then ax.annotate() it
# with an arrow so the reader can see how far above the line it sits.
# TODO: add a text block in the corner (xycoords="axes fraction") reporting m3["R2"],
# m3["MAE"], and the two end-of-range biases you computed above.

ax.set_title("Do the 35 held-out predictions land on the 1:1 line, or drift off it at one end?")
ax.set_xlabel("actual eui_kwh_m2yr (kWh/m2/yr)")
ax.set_ylabel("predicted eui_kwh_m2yr (kWh/m2/yr)")
ax.set_xlim(line_lo, line_hi)
ax.set_ylim(line_lo, line_hi)
ax.set_aspect("equal")  # equal scales, so the 1:1 line really is a 45-degree diagonal
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
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
# INPUTS/ASSUMPTIONS residual_table from cell [6]; m3["MAE"]/m3["RMSE"] from cell [4]; the
#                    palette from cell [7b]
# METHOD             fig, ax = plt.subplots(figsize=(9, 5.5)); a GREEN dashed reference line
#                    at residual=0; scatter predicted (x) against residual (y); label the
#                    largest-|residual| variant by its identifier
# CHECKS/INTERPRET   Expected once cell [4]'s fit/predict TODOs are done (the completion
#                    gate prevents a placeholder residual plot): 16 of the 35 residuals
#                    above the zero line, 19 below;
#                    residuals span -6.3373 to +4.2250 kWh/m2/yr; the labelled worst miss is
#                    V037, at predicted 26.7673, residual -6.3373. Saves
#                    week13_residual_plot.png.

# The row with the largest miss in either direction -- .abs().idxmax() finds it without
# re-sorting the whole table (cell [7] sorted it a different way for a different purpose).
worst_row = residual_table.loc[residual_table["residual"].abs().idxmax()]
# TODO: count how many residuals sit above and below the zero line. Use
# (residual_table["residual"] > 0).sum() and the matching < 0 version; assign them to
# above_zero and below_zero, then check both against CHECKS/INTERPRET above.
above_zero = (residual_table["residual"] > 0).sum()
below_zero = (residual_table["residual"] < 0).sum()

print("residuals above the zero line:", above_zero, " below:", below_zero)
print("residual range:", round(residual_table["residual"].min(), 4), "to",
      round(residual_table["residual"].max(), 4), "kWh/m2/yr")
print("largest miss:", worst_row["variant_id"], "at predicted",
      round(worst_row["predicted"], 4), "residual", round(worst_row["residual"], 4))

fig, ax = plt.subplots(figsize=(9, 5.5))
# TODO: draw the zero-error reference line with ax.axhline(0, color=GREEN, linestyle="--",
# linewidth=1.6, label="zero error (residual = 0)").
# TODO: scatter PREDICTED on x against RESIDUAL on y -- not actual on x, see COMMON ERROR:
# ax.scatter(residual_table["predicted"], residual_table["residual"], color=BLUE, s=42,
#            alpha=0.85, label="35 held-out test designs")
# TODO: annotate worst_row by name with an arrow, and add a corner text block reporting
# m3["MAE"], m3["RMSE"], and your above_zero/below_zero counts.

ax.set_ylim(-8.2, 6.4)
ax.set_title("Are the errors random scatter around zero, or do they form a shape?")
ax.set_xlabel("predicted eui_kwh_m2yr (kWh/m2/yr)")
ax.set_ylabel("residual, actual - predicted (kWh/m2/yr)")
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
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
#                    eui_kwh_m2yr) = 0.995574. CORRELATION, DEFINED: it ranges from -1
#                    to 1 and measures how closely two variables move together; 0.995574
#                    means these two columns move almost in lockstep -- near-perfect,
#                    itself suspicious for two supposedly independent measurements.

# AI ASSISTANT'S DRAFT, AS RECEIVED (paraphrased prompt/response):
# "Add est_annual_cost_index as a fourth feature -- cost is a design-relevant variable
#  too, and including it should only help the model."
FEATURES_LEAK = ["wwr", "shade_m", "glazing_shgc", "est_annual_cost_index"]
X_leak = portfolio[FEATURES_LEAK]
Xtr_leak, Xte_leak, ytr_leak, yte_leak = train_test_split(
    X_leak, y, test_size=0.25, random_state=42
)
model_leak = LinearRegression()
# TODO: model_leak.fit(Xtr_leak, ytr_leak)
# TODO: pred_leak = model_leak.predict(Xte_leak)
raise NotImplementedError(
    "Cell [9] incomplete: fit the deliberate leakage audit before interpreting it."
)

# TODO: print("leak-version coef_:", model_leak.coef_.round(4))
leak = report_metrics(yte_leak, pred_leak, "leaking")

# TODO: corr_leak_target = portfolio["est_annual_cost_index"].corr(portfolio["eui_kwh_m2yr"])
# TODO: print("corr(est_annual_cost_index, eui_kwh_m2yr):", round(corr_leak_target, 6))


# The one-off correlation check above becomes a REUSABLE tool the moment it is wrapped in
# a documented function. This one is written out for you; keep it, and run it on your own
# Project 2 feature list before you fit anything.
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

print("leakage scan -- the honest 3-feature list:")
clean = leakage_scan(FEATURES3, TARGET)
print("suspects:", clean)

# TODO: add two asserts of your own here: suspects == ["est_annual_cost_index"] and
# clean == []. Then answer, in the string below, why a HIGH correlation with the target
# is good news for an independently measured design variable but a red flag for a column
# computed FROM the target.

leakage_diagnosis = "TODO: name the bug. Why is R2=0.9923 suspicious, and what, specifically, is est_annual_cost_index computed FROM? (Hint: check the correlation you just printed, and reread the QUESTION above.)"
print(leakage_diagnosis)


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

# TODO: FEATURES_FIXED = [f for f in FEATURES3]  # est_annual_cost_index excluded
# TODO: assert "est_annual_cost_index" not in FEATURES_FIXED

# TODO: X_fixed = portfolio[FEATURES_FIXED]
# TODO: Xtr_fixed, Xte_fixed, ytr_fixed, yte_fixed = train_test_split(
#     X_fixed, y, test_size=0.25, random_state=42
# )
# TODO: model_fixed = LinearRegression()
# TODO: model_fixed.fit(Xtr_fixed, ytr_fixed)
# TODO: pred_fixed = model_fixed.predict(Xte_fixed)

# TODO: score it through the SAME helper, not a retyped metric block:
# fixed = report_metrics(yte_fixed, pred_fixed, "fixed")
# TODO: assert leakage_scan(FEATURES_FIXED, TARGET) == []

# TODO: assert round(fixed["MAE"], 4) == round(m3["MAE"], 4)
# TODO: assert round(fixed["RMSE"], 4) == round(m3["RMSE"], 4)
# TODO: assert round(fixed["R2"], 4) == round(m3["R2"], 4)

fix_explanation = "TODO: in 1-2 sentences, explain why the fix is to DROP est_annual_cost_index entirely, not to keep it with a smaller coefficient."
print(fix_explanation)
print("Fix cell reached")


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

# TODO: Add 2-4 assert statements here, checking a DIFFERENT metric (RMSE) and a
# DIFFERENT residual (the SECOND-worst, not V037). Example to complete:
# manual_rmse = np.sqrt(np.mean(residual_table["residual"] ** 2))
# second_worst = residual_table_sorted.iloc[1]
# assert round(manual_rmse, 2) == round(m3["RMSE"], 2)
# assert second_worst["variant_id"] == "V133"
# assert round(second_worst["residual"], 2) == -4.89
# assert "est_annual_cost_index" not in FEATURES_FIXED

print("Self-check cell reached")


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
1. how the 3-feature model compared to the naive baseline (MAE/RMSE/R2),
2. why V037's residual was so large and what the model could not see,
3. what made you suspicious of the AI-drafted 4-feature version's R2=0.9923,
4. what est_annual_cost_index is actually computed from, and why that makes it leakage,
5. one thing this audit still cannot tell you.
"""

print(ai_use_record)
print(exit_explanation)
