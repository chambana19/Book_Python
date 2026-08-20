# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 14 studio · TRACK B -- continuous-outcome regression refinement
Add compactness, re-evaluate, model card
Syracuse University · School of Architecture · Fall 2026

TRACK NOTE
  This is the continuous-outcome track -- it deepens Week 13's regression, it does NOT
  build a classifier. If your Project 2 decision is a yes/no call, use
  ARC500_Week14B_Student_Classification.py instead -- both tracks share Monday's theory and the
  same dataset, and both feed Week 15's synthesis.

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week14 module folder, with radley_portfolio_envelope.csv
     inside a data/ subfolder next to it (data/radley_portfolio_envelope.csv).
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict a result BEFORE running each cell, especially cells [2]-[4].
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A single train/test split's R2 is not the whole story. Every regression refinement in
  this course is checked against cross_val_score across multiple folds before its
  improvement is reported as real -- including an honestly negative fold, if there is one.
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


# %% [1] Reserve final test; rebuild Week 13's 3-feature specification
# QUESTION           How does the 3-feature specification perform on validation rows?
# INPUTS/ASSUMPTIONS wwr, shade_m, glazing_shgc only (compactness and orientation
#                    deliberately left out, per Week 13)
# METHOD             reserve 20% as untouched final test; split the other 80% into 84
#                    training and 28 validation rows; score with Week 13's helper
#                    defined -- copied here without a single edit, docstring and type
#                    hints included. label: str says label must be text; -> dict says a
#                    dictionary comes back. Every function you write in Project 2 follows
#                    this same convention.
# CHECKS/INTERPRET   Expected validation MAE=2.5583, RMSE=3.0016, R2=0.3903.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = Path("data") / "radley_portfolio_envelope.csv"
df = pd.read_csv(DATA_PATH)
print(df.shape)


def report_metrics(y_true, y_pred, label: str) -> dict:
    """Print and return MAE, RMSE and R2 for one set of predictions."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    line = f"MAE={mae:.4f} RMSE={rmse:.4f} R2={r2:.5f}"
    print(label + ":", line)
    return {"MAE": mae, "RMSE": rmse, "R2": r2}


FEATURES3 = ["wwr", "shade_m", "glazing_shgc"]
FEATURES4 = ["wwr", "shade_m", "glazing_shgc", "compactness"]

y = df["eui_kwh_m2yr"]
development_idx, test_idx = train_test_split(
    df.index, test_size=0.20, random_state=42)
train_idx, validation_idx = train_test_split(
    development_idx, test_size=0.25, random_state=42)
assert (len(train_idx), len(validation_idx), len(test_idx)) == (84, 28, 28)

X3 = df[FEATURES3]
X3_train = df.loc[train_idx, FEATURES3]
X3_validation = df.loc[validation_idx, FEATURES3]
y_train = y.loc[train_idx]
y_validation = y.loc[validation_idx]
lr3 = LinearRegression().fit(X3_train, y_train)
pred3_validation = lr3.predict(X3_validation)

print("3-feature validation coef_:", lr3.coef_.round(4),
      "intercept_:", round(lr3.intercept_, 4))
m3 = report_metrics(y_validation, pred3_validation, "3-feature validation")

assert round(m3["MAE"], 4) == 2.5583
assert round(m3["RMSE"], 4) == 3.0016
assert round(m3["R2"], 4) == 0.3903

# TODO: Explain why Week 13's already-inspected test rows cannot be reused for another
# feature choice and still be called an untouched final test.


# %% [2] Refit with compactness added -- the Track B studio task
# QUESTION           How much does adding ONE feature -- compactness -- improve the fit?
# INPUTS/ASSUMPTIONS same train_idx and validation_idx as cell [1]
# METHOD             fit on training rows and score on validation rows
# CHECKS/INTERPRET   Expected validation MAE=2.4733, RMSE=2.9129, R2=0.4258.

X4 = df[FEATURES4]
# TODO: use the fixed indices, e.g.
# X4_train = df.loc[train_idx, FEATURES4]
# X4_validation = df.loc[validation_idx, FEATURES4]
raise NotImplementedError(
    "Cell [2] incomplete: build 4-feature training/validation frames from the fixed indices."
)

# TODO: fit lr4, predict pred4, and score it through the SAME report_metrics helper from
# cell [1] -- do NOT retype the three metric calls, e.g.
# lr4 = LinearRegression().fit(X4_train, y_train)
# pred4_validation = lr4.predict(X4_validation)
# print("coef_:", lr4.coef_.round(4))
# print("intercept_:", round(lr4.intercept_, 4))
# m4 = report_metrics(y_validation, pred4_validation, "4-feature validation")
raise NotImplementedError(
    "Cell [2] incomplete: fit and evaluate the four-feature model before continuing."
)
print("Refit cell reached -- complete the TODOs above, then rerun this cell.")

# TODO: assert m4 MAE=2.4733, RMSE=2.9129, R2=0.4258 to 4 decimals.
# TODO: Once real, compare compactness's coefficient sign against the "lower compactness
# = more efficient" fact from data/README -- does a POSITIVE coefficient here make sense?


# %% [3] Compare against Week 13: hand-compute the improvement
# QUESTION           By how much, exactly, did adding compactness improve MAE, RMSE, R2?
# INPUTS/ASSUMPTIONS the m3 dictionary from cell [1]; FEATURES3/FEATURES4 from cell [1]
# METHOD             first, wrap the whole split-fit-predict-score pipeline in ONE
#                    documented function, refit_report(features, label) -> dict, and use
#                    it to rebuild BOTH models independently -- this is the shape Project
#                    2 Part IV wants. Fixed train/validation indices prevent accidental
#                    comparison on different rows while test_idx remains unopened.
#                    Then delta_mae = wk13["MAE"] - wk14["MAE"]; delta_rmse likewise;
#                    delta_r2 = wk14["R2"] - wk13["R2"]
# CHECKS/INTERPRET   Expected: delta_mae=0.0850, delta_rmse=0.0888, delta_r2=+0.0355 --
#                    real, modest, honestly reported, not a dramatic jump. wk13 must
#                    reproduce cell [1] to the decimal.


def refit_report(features: list, label: str) -> dict:
    """Fit on fixed training rows and score on fixed validation rows."""
    fitted = LinearRegression().fit(df.loc[train_idx, features], y.loc[train_idx])
    pred = fitted.predict(df.loc[validation_idx, features])
    return report_metrics(y.loc[validation_idx], pred, label)


wk13 = refit_report(FEATURES3, "3-feature")
wk14 = refit_report(FEATURES4, "4-feature")

# TODO: compute delta_mae, delta_rmse, delta_r2 from the two returned dictionaries, e.g.
# delta_mae = wk13["MAE"] - wk14["MAE"]
# delta_rmse = wk13["RMSE"] - wk14["RMSE"]
# delta_r2 = wk14["R2"] - wk13["R2"]

# TODO: assert delta_mae=.0850, delta_rmse=.0888, delta_r2=.0355 to 4 decimals.
# TODO: assert round(wk13["MAE"], 4) == round(m3["MAE"], 4) -- proves refit_report
# reproduces cell [1]'s fit rather than quietly using different rows.

print("Comparison cell reached")


# %% [3b] Figure: baseline against improved, with the size of the gain drawn on it
# QUESTION           Adding compactness lowered MAE and RMSE. Drawn side by side on one
#                    honest axis, how big is that improvement really?
# INPUTS/ASSUMPTIONS wk13 and wk14 from cell [3] (the two dictionaries refit_report
#                    returned, both already real even before your TODOs are done); both
#                    models were scored on the SAME 28 validation designs
# METHOD             grouped bars -- baseline (3-feature) in AMBER against improved
#                    (4-feature) in BLUE -- for MAE and RMSE, the two metrics that share the
#                    kWh/m2/yr unit; ax.bar_label() writes the exact value above every bar;
#                    one GREEN annotation names the size of the gain, R2 included
# CHECKS/INTERPRET   MAE 2.5583 -> 2.4733; RMSE 3.0016 -> 2.9129;
#                    R2 .3903 -> .4258. Saves week14_model_comparison.png.

import matplotlib.pyplot as plt

# The course figure palette -- these hex values are used in every ARC 500 figure.
BLUE = "#2E74B5"   # the improved / optimized case
AMBER = "#B5731A"  # the baseline case
GREEN = "#2E7D5B"  # the verified result being claimed
GRAY = "#5A5F66"   # annotation arrows and reference lines

# TODO: once cell [3]'s deltas exist, reuse them here instead of recomputing them, e.g.
# fig_delta_mae, fig_delta_rmse, fig_delta_r2 = delta_mae, delta_rmse, delta_r2
fig_delta_mae = wk13["MAE"] - wk14["MAE"]    # fallback until cell [3]'s deltas exist
fig_delta_rmse = wk13["RMSE"] - wk14["RMSE"]
fig_delta_r2 = wk14["R2"] - wk13["R2"]

metric_names = ["MAE (mean absolute error)", "RMSE (root mean squared error)"]
baseline_vals = [wk13["MAE"], wk13["RMSE"]]
improved_vals = [wk14["MAE"], wk14["RMSE"]]
x_pos = np.arange(len(metric_names))
bar_w = 0.36
print(f"baseline (3-feature) bars: MAE={baseline_vals[0]:.4f} RMSE={baseline_vals[1]:.4f}")
print(f"improved (4-feature) bars: MAE={improved_vals[0]:.4f} RMSE={improved_vals[1]:.4f}")

fig, ax = plt.subplots(figsize=(9, 5.5))
# The baseline bars are drawn for you as the pattern to copy.
bars_base = ax.bar(x_pos - bar_w / 2, baseline_vals, bar_w, color=AMBER,
                   label="baseline: 3 features (Week 13)")
ax.bar_label(bars_base, fmt="%.4f", padding=3, fontsize=9.5, color=AMBER)

# TODO: add the improved model's bars in BLUE, offset the other way, and label them, e.g.
# bars_impr = ax.bar(x_pos + bar_w / 2, improved_vals, bar_w, color=BLUE,
#                    label="improved: 4 features (+ compactness)")
# ax.bar_label(bars_impr, fmt="%.4f", padding=3, fontsize=9.5, color=BLUE)

# TODO: annotate the SIZE of the gain, so the reader never has to subtract two bar heights
# by eye, e.g.
# ax.annotate(f"adding compactness: MAE {fig_delta_mae:.4f} lower "
#             f"({100 * fig_delta_mae / wk13['MAE']:.1f}%),\n"
#             f"RMSE {fig_delta_rmse:.4f} lower "
#             f"({100 * fig_delta_rmse / wk13['RMSE']:.1f}%),\n"
#             f"R2 {wk13['R2']:.4f} -> {wk14['R2']:.4f} ({fig_delta_r2:+.4f})",
#             xy=(x_pos[0] + 0.04, improved_vals[0] + 0.02),
#             xytext=(x_pos[0] - 0.32, 3.55), va="top",
#             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4),
#             fontsize=9.5, color=GREEN)

ax.set_title("Does adding compactness actually reduce this model's error, and by how much?")
ax.set_xlabel("error metric on the same 28 validation designs")
ax.set_ylabel("validation error (kWh/m2/yr)")
ax.set_xticks(x_pos, labels=metric_names)
ax.set_ylim(0, 3.9)  # starts at 0 on purpose -- see the COMMON ERROR at the end of the cell
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig("week14_model_comparison.png", dpi=150)
print("saved week14_model_comparison.png")
# WHY THIS MATTERS: only MAE and RMSE are drawn, because both are in kWh/m2/yr and can
# honestly share one y-axis. R2 is unitless, so putting an R2 bar beside an energy-unit bar
# would compare a ratio against an energy figure -- it belongs in the annotation, not on
# this axis. Every bar height comes from the same wk13/wk14 dictionaries cell [3] returned.
# WHY THIS MATTERS: a small metric gain can be noise, and this figure is exactly where that
# risk lives. These are model-selection bars on validation, not final-test performance.
# COMMON ERROR: starting the y-axis at 1.9 instead of 0 to "show the difference better."
# The AMBER bar would then tower over the BLUE one and an 11.1% improvement would read like
# a collapse. ax.set_ylim(0, 3.9) keeps the bar LENGTHS proportional to the values, which
# is the only reading a bar chart supports.
# COMMON ERROR: scoring the two models on different splits and comparing the bars anyway.
# refit_report() uses fixed indices so both bars describe the same 28 validation designs;
# two different splits would make the
# heights incomparable, and the figure would look just as convincing.


# %% [4] Paired cross-validation on development data only
# QUESTION           Does the validation improvement recur across development folds?
# INPUTS/ASSUMPTIONS 112 development rows for both feature sets; final test excluded
# METHOD             reuse one shuffled KFold(5, random_state=42) for both models
# CHECKS/INTERPRET   mean R2 .2313 (3f) -> .3225 (4f). Fold scores are performance
#                    variability, not individual prediction-error intervals.

from sklearn.model_selection import KFold, cross_val_score

# TODO: development_cv = KFold(5, shuffle=True, random_state=42)
# X3_development = df.loc[development_idx, FEATURES3]
# X4_development = df.loc[development_idx, FEATURES4]
# y_development = y.loc[development_idx]
# cv_scores3 = cross_val_score(LinearRegression(), X3_development, y_development,
#                              cv=development_cv, scoring="r2")
# cv_scores4 = cross_val_score(LinearRegression(), X4_development, y_development,
#                              cv=development_cv, scoring="r2")
raise NotImplementedError(
    "Cell [4] incomplete: compute the requested cross-validation evidence."
)
print(cv_scores4 if cv_scores4 is not None else "TODO")

# TODO: assert mean R2 values round to .2313 and .3225.


# %% [5] Written interpretation: what paired folds do and do not show
# QUESTION           What does paired development CV add to the validation result?
# INPUTS/ASSUMPTIONS cv_scores3/cv_scores4 and m4
# METHOD             write cv_interpretation as a string addressing both required points
# CHECKS/INTERPRET   Distinguish model-selection evidence from prediction uncertainty.

cv_interpretation = (
    "TODO: explain whether paired folds support selecting four features, and why the "
    "fold-score range is NOT an expected-error range, confidence interval, or prediction "
    "interval for a new design."
)
print(cv_interpretation)


# %% [5b] Final evaluation: refit selected model and open test once
# TODO: after selection is frozen, fit final_lr4 on all 112 development rows, predict the
# 28 test rows once, and call report_metrics. Expected MAE=1.9881, RMSE=2.5210, R2=.5167.
raise NotImplementedError(
    "Cell [5b] incomplete: refit selected model and evaluate the untouched test once."
)


# %% [6] AI-generated code audit
# QUESTION           Would you accept this AI-suggested "evaluate the regressor" function
#                    as-is?
# INPUTS/ASSUMPTIONS ai_evaluate_regressor as shown; validation data from cell [2]
# METHOD             list at least four specific defects, then compare with cells [3]-[5]
# CHECKS/INTERPRET   A defensible list names the single-split, no-cross-validation,
#                    overclaiming, and missing-MAE/RMSE defects -- not merely that the
#                    code "looks wrong."

def ai_evaluate_regressor(model, X_test, y_test):
    r2 = model.score(X_test, y_test)
    print(f"Model explains {r2:.1%} of variance -- validated and ready!")
    return r2

if lr4 is not None and X4_validation is not None:
    ai_evaluate_regressor(lr4, X4_validation, y_validation)
else:
    print("TODO: complete cell [2]'s split/fit before running the AI-audit function.")

ai_defects = [
    # TODO: add at least four specific defects
]

for defect in ai_defects:
    print("-", defect)


# %% [7] Self-check / transfer: predict a NEW design by hand, not from the test set
# QUESTION           Using this model's own coefficients, what predicted EUI results for
#                    wwr=0.50, shade_m=0.20, glazing_shgc=0.45, compactness=1.10 -- a
#                    design that appears in none of the worked cells above?
# INPUTS/ASSUMPTIONS final_lr4.coef_ and final_lr4.intercept_ from cell [5b]
# METHOD             predicted = intercept_ + sum(coef_i * value_i), by hand, then confirm
#                    against final_lr4.predict(...)
# CHECKS/INTERPRET   Expected predicted EUI = 31.2886 -- this exact design is
#                    Week 15's "baseline design," fed into an optimizer next week.

new_design = {"wwr": 0.50, "shade_m": 0.20, "glazing_shgc": 0.45, "compactness": 1.10}

# TODO: compute predicted_hand = final_lr4.intercept_ + sum of each coef_ times its matching
# new_design value, e.g.
# predicted_hand = (final_lr4.intercept_ + final_lr4.coef_[0]*new_design["wwr"]
#                    + final_lr4.coef_[1]*new_design["shade_m"]
#                    + final_lr4.coef_[2]*new_design["glazing_shgc"]
#                    + final_lr4.coef_[3]*new_design["compactness"])

# TODO: compute predicted_sklearn = final_lr4.predict(pd.DataFrame([new_design]))[0]

# TODO: add 2-4 assert statements: your hand value matches predicted_sklearn (within
# 1e-6), and predicted_sklearn rounds to 31.2886. Example to complete:
# assert abs(predicted_hand - predicted_sklearn) < 1e-6

print("Self-check cell reached")


# %% [8] Track B model card
# QUESTION           What does a one-page model card say about scope, expected error, and
#                    limits for this regressor?
# INPUTS/ASSUMPTIONS cells [1]-[5]
# METHOD             fill in one dictionary, one entry per required field
# CHECKS/INTERPRET   Every field below must be filled in with a real, specific value --
#                    not a placeholder. Do not call fold-score variation a prediction
#                    interval or individual-design expected error.

model_card_track_b = {
    "scope": "TODO: n, feature ranges, orientation categories used/not used",
    "features used": "TODO: list the four features",
    "selection evidence": "TODO: validation and paired development-CV comparison",
    "final test performance": "TODO: untouched-test MAE/RMSE/R2 from cell [5b]",
    "uncertainty status": "TODO: state that fold variation/RMSE is not a prediction interval",
    "do not trust": "TODO: name the training ranges this model should not be trusted "
                    "outside of, and the no-prediction-interval caveat",
}

for field, value in model_card_track_b.items():
    print(f"{field}: {value}")

# TODO: Replace every "TODO: ..." value with your own specific, real entry.


# %% [9] AI-use record and exit reflection
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished regression refinement in 80-120 words.
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
1. how much MAE/RMSE/R2 improved after adding compactness (cite the delta values),
2. how paired development folds support or weaken that selection,
3. final untouched-test MAE/RMSE/R2,
4. the final model's baseline prediction in cell [7], and
5. why fold variability and RMSE are not an individual prediction interval.
"""

print(ai_use_record)
print(exit_explanation)
