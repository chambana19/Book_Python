# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 6 studio · Visual reasoning: static and dynamic evidence
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
    # TODO: call ax.hist(...) on df[column].dropna() with the same bins, a fill color, and
    # edgecolor="white" so the bars are visible against each other
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
# TODO: add two assert statements checking energy_counts.sum() and the last bin's count
# against the CHECKS/INTERPRET values above.


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
    # TODO: call ax.bar(...) using summary.index.astype(str) and summary["mean_value"]
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
# TODO: add two assert statements checking zone_summary.loc["North", "mean_value"] and
# zone_summary.loc["South", "mean_value"] against the CHECKS/INTERPRET values above.


# %% [4] Relationship chart: does bigger area mean more or less energy use?
# QUESTION           Do larger rooms use more or less energy per square meter -- and where
#                    does Week 5's outlier room sit on that picture?
# INPUTS/ASSUMPTIONS area_m2 and energy_kwh_m2_yr for all rooms with a measured energy value;
#                    room R306 (8.0 m2, 410.0 kWh/m2/yr) -- the outlier both Week 5 rules
#                    flagged
# METHOD             scatter area_m2 vs. energy_kwh_m2_yr, colored by zone with a legend,
#                    then use ax.annotate to label R306 directly on the figure
# CHECKS/INTERPRET   Expected: 12 North points, 11 South points (23 total -- R206's missing
#                    energy value is dropped); the annotation arrow must point AT R306's dot,
#                    not away from it.


def make_relationship_chart(df: pd.DataFrame, x_col: str, y_col: str, group_col: str, out_path: pathlib.Path) -> None:
    """Scatter x_col vs y_col, colored by group_col (North/South), with room R306 annotated."""
    plot_df = df.dropna(subset=[y_col])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for group_value, color in zip(["North", "South"], ["#3D8DFF", "#C9473A"]):
        subset = plot_df[plot_df[group_col] == group_value]
        ax.scatter(subset[x_col], subset[y_col], color=color, label=f"{group_value} (n={len(subset)})")

    r306 = df.loc[df["room_id"] == "R306"].iloc[0]
    # xy is the data point the arrow points AT; xytext is where the text box sits.
    ax.annotate(
        f"R306: {r306[x_col]} m2, {r306[y_col]} kWh/m2/yr\n(both rules flag)",
        xy=(r306[x_col], r306[y_col]),
        xytext=(52, 400),
        arrowprops=dict(arrowstyle="->"),
    )
    # TODO: add a second ax.annotate(...) call for room R309 (120.0 m2, 68.0 kWh/m2/yr) --
    # the area_m2 outlier that the IQR and z-score rules DISAGREED on in Week 5. Look up
    # r309 the same way r306 is looked up above.

    ax.set_xlabel("Room area (m2)")
    ax.set_ylabel("Energy use intensity (kWh/m2/yr)")
    ax.set_title(f"{x_col} vs. {y_col} by {group_col}, Radley Hall")
    ax.legend(loc="lower right")
    fig.savefig(out_path)
    plt.close(fig)


make_relationship_chart(df, "area_m2", "energy_kwh_m2_yr", "zone", FIGURES_DIR / "area_vs_energy_relationship.png")
print("relationship chart saved to", FIGURES_DIR / "area_vs_energy_relationship.png")


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
        # TODO: clear ax, then redraw a bar chart of plot_df.iloc[: frame + 1] --
        # remember every axis label, limit, and title must be set again inside update(),
        # because ax.clear() erases them along with the previous frame's bars.
        pass

    ani = animation.FuncAnimation(fig, update, frames=n_rooms, interval=200)
    ani.save(out_path, writer="pillow", fps=5)
    plt.close(fig)
    return n_rooms


CAPTION = ("Radley Hall's 23 measured rooms, revealed one at a time from lowest to highest "
           "energy use intensity; the final bar is room R306, the server-closet outlier.")
n_frames = build_progressive_animation(df, "energy_kwh_m2_yr", FIGURES_DIR / "energy_reporting_animation.gif")
print(n_frames)
print(CAPTION)
# TODO: add one assert statement checking n_frames against the CHECKS/INTERPRET value above.


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

# TODO: write 2-4 assert statements here, checking:
#   1) floor_summary.loc[1, "n"] equals the expected floor-1 room count
#   2) floor_summary.loc[3, "n"] equals the expected floor-3 room count
#   3) floor_summary.loc[3, "mean_value"] is greater than floor_summary.loc[1, "mean_value"]
#   4) area_counts.sum() equals the expected total room count


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

# TODO: repair the line above (one small change) so it produces counts, then print them.
# TODO: in a comment, name why ax.hist() in cell [1] ran fine on the same column, while
# plain np.histogram() here raised an error.


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

# TODO: load your own Project 1 dataset here (my_df = pd.read_csv("your_file.csv")).

# TODO: call make_distribution_chart(my_df, "<your numeric column>", <bins>, ...).

# TODO: call make_comparison_chart(my_df, "<your grouping column>", "<your numeric column>", ...).

# TODO: adapt make_relationship_chart (or write a new, similar function) for two of YOUR OWN
# numeric columns, annotating at least one outlier from your own Week 5 outlier audit.

# TODO: call build_progressive_animation(my_df, "<your numeric column>", ...) and write your
# own one-sentence CAPTION describing what the animation shows.


# %% [9] AI-use record and exit reflection
# QUESTION           Did generative AI change what you submitted, and can you defend every
#                    retained line -- including the two functions with a filled-in TODO?
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio
# METHOD             fill in the AI-use record honestly, then write a short reflection
# CHECKS/INTERPRET   you must be able to trace, test, and explain every line you submit,
#                    including why each figure uses the encoding it does

ai_use_record = """
Tool/model:
Prompt:
Suggestion received:
What I accepted:
What I modified and why:
What I rejected and why:
How I tested it:
One limitation I found:
"""
print(ai_use_record)

exit_reflection = """
In 3-5 sentences: which encoding (distribution / comparison / relationship / change-over-time)
did you choose for each of your three static figures and why; what does your animation show
that a single static frame could not; and which outlier or turning point did you annotate,
on which figure, and why that one.
"""
print(exit_reflection)

# If you did not use generative AI, replace the record with:
# ai_use_record = "No generative AI used."

# %% ARCHITECTURAL TRANSFER — 3-minute exit check
# Match each question to one encoding and unit: room-area spread; embodied carbon
# by assembly; WWR versus EUI; monthly overheating hours. For each, name the
# chart, axis unit, and one honest annotation. Use animation only if the sequence
# reveals evidence that the corresponding static figure would hide.
