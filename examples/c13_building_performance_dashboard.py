"""Create the Chapter 13 building-performance dashboard."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# 1. Prepare repeatable example data.
rng = np.random.default_rng(12)
months = np.arange(1, 13)
heating = np.array([52, 46, 35, 22, 12, 5, 3, 4, 10, 24, 38, 49])
cooling = np.array([2, 3, 5, 9, 18, 31, 38, 36, 24, 12, 5, 2])
lighting = np.array([18, 17, 16, 15, 14, 13, 13, 13, 14, 15, 17, 18])
equipment = np.full(12, 21)
outdoor_c = np.array([-2, 0, 5, 11, 17, 22, 25, 24, 20, 13, 7, 1])

occupancy = np.clip(rng.normal(38, 22, size=(7, 24)), 0, 100)
occupancy[:, :7] *= 0.15
occupancy[:, 19:] *= 0.25
occupancy[5:, :] *= 0.35

# 2. Create a 2-by-2 array of Axes.
fig, axes = plt.subplots(2, 2, figsize=(11, 7), layout="constrained")
fig.suptitle("Building performance dashboard")

# 3. Show monthly composition.
axes[0, 0].stackplot(
    months,
    heating,
    cooling,
    lighting,
    equipment,
    labels=["Heating", "Cooling", "Lighting", "Equipment"],
    colors=["tab:blue", "tab:orange", "0.60", "#C6A15B"],
    alpha=0.88,
)
axes[0, 0].set(
    title="Monthly energy by end use",
    xlabel="Month",
    ylabel="Energy (MWh)",
)
axes[0, 0].legend(fontsize=8, ncol=2)

# 4. Add temperature context and a reference band.
axes[0, 1].plot(months, outdoor_c, color="tab:blue", marker="o")
axes[0, 1].axhspan(18, 24, color="tab:green", alpha=0.14)
axes[0, 1].set(
    title="Outdoor temperature context",
    xlabel="Month",
    ylabel="Temperature (degrees C)",
)

# 5. Convert the 7-by-24 matrix into a heatmap.
heatmap = axes[1, 0].imshow(
    occupancy,
    cmap="YlOrRd",
    aspect="auto",
    vmin=0,
    vmax=100,
)
axes[1, 0].set(
    title="Weekly occupancy pattern",
    xlabel="Hour",
    ylabel="Day",
    yticks=range(7),
    yticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
)
fig.colorbar(
    heatmap,
    ax=axes[1, 0],
    orientation="horizontal",
    fraction=0.08,
    pad=0.14,
    label="Occupancy (percent)",
)

# 6. Calculate and compare totals.
totals = heating + cooling + lighting + equipment
axes[1, 1].bar(months, totals, color="tab:blue")
axes[1, 1].axhline(
    totals.mean(),
    color="tab:orange",
    linestyle="--",
    label=f"Mean {totals.mean():.1f}",
)
axes[1, 1].set(
    title="Total monthly energy",
    xlabel="Month",
    ylabel="Energy (MWh)",
)
axes[1, 1].legend()

# 7. Apply shared finishing steps and export.
for ax in axes.flat:
    ax.grid(alpha=0.18)

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "building_performance_dashboard.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)
