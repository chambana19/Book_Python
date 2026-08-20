# -*- coding: utf-8 -*-
"""ARC 500 Project 2 starter: guarded prediction, linprog, comparison, decision.

Run model_and_evaluate.py first. This default path is the project-aligned regression/LP
example: the evaluated four-feature linear surrogate becomes a linear objective while
glazing SHGC and compactness are held at an explicit scenario. Classification artifacts
remain usable for guarded probability/threshold checks, but require an independently
defined design objective rather than pretending probability is EUI.
"""

# %% 0 — LOAD THE FROZEN MODEL ARTIFACT AND DEFINE THE SCENARIO

from pathlib import Path
from time import perf_counter
import json

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import linprog

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "Submission"
ARTIFACT_FILE = OUTPUT_DIR / "model_artifact.json"
DOMAIN_FILE = OUTPUT_DIR / "model_domain_reference.csv"

if not ARTIFACT_FILE.exists() or not DOMAIN_FILE.exists():
    raise FileNotFoundError(
        "Run Starter_Code/model_and_evaluate.py first; it creates the frozen model "
        "artifact and joint-support reference used here."
    )

with ARTIFACT_FILE.open(encoding="utf-8") as handle:
    artifact = json.load(handle)
domain_reference = pd.read_csv(DOMAIN_FILE)

FEATURES = artifact["features_in_order"]
if FEATURES != ["wwr", "shade_m", "glazing_shgc", "compactness"]:
    raise ValueError(f"Unexpected feature order: {FEATURES}")

TRACK = artifact["track"]
COEFFICIENTS = np.asarray(artifact["coefficients"], dtype=float)
INTERCEPT = float(artifact["intercept"])
CLASSIFICATION_THRESHOLD = artifact["classification_probability_threshold"]

VARIABLE_FEATURES = ["wwr", "shade_m"]
FIXED_FEATURES = {"glazing_shgc": 0.45, "compactness": 1.10}
APPROVED_DESIGN_BOUNDS = np.asarray([[0.20, 0.60], [0.00, 1.20]], dtype=float)
# An approved design box can extend beyond observed evidence. The actual search box is
# the intersection with the fitted model's featurewise support; joint support is checked
# separately for every candidate.
BOUNDS = np.asarray(
    [
        [max(APPROVED_DESIGN_BOUNDS[i, 0], artifact["feature_min"][name]),
         min(APPROVED_DESIGN_BOUNDS[i, 1], artifact["feature_max"][name])]
        for i, name in enumerate(VARIABLE_FEATURES)
    ],
    dtype=float,
)
BASELINE = np.asarray([0.50, 0.20], dtype=float)
FEASIBILITY_ATOL = 1e-8


def as_candidate(candidate) -> np.ndarray:
    """Return a finite two-value float vector or raise a precise input error."""
    try:
        values = np.asarray(candidate, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError("candidate must contain two numeric values: wwr, shade_m") from exc
    if values.shape != (2,):
        raise ValueError(f"candidate shape must be (2,), received {values.shape}")
    if not np.isfinite(values).all():
        raise ValueError("candidate contains NaN or infinity")
    return values


def inside_bounds(candidate) -> bool:
    """Return True only for a finite, correctly shaped vector inside every bound."""
    try:
        values = as_candidate(candidate)
    except ValueError:
        return False
    return bool(
        np.all(values >= BOUNDS[:, 0] - FEASIBILITY_ATOL)
        and np.all(values <= BOUNDS[:, 1] + FEASIBILITY_ATOL)
    )


def full_feature_row(candidate) -> np.ndarray:
    """Build one model row in the exact feature order saved by evaluation."""
    values = as_candidate(candidate)
    row_by_name = {
        "wwr": values[0],
        "shade_m": values[1],
        **FIXED_FEATURES,
    }
    return np.asarray([row_by_name[name] for name in FEATURES], dtype=float)


def joint_support_distance(candidate) -> float:
    """Nearest standardized fit-row distance; a joint-support heuristic, not proof."""
    row = full_feature_row(candidate)
    means = np.asarray([artifact["feature_mean"][name] for name in FEATURES], dtype=float)
    scales = np.asarray([artifact["feature_scale"][name] for name in FEATURES], dtype=float)
    reference = domain_reference[FEATURES].to_numpy(dtype=float)
    z_row = (row - means) / scales
    z_reference = (reference - means) / scales
    return float(np.linalg.norm(z_reference - z_row, axis=1).min())


def model_supported(candidate) -> bool:
    """Require bounds, featurewise training ranges, and empirical joint support."""
    if not inside_bounds(candidate):
        return False
    row = full_feature_row(candidate)
    mins = np.asarray([artifact["feature_min"][name] for name in FEATURES], dtype=float)
    maxs = np.asarray([artifact["feature_max"][name] for name in FEATURES], dtype=float)
    if not (np.all(row >= mins - FEASIBILITY_ATOL) and np.all(row <= maxs + FEASIBILITY_ATOL)):
        return False
    return bool(joint_support_distance(candidate) <= artifact["joint_support_max_distance"])


def predict_supported(candidate) -> float:
    """Return EUI prediction or compliant probability after all support checks."""
    if not model_supported(candidate):
        distance = joint_support_distance(candidate) if inside_bounds(candidate) else np.nan
        raise ValueError(
            "Candidate is outside the saved model support rule "
            f"(nearest standardized distance={distance:.3f}, "
            f"limit={artifact['joint_support_max_distance']:.3f})."
        )
    linear_score = INTERCEPT + float(COEFFICIENTS @ full_feature_row(candidate))
    if TRACK == "regression":
        return linear_score
    probability = 1.0 / (1.0 + np.exp(-linear_score))
    return float(probability)


def verify_constraints(candidate) -> pd.DataFrame:
    """Return every lower/upper/support check with value, limit, slack, and pass/fail."""
    values = as_candidate(candidate)
    distance = joint_support_distance(values)
    checks = []
    for index, name in enumerate(VARIABLE_FEATURES):
        low, high = BOUNDS[index]
        checks.extend(
            [
                {"constraint": f"{name} minimum", "value": values[index], "limit": low,
                 "slack": values[index] - low,
                 "passes": bool(values[index] >= low - FEASIBILITY_ATOL)},
                {"constraint": f"{name} maximum", "value": values[index], "limit": high,
                 "slack": high - values[index],
                 "passes": bool(values[index] <= high + FEASIBILITY_ATOL)},
            ]
        )
    for name, value in FIXED_FEATURES.items():
        low = float(artifact["feature_min"][name])
        high = float(artifact["feature_max"][name])
        checks.extend(
            [
                {"constraint": f"fixed {name} training minimum", "value": value,
                 "limit": low, "slack": value - low,
                 "passes": bool(value >= low - FEASIBILITY_ATOL)},
                {"constraint": f"fixed {name} training maximum", "value": value,
                 "limit": high, "slack": high - value,
                 "passes": bool(value <= high + FEASIBILITY_ATOL)},
            ]
        )
    checks.append(
        {"constraint": "joint model support (nearest standardized fit row)",
         "value": distance, "limit": artifact["joint_support_max_distance"],
         "slack": artifact["joint_support_max_distance"] - distance,
         "passes": bool(distance <= artifact["joint_support_max_distance"])}
    )
    if TRACK == "classification":
        if CLASSIFICATION_THRESHOLD is None:
            raise ValueError("Classification artifact is missing its frozen probability threshold")
        probability = predict_supported(values)
        checks.append(
            {"constraint": "P(meets_code) minimum", "value": probability,
             "limit": CLASSIFICATION_THRESHOLD,
             "slack": probability - CLASSIFICATION_THRESHOLD,
             "passes": bool(probability >= CLASSIFICATION_THRESHOLD)}
        )
    return pd.DataFrame(checks)


# Explicit regression starter checks catch the former zip/NaN omissions.
assert not inside_bounds([0.30])
assert not inside_bounds([0.30, 0.60, 0.45])
assert not inside_bounds([np.nan, 0.60])
assert inside_bounds(BASELINE)


# %% 1 — PROJECT-ALIGNED LINEAR PROGRAM

if TRACK != "regression":
    probability = predict_supported(BASELINE)
    print(f"baseline P(meets_code)={probability:.3f}; frozen threshold="
          f"{CLASSIFICATION_THRESHOLD:.2f}")
    raise NotImplementedError(
        "The classification model supplies a probability constraint, not an EUI objective. "
        "Define and justify a separate linear design objective before using linprog."
    )

# The fitted regression is linear. Holding SHGC and compactness fixed makes its WWR and
# shade coefficients a valid linprog objective; the intercept/fixed terms do not change
# which candidate minimizes it. This is Project 2's required linear sub-component.
lp_objective = np.asarray(
    [COEFFICIENTS[FEATURES.index(name)] for name in VARIABLE_FEATURES], dtype=float
)
start = perf_counter()
lp_result = linprog(lp_objective, bounds=[tuple(row) for row in BOUNDS], method="highs")
runtime_primary_s = perf_counter() - start
if not lp_result.success:
    raise RuntimeError(f"linprog failed (status={lp_result.status}): {lp_result.message}")

candidate_primary = as_candidate(lp_result.x)
objective_primary = predict_supported(candidate_primary)
constraint_table = verify_constraints(candidate_primary)
if not bool(constraint_table["passes"].all()):
    raise RuntimeError("LP solution failed an independently recomputed constraint/support check")

print("\nLINEAR PROGRAM")
print("candidate [wwr, shade_m]:", candidate_primary.round(4))
print(f"predicted EUI={objective_primary:.4f} kWh/m2/yr")
print(f"status={lp_result.status}; message={lp_result.message}")
print(constraint_table.round(4).to_string(index=False))
constraint_table.to_csv(OUTPUT_DIR / "constraint_check.csv", index=False)


# %% 2 — TRANSPARENT GRID COMPARISON ON THE SAME BOUNDED PROBLEM

start = perf_counter()
grid_rows = []
for wwr in np.linspace(BOUNDS[0, 0], BOUNDS[0, 1], 41):
    for shade_m in np.linspace(BOUNDS[1, 0], BOUNDS[1, 1], 49):
        candidate = np.asarray([wwr, shade_m])
        if model_supported(candidate):
            grid_rows.append((predict_supported(candidate), wwr, shade_m))
if not grid_rows:
    raise RuntimeError("No grid candidates passed the model-support rule")
objective_comparison, grid_wwr, grid_shade = min(grid_rows, key=lambda row: row[0])
candidate_comparison = np.asarray([grid_wwr, grid_shade])
runtime_comparison_s = perf_counter() - start
if not np.isclose(objective_primary, objective_comparison, rtol=0.0, atol=1e-8):
    raise RuntimeError("linprog and the same-domain supported grid disagree unexpectedly")

comparison = pd.DataFrame(
    {
        "method": ["linprog", "supported grid"],
        "objective_kwh_m2yr": [objective_primary, objective_comparison],
        "runtime_s": [runtime_primary_s, runtime_comparison_s],
        "evaluated_candidates": [np.nan, len(grid_rows)],
        "feasible_and_supported": [
            bool(verify_constraints(candidate_primary)["passes"].all()),
            bool(verify_constraints(candidate_comparison)["passes"].all()),
        ],
    }
)
print("\nSOLVER COMPARISON")
print(comparison.round(5).to_string(index=False))
comparison.to_csv(OUTPUT_DIR / "solver_comparison.csv", index=False)


# %% 3 — BASELINE VERSUS RECOMMENDATION, WITH AN EXTERNAL-VALIDATION GATE

baseline_prediction = predict_supported(BASELINE)
decision_table = pd.DataFrame(
    {
        "design": ["baseline", "recommended"],
        "wwr": [BASELINE[0], candidate_primary[0]],
        "shade_m": [BASELINE[1], candidate_primary[1]],
        "glazing_shgc_fixed": [FIXED_FEATURES["glazing_shgc"]] * 2,
        "compactness_fixed": [FIXED_FEATURES["compactness"]] * 2,
        "surrogate_prediction_kwh_m2yr": [baseline_prediction, objective_primary],
        "joint_support_distance": [
            joint_support_distance(BASELINE), joint_support_distance(candidate_primary)
        ],
    }
)
decision_table.to_csv(OUTPUT_DIR / "decision_comparison.csv", index=False)
print("\nDECISION TABLE")
print(decision_table.round(4).to_string(index=False))

confirmation_file = OUTPUT_DIR / "non_surrogate_confirmation.csv"
confirmation_template = pd.DataFrame(
    {
        "design": ["baseline", "recommended"],
        "evidence_source": ["REPLACE: simulation/measurement", "REPLACE: simulation/measurement"],
        "confirmed_eui_kwh_m2yr": [np.nan, np.nan],
        "reviewer": ["REPLACE", "REPLACE"],
        "run_or_measurement_id": ["REPLACE", "REPLACE"],
    }
)

decision_ready = False
if confirmation_file.exists():
    confirmation = pd.read_csv(confirmation_file)
    expected_columns = set(confirmation_template.columns)
    if not expected_columns.issubset(confirmation.columns):
        raise ValueError(f"confirmation file must contain {sorted(expected_columns)}")
    confirmed = pd.to_numeric(confirmation["confirmed_eui_kwh_m2yr"], errors="coerce")
    if len(confirmation) != 2 or not np.isfinite(confirmed).all():
        raise ValueError("confirmation file needs finite baseline and recommended results")
    confirmed_improvement = float(confirmed.iloc[0] - confirmed.iloc[1])
    decision_ready = confirmed_improvement > 0
    print(f"independently confirmed improvement={confirmed_improvement:.4f} kWh/m2/yr")
else:
    confirmation_template.to_csv(
        OUTPUT_DIR / "non_surrogate_confirmation_TEMPLATE.csv", index=False
    )

if decision_ready:
    print("DECISION STATUS: conditionally supported by the documented independent evidence.")
else:
    print("DECISION STATUS: NOT READY. Complete non_surrogate_confirmation.csv; the surrogate "
          "optimum alone is not an accepted design recommendation.")


# %% 4 — EXPORT A SOLVER-RUN RECORD FOR THE SOLVER CARD

solver_run = {
    "family": "linear programming",
    "implementation": "scipy.optimize.linprog(method='highs')",
    "scipy_version": scipy.__version__,
    "objective": "minimize evaluated linear-regression EUI at fixed SHGC/compactness",
    "decision_variables_in_order": VARIABLE_FEATURES,
    "bounds": BOUNDS.tolist(),
    "approved_design_bounds": APPROVED_DESIGN_BOUNDS.tolist(),
    "fixed_features": FIXED_FEATURES,
    "status": int(lp_result.status),
    "success": bool(lp_result.success),
    "message": str(lp_result.message),
    "nit": int(lp_result.nit),
    "runtime_seconds": runtime_primary_s,
    "candidate": candidate_primary.tolist(),
    "predicted_objective_kwh_m2yr": objective_primary,
    "feasibility_tolerance": FEASIBILITY_ATOL,
    "joint_support_rule": artifact["joint_support_rule"],
    "joint_support_distance": joint_support_distance(candidate_primary),
    "joint_support_limit": artifact["joint_support_max_distance"],
    "comparison": "41 x 49 bounded grid, filtered by the identical support rule",
    "guarantee": (
        "linprog solves the encoded linear bound-constrained surrogate problem to numerical "
        "tolerance; it does not guarantee real-building performance"
    ),
    "independent_confirmation_complete": decision_ready,
}
with (OUTPUT_DIR / "solver_run.json").open("w", encoding="utf-8") as handle:
    json.dump(solver_run, handle, indent=2)
print("saved solver_run.json; transfer its fields into the completed solver card")
