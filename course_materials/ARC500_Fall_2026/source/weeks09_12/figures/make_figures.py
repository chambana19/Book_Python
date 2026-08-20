"""Generate deterministic rendered figures used by the Weeks 9–12 decks."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUTPUT = Path(__file__).with_name("week09b_energy_sweep_heatmap.png")


def basin(x, y, cx, cy, depth, wx, wy):
    """Return one Gaussian dip using the exact Week 9 course formula."""
    dx = ((x - cx) ** 2) / (2 * wx ** 2)
    dy = ((y - cy) ** 2) / (2 * wy ** 2)
    return -depth * np.exp(-(dx + dy))


def energy_proxy(v):
    """Return the exact two-variable Week 9 energy proxy."""
    wwr, shade_m = v
    basin_local = basin(wwr, shade_m, 0.52, 0.25, 30.0, 0.06, 0.18)
    basin_lower = basin(wwr, shade_m, 0.28, 0.90, 34.0, 0.06, 0.18)
    ridge = 6.0 * np.exp(-((wwr - 0.40) ** 2) / 0.02)
    return 20.0 + basin_local + basin_lower + ridge


def main():
    """Render the 4,941-cell sweep with fixed data, style, and output settings."""
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    wwr_fine = np.linspace(0.20, 0.60, 81)
    shade_fine = np.linspace(0.0, 1.2, 61)
    wwr_grid, shade_grid = np.meshgrid(wwr_fine, shade_fine)
    values = energy_proxy((wwr_grid, shade_grid))

    assert values.shape == (61, 81)
    best = np.unravel_index(np.argmin(values), values.shape)
    assert np.isclose(wwr_grid[best], 0.275)
    assert np.isclose(shade_grid[best], 0.9)
    assert np.isclose(values[best], -11.135, atol=0.001)

    fig, ax = plt.subplots(figsize=(7, 5))
    mesh = ax.pcolormesh(
        wwr_grid,
        shade_grid,
        values,
        cmap="RdYlGn_r",
        shading="auto",
    )
    fig.colorbar(mesh, ax=ax, label="energy_proxy (lower is better)")
    ax.set_xlabel("wwr (window-to-wall ratio)")
    ax.set_ylabel("shade_m (overhang depth, m)")
    ax.set_title("energy_proxy(wwr, shade_m) — full sweep")
    fig.tight_layout()
    fig.savefig(
        OUTPUT,
        dpi=150,
        metadata={"Software": "ARC500 deterministic heatmap generator"},
    )
    plt.close(fig)
    print(f"wrote {OUTPUT} ({values.size} cells; minimum={values[best]:.3f})")


if __name__ == "__main__":
    main()
