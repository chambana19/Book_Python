"""Optimize a simplified window ratio and verify the result visually."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar


def objective(window_ratio):
    """Return total modeled cost; lower values are preferred."""
    energy = 80 + 160 * (window_ratio - 0.18) ** 2
    daylight_penalty = 450 * max(0.0, 0.32 - window_ratio) ** 2
    glare_penalty = 600 * max(0.0, window_ratio - 0.55) ** 2
    return energy + daylight_penalty + glare_penalty


# 1. Establish feasible bounds and a transparent grid-search baseline.
lower_bound = 0.10
upper_bound = 0.70
grid = np.linspace(lower_bound, upper_bound, 13)
grid_values = np.array([objective(value) for value in grid])
grid_best_index = grid_values.argmin()
grid_best_ratio = grid[grid_best_index]

# 2. Use a bounded one-variable optimizer.
result = minimize_scalar(
    objective,
    bounds=(lower_bound, upper_bound),
    method="bounded",
)
if not result.success:
    raise RuntimeError(result.message)

# 3. Verify the recommendation rather than trusting it silently.
if not lower_bound <= result.x <= upper_bound:
    raise ValueError("Optimizer returned an infeasible ratio")

epsilon = 0.01
left_value = objective(max(lower_bound, result.x - epsilon))
right_value = objective(min(upper_bound, result.x + epsilon))
if result.fun > min(left_value, right_value):
    raise ValueError("Nearby candidates improve the reported solution")

print(f"Grid recommendation: {grid_best_ratio:.3f}")
print(f"Bounded recommendation: {result.x:.3f}")
print(f"Objective value: {result.fun:.2f}")

# 4. Plot the objective components and both searches.
ratios = np.linspace(lower_bound, upper_bound, 241)
energy = 80 + 160 * (ratios - 0.18) ** 2
daylight = 450 * np.maximum(0.0, 0.32 - ratios) ** 2
glare = 600 * np.maximum(0.0, ratios - 0.55) ** 2
total = energy + daylight + glare

fig, ax = plt.subplots(figsize=(8.2, 5.0), layout="constrained")
ax.plot(ratios, energy, color="0.45", linestyle=":", label="Energy")
ax.plot(
    ratios,
    daylight + glare,
    color="tab:orange",
    linestyle="--",
    label="Daylight + glare penalties",
)
ax.plot(ratios, total, color="tab:blue", linewidth=2.2, label="Total objective")
ax.scatter(
    grid,
    grid_values,
    facecolors="white",
    edgecolors="black",
    label="Grid candidates",
    zorder=3,
)
ax.scatter(
    [result.x],
    [result.fun],
    color="tab:orange",
    edgecolor="black",
    marker="*",
    s=170,
    label=f"Optimum {result.x:.3f}",
    zorder=4,
)
ax.set(
    title="Window-ratio optimization",
    xlabel="Window-to-wall ratio",
    ylabel="Objective value (lower is better)",
)
ax.grid(alpha=0.2)
ax.legend()

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "window_ratio_optimization.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)
