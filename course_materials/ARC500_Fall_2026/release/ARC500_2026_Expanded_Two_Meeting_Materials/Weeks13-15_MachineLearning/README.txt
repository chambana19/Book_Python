ARC 500 · WEEKS 13–15 · EVALUATED PREDICTION AND CAPSTONE SYNTHESIS
Fall 2026 · canonical consolidated authoring/build target

SOURCE-DECK POLICY
  These are complete, topic-driven source decks. There is no fixed slide
  count. The instructor may hide, skip, or shorten slides for an 80-minute
  meeting, but the distributed decks retain all worked examples, practice,
  visual explanations, and optional 2026 practice-horizon material.

CONTENTS
  Week 13A — evaluated regression: decision-time features, leakage, a naive
  baseline, train/validation/final-test roles, MAE/RMSE/R2, and residuals.

  Week 13B — complete Spyder regression studio with an instructor script and
  a fail-loud student scaffold.

  Week 14A — classification as a decision rule: confusion matrix,
  precision/recall/F1, validation-only threshold choice, development-only
  cross-validation, calibration/uncertainty horizon, and a model card.

  Week 14B — two self-contained studio tracks. Classification uses
  84 train / 28 validation / 28 untouched final-test rows and freezes the
  threshold selected by FPR <= 10%, then maximum recall. Regression compares
  specifications on validation data, freezes the selected four-feature model,
  refits on 112 development rows, and opens the 28-row final test once.

  Week 15A — predict, optimize, decide: a frozen model enters a bounded search,
  the result is compared with a baseline, and the proposed candidate requires
  non-surrogate simulation, measurement, or expert confirmation.

DATA AND MIRRORS
  The Week 13–15 handouts and Project 2 use the same 140-row/four-feature
  portfolio schema. Week13_Machine_Learning,
  Week14_Classification_and_Model_Cards, and Week15_Capstone are convenience
  mirrors for distribution. Do not edit those copies independently.

ENVIRONMENT
  Use the external arc500-f26 environment declared in
  ../Weeks01-03_Foundations/ARC500_environment.yml and connect Spyder 6 to its
  interpreter. Do not install packages into a standalone Spyder internal
  environment.

Revision date: August 20, 2026
