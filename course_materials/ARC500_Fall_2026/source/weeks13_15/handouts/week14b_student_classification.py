# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 14 studio · TRACK A -- go/no-go classification
Confusion matrix, threshold, cross_val_score, model card
Syracuse University · School of Architecture · Fall 2026

TRACK NOTE
  This is the go/no-go track. If your Project 2 decision is "how much" rather than
  "yes/no," use ARC500_Week14B_Student_Regression.py instead -- both tracks share Monday's
  theory and the same dataset, and both feed Week 15's synthesis.

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week14 module folder, with radley_portfolio_envelope.csv
     inside a data/ subfolder next to it (data/radley_portfolio_envelope.csv).
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict a result BEFORE running each cell, especially cells [3]-[5].
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A classifier is not reported by accuracy alone. Precision, recall, and F1, hand-computed
  from the raw confusion-matrix counts, and a stated operating threshold with a written
  consequences argument, are all required before a classifier is "done."
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

# TODO: If your shape does not print (140, 9), check DATA_PATH before anything else.


# %% [2] Stratified train/validation/test split, then fit LogisticRegression
# QUESTION           Fit a classifier on meets_code from four design variables. Do the
#                    coefficient signs match Week 13's regression coefficients?
# INPUTS/ASSUMPTIONS features wwr, shade_m, glazing_shgc, compactness; stratify=yc keeps
#                    the ~34%/66% class balance in all three partitions
# METHOD             reserve 20% as final test; split the remaining 80% into training and
#                    validation; fit ONLY on training
# CHECKS/INTERPRET   Expected train/validation/test rows=84/28/28; coef_ =
#                    [-1.4322, 1.6772, -0.1674, -0.6965], intercept_=-0.2802.

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

Xc = df[["wwr", "shade_m", "glazing_shgc", "compactness"]]
yc = df["meets_code"]

# TODO: make the two stratified splits, e.g.
# Xc_development, Xc_test, yc_development, yc_test = train_test_split(
#     Xc, yc, test_size=0.20, random_state=42, stratify=yc)
# Xc_train, Xc_validation, yc_train, yc_validation = train_test_split(
#     Xc_development, yc_development, test_size=0.25, random_state=42,
#     stratify=yc_development)
raise NotImplementedError(
    "Cell [2] incomplete: create disjoint fit/validation/final-test data before fitting."
)

# TODO: fit clf = LogisticRegression().fit(Xc_train, yc_train)
raise NotImplementedError(
    "Cell [2] incomplete: fit the classifier on fit rows only."
)

# TODO: print/assert 84 training, 28 validation, 28 untouched test rows.
print("coef_:", clf.coef_.round(4) if clf is not None else "TODO")
print("intercept_:", clf.intercept_.round(4) if clf is not None else "TODO")

# TODO: Compare coefficient directions with Week 13, but state that these fitted
# associations are not causal effects and magnitudes are not comparable across units.


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

# TODO: compute validation_proba = clf.predict_proba(Xc_validation)[:, 1], e.g.
# validation_proba = clf.predict_proba(Xc_validation)[:, 1]
raise NotImplementedError(
    "Cell [3] incomplete: calculate probability scores on the requested held-back rows."
)

# TODO: pred_05 = (validation_proba >= 0.5).astype(int)
raise NotImplementedError(
    "Cell [3] incomplete: threshold the probability scores before continuing."
)

# TODO: cm_05 = confusion_matrix(yc_validation, pred_05, labels=[0, 1]); print it
raise NotImplementedError(
    "Cell [3] incomplete: compute the confusion matrix before continuing."
)
print(cm_05 if cm_05 is not None else "TODO")

# TODO: unpack tn, fp, fn, tp = cm_05.ravel() and print them


# %% [4] Hand-compute precision, recall, F1 -- then confirm against sklearn
# QUESTION           From TN=18, FP=1, FN=3, TP=6 alone, what are precision, recall, F1?
# INPUTS/ASSUMPTIONS tn, fp, fn, tp from cell [3]
# METHOD             the three formulas are wrapped in ONE documented function below --
#                    rates_from_counts(tn, fp, fn, tp) -> dict -- because cell [9] needs
#                    the exact same arithmetic at a different threshold. It follows the
#                    course convention required on every function since Week 4: a one-line
#                    docstring in triple quotes, plus type hints (tn: int ... -> dict).
#                    Read it, then call it; do not retype the formulas anywhere else.
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


# TODO: once cell [3] gives you tn/fp/fn/tp, call the helper, e.g.
# hand_05 = rates_from_counts(tn, fp, fn, tp)

from sklearn.metrics import precision_score, recall_score, f1_score

# TODO: compute precision_skl, recall_skl, f1_skl using validation labels, e.g.
# precision_skl = precision_score(yc_validation, pred_05)

# TODO: assert your hand values match the sklearn values, rounded to 4 decimals, e.g.
# assert round(hand_05["precision"], 4) == round(precision_skl, 4)

print("Self-check cell reached")


# %% [5] Threshold sweep: same model, only the cutoff on P(meets code) changes
# QUESTION           How do precision, recall, and F1 trade off as the threshold rises?
# INPUTS/ASSUMPTIONS validation_proba from cell [3]; thresholds 0.3-0.7
# METHOD             the sweep is wrapped in ONE documented function for you,
#                    sweep_thresholds(y_true, proba, cuts) -> pd.DataFrame; fill in its
#                    loop body so each cutoff appends one dict of counts+metrics
# CHECKS/INTERPRET   Expected precision/recall/F1 at each threshold:
#                    0.3 -> 0.533/0.889/0.667; 0.4 -> 0.800/0.889/0.842;
#                    0.5 -> 0.857/0.667/0.750; 0.6 -> 1.000/0.111/0.200;
#                    0.7 -> 0.000/0.000/0.000.
# WARNING            At threshold=0.7, TP=0 AND FP=0. Do NOT reuse cell [4]'s raw hand
#                    formula (precision = tp / (tp + fp)) unguarded inside this loop --
#                    0/0 raises ZeroDivisionError in real Python, it does not quietly
#                    become 0. Either guard it yourself, e.g.
#                    precision = tp_t / (tp_t + fp_t) if (tp_t + fp_t) else 0.0, or use
#                    sklearn's precision_score(..., zero_division=0) /
#                    recall_score(..., zero_division=0) / f1_score(..., zero_division=0)
#                    for this cell instead of the cell [4] hand formulas.

def sweep_thresholds(y_true, proba, cuts: list) -> pd.DataFrame:
    """Score one classifier at several cutoffs; one table row per threshold."""
    records = []
    for t in cuts:
        # TODO: predict at this threshold, build the confusion matrix, and append one dict
        # of {"threshold": t, "TN":..., "FP":..., "FN":..., "TP":..., "precision":...,
        # "recall":..., "F1":...} to records. Example to complete:
        # pred_t = (proba >= t).astype(int)
        # cm_t = confusion_matrix(y_true, pred_t, labels=[0, 1])
        # tn_t, fp_t, fn_t, tp_t = cm_t.ravel()
        # precision_t = precision_score(y_true, pred_t, zero_division=0)  # NOT tp_t/(tp_t+fp_t)
        # recall_t = recall_score(y_true, pred_t, zero_division=0)
        # f1_t = f1_score(y_true, pred_t, zero_division=0)
        # records.append({...})
        raise NotImplementedError(
            "Cell [5] incomplete: append the metrics for every candidate threshold."
        )
    return pd.DataFrame(records)


threshold_sweep = sweep_thresholds(
    yc_validation, validation_proba, [0.3, 0.4, 0.5, 0.6, 0.7])
print(threshold_sweep)

# TODO: Confirm threshold_sweep has 5 rows once the loop body above is filled in, e.g.
# assert len(threshold_sweep) == 5
# TODO: verify threshold 0.5 has validation FP=1 and FPR=1/19=5.3%.


# %% [6] The consequences argument -- choose the operating threshold, in writing
# QUESTION           Given the threshold sweep, which threshold should this classifier
#                    actually operate at?
# INPUTS/ASSUMPTIONS threshold_sweep from cell [5]
# METHOD             predeclare: validation FPR <=10%, then highest recall among qualifying
# CHECKS/INTERPRET   0.5 qualifies; 0.4 narrowly fails and 0.6 sacrifices too much recall.

threshold_justification = (
    "TODO: state which error direction (false positive or false negative) is dangerous "
    "here and why, then state your chosen threshold and defend it using that reasoning -- "
    "not by pointing at whichever threshold has the highest F1."
)
CHOSEN_THRESHOLD = None  # TODO: set this to the threshold you defend above
if CHOSEN_THRESHOLD is None:
    raise NotImplementedError(
        "Cell [6] incomplete: set the validation-selected threshold and defend it."
    )
print(threshold_justification)
print("chosen threshold:", CHOSEN_THRESHOLD)


# %% [6b] Figure: the threshold trade-off, with the chosen cutoff drawn on it
# QUESTION           Cell [6] defended 0.5 in a paragraph. Drawn as curves, what does that
#                    cutoff BUY in precision, and what does it PAY in recall?
# INPUTS/ASSUMPTIONS threshold_sweep from cell [5]; CHOSEN_THRESHOLD from cell [6]; the
#                    course figure palette defined below and reused in cell [9b]
# METHOD             plot precision, recall and F1 against the cutoff as three lines, mark
#                    your chosen cutoff with a GREEN dashed ax.axvline(), then ax.annotate()
#                    the precision/recall/F1 that cutoff actually delivers
# CHECKS/INTERPRET   Expected once cells [5] and [6]'s TODOs are done. Their completion
#                    gates now stop this figure rather than drawing plausible-looking zeros:
#                    the GREEN dashed line lands at 0.5, annotated precision=.857,
#                    recall=.667, F1=.750, FP=1 and FN=3 -- the same numbers cell [5]'s
#                    table printed.
#                    Saves week14_threshold_sweep.png.

import matplotlib.pyplot as plt

# The course figure palette -- these hex values are used in every ARC 500 figure.
BLUE = "#2E74B5"   # the main series (precision)
AMBER = "#B5731A"  # the contrasting series (recall)
GREEN = "#2E7D5B"  # the chosen, defended value
GRAY = "#5A5F66"   # reference lines, annotation arrows, de-emphasized series

if threshold_sweep.empty:
    raise NotImplementedError(
        "Cell [5] incomplete: threshold_sweep has no real validation results."
    )
sweep_plot = threshold_sweep
chosen_cut = CHOSEN_THRESHOLD
if chosen_cut not in set(sweep_plot["threshold"]):
    raise ValueError("CHOSEN_THRESHOLD must be one of the evaluated validation cutoffs")

chosen_row = sweep_plot.loc[sweep_plot["threshold"] == chosen_cut].iloc[0]
print(f"figure marks cutoff {chosen_cut}: precision={chosen_row['precision']:.3f} "
      f"recall={chosen_row['recall']:.3f} F1={chosen_row['F1']:.3f} "
      f"FP={int(chosen_row['FP'])} FN={int(chosen_row['FN'])}")

fig, ax = plt.subplots(figsize=(9, 5.5))
# The precision line is drawn for you as the pattern to copy.
ax.plot(sweep_plot["threshold"], sweep_plot["precision"], color=BLUE,
        marker="o", linewidth=2, label="precision = TP/(TP+FP)")
# TODO: add the other two lines, following the pattern above -- recall in AMBER
# (marker="s", linewidth=2, label="recall = TP/(TP+FN)") and F1 in GRAY
# (marker="^", linewidth=1.6, linestyle=":", label="F1 (balances the two)").

# TODO: mark your chosen cutoff with a GREEN dashed vertical line, e.g.
# ax.axvline(chosen_cut, color=GREEN, linestyle="--", linewidth=1.8,
#            label=f"chosen cutoff = {chosen_cut}")

# TODO: annotate what that cutoff actually delivers, so the reader never has to guess
# which mark is the answer, e.g.
# ax.annotate(f"cutoff {chosen_cut}: precision {chosen_row['precision']:.3f}, "
#             f"recall {chosen_row['recall']:.3f}, F1 {chosen_row['F1']:.3f}",
#             xy=(chosen_cut, chosen_row["precision"]), xytext=(0.365, 0.95), va="top",
#             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4),
#             fontsize=9.5, color=GREEN)

ax.set_title("Which cutoff can you defend -- and what does its precision cost in recall?")
ax.set_xlabel("decision threshold on P(meets_code = 1) (probability, 0-1)")
ax.set_ylabel("precision / recall / F1 (unitless, 0-1)")
ax.set_xticks(list(sweep_plot["threshold"]))
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
# decision RULE being chosen, which is exactly the thing cell [6] asks you to argue for.
# WHY THIS MATTERS: at 0.5 one of 19 non-compliant validation designs is wrongly cleared
# and three of nine compliant designs are missed. Moving to 0.6 removes one FP but misses
# eight of nine compliant designs. The chosen point follows the stated constraint, not a
# default or a peek at the final test.
# COMMON ERROR: setting CHOSEN_THRESHOLD to a value that is not in cell [5]'s cuts list
# (0.55, say). sweep_plot has no row for it, so .iloc[0] on an empty selection raises
# IndexError: single positional indexer is out-of-bounds -- add your cutoff to the cuts
# list in cell [5] first, so the sweep actually scores it.
# COMMON ERROR: reading the collapse to 0.000 at cutoff 0.7 as "precision got worse."
# At 0.7 the model calls NOTHING "go" (TP=0, FP=0), so precision is undefined and
# zero_division=0 reports it as 0.000 by convention -- see cell [5]'s WARNING.


# %% [7] Cross-validation on development data only
# QUESTION           Is default-threshold accuracy stable across development folds?
# INPUTS/ASSUMPTIONS Xc_development, yc_development; final test remains excluded
# METHOD             shuffled StratifiedKFold(5, random_state=42), scoring="accuracy"
# CHECKS/INTERPRET   [.7826,.6957,.8636,.6364,.8182], mean=.7593. This is not a
#                    confidence interval and does not validate thresholds other than 0.5.

from sklearn.model_selection import StratifiedKFold, cross_val_score

# TODO: development_cv = StratifiedKFold(5, shuffle=True, random_state=42)
# cv_scores = cross_val_score(LogisticRegression(), Xc_development, yc_development,
#                             cv=development_cv, scoring="accuracy")
raise NotImplementedError(
    "Cell [7] incomplete: compute the stated cross-validation evidence."
)
print(cv_scores if cv_scores is not None else "TODO")


# %% [8] AI-generated code audit
# QUESTION           Would you accept this AI-suggested "evaluate the classifier"
#                    function as-is?
# INPUTS/ASSUMPTIONS ai_evaluate_classifier as shown; validation data from cell [2]
# METHOD             list at least four specific defects, then compare with cells [3]-[6]
# CHECKS/INTERPRET   A defensible list names the default-threshold, hidden-recall,
#                    imbalance, and no-model-card defects -- not merely that the code
#                    "looks wrong."

def ai_evaluate_classifier(clf, X_test, yc_test):
    preds = clf.predict(X_test)
    acc = (preds == yc_test).mean()
    print(f"Model is {acc:.1%} accurate -- ready to use!")
    return acc

if clf is not None and Xc_validation is not None:
    ai_evaluate_classifier(clf, Xc_validation, yc_validation)
else:
    print("TODO: complete cell [2]'s split/fit before running the AI-audit function.")

ai_defects = [
    # TODO: add at least four specific defects
]

for defect in ai_defects:
    print("-", defect)


# %% [9] Final evaluation: open the untouched test set once
# QUESTION           How does the frozen validation-selected threshold transfer?
# INPUTS/ASSUMPTIONS Xc_test/yc_test have not appeared in cells [3]-[8]
# METHOD             predict once, apply CHOSEN_THRESHOLD, report counts and rates; do not
#                    revise the threshold after seeing these labels
# CHECKS/INTERPRET   At frozen 0.5: TN=16, FP=2, FN=8, TP=2; precision=.500,
#                    recall=.200, F1=.286.

# TODO: test_proba = clf.predict_proba(Xc_test)[:, 1]
# test_pred_chosen = (test_proba >= CHOSEN_THRESHOLD).astype(int)
# cm_test = confusion_matrix(yc_test, test_pred_chosen, labels=[0, 1])
# tn_test, fp_test, fn_test, tp_test = cm_test.ravel()

# TODO: call the SAME helper, e.g.
# test_rates = rates_from_counts(tn_test, fp_test, fn_test, tp_test)

# TODO: assert the counts are (16,2,8,2) and hand rates match sklearn. Do not retune.

print("Self-check cell reached")


# %% [9b] Figure: the confusion matrix at the chosen cutoff, as a heatmap
# QUESTION           At the frozen cutoff, where do the 28 untouched test
#                    designs land -- and which of the two error cells is the dangerous one?
# INPUTS/ASSUMPTIONS cm_test from cell [9]; chosen_cut and the palette from cell [6b]; rows
#                    are the ACTUAL class, columns the PREDICTED class, order
#                    [no-go (0), go (1)] -- the same layout as cell [3]'s printed matrix
# METHOD             ax.imshow() the 2x2 counts as a colour field, write each count INTO its
#                    own cell with ax.text(), pick each cell's text colour from that cell's
#                    own background brightness (white on dark, near-black on light), add a
#                    labelled colorbar, then annotate the FP cell -- the one cell [6]'s
#                    consequences argument is really about
# CHECKS/INTERPRET   Expected once cell [9]'s TODOs are done and cm_chosen is set to
#                    your own cm_test: TN=16, FP=2, FN=8, TP=2; precision=.500,
#                    recall=.200.
#                    Saves week14_confusion_matrix.png.

# TODO: once cell [9] builds cm_test, plot THAT matrix, e.g. cm_chosen = cm_test
raise NotImplementedError(
    "Cell [9b] incomplete: use the real confusion matrix at the frozen threshold."
)
tn_c, fp_c, fn_c, tp_c = cm_chosen.ravel()

# Guarded division, the cell [5] lesson reused: a cutoff strict enough to call nothing "go"
# makes both denominators zero, and Python does not treat 0/0 as 0.
precision_c = tp_c / (tp_c + fp_c) if (tp_c + fp_c) else 0.0
recall_c = tp_c / (tp_c + fn_c) if (tp_c + fn_c) else 0.0
print(f"figure draws cutoff {chosen_cut}: TN={tn_c} FP={fp_c} FN={fn_c} TP={tp_c}")
print(f"recomputed from the drawn cells: precision={precision_c:.4f} recall={recall_c:.4f}")

# TODO: once cm_chosen is real, add two asserts proving the figure cannot disagree with the
# numbers cell [9] printed, e.g.
# assert round(precision_c, 4) == round(test_rates["precision"], 4)
# assert round(recall_c, 4) == round(test_rates["recall"], 4)

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
        # The count goes INSIDE its own cell, with the meaning on a second line below it.
        ax.text(j, i - 0.09, f"{cell_labels[i][j]} = {count}", ha="center", va="center",
                color=text_color, fontsize=14, fontweight="bold")
        ax.text(j, i + 0.05, cell_meaning[i][j], ha="center", va="center",
                color=text_color, fontsize=9.5)

# The FP cell is the one cell [6]'s consequences argument is really about, so it is the
# cell that gets the arrow. Its wording follows the count, so this figure stays honest at
# any cutoff -- including one where FP is not zero.
fp_note = ("zero false 'go'\ncalls -- exactly what\ncell [6]'s argument asks for"
           if fp_c == 0 else
           "designs cleared to 'go'\nthat actually fail code --\nthe dangerous error")

# TODO: annotate the FP cell -- the one cell [6]'s consequences argument is really about --
# and name the recall it costs, e.g.
# ax.annotate(f"FP = {fp_c}: {fp_note}",
#             xy=(1.48, 0), xytext=(1.62, -0.18), ha="left", va="center",
#             arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.4),
#             fontsize=9.5, color=GREEN)
# ax.text(1.62, 1.0, f"the price: FN = {fn_c}\nrecall {recall_c:.3f} -- {fn_c} of "
#         f"{fn_c + tp_c}\ncompliant designs missed",
#         ha="left", va="center", fontsize=9.5, color=AMBER)

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
# WHY THIS MATTERS: this is cell [3]'s table with colour and position added, drawn at the
# frozen on validation. Compare validation [[18,1],[3,6]] with final test
# [[16,2],[8,2]]. Report the weaker transfer; never move the threshold to repair test.
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
    "scope": "TODO: n, feature ranges, orientation categories used/not used",
    "selection rule": "TODO: validation FPR<=10%, then highest recall; selected threshold",
    "final test performance": "TODO: counts and precision/recall/F1 at frozen threshold",
    "development stability": "TODO: 5-fold default-threshold accuracy range and mean; "
                             "state what it does not measure",
    "do not trust": "TODO: name the training ranges this model should not be trusted "
                    "outside of",
}

for field, value in model_card_track_a.items():
    print(f"{field}: {value}")

# TODO: Replace every "TODO: ..." value with your own specific, real entry.


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
1. the validation confusion matrix and resulting precision, recall, and F1,
2. which error direction (false positive or false negative) is dangerous here and why,
3. the predeclared validation rule and frozen threshold,
4. final untouched-test counts/metrics without retuning, and
5. what development cross-validation does and does not show.
"""

print(ai_use_record)
print(exit_explanation)
