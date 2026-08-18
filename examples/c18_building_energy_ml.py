"""Train and evaluate an introductory building-energy regression model."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def make_building_data(seed=42, sample_count=240):
    """Return reproducible synthetic features and an energy target."""
    rng = np.random.default_rng(seed)
    features = pd.DataFrame(
        {
            "floor_area_m2": rng.uniform(80, 520, sample_count),
            "glazing_ratio": rng.uniform(0.12, 0.65, sample_count),
            "occupants": rng.integers(2, 45, sample_count),
            "outdoor_temp_c": rng.uniform(-5, 31, sample_count),
        }
    )
    noise = rng.normal(0, 10, sample_count)
    target = (
        28
        + 0.24 * features["floor_area_m2"]
        + 66 * features["glazing_ratio"]
        + 1.35 * features["occupants"]
        - 2.1 * features["outdoor_temp_c"]
        + noise
    )
    return features, target


# 1. Define features X and target y.
X, y = make_building_data()

# 2. Protect a test set before fitting or evaluating choices.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
)

# 3. Establish a baseline using only the training-target mean.
baseline_predictions = np.full(len(y_test), y_train.mean())
baseline_mae = mean_absolute_error(y_test, baseline_predictions)

# 4. Fit on training data and predict unseen test rows.
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# 5. Evaluate magnitude of error and explained variation.
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
print(f"Baseline MAE: {baseline_mae:.2f}")
print(f"Model MAE: {mae:.2f}")
print(f"Test R2: {r2:.3f}")

coefficients = pd.Series(model.coef_, index=X.columns, name="coefficient")
print(coefficients)

# 6. Inspect agreement and residual structure.
residuals = y_test - predictions
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8), layout="constrained")
axes[0].scatter(y_test, predictions, color="tab:blue", edgecolor="black", alpha=0.76)
limits = [min(y_test.min(), predictions.min()), max(y_test.max(), predictions.max())]
axes[0].plot(limits, limits, color="tab:orange", linestyle="--", label="Perfect agreement")
axes[0].set(
    title="Predicted versus actual test values",
    xlabel="Actual energy",
    ylabel="Predicted energy",
)
axes[0].legend()

axes[1].scatter(predictions, residuals, color="tab:blue", edgecolor="black", alpha=0.76)
axes[1].axhline(0, color="tab:orange", linestyle="--")
axes[1].set(
    title=f"Residual check (MAE={mae:.1f}, R2={r2:.2f})",
    xlabel="Predicted energy",
    ylabel="Actual - predicted",
)

for ax in axes:
    ax.grid(alpha=0.2)

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "building_energy_regression.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)
