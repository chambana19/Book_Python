# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 14 studio · TRACK A -- INSTRUCTOR SOLUTIONS
Go/no-go classification: confusion matrix, threshold, cross_val_score, model card
Syracuse University · School of Architecture · Fall 2026

TRACK NOTE
  This is the go/no-go track. If your Project 2 decision is "how much" rather than
  "yes/no," use ARC500_Week14B_Instructor_Regression.py instead -- both tracks share the same
  Monday theory and the same dataset, and both feed Week 15's synthesis.
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


# %% [1] Load the shared dataset; recall meets_code and its class balance
# QUESTION           How many of the 140 explored variants meet code, and how many don't?
# INPUTS/ASSUMPTIONS data/radley_portfolio_envelope.csv, the same file Week 13 used;
#                    meets_code = 1 if eui_kwh_m2yr <= 27.0 else 0, already in the CSV
# METHOD             pd.read_csv, then value_counts() on meets_code
# CHECKS/INTERPRET   Expected: 92 rows with meets_code=0 ("no"), 48 rows with
#                    meets_code=1 ("yes") -- 34.3% meet code.

import numpy as np
import pandas as pd

DATA_PATH = Path("data") / "radley_portfolio_envelope.csv"
df = pd.read_csv(DATA_PATH)
print(df.shape)
print(df["meets_code"].value_counts())

share_yes = df["meets_code"].mean()
print("share meeting code:", round(share_yes, 4))
# WHY THIS MATTERS: 34.3% is imbalanced enough to be realistic -- a model that always
# guesses "no" would already be right 65.7% of the time on the full set -- but not so
# extreme that the confusion matrix below becomes degenerate (all one class).


# %% [2] Stratified train/validation/test split, then fit LogisticRegression
# QUESTION           Fit a classifier on meets_code from four design variables. Do the
#                    coefficient signs match Week 13's regression coefficients?
# INPUTS/ASSUMPTIONS features wwr, shade_m, glazing_shgc, compactness; stratify=yc keeps
#                    the ~34%/66% class balance in all three partitions
# METHOD             first reserve 20% as an untouched final test set; split the remaining
#                    80% into 84 training and 28 validation rows; fit ONLY on training
# CHECKS/INTERPRET   Expected train/validation/test rows = 84/28/28; coef_ =
#                    [-1.4322, 1.6772, -0.1674, -0.6965], intercept_ = -0.2802.

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

Xc = df[["wwr", "shade_m", "glazing_shgc", "compactness"]]
yc = df["meets_code"]

Xc_development, Xc_test, yc_development, yc_test = train_test_split(
    Xc, yc, test_size=0.20, random_state=42, stratify=yc)
Xc_train, Xc_validation, yc_train, yc_validation = train_test_split(
    Xc_development, yc_development, test_size=0.25, random_state=42,
    stratify=yc_development)
print("train / validation / untouched test rows:",
      len(Xc_train), len(Xc_validation), len(Xc_test))
assert (len(Xc_train), len(Xc_validation), len(Xc_test)) == (84, 28, 28)

clf = LogisticRegression().fit(Xc_train, yc_train)
print("coef_ [wwr, shade_m, glazing_shgc, compactness]:", clf.coef_.round(4))
print("intercept_:", clf.intercept_.round(4))
# WHY THIS MATTERS: the coefficient directions are consistent with this synthetic
# dataset and Week 13's regression, but they are associations, not proof of causation or
# physical laws. Their magnitudes also are not directly comparable because the features
# use different units and were not standardized.
# COMMON ERROR: looking at Xc_test while choosing features or a threshold. The final 28
# rows remain untouched until cell [9]; cells [3]-[8] use training/validation/development
# data only.


# %% [3] Validation confusion matrix at the default 0.5 threshold
# QUESTION           At the default cutoff, how many of each outcome does the classifier
#                    produce?
# INPUTS/ASSUMPTIONS clf, Xc_validation, yc_validation from cell [2]
# METHOD             clf.predict_proba(Xc_validation)[:, 1] to get P(meets code), then
#                    (proba >= 0.5) as the predicted class, then
#                    sklearn.metrics.confusion_matrix(..., labels=[0, 1])
# CHECKS/INTERPRET   Expected matrix (rows=actual, cols=predicted, order [no, yes]):
#                    [[18, 1], [3, 6]] -- TN=18, FP=1, FN=3, TP=6.

from sklearn.metrics import confusion_matrix

validation_proba = clf.predict_proba(Xc_validation)[:, 1]
pred_05 = (validation_proba >= 0.5).astype(int)

cm_05 = confusion_matrix(yc_validation, pred_05, labels=[0, 1])
print("VALIDATION confusion matrix @ 0.5 [rows=actual(no,yes), cols=predicted(no,yes)]:")
print(cm_05)

tn, fp, fn, tp = cm_05.ravel()
print(f"TN={tn} FP={fp} FN={fn} TP={tp}")
# WHY THIS MATTERS: confusion matrix, defined -- a table of actual class (rows) against
# predicted class (columns). TN/TP are correct calls; FP/FN are the two DIFFERENT ways
# to be wrong, and (see cell [6]) they are not equally costly here.


# %% [4] Hand-compute precision, recall, F1 -- then confirm against sklearn
# QUESTION           From TN=18, FP=1, FN=3, TP=6 alone, what are precision, recall, F1?
# INPUTS/ASSUMPTIONS tn, fp, fn, tp from cell [3]
# METHOD             wrap the three formulas in ONE documented function --
#                    rates_from_counts(tn, fp, fn, tp) -> dict, following the course
#                    convention required on every function since Week 4 (one-line
#                    docstring in triple quotes + type hints) -- because cell [9] needs
#                    the exact same arithmetic at a different threshold. precision =
#                    TP/(TP+FP); recall = TP/(TP+FN); F1 =
#                    2*precision*recall/(precision+recall); then confirm with
#                    sklearn.metrics.precision_score/recall_score/f1_score
# CHECKS/INTERPRET   Expected: precision=0.8571, recall=0.6667, F1=0.7500 -- matches
#                    sklearn to 4 decimals.


def rates_from_counts(tn: int, fp: int, fn: int, tp: int) -> dict:
    """Print and return precision, recall and F1 from four raw confusion counts."""
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)
          if (precision + recall) else 0.0)
    print(f"hand-computed: precision={precision:.4f} recall={recall:.4f} f1={f1:.4f}")
    return {"precision": precision, "recall": recall, "f1": f1}


hand_05 = rates_from_counts(tn, fp, fn, tp)

from sklearn.metrics import precision_score, recall_score, f1_score

precision_skl = precision_score(yc_validation, pred_05)
recall_skl = recall_score(yc_validation, pred_05)
f1_skl = f1_score(yc_validation, pred_05)
print(f"sklearn:       precision={precision_skl:.4f} recall={recall_skl:.4f} f1={f1_skl:.4f}")

assert round(hand_05["precision"], 4) == round(precision_skl, 4)
assert round(hand_05["recall"], 4) == round(recall_skl, 4)
assert round(hand_05["f1"], 4) == round(f1_skl, 4)
print("Hand-compute matches sklearn.")
# WHY THIS MATTERS: "docstring + type hints, recalled" -- tn: int ... tp: int state that
# the four arguments are whole counts, -> dict states that a dictionary comes back, and
# the triple-quoted first line says what the function does. Writing the three formulas
# ONCE means cell [9]'s final test check cannot accidentally use a
# different (or mistyped) denominator than this cell did.
# WHY THIS MATTERS: these are validation results used to choose a decision rule. They are
# not final performance. The untouched test rows get exactly one evaluation in cell [9].
# COMMON ERROR: dividing by (TP+FN) when computing precision, or by (TP+FP) when
# computing recall -- the two denominators are easy to swap under time pressure.


# %% [5] Threshold sweep: same model, only the cutoff on P(meets code) changes
# QUESTION           How do precision, recall, and F1 trade off as the threshold rises?
# INPUTS/ASSUMPTIONS validation_proba from cell [3]; thresholds 0.3-0.7
# METHOD             wrap the whole sweep in ONE documented function,
#                    sweep_thresholds(y_true, proba, cuts) -> pd.DataFrame: loop over the
#                    cutoffs, build one dict of counts+metrics per threshold, and return
#                    them as a DataFrame
# CHECKS/INTERPRET   Expected precision/recall/F1 at each threshold:
#                    0.3 -> 0.533/0.889/0.667; 0.4 -> 0.800/0.889/0.842;
#                    0.5 -> 0.857/0.667/0.750; 0.6 -> 1.000/0.111/0.200;
#                    0.7 -> 0.000/0.000/0.000.

def sweep_thresholds(y_true, proba, cuts: list) -> pd.DataFrame:
    """Score one classifier at several cutoffs; one table row per threshold."""
    records = []
    for t in cuts:
        pred_t = (proba >= t).astype(int)
        cm_t = confusion_matrix(y_true, pred_t, labels=[0, 1])
        tn_t, fp_t, fn_t, tp_t = cm_t.ravel()
        records.append({
            "threshold": t, "TN": tn_t, "FP": fp_t, "FN": fn_t, "TP": tp_t,
            "precision": round(precision_score(y_true, pred_t, zero_division=0), 3),
            "recall": round(recall_score(y_true, pred_t, zero_division=0), 3),
            "F1": round(f1_score(y_true, pred_t, zero_division=0), 3),
        })
    return pd.DataFrame(records)


threshold_sweep = sweep_thresholds(
    yc_validation, validation_proba, [0.3, 0.4, 0.5, 0.6, 0.7])
print(threshold_sweep)

assert len(threshold_sweep) == 5
assert threshold_sweep.loc[threshold_sweep["threshold"] == 0.5, "FP"].iloc[0] == 1
# WHY THIS MATTERS: the sweep is a FUNCTION, not a loop typed once, because Project 2 will
# ask you to rerun it on your own classifier, your own test set, and your own list of
# candidate cutoffs. cuts: list and -> pd.DataFrame say exactly what goes in and what
# comes back.
# WHY THIS MATTERS: as the threshold rises, precision rises (fewer false "go" calls) and
# recall falls (more truly compliant designs missed) -- the standard precision/recall
# trade-off, made concrete on one real confusion matrix instead of an abstract curve.
# COMMON ERROR: at threshold=0.7, TP=0 AND FP=0 (see the printed table above). A raw hand
# formula copied straight from cell [4] -- precision = tp / (tp + fp) -- divides 0 by 0
# and raises ZeroDivisionError; Python does not treat 0/0 as 0. That is exactly why this
# loop calls sklearn's precision_score/recall_score/f1_score with zero_division=0 instead
# of the cell [4] hand formulas. If you hand-compute a threshold sweep yourself, either
# guard the division (precision = tp / (tp + fp) if (tp + fp) else 0.0) or pass
# zero_division=0 to sklearn's metric functions, as done here.


# %% [6] The consequences argument -- choose the operating threshold, in writing
# QUESTION           Given the threshold sweep, which threshold should this classifier
#                    actually operate at?
# INPUTS/ASSUMPTIONS threshold_sweep from cell [5]
# METHOD             name which error direction (false positive vs. false negative) is
#                    dangerous here, then state the chosen threshold and defend it in one
#                    written paragraph. Apply a predeclared validation rule: false-positive
#                    rate <= 10%, then highest recall among qualifying thresholds.
# CHECKS/INTERPRET   0.5 qualifies (validation FPR=1/19=5.3%) and preserves much more
#                    recall than 0.6; the test set remains untouched while this is chosen.

threshold_justification = (
    "A false positive here (the model predicts 'meets code' when the design actually "
    "does not) is the dangerous direction: it means proceeding with a design that then "
    "fails a real code review, triggering real rework. A false negative (the model "
    "predicts 'no-go' when the design would have actually passed) only means an "
    "unnecessarily discarded viable option -- wasteful, not dangerous. Given that "
    "asymmetry, I require a validation false-positive rate no greater than 10%, then "
    "choose the qualifying threshold with the highest recall. Threshold 0.4 narrowly "
    "fails (2/19 = 10.5%); 0.5 qualifies (1/19 = 5.3%) and retains 6/9 compliant "
    "validation designs. Threshold 0.6 also qualifies but retains only 1/9, so its "
    "zero false positives are bought with an unusably large recall loss. The selected "
    "value happens to equal the software default, but it is justified by a stated rule, "
    "not accepted because it is the default. The final test set has not been examined."
)
CHOSEN_THRESHOLD = 0.5
print(threshold_justification)
print("chosen threshold:", CHOSEN_THRESHOLD)
# WHY THIS MATTERS: this is the plan's actual point -- choosing a threshold from real
# consequences, not a default, and not simply the threshold with the best F1. A student
# who reports a threshold without a validation-only rule has not yet made the argument
# the studio requires.


# %% [6b] Figure: the threshold trade-off, with the chosen cutoff drawn on it
# QUESTION           Cell [6] defended 0.5 in a paragraph. Drawn as curves, what does that
#                    cutoff BUY in precision, and what does it PAY in recall?
# INPUTS/ASSUMPTIONS threshold_sweep from cell [5]; CHOSEN_THRESHOLD from cell [6]; the
#                    course figure palette defined below and reused in cell [9b]
# METHOD             plot precision, recall and F1 against the cutoff as three lines, mark
#                    CHOSEN_THRESHOLD with a GREEN dashed ax.axvline(), then ax.annotate()
#                    the precision/recall/F1 that cutoff actually delivers
# CHECKS/INTERPRET   Expected: the GREEN dashed line lands at 0.5, annotated
#                    precision=0.857, recall=0.667, F1=0.750, FP=1 and FN=3 -- the same
#                    numbers cell [5]'s table printed. Saves week14_threshold_sweep.png.

import matplotlib.pyplot as plt

# The course figure palette -- these hex values are used in every ARC 500 figure.
BLUE = "#2E74B5"   # the main series (precision)
AMBER = "#B5731A"  # the contrasting series (recall)
GREEN = "#2E7D5B"  # the chosen, defended value
GRAY = "#5A5F66"   # reference lines, annotation arrows, de-emphasized series

chosen_cut = CHOSEN_THRESHOLD  # 0.5 -- selected on validation by the stated rule
chosen_row = threshold_sweep.loc[threshold_sweep["threshold"] == chosen_cut].iloc[0]
print(f"figure marks cutoff {chosen_cut}: precision={chosen_row['precision']:.3f} "
      f"recall={chosen_row['recall']:.3f} F1={chosen_row['F1']:.3f} "
      f"FP={int(chosen_row['FP'])} FN={int(chosen_row['FN'])}")

fig, ax = plt.subplots(figsize=(9, 5.5))
ax.plot(threshold_sweep["threshold"], threshold_sweep["precision"], color=BLUE,
        marker="o", linewidth=2, label="precision = TP/(TP+FP)")
ax.plot(threshold_sweep["threshold"], threshold_sweep["recall"], color=AMBER,
        marker="s", linewidth=2, label="recall = TP/(TP+FN)")
ax.plot(threshold_sweep["threshold"], threshold_sweep["F1"], color=GRAY,
        marker="^", linewidth=1.6, linestyle=":", label="F1 (balances the two)")
ax.axvline(chosen_cut, color=GREEN, linestyle="--", linewidth=1.8,
           label=f"chosen cutoff = {chosen_cut}")
ax.annotate(f"cutoff {chosen_cut} (chosen in cell [6]):\n"
            f"precision {chosen_row['precision']:.3f}, recall {chosen_row['recall']:.3f}, "
            f"F1 {chosen_row['F1']:.3f}\n"
            f"FP = {int(chosen_row['FP'])}, but {int(chosen_row['FN'])} of "
            f"{int(chosen_row['FN'] + chosen_row['TP'])} compliant designs missed",
            xy=(chosen_cut, chosen_row["precision"]), xytext=(0.365, 0.95), va="top",
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4),
            fontsize=9.5, color=GREEN)

ax.set_title("Which cutoff can you defend -- and what does its precision cost in recall?")
ax.set_xlabel("decision threshold on P(meets_code = 1) (probability, 0-1)")
ax.set_ylabel("precision / recall / F1 (unitless, 0-1)")
ax.set_xticks(list(threshold_sweep["threshold"]))
ax.set_xlim(0.27, 0.73)
ax.set_ylim(-0.05, 1.12)
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="lower left", fontsize=9)  # the one corner the curves never enter
fig.tight_layout()
fig.savefig("week14_threshold_sweep.png", dpi=150)
print("saved week14_threshold_sweep.png")
# WHY THIS MATTERS: nothing is refit anywhere in this figure -- clf.coef_ is identical at
# every point on every line. Only the cutoff moves, so the whole picture is one model's
# decision RULE being chosen, which is exactly the thing cell [6] wrote a paragraph about.
# WHY THIS MATTERS: this entire figure is validation evidence. It chooses the rule but
# cannot estimate final performance. At 0.5, one of 19 non-compliant validation designs
# is wrongly cleared and three of nine compliant designs are missed. Moving to 0.6
# removes that one false positive but misses eight of nine compliant designs.
# COMMON ERROR: setting CHOSEN_THRESHOLD to a value that is not in cell [5]'s cuts list
# (0.55, say). threshold_sweep has no row for it, so .iloc[0] on an empty selection raises
# IndexError: single positional indexer is out-of-bounds -- add your cutoff to the cuts
# list in cell [5] first, so the sweep actually scores it.
# COMMON ERROR: reading the collapse to 0.000 at cutoff 0.7 as "precision got worse."
# At 0.7 the model calls NOTHING "go" (TP=0, FP=0), so precision is undefined and
# cell [5]'s zero_division=0 reports it as 0.000 by convention -- see cell [5]'s WARNING.


# %% [7] Cross-validation on development data only
# QUESTION           Is default-threshold accuracy stable across the 112 development rows?
# INPUTS/ASSUMPTIONS Xc_development, yc_development; the 28 final test rows stay excluded
# METHOD             shuffled, stratified 5-fold cross_val_score at the default 0.5 rule
# CHECKS/INTERPRET   Expected scores [0.7826, 0.6957, 0.8636, 0.6364, 0.8182],
#                    mean=0.7593. This does NOT validate the selected threshold.

from sklearn.model_selection import StratifiedKFold, cross_val_score

development_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(
    LogisticRegression(), Xc_development, yc_development,
    cv=development_cv, scoring="accuracy")
print("development-only 5-fold accuracy @ default 0.5:", cv_scores.round(4))
print("mean:", round(cv_scores.mean(), 4))
assert round(cv_scores.mean(), 4) == 0.7593
# WHY THIS MATTERS: this is a useful stability diagnostic for the model class at 0.5,
# but it is not evidence for the chosen operating rule at other thresholds. Evaluating a
# tuned threshold by cross-validation requires out-of-fold probabilities and applying
# that fixed rule inside every fold. Most importantly, the final test rows remain absent.


# %% [8] AI-generated code audit
# QUESTION           Would you accept this AI-suggested "evaluate the classifier"
#                    function as-is?
# INPUTS/ASSUMPTIONS ai_evaluate_classifier as shown; validation data from cell [2]
# METHOD             list at least four specific defects, then compare with cells [3]-[6]
# CHECKS/INTERPRET   A defensible list names the default-threshold, hidden-recall,
#                    imbalance, and no-model-card defects -- not merely that the code
#                    "looks wrong."

def ai_evaluate_classifier(clf, X_eval, y_eval):
    preds = clf.predict(X_eval)
    acc = (preds == y_eval).mean()
    print(f"Model is {acc:.1%} accurate -- ready to use!")
    return acc

ai_evaluate_classifier(clf, Xc_validation, yc_validation)

ai_defects = [
    "clf.predict() silently uses the default 0.5 threshold with no threshold reasoning "
    "at all -- cell [6]'s consequences argument never gets a chance to apply.",
    "Reporting accuracy alone hides recall entirely: cell [4] shows validation recall="
    "0.6667 at this same threshold, invisible from the accuracy number alone.",
    "The 85.7% validation accuracy must be compared with the naive 'always guess no' "
    "baseline of 19/28=67.9%; neither number is final test performance.",
    "'Ready to use!' with no model card, no stated operating threshold, and no mention "
    "of the training ranges this model should not be trusted outside of.",
]

for defect in ai_defects:
    print("-", defect)
# WHY THIS MATTERS: every one of these four defects is individually plausible and easy
# to accept under time pressure, especially since the printed accuracy number (71.4%)
# sounds respectable on its own. This is why a classifier is never reported by accuracy
# alone and why validation evidence must not be mislabeled as final test evidence.


# %% [9] Final evaluation: use the untouched test set exactly once
# QUESTION           After freezing the 0.5 operating threshold, how well does it transfer
#                    to genuinely untouched rows?
# INPUTS/ASSUMPTIONS clf fitted on 84 training rows; threshold selected on 28 validation
#                    rows; Xc_test/yc_test have not appeared in cells [3]-[8]
# METHOD             predict probabilities once, apply the frozen threshold, compute raw
#                    counts and rates, and do not revise the threshold afterward
# CHECKS/INTERPRET   Expected TN=16, FP=2, FN=8, TP=2; precision=0.5000,
#                    recall=0.2000, F1=0.2857.

test_proba = clf.predict_proba(Xc_test)[:, 1]
test_pred_chosen = (test_proba >= CHOSEN_THRESHOLD).astype(int)
cm_test = confusion_matrix(yc_test, test_pred_chosen, labels=[0, 1])
tn_test, fp_test, fn_test, tp_test = cm_test.ravel()

print(f"FINAL TEST @ {CHOSEN_THRESHOLD}: TN={tn_test} FP={fp_test} "
      f"FN={fn_test} TP={tp_test}")
test_rates = rates_from_counts(tn_test, fp_test, fn_test, tp_test)

assert (tn_test, fp_test, fn_test, tp_test) == (16, 2, 8, 2)
assert abs(test_rates["precision"] - precision_score(yc_test, test_pred_chosen)) < 1e-9
assert abs(test_rates["recall"] - recall_score(yc_test, test_pred_chosen)) < 1e-9
assert abs(test_rates["f1"] - f1_score(yc_test, test_pred_chosen)) < 1e-9
print("Final-test check passed. Threshold remains frozen despite weaker transfer.")
# WHY THIS MATTERS: validation precision 0.857 did not guarantee final-test precision;
# it fell to 0.500 on only 28 test rows. That gap is sampling uncertainty, not permission
# to tune on the test set. Report it, keep the threshold fixed, and require real code
# simulation/review before any consequential go/no-go decision.


# %% [9b] Figure: the confusion matrix at the chosen cutoff, as a heatmap
# QUESTION           At the frozen cutoff, where do the 28 untouched test
#                    designs land -- and which of the two error cells is the dangerous one?
# INPUTS/ASSUMPTIONS cm_test and test_rates from cell [9]; chosen_cut and palette from cell
#                    [6b]; rows are the ACTUAL class, columns the PREDICTED class, order
#                    [no-go (0), go (1)] -- the same layout as cell [3]'s printed matrix
# METHOD             ax.imshow() the 2x2 counts as a colour field, write each count INTO its
#                    own cell with ax.text(), pick each cell's text colour from that cell's
#                    own background brightness (white on dark, near-black on light), add a
#                    labelled colorbar, then annotate the FP cell -- the one cell [6]'s
#                    consequences argument is really about
# CHECKS/INTERPRET   Expected: TN=16, FP=2, FN=8, TP=2; precision=0.5000 and
#                    recall=0.2000 recomputed from the drawn cells equal cell [9].
#                    Saves week14_confusion_matrix.png.

cm_chosen = cm_test  # final test matrix at the frozen cutoff -- not refit or retuned here
tn_c, fp_c, fn_c, tp_c = cm_chosen.ravel()

# Guarded division, the cell [5] lesson reused: a cutoff strict enough to call nothing "go"
# makes both denominators zero, and Python does not treat 0/0 as 0.
precision_c = tp_c / (tp_c + fp_c) if (tp_c + fp_c) else 0.0
recall_c = tp_c / (tp_c + fn_c) if (tp_c + fn_c) else 0.0
print(f"figure draws cutoff {chosen_cut}: TN={tn_c} FP={fp_c} FN={fn_c} TP={tp_c}")
print(f"recomputed from the drawn cells: precision={precision_c:.4f} recall={recall_c:.4f}")

assert round(precision_c, 4) == round(test_rates["precision"], 4)
assert round(recall_c, 4) == round(test_rates["recall"], 4)
print("Figure agrees with cell [9]'s hand-computed rates.")

fig, ax = plt.subplots(figsize=(9, 5.5))
im = ax.imshow(cm_chosen, cmap="Blues", vmin=0, vmax=max(cm_chosen.max(), 1), aspect="auto")
cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.set_label("designs in this cell (count, of 28 untouched test designs)")

cell_labels = [["TN", "FP"], ["FN", "TP"]]
cell_meaning = [["correctly discarded", "false 'go' -- dangerous"],
                ["wasted option", "correctly approved"]]
for i in range(2):          # i = actual class (row):    0 = no-go, 1 = go
    for j in range(2):      # j = predicted class (col): 0 = no-go, 1 = go
        count = cm_chosen[i, j]
        # im.norm() maps a count to 0-1 on the colour scale; im.cmap() turns that into the
        # cell's actual RGBA. The 0.299/0.587/0.114 weights are the standard luminance
        # formula, so dark cells get white text and light cells get near-black text.
        r_col, g_col, b_col, _ = im.cmap(im.norm(count))
        brightness = 0.299 * r_col + 0.587 * g_col + 0.114 * b_col
        text_color = "white" if brightness < 0.55 else "#1A1A1A"
        ax.text(j, i - 0.09, f"{cell_labels[i][j]} = {count}", ha="center", va="center",
                color=text_color, fontsize=14, fontweight="bold")
        ax.text(j, i + 0.05, cell_meaning[i][j], ha="center", va="center",
                color=text_color, fontsize=9.5)

# The FP cell is the one cell [6]'s consequences argument is really about, so it is the
# cell that gets the arrow. Its wording follows the count, so this figure stays honest at
# any cutoff -- including one where FP is not zero.
fp_note = ("zero false 'go'\ncalls on this final test"
           if fp_c == 0 else
           "designs cleared to 'go'\nthat actually fail code --\nthe dangerous error")
ax.annotate(f"FP = {fp_c}: {fp_note}",
            xy=(1.48, 0), xytext=(1.62, -0.18), ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4), fontsize=9.5, color=GREEN)
ax.text(1.62, 1.0, f"the price: FN = {fn_c}\nrecall {recall_c:.3f} -- {fn_c} of "
        f"{fn_c + tp_c}\ncompliant designs missed",
        ha="left", va="center", fontsize=9.5, color=AMBER)

ax.set_title(f"At the chosen {chosen_cut} cutoff, which way does this classifier "
             f"get it wrong?")
ax.set_xlabel("predicted class (meets_code: no-go = 0, go = 1)")
ax.set_ylabel("actual class (meets_code: no-go = 0, go = 1)")
ax.set_xticks([0, 1], labels=["predicted: no-go (0)", "predicted: go (1)"])
ax.set_yticks([0, 1], labels=["actual:\nno-go (0)", "actual:\ngo (1)"])
ax.set_xlim(-0.5, 2.8)   # the empty band on the right is where the annotations live
ax.set_ylim(1.5, -0.5)   # row 0 on top, matching how the matrix prints in the console
ax.grid(False)           # a heatmap's cells ARE the grid; gridlines would cross the counts
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig("week14_confusion_matrix.png", dpi=150)
print("saved week14_confusion_matrix.png")
# WHY THIS MATTERS: cell [3]'s matrix was validation evidence used to choose the rule;
# this is a different matrix on the final test rows. Validation [[18, 1], [3, 6]] became
# test [[16, 2], [8, 2]]. The performance drop must be reported, not repaired by moving
# the threshold after seeing test labels.
# WHY THIS MATTERS: the colour scale is the reason each count needs its own text colour.
# TN=16 sits at the dark end of Blues, so white text is the readable choice; FP=2
# sits at the near-white end, where white text would vanish. Computing the choice from the
# cell's own brightness means the figure stays readable even if your counts change.
# COMMON ERROR: calling confusion_matrix(pred, y_true) with the arguments swapped. Nothing
# raises -- you get the TRANSPOSE, which silently exchanges FP with FN. The figure then
# reads "9 designs wrongly cleared to go, 0 viable options missed," the exact opposite of
# the truth, and cell [6]'s whole consequences argument inverts with it.
# COMMON ERROR: leaving ax.grid(alpha=0.3) on from the other figures in this handout. The
# gridlines land at the tick positions -- the centres of the cells -- and strike straight
# through the four counts this figure exists to show.


# %% [10] Track A model card
# QUESTION           What does a one-page model card say about scope, threshold, and
#                    limits for this classifier?
# INPUTS/ASSUMPTIONS cells [1]-[9]
# METHOD             fill in one dictionary, one entry per required field
# CHECKS/INTERPRET   Every field below must be filled in with a real, specific value --
#                    not a placeholder.

model_card_track_a = {
    "scope": "fitted on 84 of 140 synthetic Radley Hall portfolio variants; wwr 0.20-0.60, "
             "shade_m 0.0-1.2, glazing_shgc 0.25-0.65, compactness 0.8-1.4, 4 "
             "orientation categories (not used as a feature here).",
    "selection rule": "on 28 validation rows, require false-positive rate <=10%, then "
             "maximize recall; this selects threshold 0.5 (validation FPR=1/19=5.3%).",
    "final test performance": "at frozen threshold 0.5 on 28 untouched rows: TN=16, "
             "FP=2, FN=8, TP=2; precision=0.500, recall=0.200, F1=0.286. Validation "
             "performance was better, so do not present it as final performance.",
    "development stability": "5-fold default-threshold accuracy on the 112 development "
             "rows ranges 0.6364-0.8636, mean 0.7593; this is variability in accuracy, "
             "not a confidence interval and not validation of other thresholds.",
    "do not trust": "predictions for designs outside the ranges stated in 'scope' above "
             "(see Week 13's silent-extrapolation note).",
}

for field, value in model_card_track_a.items():
    print(f"{field}: {value}")
# WHY THIS MATTERS: this model card IS this week's Project 2 evaluated-prediction
# checkpoint for the go/no-go track. Week 15 may reuse the frozen threshold only with
# this weaker final-test evidence and an independent simulation/code-review safeguard.


# %% [11] AI-use record and exit reflection
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished classifier in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing this
#                    script cannot tell you.

ai_use_record = """
Tool/model: Example assistant
Prompt: Write a function that evaluates a fitted LogisticRegression classifier and tells
me if it's good enough to use.
Suggestion received: ai_evaluate_classifier(), exactly as shown in cell [8] -- default
threshold, accuracy only, "ready to use!" with no other context.
What I accepted: The idea of wrapping evaluation in one small function, and the general
predict_proba() >= threshold pattern.
What I modified and why: Reserved a final test set before fitting, computed
precision/recall/F1 at multiple thresholds on validation rows only, and selected 0.5 by
a predeclared rule: validation false-positive rate <=10%, then highest recall. Added the
naive "always guess no" comparison to show accuracy alone is not a strong claim.
What I rejected and why: The "ready to use!" framing -- a single accuracy number, at an
unexamined default threshold, is not sufficient evidence to deploy a go/no-go classifier
whose false positives carry real construction-rework cost.
How I tested it: Hand-computed validation rates in cell [4], froze the threshold, then
evaluated it once on 28 untouched test rows in cell [9] and confirmed the raw counts and
sklearn metrics agree.
One limitation I found: Final-test precision=0.500 and recall=0.200 are much weaker than
validation, so this small classifier may rank candidates for review but cannot replace
a real code-compliance check.
"""

exit_explanation = """
This classifier predicts meets_code from wwr, shade_m, glazing_shgc, and compactness.
The classifier is fitted on 84 training rows, while 28 validation rows choose the
operating rule and 28 final rows remain untouched. Requiring validation false-positive
rate <=10%, then maximizing recall, selects threshold 0.5: validation precision=0.857,
recall=0.667. Once frozen, that rule transfers poorly to the final test: TN=16, FP=2,
FN=8, TP=2, so precision=0.500, recall=0.200, and F1=0.286. Development-only five-fold
accuracy also varies from 0.636 to 0.864. This evidence supports using the classifier to
rank candidates for simulation, not to certify compliance. The script cannot show that
the probability estimates are calibrated or that results transfer to another building
type or code cycle.
"""

print(ai_use_record)
print(exit_explanation)
print(len(exit_explanation.split()), "words")
