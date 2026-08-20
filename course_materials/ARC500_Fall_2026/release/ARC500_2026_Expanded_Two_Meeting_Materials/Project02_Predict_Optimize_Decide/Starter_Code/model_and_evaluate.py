# -*- coding: utf-8 -*-
"""ARC 500 Project 2 starter: audit, select, freeze, and evaluate one model.

The default regression path runs end to end. Change TRACK once, near the top, if the
approved project uses classification. Model/threshold choices use validation evidence;
the final test remains untouched until the choice is frozen.
"""

# %% 0 — ENVIRONMENT, PATHS, AND CONFIGURATION

from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn

try:
    from sklearn.dummy import DummyClassifier, DummyRegressor
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.metrics import (
        brier_score_loss,
        confusion_matrix,
        f1_score,
        mean_absolute_error,
        mean_squared_error,
        precision_score,
        r2_score,
        recall_score,
    )
    from sklearn.metrics import pairwise_distances
    from sklearn.model_selection import train_test_split
except ImportError as exc:
    raise ImportError("Install scikit-learn in the Python environment used by Spyder.") from exc

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "Data" / "radley_portfolio_envelope.csv"
OUTPUT_DIR = PROJECT_DIR / "Submission"
OUTPUT_DIR.mkdir(exist_ok=True)

TRACK = "regression"  # Choose once: "regression" or "classification".
FEATURES = ["wwr", "shade_m", "glazing_shgc", "compactness"]
REGRESSION_TARGET = "eui_kwh_m2yr"
CLASSIFICATION_TARGET = "meets_code"  # supplied label: 1 when EUI <= 27.0
THRESHOLD_CANDIDATES = [0.30, 0.40, 0.50, 0.60, 0.70]
FALSE_GO_COST = 5.0   # false compliant/go call is the more serious error here
FALSE_NO_COST = 1.0

if TRACK not in {"regression", "classification"}:
    raise ValueError("TRACK must be exactly 'regression' or 'classification'.")


# %% 1 — LOAD AND AUDIT THE CANONICAL WEEK 13–15 DATASET

data = pd.read_csv(DATA_FILE)
required_columns = {
    "variant_id", "wwr", "shade_m", "glazing_shgc", "compactness",
    "orientation", "eui_kwh_m2yr", "est_annual_cost_index", "meets_code",
}
missing_columns = required_columns - set(data.columns)
if missing_columns:
    raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")
if len(data) != 140:
    raise ValueError(f"Expected 140 canonical portfolio rows, found {len(data)}")
if not data["variant_id"].is_unique:
    raise ValueError("variant_id must be unique")
if data[list(required_columns)].isna().any().any():
    raise ValueError("Canonical project columns contain missing values")
if not set(data["meets_code"].unique()).issubset({0, 1}):
    raise ValueError("meets_code must contain only 0/1")
expected_label = (data["eui_kwh_m2yr"] <= 27.0).astype(int)
if not data["meets_code"].equals(expected_label):
    raise ValueError("meets_code does not match the documented EUI <= 27.0 rule")

print("data file:", DATA_FILE)
print("shape:", data.shape)
print("class counts:\n", data["meets_code"].value_counts().sort_index())
print("feature ranges:\n", data[FEATURES].agg(["min", "max"]).round(3))

target_for_outliers = REGRESSION_TARGET
q1, q3 = data[target_for_outliers].quantile([0.25, 0.75])
iqr = q3 - q1
outlier_mask = (
    (data[target_for_outliers] < q1 - 1.5 * iqr)
    | (data[target_for_outliers] > q3 + 1.5 * iqr)
)
print(f"IQR audit on {target_for_outliers}: {int(outlier_mask.sum())} flagged row(s)")


# %% 2 — DEFINE X/y WITHOUT LEAKAGE

TARGET = REGRESSION_TARGET if TRACK == "regression" else CLASSIFICATION_TARGET
FORBIDDEN_PREDICTORS = {
    "variant_id", "orientation", "eui_kwh_m2yr", "est_annual_cost_index", "meets_code"
}
if set(FEATURES) & FORBIDDEN_PREDICTORS:
    raise ValueError("FEATURES contains an ID, target, label, or answer-derived column")

X = data[FEATURES].copy()
y = data[TARGET].copy()
if not np.isfinite(X.to_numpy(dtype=float)).all():
    raise ValueError("Model features contain NaN or infinity")


# %% 3 — RESERVE FINAL TEST FIRST, THEN CREATE A VALIDATION SET

first_split = {"test_size": 0.25, "random_state": 7}
if TRACK == "classification":
    first_split["stratify"] = y
X_pool, X_test, y_pool, y_test = train_test_split(X, y, **first_split)

second_split = {"test_size": 0.25, "random_state": 11}
if TRACK == "classification":
    second_split["stratify"] = y_pool
X_fit, X_val, y_fit, y_val = train_test_split(X_pool, y_pool, **second_split)

index_sets = [set(frame.index) for frame in (X_fit, X_val, X_test)]
if any(index_sets[i] & index_sets[j] for i in range(3) for j in range(i + 1, 3)):
    raise RuntimeError("fit, validation, and final-test rows must be disjoint")
if set().union(*index_sets) != set(data.index):
    raise RuntimeError("split rows do not reconstruct the full dataset")
print(f"fit/validation/final-test rows: {len(X_fit)}/{len(X_val)}/{len(X_test)}")


def regression_metrics(y_true, prediction) -> dict:
    """Return regression metrics with their original physical-unit interpretation."""
    return {
        "mae": float(mean_absolute_error(y_true, prediction)),
        "rmse": float(mean_squared_error(y_true, prediction) ** 0.5),
        "r2": float(r2_score(y_true, prediction)),
    }


def classification_metrics(y_true, prediction) -> dict:
    """Return counts and metrics for one already-thresholded classifier."""
    tn, fp, fn, tp = confusion_matrix(y_true, prediction, labels=[0, 1]).ravel()
    return {
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "precision": float(precision_score(y_true, prediction, zero_division=0)),
        "recall": float(recall_score(y_true, prediction, zero_division=0)),
        "f1": float(f1_score(y_true, prediction, zero_division=0)),
    }


# %% 4 — USE VALIDATION EVIDENCE; FREEZE THE MODEL AND OPERATING RULE

if TRACK == "regression":
    baseline = DummyRegressor(strategy="mean").fit(X_fit, y_fit)
    model = LinearRegression().fit(X_fit, y_fit)
    validation = pd.DataFrame(
        [
            {"model": "baseline", **regression_metrics(y_val, baseline.predict(X_val))},
            {"model": "proposed", **regression_metrics(y_val, model.predict(X_val))},
        ]
    )
    chosen_threshold = None
    threshold_table = None
    threshold_reason = "not applicable to regression"
    calibration_status = "split-conformal or bootstrap interval still required for decisions"
else:
    baseline = DummyClassifier(strategy="most_frequent").fit(X_fit, y_fit)
    model = LogisticRegression(max_iter=1000, random_state=7).fit(X_fit, y_fit)
    proba_val = model.predict_proba(X_val)[:, 1]
    threshold_rows = []
    for threshold in THRESHOLD_CANDIDATES:
        pred_val = (proba_val >= threshold).astype(int)
        row = classification_metrics(y_val, pred_val)
        row.update(
            {
                "threshold": threshold,
                "consequence_cost": FALSE_GO_COST * row["fp"] + FALSE_NO_COST * row["fn"],
                "predicted_positive_n": int(pred_val.sum()),
            }
        )
        threshold_rows.append(row)
    threshold_table = pd.DataFrame(threshold_rows)
    chosen_row = threshold_table.sort_values(
        ["consequence_cost", "fp", "recall", "threshold"],
        ascending=[True, True, False, False],
    ).iloc[0]
    chosen_threshold = float(chosen_row["threshold"])
    threshold_reason = (
        f"selected on validation rows only by minimizing {FALSE_GO_COST:g}*FP + "
        f"{FALSE_NO_COST:g}*FN; ties prefer fewer FP, then higher recall"
    )
    calibration_status = (
        "not calibrated; predict_proba is treated as a score until calibration is assessed"
    )
    validation = threshold_table.copy()

print("\nVALIDATION EVIDENCE (used for model/threshold choice):")
print(validation.round(3).to_string(index=False))
if threshold_table is not None:
    threshold_table.to_csv(OUTPUT_DIR / "threshold_selection_validation_only.csv", index=False)
    print(f"frozen threshold={chosen_threshold:.2f}: {threshold_reason}")


# %% 5 — OPEN THE UNTOUCHED FINAL TEST ONCE

pred_base = baseline.predict(X_test)
if TRACK == "regression":
    pred_model = model.predict(X_test)
    final_metrics = pd.DataFrame(
        [
            {"model": "baseline", **regression_metrics(y_test, pred_base)},
            {"model": "proposed", **regression_metrics(y_test, pred_model)},
        ]
    )
    manual_mae = np.mean(np.abs(y_test.to_numpy() - pred_model))
    if not np.isclose(manual_mae, final_metrics.loc[1, "mae"]):
        raise RuntimeError("manual and library MAE disagree")
    brier = None
else:
    proba_test = model.predict_proba(X_test)[:, 1]
    pred_model = (proba_test >= chosen_threshold).astype(int)
    final_metrics = pd.DataFrame(
        [
            {"model": "baseline", "threshold": None,
             **classification_metrics(y_test, pred_base)},
            {"model": "proposed", "threshold": chosen_threshold,
             **classification_metrics(y_test, pred_model)},
        ]
    )
    brier = float(brier_score_loss(y_test, proba_test))

print("\nFINAL TEST EVIDENCE (not used for selection):")
print(final_metrics.round(3).to_string(index=False))
if TRACK == "classification":
    print(f"final-test Brier score={brier:.4f}; {calibration_status}")
final_metrics.to_csv(OUTPUT_DIR / "model_metrics_final_test.csv", index=False)


# %% 6 — CREATE THE TRACK-APPROPRIATE FINAL-TEST DIAGNOSTIC

fig, ax = plt.subplots(figsize=(7, 5))
if TRACK == "regression":
    residual = y_test.to_numpy() - pred_model
    ax.scatter(pred_model, residual, color="#2E74B5", alpha=0.85)
    ax.axhline(0, color="#5A5F66", linewidth=1)
    ax.set_xlabel("Predicted EUI (kWh/m2/yr)")
    ax.set_ylabel("Actual - prediction (kWh/m2/yr)")
    ax.set_title("Untouched final-test residuals")
else:
    cm = confusion_matrix(y_test, pred_model, labels=[0, 1])
    image = ax.imshow(cm, cmap="Blues")
    for row in range(2):
        for column in range(2):
            ax.text(column, row, str(cm[row, column]), ha="center", va="center")
    ax.set_xticks([0, 1], ["Predicted 0", "Predicted 1"])
    ax.set_yticks([0, 1], ["Actual 0", "Actual 1"])
    ax.set_title(f"Untouched final-test confusion matrix (threshold={chosen_threshold:.2f})")
    fig.colorbar(image, ax=ax)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / "model_diagnostic_final_test.png", dpi=200)
plt.close(fig)


# %% 7 — SAVE A REPRODUCIBLE MODEL ARTIFACT AND JOINT-SUPPORT REFERENCE

feature_min = X_fit.min()
feature_max = X_fit.max()
feature_mean = X_fit.mean()
feature_scale = X_fit.std(ddof=0).replace(0.0, 1.0)
z_fit = (X_fit - feature_mean) / feature_scale
distances = pairwise_distances(z_fit.to_numpy())
np.fill_diagonal(distances, np.inf)
nearest_neighbor_distances = distances.min(axis=1)
joint_support_max_distance = float(np.quantile(nearest_neighbor_distances, 0.99) * 1.10)

domain_reference = X_fit.copy()
domain_reference.insert(0, "variant_id", data.loc[X_fit.index, "variant_id"])
domain_reference.to_csv(OUTPUT_DIR / "model_domain_reference.csv", index=False)

artifact = {
    "schema_version": 2,
    "data_file": DATA_FILE.name,
    "track": TRACK,
    "features_in_order": FEATURES,
    "target": TARGET,
    "fit_n": len(X_fit),
    "validation_n": len(X_val),
    "final_test_n": len(X_test),
    "split_seeds": {"final_test": 7, "validation": 11},
    "estimator": type(model).__name__,
    "library_versions": {
        "numpy": np.__version__, "pandas": pd.__version__, "scikit_learn": sklearn.__version__
    },
    "intercept": float(np.asarray(model.intercept_).reshape(-1)[0]),
    "coefficients": [float(value) for value in np.asarray(model.coef_).reshape(-1)],
    "classification_probability_threshold": chosen_threshold,
    "threshold_selection": threshold_reason,
    "false_go_cost": FALSE_GO_COST if TRACK == "classification" else None,
    "false_no_cost": FALSE_NO_COST if TRACK == "classification" else None,
    "probability_calibration_status": calibration_status,
    "final_test_brier_score": brier,
    "feature_min": {name: float(feature_min[name]) for name in FEATURES},
    "feature_max": {name: float(feature_max[name]) for name in FEATURES},
    "feature_mean": {name: float(feature_mean[name]) for name in FEATURES},
    "feature_scale": {name: float(feature_scale[name]) for name in FEATURES},
    "joint_support_rule": (
        "nearest standardized training row distance <= the saved 1.10*99th-percentile "
        "leave-one-out nearest-neighbor distance; heuristic guard, not proof of validity"
    ),
    "joint_support_max_distance": joint_support_max_distance,
    "domain_reference_file": "model_domain_reference.csv",
    "final_test_metrics": final_metrics.to_dict(orient="records"),
}
with (OUTPUT_DIR / "model_artifact.json").open("w", encoding="utf-8") as handle:
    json.dump(artifact, handle, indent=2)

print("\nSaved model_artifact.json and model_domain_reference.csv")
print("The final test was opened only after the feature plan and operating rule were frozen.")
print("Before optimization, complete the model card and preserve this artifact unchanged.")
