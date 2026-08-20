ARC 500 · WEEK 14 · CLASSIFICATION, CONFUSION MATRICES, AND MODEL CARDS
Fall 2026 · two nominal 80-minute meetings; complete source decks are
instructor-paced and are not cut to a fixed slide count

CONTENTS

Meeting A
  ARC500_Week14A_Classification_Confusion_Matrices_Model_Cards.pptx
  Classification as a decision rule, the confusion matrix, precision vs.
  recall, choosing an operating threshold from real consequences (not the
  default 0.5), cross_val_score, and the model card.

Meeting B
  ARC500_Week14B_Classification_and_Regression_Studio.pptx
  Handouts/ARC500_Week14B_Student_Classification.py
  Handouts/ARC500_Week14B_Instructor_Classification.py
  Handouts/ARC500_Week14B_Student_Regression.py
  Handouts/ARC500_Week14B_Instructor_Regression.py
  Handouts/data/radley_portfolio_envelope.csv
  Studio meeting, forked by track (see below).

MEETING B'S TRACK-DEPENDENT SPLIT

Meeting B is not one script — it is two parallel, self-contained handouts,
and every student works only one of them for the full studio period:

  Track A — Classification
    ARC500_Week14B_Student_Classification.py /
    ARC500_Week14B_Instructor_Classification.py
    Fits a LogisticRegression go/no-go classifier on meets_code, reads a
    confusion matrix, hand-computes precision/recall/F1, sweeps thresholds,
    uses an 84-train / 28-validation / 28-untouched-final-test protocol,
    selects a threshold on validation evidence with the predeclared rule
    FPR <= 10% then maximum recall, freezes threshold=0.5, opens the final
    test once, and closes with a Track A model card. Development-only
    cross-validation describes variability; it does not tune the threshold
    or touch the final test.

  Track B — Regression
    ARC500_Week14B_Student_Regression.py /
    ARC500_Week14B_Instructor_Regression.py
    Compares Week 13's 3-feature LinearRegression with a 4-feature model on
    validation data, uses paired shuffled development-only folds as a
    variability check, freezes the selected 4-feature specification, refits
    on all 112 development rows, and opens the 28-row final test once. MAE,
    RMSE, and R2 are evaluation metrics; neither fold spread nor plus/minus
    RMSE is presented as an individual prediction interval.

Students choose their track from their own Project 2 framing (a yes/no
decision -> Track A; a continuous-outcome prediction -> Track B). Both
tracks load the exact same shared dataset —
Handouts/data/radley_portfolio_envelope.csv, the same 140-row Radley Hall
portfolio used across Weeks 13-15 — and both feed directly into Week 15's
predict-optimize-decide demo: Track B's regressor becomes the optimizer's
objective; Track A's classifier becomes a constraint. Do not merge the two
tracks' handouts or skip the fork; each is a complete, independently
runnable studio on its own.

PREFLIGHT: SCIKIT-LEARN IN THE COURSE ENVIRONMENT

Spyder 6 connects to the shared external arc500-f26 environment documented
in Weeks01-03_Foundations/Spyder_Installation_and_Course_Environment_Guide.txt.
Do not install packages into a standalone Spyder internal environment. In a
console connected to arc500-f26, run:

  import sklearn; print(sklearn.__version__)

A version string (no ImportError) is a passing check. If it fails, update or
recreate arc500-f26 from Weeks01-03_Foundations/ARC500_environment.yml, then
reconnect Spyder to that interpreter. pandas, NumPy, Matplotlib, and
scikit-learn are all declared in the same environment file.

COURSE WORKFLOW

Students may use generative AI for coding support, but must preserve an
AI-use record and be able to trace, test, modify, and explain every
submitted line — both decks this week include an AI-drafted evaluation that
overclaims ("ready to use!" / "validated and ready!") and asks students to
name exactly what it got wrong. Before submission, each track's completed
.py file should run from the top after a Spyder kernel restart, with
random_state=42 on every split.
