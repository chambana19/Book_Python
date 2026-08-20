# -*- coding: utf-8 -*-
"""ARC 500 Project 1 provided module: one shared look for every figure.

This is a PROVIDED, BLACK-BOX module. You call apply_house_style(); you do
not need to read or edit the code below it to use it correctly. (If you are
curious, the code is short and plain on purpose - open it any time.)

Typical use, right after you build a figure:

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(summary["orientation"], summary["mean"])
    apply_house_style(
        ax,
        title="Mean energy use intensity by orientation, Radley Hall",
        xlabel="Orientation",
        ylabel="Energy use intensity (kWh/m2/yr)",
        source_note="Source: building_rooms.csv, course dataset",
    )
    fig.tight_layout()
    fig.savefig(SUBMISSION_DIR / "figure_01.png", dpi=200)

Every keyword argument (title=, xlabel=, ylabel=, source_note=) is passed
by NAME, not by position - this is the "call a function you didn't write,
with keyword arguments" pattern from Week 4.
"""

from matplotlib.axes import Axes


def apply_house_style(ax: Axes, title: str, xlabel: str, ylabel: str, source_note: str) -> Axes:
    """Label ax, add a small source note, and apply one consistent look; return ax."""
    # Title and axis labels: every figure states its question and units the same way.
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # A light grid makes values easier to read without dominating the figure.
    ax.grid(alpha=0.3)

    # Drop the top and right border lines; they carry no information here and
    # a plain three-sided frame reads as less cluttered.
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Small source note in the bottom-right corner, in axes-fraction coordinates
    # (0, 0) is the bottom-left of the plot area and (1, 1) is the top-right, so
    # this position stays in the same corner no matter what data is plotted.
    ax.text(
        1.0,
        -0.14,
        source_note,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8,
        color="gray",
    )

    return ax
