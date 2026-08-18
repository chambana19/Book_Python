"""Classify comfort complaints and select a model without spending the test set.

The workflow runs in the only order that keeps its final numbers believable:
split, baseline, cross-validated comparison, tuning, one test evaluation, then
threshold and importance analysis.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


# 1. Prepare reproducible data with a documented generating rule.
def make_comfort_data(seed=42, sample_count=900):
    """Return synthetic features and a binary complaint target."""
    rng = np.random.default_rng(seed)
    features = pd.DataFrame(
        {
            "floor_area_m2": rng.uniform(60, 520, sample_count),
            "glazing_ratio": rng.uniform(0.10, 0.68, sample_count),
            "occupant_density": rng.uniform(0.02, 0.16, sample_count),
            "setpoint_deviation_c": rng.normal(0.0, 2.4, sample_count),
            "outdoor_temp_c": rng.uniform(-8, 34, sample_count),
            "months_since_service": rng.integers(0, 36, sample_count),
        }
    )
    risk = (
        -9.0
        + 1.10 * np.abs(features["setpoint_deviation_c"])
        + 4.5 * features["glazing_ratio"] * (features["outdoor_temp_c"] > 26)
        + 30.0 * features["occupant_density"]
        + 0.11 * features["months_since_service"]
        + rng.normal(0, 0.30, sample_count)
    )
    probability = 1 / (1 + np.exp(-risk))
    target = pd.Series(
        (rng.random(sample_count) < probability).astype(int), name="complaint"
    )
    return features, target


X, y = make_comfort_data()
print(f"Rows: {len(X)}   complaint rate: {y.mean():.3f}")

# 2. Protect the test set before anything else touches the data.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print(f"Training rows: {len(y_train)} ({int(y_train.sum())} positive)")
print(f"Test rows:     {len(y_test)} ({int(y_test.sum())} positive)")

# 3. Establish the no-information baseline.
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
baseline_accuracy = baseline.score(X_test, y_test)
print(f"\nMajority-class baseline accuracy: {baseline_accuracy:.3f}")
print(confusion_matrix(y_test, baseline.predict(X_test)))

# 4. Compare candidates with cross-validation, inside the training data.
candidates = {
    "logistic pipeline": Pipeline(
        [("scale", StandardScaler()), ("model", LogisticRegression(max_iter=1000))]
    ),
    "decision tree (depth 5)": DecisionTreeClassifier(max_depth=5, random_state=42),
    "random forest": RandomForestClassifier(n_estimators=300, random_state=42),
}

print("\nCross-validated ROC-AUC on training folds")
for name, estimator in candidates.items():
    scores = cross_val_score(estimator, X_train, y_train, cv=folds, scoring="roc_auc")
    print(f"  {name:<24} {scores.mean():.3f} +/- {scores.std():.3f}")

# 5. Tune the leading candidate, still inside the training data.
search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid={
        "n_estimators": [200, 400],
        "max_depth": [4, 8, None],
        "min_samples_leaf": [1, 5],
    },
    cv=folds,
    scoring="roc_auc",
    n_jobs=-1,
).fit(X_train, y_train)
tuned = search.best_estimator_
print(f"\nBest settings: {search.best_params_}")
print(f"Best cross-validated ROC-AUC: {search.best_score_:.3f}")

# 6. Open the test set once, and report it beside the cross-validated score.
probabilities = tuned.predict_proba(X_test)[:, 1]
predictions = tuned.predict(X_test)
print(f"\nTest ROC-AUC: {roc_auc_score(y_test, probabilities):.3f}")
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions, digits=3))

# 7. Show that the threshold, not the model, controls the precision-recall trade.
print("Threshold study on the tuned forest")
for threshold in (0.2, 0.3, 0.4, 0.5, 0.6):
    predicted = (probabilities >= threshold).astype(int)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, predicted, average="binary", zero_division=0
    )
    print(f"  threshold {threshold:.1f}  precision {precision:.3f}  "
          f"recall {recall:.3f}  F1 {f1:.3f}")

# 8. Ask which columns the fitted model actually relied on.
importance = permutation_importance(
    tuned, X_test, y_test, n_repeats=20, random_state=42, scoring="roc_auc"
)
print("\nPermutation importance (drop in test ROC-AUC when shuffled)")
for index in importance.importances_mean.argsort()[::-1]:
    print(f"  {X.columns[index]:<22} {importance.importances_mean[index]:+.4f} "
          f"+/- {importance.importances_std[index]:.4f}")

# 9. Export the diagnostic figure: ROC curve and threshold trade-off.
logistic = candidates["logistic pipeline"].fit(X_train, y_train)
logistic_probabilities = logistic.predict_proba(X_test)[:, 1]

thresholds = np.linspace(0.05, 0.95, 91)
precision_line, recall_line = [], []
for threshold in thresholds:
    precision, recall, _, _ = precision_recall_fscore_support(
        y_test, (probabilities >= threshold).astype(int),
        average="binary", zero_division=0,
    )
    precision_line.append(precision)
    recall_line.append(recall)

fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8), layout="constrained")

for name, scores, color, linestyle in (
    ("Logistic pipeline", logistic_probabilities, "tab:orange", "--"),
    ("Tuned random forest", probabilities, "tab:blue", "-"),
):
    false_rate, true_rate, _ = roc_curve(y_test, scores)
    axes[0].plot(
        false_rate, true_rate, color=color, linestyle=linestyle, linewidth=2.0,
        label=f"{name}: AUC {roc_auc_score(y_test, scores):.3f}",
    )
axes[0].plot([0, 1], [0, 1], color="0.45", linestyle=":", label="Chance: AUC 0.500")
axes[0].set(
    title="Test-set ROC curves",
    xlabel="False positive rate",
    ylabel="True positive rate (recall)",
)
axes[0].grid(alpha=0.2)
axes[0].legend(loc="lower right", fontsize=8)

axes[1].plot(thresholds, precision_line, color="tab:orange", linestyle="--",
             linewidth=2.0, label="Precision")
axes[1].plot(thresholds, recall_line, color="tab:blue", linestyle="-",
             linewidth=2.0, label="Recall")
axes[1].axvline(0.5, color="0.35", linestyle=":", label="Default threshold 0.50")
axes[1].set(
    title="Precision and recall against decision threshold",
    xlabel="Decision threshold on predicted probability",
    ylabel="Score",
    ylim=(0, 1.05),
)
axes[1].grid(alpha=0.2)
axes[1].legend(loc="lower left", fontsize=8)

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "comfort_complaint_classification.png", dpi=200, bbox_inches="tight"
)
plt.show()
plt.close(fig)
