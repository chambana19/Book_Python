# -*- coding: utf-8 -*-
"""Shared matplotlib style for every ARC 500 slide figure.

One style module for all four course blocks, for the same reason the decks share
`_design/tokens.mjs`: a figure in Week 4 and a figure in Week 14 should look like they
belong to the same course. Colours here are the deck palette from tokens.mjs, so a chart
on a slide sits in the same visual language as the slide around it.

Every figure a deck shows is produced by one of the `make_figures.py` scripts that import
this module, using the real course datasets and the same code students run in the
handouts -- so a slide's picture can never drift from the code that produced it.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Deck palette (must match _design/tokens.mjs)
INK = "#111316"
MUTED = "#5A5F66"
RULE = "#DDE0E5"
ACCENT = "#2F7BE8"
ACCENT_DEEP = "#1B5FC4"
GREEN = "#2E7D5B"
RED = "#C9473A"
AMBER = "#B5731A"
PANEL = "#F6F7F9"

# Categorical order used consistently across the course: North vs South, keep/flag, etc.
SERIES = [ACCENT, RED, GREEN, AMBER, ACCENT_DEEP]

# Figures are rendered into a panel roughly 700x430pt on a 1280x720 slide. Rendering at
# 7.2x4.4in / 200dpi keeps text crisp at that size without the labels turning to mush.
FIGSIZE = (7.2, 4.4)
DPI = 200


def apply_style() -> None:
    """Set the shared rcParams. Call once at the top of a make_figures.py script."""
    plt.rcParams.update({
        "figure.figsize": FIGSIZE,
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans"],
        # Deliberately large: the figure is scaled down into a slide panel, so anything
        # under ~13pt here becomes unreadable from the back of a room.
        "font.size": 13,
        "axes.titlesize": 15,
        "axes.labelsize": 13,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.grid": True,
        "grid.color": RULE,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "figure.autolayout": True,
    })


# The slide's figure panel is about 724x408pt, so roughly 1.75:1. Figures near that
# aspect fill the panel; much wider or taller ones letterbox (fit is "contain", which
# never crops, so letterboxing is the safe failure rather than a cut-off axis label).
TARGET_ASPECT = 1.75


def concept_fig(width: float = 7.6, height: float = 4.3):
    """Blank canvas for a concept diagram, in convenient 0-100 x 0-100 coordinates.

    Concept diagrams are drawn with the same toolchain and palette as the data plots so
    a diagram and a chart on consecutive slides look like the same course, rather than
    one being clip-art pasted next to the other.
    """
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.grid(False)
    return fig, ax


def box(ax, x, y, w, h, label, face=PANEL, edge=ACCENT, text_color=INK,
        bold=True, fontsize=13, radius=2.0):
    """Rounded label box on a concept_fig canvas. (x, y) is the box's centre."""
    from matplotlib.patches import FancyBboxPatch
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=face, edgecolor=edge, linewidth=1.8, zorder=2,
    ))
    ax.text(x, y, label, ha="center", va="center", color=text_color,
            fontsize=fontsize, fontweight="bold" if bold else "normal", zorder=3)


def arrow(ax, x1, y1, x2, y2, color=MUTED, label=None, fontsize=11):
    """Arrow between two points on a concept_fig canvas, with an optional mid label."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, linewidth=2.0,
                                shrinkA=2, shrinkB=2), zorder=1)
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 3.5, label, ha="center", va="bottom",
                color=color, fontsize=fontsize)


def save(fig, out_dir, name: str) -> str:
    """Save `fig` as a PNG into out_dir and return the path. Closes the figure."""
    from pathlib import Path
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  wrote {name}")
    return str(path)
