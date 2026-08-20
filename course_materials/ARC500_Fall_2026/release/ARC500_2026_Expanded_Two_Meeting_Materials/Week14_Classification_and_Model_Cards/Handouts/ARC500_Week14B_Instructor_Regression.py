# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 14 studio · TRACK B -- INSTRUCTOR SOLUTIONS
Continuous-outcome regression refinement: add compactness, re-evaluate, model card
Syracuse University · School of Architecture · Fall 2026

TRACK NOTE
  This is the continuous-outcome track -- it deepens Week 13's regression, it does NOT
  build a classifier. If your Project 2 decision is a yes/no call, use
  ARC500_Week14B_Instructor_Classification.py instead -- both tracks share the same Monday
  theory and the same dataset, and both feed Week 15's synthesis.
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


# %% [1] Reserve a final test set; rebuild Week 13's 3-feature specification
# QUESTION           How does the Week 13 feature specification perform on validation rows?
# INPUTS/ASSUMPTIONS wwr, shade_m, glazing_shgc only (compactness and orientation
#                    deliberately left out, per Week 13)
# METHOD             reserve 20% as an untouched final test set; split the other 80% into
#                    84 training and 28 validation rows; fit and score on validation only
# CHECKS/INTERPRET   Expected train/validation/test rows=84/28/28; validation
#                    MAE=2.5583, RMSE=3.0016, R2=0.3903.

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
print("train / validation / untouched test rows:",
      len(train_idx), len(validation_idx), len(test_idx))
assert (len(train_idx), len(validation_idx), len(test_idx)) == (84, 28, 28)

X3 = df[FEATURES3]
X3_train = df.loc[train_idx, FEATURES3]
X3_validation = df.loc[validation_idx, FEATURES3]
y_train = y.loc[train_idx]
y_validation = y.loc[validation_idx]

lr3 = LinearRegression().fit(X3_train, y_train)
pred3_validation = lr3.predict(X3_validation)

print("3-feature validation model coef_:", lr3.coef_.round(4),
      "intercept_:", round(lr3.intercept_, 4))
m3 = report_metrics(y_validation, pred3_validation, "3-feature validation")

assert round(m3["MAE"], 4) == 2.5583
assert round(m3["RMSE"], 4) == 3.0016
assert round(m3["R2"], 4) == 0.3903
# WHY THIS MATTERS: "docstring + type hints, recalled" -- label: str states that label must
# be text, -> dict states that a dictionary comes back, and the triple-quoted first line
# says what the function does in one line. Every function you write in Project 2 follows
# this same convention. Reusing Week 13's helper verbatim, rather than retyping three
# metric calls, is what guarantees the two validation models in cell [3] are comparable.
# WHY THIS MATTERS: Week 13's old test split has already informed the decision to try
# compactness. Reusing that same test set again would make it a selection set, not an
# untouched final test. This fresh three-way split keeps selection and final evaluation
# separate.


# %% [2] Refit with compactness added -- the Track B studio task
# QUESTION           How much does adding ONE feature -- compactness -- improve the fit?
# INPUTS/ASSUMPTIONS same 84 training and 28 validation rows as cell [1]
# METHOD             fit the 4-feature model on training; score on validation
# CHECKS/INTERPRET   Expected validation MAE=2.4733, RMSE=2.9129, R2=0.4258.

X4 = df[FEATURES4]
X4_train = df.loc[train_idx, FEATURES4]
X4_validation = df.loc[validation_idx, FEATURES4]

lr4 = LinearRegression().fit(X4_train, y_train)
pred4_validation = lr4.predict(X4_validation)

print("Track B (4-feature) coef_ [wwr, shade_m, glazing_shgc, compactness]:", lr4.coef_.round(4))
print("intercept_:", round(lr4.intercept_, 4))
m4 = report_metrics(y_validation, pred4_validation, "4-feature validation")

assert round(m4["MAE"], 4) == 2.4733
assert round(m4["RMSE"], 4) == 2.9129
assert round(m4["R2"], 4) == 0.4258
# WHY THIS MATTERS: compactness's coefficient is positive. Recall compactness is a
# surface-to-volume proxy where LOWER = more compact/efficient -- a positive coefficient
# on this raw scale means higher compactness numbers (less efficient shapes) raise
# predicted EUI, directionally consistent with the synthetic-data design. It remains an
# association from this fit, not proof that changing compactness alone causes that effect.


# %% [3] Compare against Week 13: hand-compute the improvement
# QUESTION           By how much, exactly, did adding compactness improve MAE, RMSE, R2?
# INPUTS/ASSUMPTIONS the m3 dictionary from cell [1] and the m4 dictionary from cell [2],
#                    both produced by the same report_metrics helper
# METHOD             first, wrap the whole split-fit-predict-score pipeline in ONE
#                    documented function, refit_report(features, label) -> dict, and use
#                    it to rebuild BOTH models independently -- this is the shape Project
#                    2 Part IV wants. Then delta_mae = wk13["MAE"] - wk14["MAE"];
#                    delta_rmse likewise; delta_r2 = wk14["R2"] - wk13["R2"]
# CHECKS/INTERPRET   Expected: delta_mae=0.0850, delta_rmse=0.0888, delta_r2=+0.0355 --
#                    real, modest, honestly reported, not a dramatic jump. refit_report
#                    must reproduce cells [1] and [2] to the decimal; if it does not,
#                    something about the split settings has drifted.


def refit_report(features: list, label: str) -> dict:
    """Fit on the fixed training rows and score on fixed validation rows."""
    fitted = LinearRegression().fit(df.loc[train_idx, features], y.loc[train_idx])
    pred = fitted.predict(df.loc[validation_idx, features])
    return report_metrics(y.loc[validation_idx], pred, label)


wk13 = refit_report(FEATURES3, "3-feature")
wk14 = refit_report(FEATURES4, "4-feature")

assert round(wk13["MAE"], 4) == round(m3["MAE"], 4)
assert round(wk14["MAE"], 4) == round(m4["MAE"], 4)

delta_mae = wk13["MAE"] - wk14["MAE"]
delta_rmse = wk13["RMSE"] - wk14["RMSE"]
delta_r2 = wk14["R2"] - wk13["R2"]

print(f"delta MAE = {delta_mae:.4f} (MAE drops from {wk13['MAE']:.4f} to {wk14['MAE']:.4f})")
print(f"delta RMSE = {delta_rmse:.4f}")
print(f"delta R2 = {delta_r2:+.4f} ({wk13['R2']:.4f} -> {wk14['R2']:.4f})")

assert round(delta_mae, 4) == 0.0850
assert round(delta_rmse, 4) == 0.0888
assert round(delta_r2, 4) == 0.0355

comparison_table = pd.DataFrame({
    "metric": ["MAE", "RMSE", "R2"],
    "Week13_3feature": [round(wk13["MAE"], 4), round(wk13["RMSE"], 4), round(wk13["R2"], 4)],
    "Week14_4feature": [round(wk14["MAE"], 4), round(wk14["RMSE"], 4), round(wk14["R2"], 4)],
    "delta": [round(delta_mae, 4), round(delta_rmse, 4), round(delta_r2, 4)],
})
print(comparison_table)
# WHY THIS MATTERS: fixed train/validation indices make the model comparison fair while
# keeping test_idx unavailable. The validation improvement is small and is only model-
# selection evidence; it must not be presented as final generalization performance.


# %% [3b] Figure: baseline against improved, with the size of the gain drawn on it
# QUESTION           Adding compactness lowered MAE and RMSE. Drawn side by side on one
#                    honest axis, how big is that improvement really?
# INPUTS/ASSUMPTIONS wk13 and wk14 from cell [3] (the two dictionaries refit_report
#                    returned) and the deltas cell [3] already asserted; both models were
#                    scored on the SAME 28 validation designs
# METHOD             grouped bars -- baseline (3-feature) in AMBER against improved
#                    (4-feature) in BLUE -- for MAE and RMSE, the two metrics that share the
#                    kWh/m2/yr unit; ax.bar_label() writes the exact value above every bar;
#                    one GREEN annotation names the size of the gain, R2 included
# CHECKS/INTERPRET   Expected bars: MAE 2.5583 -> 2.4733, RMSE 3.0016 -> 2.9129;
#                    R2 0.3903 -> 0.4258. Saves week14_model_comparison.png.

import matplotlib.pyplot as plt

# The course figure palette -- these hex values are used in every ARC 500 figure.
BLUE = "#2E74B5"   # the improved / optimized case
AMBER = "#B5731A"  # the baseline case
GREEN = "#2E7D5B"  # the verified result being claimed
GRAY = "#5A5F66"   # annotation arrows and reference lines

# The three deltas cell [3] already computed and asserted -- reused, never recomputed, so
# the figure cannot drift away from the printed comparison_table.
fig_delta_mae, fig_delta_rmse, fig_delta_r2 = delta_mae, delta_rmse, delta_r2

metric_names = ["MAE (mean absolute error)", "RMSE (root mean squared error)"]
baseline_vals = [wk13["MAE"], wk13["RMSE"]]
improved_vals = [wk14["MAE"], wk14["RMSE"]]
x_pos = np.arange(len(metric_names))
bar_w = 0.36
print(f"baseline (3-feature) bars: MAE={baseline_vals[0]:.4f} RMSE={baseline_vals[1]:.4f}")
print(f"improved (4-feature) bars: MAE={improved_vals[0]:.4f} RMSE={improved_vals[1]:.4f}")

fig, ax = plt.subplots(figsize=(9, 5.5))
bars_base = ax.bar(x_pos - bar_w / 2, baseline_vals, bar_w, color=AMBER,
                   label="baseline: 3 features (Week 13)")
bars_impr = ax.bar(x_pos + bar_w / 2, improved_vals, bar_w, color=BLUE,
                   label="improved: 4 features (+ compactness)")
ax.bar_label(bars_base, fmt="%.4f", padding=3, fontsize=9.5, color=AMBER)
ax.bar_label(bars_impr, fmt="%.4f", padding=3, fontsize=9.5, color=BLUE)

ax.annotate(f"adding compactness: MAE {fig_delta_mae:.4f} lower "
            f"({100 * fig_delta_mae / wk13['MAE']:.1f}%),\n"
            f"RMSE {fig_delta_rmse:.4f} lower "
            f"({100 * fig_delta_rmse / wk13['RMSE']:.1f}%),\n"
            f"R2 {wk13['R2']:.4f} -> {wk14['R2']:.4f} ({fig_delta_r2:+.4f})",
            xy=(x_pos[0] + 0.04, improved_vals[0] + 0.02),
            xytext=(x_pos[0] - 0.32, 3.65), va="top",
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4),
            fontsize=9.5, color=GREEN)

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
# honestly share one y-axis. R2 is unitless, so putting it beside energy-unit bars
# would compare a ratio against an energy figure -- it belongs in the annotation, not on
# this axis. Every bar height comes from the same wk13/wk14 dictionaries cell [3] asserted.
# WHY THIS MATTERS: a small metric gain can be noise, and this figure is exactly where that
# risk lives. Both bar pairs come from one 28-row validation split. Cell [4] compares the
# specifications on paired development folds; cell [5b] gives the selected model one final
# untouched test. Read these bars as selection evidence, not final performance.
# COMMON ERROR: starting the y-axis at 1.9 instead of 0 to "show the difference better."
# The AMBER bar would then tower over the BLUE one and a small improvement would read like
# a collapse. ax.set_ylim(0, 3.9) keeps the bar LENGTHS proportional to the values, which
# is the only reading a bar chart supports.
# COMMON ERROR: scoring the two models on different splits and comparing the bars anyway.
# refit_report() in cell [3] uses fixed indices so the two bars describe the same 28
# validation designs; two different splits would make the
# heights incomparable, and the figure would look just as convincing.


# %% [4] Paired cross-validation on development data only
# QUESTION           Does the small validation improvement recur across development folds?
# INPUTS/ASSUMPTIONS the same 112 development rows for both feature specifications;
#                    the 28 final test rows remain excluded
# METHOD             one shuffled KFold object, reused for both cross_val_score calls
# CHECKS/INTERPRET   3-feature mean R2=0.2313; 4-feature mean R2=0.3225. Fold scores
#                    describe variability in performance, not prediction-error intervals.

from sklearn.model_selection import KFold, cross_val_score

development_cv = KFold(n_splits=5, shuffle=True, random_state=42)
X3_development = df.loc[development_idx, FEATURES3]
X4_development = df.loc[development_idx, FEATURES4]
y_development = y.loc[development_idx]
cv_scores3 = cross_val_score(
    LinearRegression(), X3_development, y_development,
    cv=development_cv, scoring="r2")
cv_scores4 = cross_val_score(
    LinearRegression(), X4_development, y_development,
    cv=development_cv, scoring="r2")
print("development 3-feature R2:", cv_scores3.round(4))
print("development 4-feature R2:", cv_scores4.round(4))
print("mean 3-feature / 4-feature:",
      round(cv_scores3.mean(), 4), round(cv_scores4.mean(), 4))

assert round(cv_scores3.mean(), 4) == 0.2313
assert round(cv_scores4.mean(), 4) == 0.3225
# WHY THIS MATTERS: the same fold membership makes this a paired comparison. The
# 4-feature mean is higher, which supports the validation choice, but the five R2 values
# are performance estimates across folds. Their min/max is not an error bar for an
# individual prediction and not an "honest expected-error range."


# %% [5] Written interpretation: what paired folds do and do not show
# QUESTION           What does development cross-validation add to the validation result?
# INPUTS/ASSUMPTIONS cv_scores3 and cv_scores4 from cell [4]; m4 from cell [2]
# METHOD             write cv_interpretation as a string addressing both required points
# CHECKS/INTERPRET   Distinguish model-selection evidence from prediction uncertainty.

cv_interpretation = (
    "On the 28 validation rows, adding compactness raises R2 from 0.3903 to 0.4258. "
    "Paired five-fold checks on the 112 development rows point the same direction: mean "
    "R2 rises from 0.2313 to 0.3225. That agreement supports selecting the 4-feature "
    "specification before the final test. The fold scores still vary, so a single split "
    "is not a complete stability claim. Their range describes performance across these "
    "partitions; it is not the expected error of a new design, a confidence interval, or "
    "a prediction interval. Those require a separate uncertainty method."
)
print(cv_interpretation)
# WHY THIS MATTERS: cross-validation helps compare model specifications before testing;
# it does not convert fold-to-fold variation into uncertainty for a prediction.


# %% [5b] Final evaluation: refit the selected model, then open the test set once
# QUESTION           How does the selected 4-feature model perform on untouched rows?
# INPUTS/ASSUMPTIONS selection is frozen; development_idx has 112 rows, test_idx has 28
# METHOD             refit on all development rows, predict the final test once
# CHECKS/INTERPRET   Expected MAE=1.9881, RMSE=2.5210, R2=0.5167.

final_lr4 = LinearRegression().fit(X4_development, y_development)
final_test_pred4 = final_lr4.predict(df.loc[test_idx, FEATURES4])
final_m4 = report_metrics(y.loc[test_idx], final_test_pred4, "FINAL 4-feature test")

assert round(final_m4["MAE"], 4) == 1.9881
assert round(final_m4["RMSE"], 4) == 2.5210
assert round(final_m4["R2"], 4) == 0.5167
print("Final test evaluated once; model specification remains frozen.")


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

ai_evaluate_regressor(lr4, X4_validation, y_validation)

ai_defects = [
    "model.score() reruns the SAME validation split already reported in cell [2] --"
    " nothing new is being 'validated' here at all.",
    "No paired cross-validation anywhere in this function, so it cannot show whether "
    "the small feature-addition gain recurs across development folds.",
    "'Validated and ready!' overclaims what a single .score() call can support -- "
    "nothing here checks for leakage (Week 13's est_annual_cost_index bug) or "
    "extrapolation outside the training ranges.",
    "No MAE or RMSE reported at all -- a bare variance percentage cannot be sanity-"
    "checked against real kWh/m2/yr units the way cell [5b]'s test MAE=1.9881 can.",
]

for defect in ai_defects:
    print("-", defect)
# WHY THIS MATTERS: the printed validation R2 sounds final, but it is model-selection
# evidence. Cell [5b], not this helper, owns the untouched final evaluation.


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

predicted_hand = (
    final_lr4.intercept_
    + final_lr4.coef_[0] * new_design["wwr"]
    + final_lr4.coef_[1] * new_design["shade_m"]
    + final_lr4.coef_[2] * new_design["glazing_shgc"]
    + final_lr4.coef_[3] * new_design["compactness"]
)

new_design_df = pd.DataFrame([new_design])
predicted_sklearn = final_lr4.predict(new_design_df)[0]

print("hand-computed predicted EUI:", round(predicted_hand, 4))
print("final_lr4.predict() predicted EUI:", round(predicted_sklearn, 4))

assert abs(predicted_hand - predicted_sklearn) < 1e-6
assert round(predicted_sklearn, 4) == 31.2886
print("Self-check passed: hand-computed prediction matches final_lr4.predict() exactly.")
# WHY THIS MATTERS: this is the required weekly transfer check -- a genuinely different
# design (none of these four values appear in the worked test-set rows above), verified
# by hand-applying the linear formula, not just calling .predict(). It is also a
# deliberate continuity hook: Week 15's demo uses this EXACT design as its "baseline"
# and feeds this EXACT model into scipy.optimize.minimize as the objective.


# %% [8] Track B model card
# QUESTION           What does a one-page model card say about scope, expected error, and
#                    limits for this regressor?
# INPUTS/ASSUMPTIONS cells [1]-[5]
# METHOD             fill in one dictionary, one entry per required field
# CHECKS/INTERPRET   Every field below must be filled in with a real, specific value --
#                    not a placeholder. Fold variability must not be called prediction
#                    uncertainty or an individual-design error interval.

model_card_track_b = {
    "scope": "final model fitted on 112 development rows from n=140 synthetic Radley Hall "
             "portfolio variants; wwr 0.20-0.60, "
             "shade_m 0.0-1.2, glazing_shgc 0.25-0.65, compactness 0.8-1.4, 4 "
             "orientation categories (orientation itself not yet used as a feature).",
    "features used": "wwr, shade_m, glazing_shgc, compactness.",
    "selection evidence": "validation R2 0.3903 -> 0.4258 and paired development-CV "
             "mean R2 0.2313 -> 0.3225 support selecting the 4-feature model.",
    "final test performance": "on 28 untouched rows: MAE=1.9881 kWh/m2/yr, "
             "RMSE=2.5210 kWh/m2/yr, R2=0.5167.",
    "uncertainty status": "fold-to-fold R2 variation is not a prediction interval; this "
             "script does not yet quantify uncertainty for an individual design.",
    "do not trust": "predictions for designs outside the ranges stated in 'scope' above "
             "(Week 13's silent-extrapolation note), or claims that test RMSE is an "
             "individual prediction interval.",
}

for field, value in model_card_track_b.items():
    print(f"{field}: {value}")
# WHY THIS MATTERS: this model card IS this week's Project 2 evaluated-prediction
# checkpoint for the continuous-outcome track -- Week 15 reuses this exact 4-feature
# model directly as the optimization objective.


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
Tool/model: Example assistant
Prompt: Write a function that tells me if my regression model, after adding a feature,
is validated and ready to use.
Suggestion received: ai_evaluate_regressor(), exactly as shown in cell [6] -- a single
model.score() call on validation rows, mislabeled as final validation.
What I accepted: The idea of wrapping evaluation in a small, reusable function.
What I modified and why: Reserved a final test before comparing features, used validation
plus paired development-only cross-validation for model selection, then refitted the
selected model and evaluated the untouched test exactly once. Reported MAE/RMSE with R2.
What I rejected and why: The "validated and ready!" framing -- neither one validation
score nor cross-validation replaces an untouched final test or a deployment safeguard.
How I tested it: Hand-computed both the delta-MAE/delta-RMSE/delta-R2 improvement over Week 13 (cell
[3]) and a brand-new design's predicted EUI from raw coefficients (cell [7], the
required transfer check), confirming both match sklearn's own output exactly.
One limitation I found: Fold-to-fold R2 variation and final-test RMSE do not quantify an
individual prediction interval; a separate conformal or bootstrap method is needed.
"""

exit_explanation = """
Adding compactness improves validation modestly: MAE falls 2.5583 to 2.4733 and R2 rises
0.3903 to 0.4258. Paired five-fold checks on development data support that direction;
mean R2 rises from 0.2313 to 0.3225. Only after selecting the specification is the
4-feature model refitted on 112 development rows and evaluated once on 28 untouched
test rows: MAE=1.9881, RMSE=2.5210, R2=0.5167. Its coefficients predict 31.2886 for the
new baseline design. This script cannot provide an individual prediction interval, and
the fold-score range is not one. It also cannot establish causal effects or tell whether
orientation would improve performance without another properly nested selection cycle.
"""

print(ai_use_record)
print(exit_explanation)
print(len(exit_explanation.split()), "words")
