# -*- coding: utf-8 -*-
"""ARC 500 Project 1 starter: create two static figures and one extension."""

# %% 0 — QUESTION
# Can this script find the cleaned evidence produced by analysis.py?
# INPUTS/ASSUMPTIONS
# Run analysis.py first from the same project package.
# METHOD
# Load exports with pathlib and pandas.
# CHECKS/INTERPRETATION
# Stop if an expected export is missing.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.text import Annotation

from course_style import apply_house_style

PROJECT_DIR = Path(__file__).resolve().parent.parent
SUBMISSION_DIR = PROJECT_DIR / "Submission"
CLEAN_FILE = SUBMISSION_DIR / "cleaned_data.csv"
SOURCE_NOTE = "Source: building_rooms.csv, course dataset"

if not CLEAN_FILE.exists():
    raise FileNotFoundError(
        "INPUT FILE ERROR [cell 0]: run the completed analysis.py first; cleaned_data.csv "
        "does not exist."
    )
data = pd.read_csv(CLEAN_FILE)
if data.empty:
    raise AssertionError("INPUT DATA CHECK FAILURE [cell 0]: cleaned_data.csv has no rows.")


def require_figure_ready(ax, cell: str, *, require_annotation: bool = False) -> None:
    """Stop before save when a figure still has placeholder labels or no data marks."""
    labels = [ax.get_title(), ax.get_xlabel(), ax.get_ylabel()]
    if any(not label.strip() or "TODO" in label.upper() for label in labels):
        raise NotImplementedError(
            f"EXPECTED TODO STOP [{cell}]: replace the title and both axis-label placeholders."
        )
    data_artist_count = len(ax.lines) + len(ax.collections) + len(ax.patches) + len(ax.images)
    if data_artist_count == 0:
        raise NotImplementedError(
            f"EXPECTED TODO STOP [{cell}]: plot data before save; no blank PNG was written."
        )
    if not any(text.get_text() == SOURCE_NOTE for text in ax.texts):
        raise AssertionError(f"FIGURE CHECK FAILURE [{cell}]: the source note is missing.")
    if require_annotation and not any(isinstance(text, Annotation) for text in ax.texts):
        raise NotImplementedError(
            f"EXPECTED TODO STOP [{cell}]: annotate one verified feature before save."
        )


# %% 1 — QUESTION
# What distribution or group comparison answers the project question?
# INPUTS/ASSUMPTIONS
# Use one meaningful group and one outcome with units.
# METHOD
# Build Figure 1 using the object-oriented fig/ax pattern.
# CHECKS/INTERPRETATION
# Verify labels, units, source note, and the saved PNG.

fig, ax = plt.subplots(figsize=(8, 5))
# TODO: create the distribution or grouped-comparison figure.
# apply_house_style is a PROVIDED, black-box function (see course_style.py):
# call it with keyword arguments, same as Week 4's pd.read_csv(path, sep=",").
apply_house_style(
    ax,
    title="TODO: evidence question, not a generic chart title",
    xlabel="TODO: variable and unit",
    ylabel="TODO: variable and unit",
    source_note=SOURCE_NOTE,
)
require_figure_ready(ax, "cell 1")
fig.tight_layout(rect=(0, 0.06, 1, 1))
fig.savefig(SUBMISSION_DIR / "figure_01.png", dpi=200, bbox_inches="tight")


# %% 2 — QUESTION
# What relationship or change qualifies the first finding?
# INPUTS/ASSUMPTIONS
# Use a different visual question from Figure 1.
# METHOD
# Build Figure 2 and annotate one important feature.
# CHECKS/INTERPRETATION
# The annotation must point to a value verified in the table.

fig, ax = plt.subplots(figsize=(8, 5))
# TODO: create the relationship or change figure.
# ax.annotate(...)
apply_house_style(
    ax,
    title="TODO: second evidence question",
    xlabel="TODO: variable and unit",
    ylabel="TODO: variable and unit",
    source_note=SOURCE_NOTE,
)
require_figure_ready(ax, "cell 2", require_annotation=True)
fig.tight_layout(rect=(0, 0.06, 1, 1))
fig.savefig(SUBMISSION_DIR / "figure_02.png", dpi=200, bbox_inches="tight")


# %% 3 — QUESTION
# Which single extension adds evidence: a map OR an animation?
# INPUTS/ASSUMPTIONS
# Complete only the relevant track using the Week 6 or Week 7 handout.
# METHOD
# Export map.png OR animation.gif.
# CHECKS/INTERPRETATION
# State what changes in the claim after seeing this extension.

# TODO: complete one track. Do not submit both unless approved as an extension, then set
# EXTENSION_FILE to the Path you created (for example SUBMISSION_DIR / "map.png").
EXTENSION_FILE = None

if EXTENSION_FILE is None:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 3]: complete one map OR animation track and set EXTENSION_FILE."
    )
EXTENSION_FILE = Path(EXTENSION_FILE)
if not EXTENSION_FILE.exists() or EXTENSION_FILE.stat().st_size == 0:
    raise FileNotFoundError(f"EXTENSION CHECK FAILURE [cell 3]: {EXTENSION_FILE} is missing or empty.")
if EXTENSION_FILE.suffix.lower() not in {".png", ".gif"}:
    raise AssertionError("EXTENSION CHECK FAILURE [cell 3]: export one PNG map or GIF animation.")
print("Extension verified:", EXTENSION_FILE)
