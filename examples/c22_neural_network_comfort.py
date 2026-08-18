"""Build a neural network from arrays, verify its gradient, then benchmark it.

The hand-written network shows what training actually does. The scikit-learn
network then takes its turn as one candidate in the Chapter 21 workflow, where
it must earn its place against a linear model and a tree ensemble.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# 1. Reuse the Chapter 21 dataset so the comparison is direct.
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


# 2. The network itself: initialize, forward, loss, backward, train.
def sigmoid(values):
    return 1 / (1 + np.exp(-values))


def initialize(input_count, hidden_count, seed=0):
    """Small random weights, zero biases, one reproducible stream."""
    rng = np.random.default_rng(seed)
    return {
        "W1": rng.normal(0, np.sqrt(1 / input_count), (input_count, hidden_count)),
        "b1": np.zeros(hidden_count),
        "W2": rng.normal(0, np.sqrt(1 / hidden_count), (hidden_count, 1)),
        "b2": np.zeros(1),
    }


def forward(parameters, X):
    """Return the hidden activations and the output probabilities."""
    hidden_input = X @ parameters["W1"] + parameters["b1"]
    hidden_output = np.tanh(hidden_input)
    output_input = hidden_output @ parameters["W2"] + parameters["b2"]
    return hidden_output, sigmoid(output_input).ravel()


def cross_entropy(probabilities, targets):
    safe = np.clip(probabilities, 1e-12, 1 - 1e-12)
    return -np.mean(targets * np.log(safe) + (1 - targets) * np.log(1 - safe))


def backward(parameters, X, targets, hidden_output, probabilities):
    """Return one gradient array per parameter."""
    sample_count = X.shape[0]

    output_delta = ((probabilities - targets) / sample_count).reshape(-1, 1)
    grad_W2 = hidden_output.T @ output_delta
    grad_b2 = output_delta.sum(axis=0)

    hidden_delta = (output_delta @ parameters["W2"].T) * (1 - hidden_output**2)
    grad_W1 = X.T @ hidden_delta
    grad_b1 = hidden_delta.sum(axis=0)

    return {"W1": grad_W1, "b1": grad_b1, "W2": grad_W2, "b2": grad_b2}


def gradient_check(parameters, X, targets, step=1e-6):
    """Largest disagreement between backpropagation and central differences."""
    hidden_output, probabilities = forward(parameters, X)
    analytic = backward(parameters, X, targets, hidden_output, probabilities)

    worst_gap = 0.0
    for key in parameters:
        flat = parameters[key].ravel()
        for index in range(flat.size):
            original = flat[index]
            flat[index] = original + step
            raised = cross_entropy(forward(parameters, X)[1], targets)
            flat[index] = original - step
            lowered = cross_entropy(forward(parameters, X)[1], targets)
            flat[index] = original

            estimate = (raised - lowered) / (2 * step)
            gap = abs(estimate - analytic[key].ravel()[index])
            worst_gap = max(worst_gap, gap)

    return worst_gap


def train(X, targets, hidden_count=8, learning_rate=0.5, epochs=400, seed=0,
          X_valid=None, targets_valid=None):
    """Full-batch gradient descent, recording the loss each epoch."""
    parameters = initialize(X.shape[1], hidden_count, seed)
    history = []

    for _ in range(epochs):
        hidden_output, probabilities = forward(parameters, X)
        gradients = backward(parameters, X, targets, hidden_output, probabilities)
        for key in parameters:
            parameters[key] -= learning_rate * gradients[key]

        row = [cross_entropy(probabilities, targets)]
        if X_valid is not None:
            row.append(cross_entropy(forward(parameters, X_valid)[1], targets_valid))
        history.append(row)

    return parameters, np.array(history)


# 3. Prepare the data exactly as Chapter 21 did.
X, y = make_comfort_data()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scaler = StandardScaler().fit(X_train)
scaled_train = scaler.transform(X_train)
scaled_test = scaler.transform(X_test)
targets_train = y_train.to_numpy().astype(float)
targets_test = y_test.to_numpy().astype(float)

# 4. Depth without a nonlinearity buys nothing. Show it, do not assert it.
rng = np.random.default_rng(3)
first_layer = rng.normal(size=(6, 4))
second_layer = rng.normal(size=(4, 1))
sample = rng.normal(size=(5, 6))
print("Two stacked linear layers equal one:",
      np.allclose(sample @ first_layer @ second_layer,
                  sample @ (first_layer @ second_layer)))

# 5. Never trust an unverified gradient.
gap = gradient_check(initialize(scaled_train.shape[1], 8, seed=0),
                     scaled_train, targets_train)
print(f"Largest backpropagation gap: {gap:.3e}")
if gap > 1e-7:
    raise ValueError("Backpropagation disagrees with the finite-difference gradient")

# 6. Train the hand-written network.
parameters, history = train(
    scaled_train, targets_train, hidden_count=8, learning_rate=0.5, epochs=400,
    seed=0, X_valid=scaled_test, targets_valid=targets_test,
)
scratch_scores = forward(parameters, scaled_test)[1]
print(f"\nHand-written network: loss {history[0, 0]:.4f} -> {history[-1, 0]:.4f}")
print(f"Hand-written network: test ROC-AUC {roc_auc_score(targets_test, scratch_scores):.3f}")

# 7. Scaling is mandatory, not advisable.
unscaled = MLPClassifier(hidden_layer_sizes=(16,), alpha=1e-3, max_iter=2000,
                         random_state=42)
scaled = Pipeline([
    ("scale", StandardScaler()),
    ("model", MLPClassifier(hidden_layer_sizes=(16,), alpha=1e-3, max_iter=2000,
                            random_state=42)),
])
print("\nEffect of feature scaling")
for name, estimator in (("without scaler", unscaled), ("with scaler", scaled)):
    scores = cross_val_score(estimator, X_train, y_train, cv=folds, scoring="roc_auc")
    print(f"  {name:<16} CV ROC-AUC {scores.mean():.3f} +/- {scores.std():.3f}")

# 8. The network is one candidate among several, judged the same way.
candidates = {
    "logistic pipeline": Pipeline([
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000)),
    ]),
    "random forest": RandomForestClassifier(n_estimators=300, random_state=42),
    "neural network": scaled,
}

print("\nCross-validated ROC-AUC on training folds")
cross_validated = {}
for name, estimator in candidates.items():
    scores = cross_val_score(estimator, X_train, y_train, cv=folds, scoring="roc_auc")
    cross_validated[name] = scores.mean()
    print(f"  {name:<20} {scores.mean():.3f} +/- {scores.std():.3f}")

selected = max(cross_validated, key=cross_validated.get)
print(f"Selected by cross-validation: {selected}")

# 9. Only now does the test set open, once, for every candidate.
print("\nTest ROC-AUC (reported after selection, not used to select)")
for name, estimator in candidates.items():
    fitted = estimator.fit(X_train, y_train)
    test_auc = roc_auc_score(y_test, fitted.predict_proba(X_test)[:, 1])
    print(f"  {name:<20} {test_auc:.3f}")

# 10. A network's result is a random variable; report the spread.
seed_scores = []
for seed in range(1, 9):
    model = Pipeline([
        ("scale", StandardScaler()),
        ("model", MLPClassifier(hidden_layer_sizes=(16,), alpha=1e-3,
                                max_iter=2000, random_state=seed)),
    ]).fit(X_train, y_train)
    seed_scores.append(roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))
print(f"\nNetwork test ROC-AUC over seeds 1-8: min {min(seed_scores):.3f} "
      f"max {max(seed_scores):.3f} mean {np.mean(seed_scores):.3f}")

# 11. Plot the loss curve and the decision boundary the hidden layer bought.
pair = ["setpoint_deviation_c", "occupant_density"]
pair_train = X_train[pair]
linear_pair = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
]).fit(pair_train, y_train)
network_pair = Pipeline([
    ("scale", StandardScaler()),
    ("model", MLPClassifier(hidden_layer_sizes=(16,), alpha=1e-3, max_iter=4000,
                            random_state=42)),
]).fit(pair_train, y_train)

deviation = np.linspace(-8, 8, 240)
density = np.linspace(0.02, 0.16, 240)
mesh_deviation, mesh_density = np.meshgrid(deviation, density)
grid_frame = pd.DataFrame(
    {pair[0]: mesh_deviation.ravel(), pair[1]: mesh_density.ravel()}
)
network_surface = network_pair.predict_proba(grid_frame)[:, 1].reshape(mesh_deviation.shape)
linear_surface = linear_pair.predict_proba(grid_frame)[:, 1].reshape(mesh_deviation.shape)

fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.7), layout="constrained")

epochs = np.arange(1, len(history) + 1)
axes[0].plot(epochs, history[:, 0], color="tab:blue", linewidth=2.0,
             label=f"Training loss: {history[-1, 0]:.3f}")
axes[0].plot(epochs, history[:, 1], color="tab:orange", linestyle="--", linewidth=2.0,
             label=f"Held-out loss: {history[-1, 1]:.3f}")
axes[0].set(
    title="Hand-written network, 400 full-batch epochs",
    xlabel="Epoch",
    ylabel="Mean cross-entropy loss",
)
axes[0].grid(alpha=0.2)
axes[0].legend()

filled = axes[1].contourf(mesh_deviation, mesh_density, network_surface, levels=20,
                          cmap="Blues", alpha=0.75)
fig.colorbar(filled, ax=axes[1], label="Network complaint probability")
axes[1].contour(mesh_deviation, mesh_density, network_surface, levels=[0.5],
                colors=["tab:blue"], linewidths=2.2)
axes[1].contour(mesh_deviation, mesh_density, linear_surface, levels=[0.5],
                colors=["tab:orange"], linewidths=2.2, linestyles="--")
axes[1].scatter(pair_train[pair[0]][y_train == 0], pair_train[pair[1]][y_train == 0],
                s=9, color="0.35", marker="o", alpha=0.55, label="No complaint")
axes[1].scatter(pair_train[pair[0]][y_train == 1], pair_train[pair[1]][y_train == 1],
                s=13, color="tab:orange", marker="^", edgecolor="black",
                linewidth=0.3, label="Complaint")
axes[1].plot([], [], color="tab:blue", linewidth=2.2, label="Network boundary (0.50)")
axes[1].plot([], [], color="tab:orange", linewidth=2.2, linestyle="--",
             label="Logistic boundary (0.50)")
axes[1].set(
    title="Two features, two decision boundaries",
    xlabel="Setpoint deviation (C)",
    ylabel="Occupant density",
)
axes[1].legend(fontsize=7, loc="upper center", ncol=2, framealpha=0.92)

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "neural_network_comfort.png", dpi=200, bbox_inches="tight"
)
plt.show()
plt.close(fig)
