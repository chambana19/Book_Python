# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 6 studio · Visual reasoning: static and dynamic evidence · INSTRUCTOR SOLUTIONS
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in the same folder as building_rooms.csv.
  2. Click inside one # %% cell and press Ctrl+Enter to run just that cell.
  3. Watch the Plots pane and the Files pane (for saved .png/.gif files) after each cell.
  4. Predict what each figure will show before you run the cell, then compare.
  5. Restart the kernel and run from the top before submission.

LEARNING TARGETS
  - Match a question (distribution / comparison / relationship / change-over-time) to the
    right chart encoding, using the fig, ax pattern taught in Meeting A.
  - Label every axis with its unit, add a legend whenever more than one series is plotted,
    and annotate at least one outlier directly on a figure.
  - Build one matplotlib.animation.FuncAnimation and save it as a .gif -- dynamic evidence,
    treated as equal in weight to the three static figures, not a lecture aside.
  - Apply this exact pipeline to your OWN Project 1 dataset for this week's submission.

AI-USE RULE
  You may use generative AI. You may not submit code you cannot trace, test, and explain.
  Keep a short record (2-3 sentences per item): one suggestion you accepted, one you
  modified, one you rejected -- and why.
"""

# %% [0] Confirm your libraries and the Radley Hall data are ready
# QUESTION           Do pandas, NumPy, and Matplotlib import cleanly, and is the shared
#                    Radley Hall dataset sitting where this script expects it?
# INPUTS/ASSUMPTIONS building_rooms.csv, saved in the same folder as this script
# METHOD             import the three libraries, read the CSV, and print its shape and the
#                    number of missing energy_kwh_m2_yr values
# CHECKS/INTERPRET   Expected shape: (24, 12). Expected missing energy_kwh_m2_yr count: 1
#                    (room R206 -- the same missing value the Week 4 trustworthiness
#                    interview and the Week 5 groupby both already worked around).

import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

DATA_PATH = "building_rooms.csv"
FIGURES_DIR = pathlib.Path("week06_figures")
FIGURES_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)
print(df.shape)
print(df["energy_kwh_m2_yr"].isna().sum())
assert df.shape == (24, 12)
assert df["energy_kwh_m2_yr"].isna().sum() == 1

# WHY THIS MATTERS: every figure below is only as trustworthy as this cell. If shape or the
# missing-value count is ever wrong, every downstream chart is evidence about the wrong data.


# %% [1] Distribution chart: how spread out is room energy use?
# QUESTION           How is energy_kwh_m2_yr spread across Radley Hall's 24 rooms?
# INPUTS/ASSUMPTIONS the energy_kwh_m2_yr column (1 missing value, dropped before plotting)
# METHOD             write a function that builds a labeled histogram with fig, ax, saves it
#                    as a .png, and returns the bin counts so they can be checked
# CHECKS/INTERPRET   Expected bin counts (bins=6): [13  9  0  0  0  1] -- the counts must sum
#                    to 23, and the last bin (room R306's 410.0 kWh/m2/yr) should hold exactly 1.


def make_distribution_chart(df: pd.DataFrame, column: str, bins: int, out_path: pathlib.Path) -> np.ndarray:
    """Save a histogram of one numeric column, with labeled axes and units; return bin counts."""
    counts, edges = np.histogram(df[column].dropna(), bins=bins)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df[column].dropna(), bins=bins, color="#3D8DFF", edgecolor="white")
    ax.set_xlabel("Energy use intensity (kWh/m2/yr)")
    ax.set_ylabel("Number of rooms")
    ax.set_title("Distribution of room energy use, Radley Hall")
    fig.savefig(out_path)
    # plt.close(fig) releases this figure from memory once it is saved -- harmless the one
    # time a script builds a single chart, but this function (and the three after it) gets
    # called several times today (cells [3], [6], [8]), so skipping this line would leave one
    # open figure sitting in memory per call instead of just the one currently on screen.
    plt.close(fig)
    return counts


energy_counts = make_distribution_chart(df, "energy_kwh_m2_yr", 6, FIGURES_DIR / "energy_distribution.png")
print(energy_counts)
assert energy_counts.sum() == 23
assert energy_counts[-1] == 1

# COMMON ERROR: calling ax.hist(df[column], bins=bins) WITHOUT .dropna() first. ax.hist()
# happens to tolerate a NaN silently (it drops it internally before binning) -- but the
# plain np.histogram() call two lines above it does NOT, and raises ValueError if it ever
# receives the undropped column. Cell [7]'s AI audit is built around exactly this gap.
# WHY THIS MATTERS: four straight empty bins is not a bug in your code -- it is real
# evidence that one extreme value (R306) can distort the entire visible range. Reporting a
# distribution without noticing this would misrepresent the other 22 rooms' actual spread.


# %% [2] Build the histogram bins yourself
# QUESTION           What exactly does bins=6 do before a single bar is ever drawn?
# INPUTS/ASSUMPTIONS the same energy_kwh_m2_yr column, missing value dropped
# METHOD             call np.histogram directly and print both the counts and the bin edges
# CHECKS/INTERPRET   Expected counts: [13  9  0  0  0  1]. Expected edges (rounded to 1
#                    decimal): [ 12.   78.3 144.7 211.  277.3 343.7 410. ] -- four empty
#                    bins in a row is not a bug; one extreme value (R306) stretches the
#                    whole axis.

counts, edges = np.histogram(df["energy_kwh_m2_yr"].dropna(), bins=6)
print(counts)
print(np.round(edges, 1))


# %% [3] Comparison chart: North vs. South, made visible
# QUESTION           How much higher is South zone's mean energy use than North's -- and can
#                    a reader see that gap without reading a table?
# INPUTS/ASSUMPTIONS the Week 5 headline finding: North vs. South mean energy_kwh_m2_yr
# METHOD             write a function that groups by any column, builds a labeled bar chart
#                    with per-bar value annotations, saves it, and returns the summary table
# CHECKS/INTERPRET   Expected: North mean_value 64.25 (n=12), South mean_value 115.68 (n=12)
#                    -- the exact Week 5 numbers; this chart does not recompute them.


def make_comparison_chart(df: pd.DataFrame, group_col: str, value_col: str, out_path: pathlib.Path) -> pd.DataFrame:
    """Bar chart of mean(value_col) by group_col; return the (mean_value, n) summary table."""
    summary = df.groupby(group_col).agg(
        mean_value=(value_col, "mean"),
        n=("room_id", "count"),
    ).round(2)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(summary.index.astype(str), summary["mean_value"], color="#3D8DFF")
    ax.set_xlabel(str(group_col).capitalize())
    ax.set_ylabel(f"Mean {value_col} (kWh/m2/yr)")
    ax.set_title(f"Mean {value_col} by {group_col}, Radley Hall")
    for i, v in enumerate(summary["mean_value"]):
        ax.annotate(f"{v:.2f}", (i, v), ha="center", va="bottom")
    fig.savefig(out_path)
    plt.close(fig)
    return summary


zone_summary = make_comparison_chart(df, "zone", "energy_kwh_m2_yr", FIGURES_DIR / "zone_energy_comparison.png")
print(zone_summary)
assert zone_summary.loc["North", "mean_value"] == 64.25
assert zone_summary.loc["South", "mean_value"] == 115.68

# COMMON ERROR: leaving only ax.set_xlabel() filled in and skipping ax.set_ylabel(), or
# labeling the y-axis "energy" with no unit. An unlabeled or unit-free axis leaves a bar
# chart's actual claim ambiguous -- exactly the mistake the Meeting A "labeled axes with
# units" slide warns about.
# WHY THIS MATTERS: this bar chart is how you make the Week 5 group-difference finding
# legible to a reader who will never open the groupby table -- Project 1 Part III requires
# a comparison figure for exactly this reason.


# %% [4] Relationship chart: does bigger area mean more or less energy use?
# QUESTION           Do larger rooms use more or less energy per square meter -- and where
#                    does Week 5's outlier room sit on that picture?
# INPUTS/ASSUMPTIONS area_m2 and energy_kwh_m2_yr for all rooms with a measured energy value;
#                    room R306 (8.0 m2, 410.0 kWh/m2/yr) -- the outlier both Week 5 rules
#                    flagged
# METHOD             scatter area_m2 vs. energy_kwh_m2_yr, colored by zone with a legend,
#                    then use ax.annotate to label R306 and R309 directly on the figure
# CHECKS/INTERPRET   Expected: 12 North points, 11 South points (23 total -- R206's missing
#                    energy value is dropped); both annotation arrows must point AT their
#                    room's dot, not away from it.


def make_relationship_chart(df: pd.DataFrame, x_col: str, y_col: str, group_col: str, out_path: pathlib.Path) -> None:
    """Scatter x_col vs y_col, colored by group_col (North/South), with R306 and R309 annotated."""
    plot_df = df.dropna(subset=[y_col])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for group_value, color in zip(["North", "South"], ["#3D8DFF", "#C9473A"]):
        subset = plot_df[plot_df[group_col] == group_value]
        ax.scatter(subset[x_col], subset[y_col], color=color, label=f"{group_value} (n={len(subset)})")

    # xy is the data point the arrow points AT; xytext is where the text box sits.
    r306 = df.loc[df["room_id"] == "R306"].iloc[0]
    ax.annotate(
        f"R306: {r306[x_col]} m2, {r306[y_col]} kWh/m2/yr\n(both rules flag)",
        xy=(r306[x_col], r306[y_col]),
        xytext=(52, 400),
        arrowprops=dict(arrowstyle="->"),
    )
    r309 = df.loc[df["room_id"] == "R309"].iloc[0]
    ax.annotate(
        f"R309: {r309[x_col]} m2, {r309[y_col]} kWh/m2/yr\n(rules disagree)",
        xy=(r309[x_col], r309[y_col]),
        xytext=(58, 190),
        arrowprops=dict(arrowstyle="->"),
    )

    ax.set_xlabel("Room area (m2)")
    ax.set_ylabel("Energy use intensity (kWh/m2/yr)")
    ax.set_title(f"{x_col} vs. {y_col} by {group_col}, Radley Hall")
    ax.legend(loc="lower right")
    fig.savefig(out_path)
    plt.close(fig)


make_relationship_chart(df, "area_m2", "energy_kwh_m2_yr", "zone", FIGURES_DIR / "area_vs_energy_relationship.png")
print("relationship chart saved to", FIGURES_DIR / "area_vs_energy_relationship.png")

# COMMON ERROR: swapping xy and xytext -- the arrow then points FROM the data at empty
# space TO the text box, backwards from what a reader expects. xy is always the claim
# ("this is the point"); xytext is always the label's own position.
# WHY THIS MATTERS: an annotated scatter is how a reviewer sees a room's severity (energy)
# and its context (area) at the same time -- Project 1 Part III requires at least one
# annotated outlier or turning point for exactly this reason.


# %% [5] Dynamic evidence: animate rooms reporting in
# QUESTION           Can the SAME energy evidence be shown changing over a sequence, instead
#                    of only as one finished, static picture?
# INPUTS/ASSUMPTIONS the 23 rooms with a measured energy_kwh_m2_yr value, sorted low to high
# METHOD             write update(frame) to redraw a bar chart through the current frame's
#                    rooms only, wrap it in FuncAnimation, and save the result as a .gif
# CHECKS/INTERPRET   Expected frame count: 23 (one frame per measured room). The .gif's last
#                    frame should look exactly like the static bar chart with all 23 rooms
#                    shown, sorted ascending, ending on room R306's tall final bar.


def build_progressive_animation(df: pd.DataFrame, value_col: str, out_path: pathlib.Path) -> int:
    """Animate rooms appearing one at a time, sorted by value_col; save as a .gif; return frame count."""
    plot_df = df.dropna(subset=[value_col]).sort_values(value_col).reset_index(drop=True)
    n_rooms = len(plot_df)
    fig, ax = plt.subplots(figsize=(7, 4))

    def update(frame: int):
        ax.clear()
        shown = plot_df.iloc[: frame + 1]
        ax.bar(shown["room_id"], shown[value_col], color="#3D8DFF")
        ax.set_xlim(-0.5, n_rooms - 0.5)
        ax.set_ylim(0, plot_df[value_col].max() * 1.05)
        ax.set_xlabel("Room (sorted low to high)")
        ax.set_ylabel(f"{value_col} (kWh/m2/yr)")
        ax.set_title(f"Radley Hall rooms reporting in: {frame + 1} of {n_rooms}")
        ax.tick_params(axis="x", rotation=90, labelsize=6)

    ani = animation.FuncAnimation(fig, update, frames=n_rooms, interval=200)
    ani.save(out_path, writer="pillow", fps=5)
    plt.close(fig)
    return n_rooms


CAPTION = ("Radley Hall's 23 measured rooms, revealed one at a time from lowest to highest "
           "energy use intensity; the final bar is room R306, the server-closet outlier.")
n_frames = build_progressive_animation(df, "energy_kwh_m2_yr", FIGURES_DIR / "energy_reporting_animation.gif")
print(n_frames)
print(CAPTION)
assert n_frames == 23

# COMMON ERROR: forgetting ax.clear() at the top of update(), so every frame's bars pile on
# top of the previous frame's instead of being redrawn cleanly; or clearing ax but forgetting
# to reset set_xlim/set_ylim/labels/title inside update(), since ax.clear() erases all of
# them along with the old bars, not just the data.
# WHY THIS MATTERS: a captioned .gif shows evidence accumulating, room by room, not just a
# finished state -- static and dynamic are graded as two co-equal figures this week, not one
# primary chart plus an optional extra.


# %% [6] CHECKS/INTERPRET: self-generated check on a different input
# QUESTION           Do the SAME two functions from cells [1] and [3] hold up correctly on a
#                    different grouping column (floor instead of zone) and a different
#                    measured column (area_m2 instead of energy_kwh_m2_yr)?
# INPUTS/ASSUMPTIONS the same Radley Hall dataset; group by "floor" instead of "zone"; a
#                    4-bin histogram of area_m2 instead of a 6-bin histogram of
#                    energy_kwh_m2_yr
# METHOD             call make_comparison_chart(df, "floor", "energy_kwh_m2_yr", ...) and
#                    np.histogram(df["area_m2"], bins=4); write 2-4 asserts checking the
#                    results against the expected values stated below
# CHECKS/INTERPRET   Expected room counts by floor: floor 1 -> 7, floor 2 -> 8, floor 3 -> 9.
#                    Floor 3's mean energy should be the highest of the three floors.
#                    Expected area_m2 histogram counts (bins=4): they must sum to 24 (area_m2
#                    has no missing values, unlike energy_kwh_m2_yr).

floor_summary = make_comparison_chart(df, "floor", "energy_kwh_m2_yr", FIGURES_DIR / "floor_energy_selfcheck.png")
print(floor_summary)

area_counts, area_edges = np.histogram(df["area_m2"], bins=4)
print(area_counts)

assert floor_summary.loc[1, "n"] == 7
assert floor_summary.loc[2, "n"] == 8
assert floor_summary.loc[3, "n"] == 9
assert floor_summary.loc[3, "mean_value"] > floor_summary.loc[1, "mean_value"]
assert area_counts.sum() == 24

# COMMON ERROR: writing floor_summary.loc["1", "n"] with the floor number as a string. The
# floor column is int64 (see Week 4's dtype interview), so its index labels after groupby
# are integers too -- floor_summary.loc[1, ...], not floor_summary.loc["1", ...].
# WHY THIS MATTERS: this is the week's required transfer safeguard -- the same two
# functions, unchanged, must produce correct evidence on a different column and a different
# grouping variable, not just on the one example worked through live.


# %% [7] AI-code audit
# QUESTION           An AI assistant wrote the two lines below to redo cell [2]'s histogram
#                    "more directly." Predict what happens before you run it.
# INPUTS/ASSUMPTIONS the same energy_kwh_m2_yr column used in cells [1]-[2], WITHOUT calling
#                    .dropna() first
# METHOD             run the AI snippet inside a try/except, read the exact error, then
#                    write the one-line repair and confirm it produces the correct counts
# CHECKS/INTERPRET   The AI snippet raises ValueError: autodetected range of [nan, nan] is
#                    not finite. Name why ax.hist() from cell [1] did not raise this same
#                    error on the identical column, then apply the one-line fix below.

try:
    ai_counts, ai_edges = np.histogram(df["energy_kwh_m2_yr"], bins=6)
    print(ai_counts)
except ValueError as e:
    print("ValueError:", e)

fixed_counts, fixed_edges = np.histogram(df["energy_kwh_m2_yr"].dropna(), bins=6)
print(fixed_counts)
assert list(fixed_counts) == [13, 9, 0, 0, 0, 1]

# Defect named: np.histogram(df["energy_kwh_m2_yr"], bins=6) is called on the raw column,
# which still contains room R206's missing value. np.histogram tries to auto-detect the
# data's min/max range first; with a NaN present, that auto-detected range is itself NaN,
# so numpy refuses to build bins at all and raises immediately -- there is no partial or
# silently-wrong result here, just a hard stop.
# Why ax.hist() did not: matplotlib's Axes.hist() runs its own finite-value filtering
# before it ever calls np.histogram internally, so it silently drops the one NaN row and
# still returns the correct 23-room counts -- ax.hist() and a bare np.histogram() call are
# NOT interchangeable on data with missing values, even though they look equivalent.
# The one-line fix: add .dropna() before the column reaches np.histogram, exactly as cell
# [2] already does.
# WHY THIS MATTERS: an AI assistant will often copy a pattern that "looks like" a working
# example nearby without noticing the one call that filters missing data internally and the
# one that does not -- reading the actual error message, not guessing, is the reproducible
# habit this course is building.


# %% [8] Apply this pipeline to YOUR OWN Project 1 dataset
# QUESTION           Does this exact pattern -- distribution, comparison, relationship, and
#                    one animation -- produce defensible evidence on YOUR chosen dataset?
# INPUTS/ASSUMPTIONS your own cleaned Project 1 CSV from Weeks 4-5, with at least one numeric
#                    column and one categorical grouping column of your own
# METHOD             copy cells [1], [3], [4], and [5] below one at a time, replacing the
#                    Radley Hall column names with your own dataset's column names, and
#                    annotate at least one outlier or turning point from YOUR OWN Week 5 work
# CHECKS/INTERPRET   This week's submission is three static figures (distribution,
#                    comparison, relationship) plus one captioned .gif, built on YOUR dataset
#                    -- not a second copy of the Radley Hall figures above.

# Example shape only -- column names below are illustrative, not literal:
#
# my_df = pd.read_csv("my_project1_data.csv")
# make_distribution_chart(my_df, "my_numeric_column", 6, FIGURES_DIR / "my_distribution.png")
# make_comparison_chart(my_df, "my_group_column", "my_numeric_column", FIGURES_DIR / "my_comparison.png")
# make_relationship_chart(my_df, "my_x_column", "my_y_column", "my_group_column", FIGURES_DIR / "my_relationship.png")
# build_progressive_animation(my_df, "my_numeric_column", FIGURES_DIR / "my_animation.gif")
#
# make_relationship_chart above still hardcodes "North"/"South" and room R306 -- reusing it
# unchanged on a different dataset is itself a plausible AI-suggested shortcut worth
# rejecting; adapt the group values and the annotated room/row to your own data and your own
# Week 5 outlier finding instead of copying this function's internals verbatim.

# WHY THIS MATTERS: this is the Week 6 Project 1 milestone -- the same skill applied to your
# own research question, not a second exercise layered on top of it.


# %% [9] AI-use record and exit reflection
# QUESTION           Did generative AI change what you submitted, and can you defend every
#                    retained line -- including the two functions with a filled-in TODO?
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio
# METHOD             fill in the AI-use record honestly, then write a short reflection
# CHECKS/INTERPRET   you must be able to trace, test, and explain every line you submit,
#                    including why each figure uses the encoding it does

ai_use_record = """
Tool/model: Example assistant
Prompt: Write update(frame) for a FuncAnimation that redraws a bar chart of rooms reporting in.
Suggestion received: An update(frame) that called ax.bar() every frame without ever calling
ax.clear() first, and a FuncAnimation block with no plt.close(fig) after ani.save().
What I accepted: The overall shape -- sort by value_col, build one fig, ax outside update(),
call FuncAnimation with frames=n_rooms.
What I modified and why: Added ax.clear() at the top of update() and re-set every axis limit,
label, and title inside it, since ax.clear() wipes them along with the previous frame's bars;
also added plt.close(fig) after each figure is saved, since this file now builds four figures
in one run and an unclosed figure stays in memory even after its .png or .gif is written.
What I rejected and why: The AI's version of cell [2]'s histogram call, which reused the same
undropped np.histogram(df["energy_kwh_m2_yr"], bins=6) pattern that cell [7]'s AI audit shows
raises ValueError -- the same defect, offered twice by the same assistant.
How I tested it: Reran build_progressive_animation, asserted n_frames == 23, then opened the
saved energy_reporting_animation.gif and confirmed its last frame matched the static bar
chart from cell [3] with all 23 rooms shown.
One limitation I found: A saved .gif can only be watched linearly -- unlike a live
FuncAnimation inside Spyder, a reader cannot pause it or scrub back to an earlier frame.
"""
print(ai_use_record)

exit_reflection = """
I chose a histogram for the distribution question (cell [1]), a bar chart for the North vs.
South comparison (cell [3]), and a colored scatter for the area-vs-energy relationship
(cell [4]) -- matching each question (spread, group difference, correlation) to the encoding
built for exactly that question in Meeting A. The animation (cell [5]) shows the same 23
rooms accumulating one at a time, sorted low to high, which no single static frame can: a
viewer sees most rooms cluster quietly below 100 kWh/m2/yr for most of the sequence, then
watches room R306's bar jump far above every other room only in the final frame -- a sense
of gradual buildup that a finished bar chart compresses into one static fact. On the
relationship scatter I annotated both R306 (410.0 kWh/m2/yr on just 8.0 m2, the server
closet both Week 5 outlier rules flagged) and R309 (120.0 m2, the area outlier the two rules
disagreed on), because that figure is the one place a room's energy severity and its
physical size are visible at the same time.
"""
print(exit_reflection)

# If you did not use generative AI, replace the record with:
# ai_use_record = "No generative AI used."

print("all checks passed")

# %% ARCHITECTURAL TRANSFER — 3-minute exit check
# Expected encodings: histogram for room-area spread (m²); bar for carbon by
# assembly (kgCO2e); scatter for WWR–EUI (dimensionless, kWh/m²/yr); line for
# monthly overheating (hours/month). Animation is justified only when an
# accumulation or transition—not decorative motion—is part of the evidence.
