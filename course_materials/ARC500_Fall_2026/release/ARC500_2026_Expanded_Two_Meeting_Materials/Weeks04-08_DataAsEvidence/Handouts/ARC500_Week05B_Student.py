# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 5 studio · Grouping, dual-rule outlier audits, and your Project 1 checkpoint
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file, and building_rooms.csv, in the same Week05 module folder.
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict the printed value before running; compare with CHECKS/INTERPRET.
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A flag from the IQR rule or the z-score rule is a question, not a verdict. Every flagged
  row gets a written keep / investigate / exclude decision - never a silent delete.
"""

# %% [0] Environment and working-folder check
# QUESTION           Run the cell and confirm your Python version, executable, and working
#                    folder, and that building_rooms.csv sits in the same folder.
# INPUTS/ASSUMPTIONS no inputs; Spyder is installed, this file is open, and
#                    building_rooms.csv (the shared Weeks 4-7 dataset) is saved alongside it.
# METHOD             run the cell and read the three printed environment lines in the
#                    console.
# CHECKS/INTERPRET   You should see a Python version, an executable path, and a folder path
#                    with no error.

from pathlib import Path
import sys

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())


# %% [1] Load Radley Hall and recall the trustworthiness numbers
# QUESTION           Confirm the shared Radley Hall dataset loads and matches Week 4's
#                    trustworthiness-interview numbers.
# INPUTS/ASSUMPTIONS building_rooms.csv: 24 rooms, 12 columns; one missing has_daylight
#                    value (room R303) and one missing energy_kwh_m2_yr value (room R206).
# METHOD             read_csv, then print the shape and a five-column dtype subset.
# CHECKS/INTERPRET   Expected shape: (24, 12). area_m2 and energy_kwh_m2_yr should print as
#                    float64; room_id, zone, and room_type as str.

import pandas as pd

df = pd.read_csv("building_rooms.csv")

print(df.shape)
print(df[["room_id", "zone", "room_type", "area_m2", "energy_kwh_m2_yr"]].dtypes)

if df.shape != (24, 12):
    raise AssertionError(f"DATA CHECK FAILURE [cell 1]: expected (24, 12), loaded {df.shape}.")


# %% [2] Recall: group by zone with multiple named aggregations
# QUESTION           Reproduce Meeting A's headline zone comparison before extending the
#                    pattern to a new category.
# INPUTS/ASSUMPTIONS energy_kwh_m2_yr, area_m2, room_id columns; group key is zone.
# METHOD             complete the three named aggregations below, then round to 2 decimals.
# CHECKS/INTERPRET   Expected: North mean_energy 64.25, South mean_energy 115.68; mean_area
#                    40.98 and 38.25; n = 12 for both zones.

zone_summary = df.groupby("zone").agg(
    mean_energy=("energy_kwh_m2_yr", "sum"),  # TODO: change "sum" to "mean"
    mean_area=("area_m2", "sum"),              # TODO: change "sum" to "mean"
    n=("room_id", "count"),
).round(2)

print(zone_summary)

if not (
    abs(zone_summary.loc["North", "mean_energy"] - 64.25) < 0.01
    and abs(zone_summary.loc["South", "mean_energy"] - 115.68) < 0.01
    and abs(zone_summary.loc["North", "mean_area"] - 40.98) < 0.01
    and abs(zone_summary.loc["South", "mean_area"] - 38.25) < 0.01
    and zone_summary["n"].tolist() == [12, 12]
):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 2]: change both placeholder aggregations from sum to mean."
    )


# %% [3] Studio 1 - group by room_type and rank
# QUESTION           Build the same three-aggregation pattern for room_type instead of zone,
#                    then rank the result by mean energy.
# INPUTS/ASSUMPTIONS same columns as cell [2]; group key is now room_type (7 categories).
# METHOD             copy the pattern from cell [2], then sort_values on mean_energy.
# CHECKS/INTERPRET   Expected top of ranking: Server (410.0, n=1), Studio (94.0, n=6).
#                    Expected bottom: Closet (12.0, n=1).

room_type_summary = df.groupby("room_type").agg(
    mean_energy=("energy_kwh_m2_yr", "sum"),  # TODO: change "sum" to "mean"
    n=("room_id", "count"),
).round(2)

ranked = room_type_summary  # TODO: sort_values by mean_energy, descending

print(ranked)

# TODO: Server and Closet both have n = 1. Write one sentence: does a single-room category
# deserve the same confidence as a 10-room category?

if (
    ranked.index[0] != "Server"
    or abs(ranked.iloc[0]["mean_energy"] - 410.0) > 0.01
    or ranked.index[-1] != "Closet"
    or abs(ranked.iloc[-1]["mean_energy"] - 12.0) > 0.01
):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 3]: calculate mean energy by room type and rank descending."
    )


# %% [4] describe() and value_counts(): a fast first look
# QUESTION           Read a column's overall shape and a category's frequency, with no
#                    grouping at all.
# INPUTS/ASSUMPTIONS energy_kwh_m2_yr (23 non-missing values) and zone (24 values, none
#                    missing).
# METHOD             call .describe() on one numeric column and .value_counts() on one
#                    categorical column.
# CHECKS/INTERPRET   Expected describe() count: 23 (one missing value, room R206). Expected
#                    value_counts(): North 12, South 12.

print(df["energy_kwh_m2_yr"].describe())
print(df["zone"].value_counts())


# %% [5] Write the IQR-rule function
# QUESTION           Turn the IQR/boxplot rule from Meeting A into one reusable function.
# INPUTS/ASSUMPTIONS any numeric Series; Q1 and Q3 come from .quantile(0.25) /
#                    .quantile(0.75).
# METHOD             complete iqr_bounds() to return the fence bounds, then complete
#                    flag_iqr() to compare each value against those bounds. IMPORTANT:
#                    combining two Boolean Series needs & and |, each condition in its own
#                    parentheses - NOT Python's and/or from Weeks 2-3, which raises
#                    "ValueError: The truth value of a Series is ambiguous" on a Series.
# CHECKS/INTERPRET   Cell [6] checks this function against room R306; expect True.

def iqr_bounds(values: pd.Series) -> tuple[float, float]:
    """Return (low, high) IQR fence bounds."""
    q1, q3 = values.quantile(0.25), values.quantile(0.75)
    iqr = q3 - q1
    # TODO: return low = q1 - 1.5 * iqr and high = q3 + 1.5 * iqr
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: return q1 - 1.5*IQR and q3 + 1.5*IQR."
    )


def flag_iqr(df: pd.DataFrame, col: str) -> pd.Series:
    """True where df[col] sits outside the IQR bounds."""
    low, high = iqr_bounds(df[col])
    # TODO: return a Boolean Series, True where (df[col] < low) | (df[col] > high).
    # Use & / | with parentheses around each condition - NOT and/or, which errors on a Series.
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: return the two-sided Boolean IQR flag Series."
    )


# %% [6] Studio 2 - apply the IQR rule to energy_kwh_m2_yr
# QUESTION           Confirm your flag_iqr() function catches the room Meeting A flagged.
# INPUTS/ASSUMPTIONS the flag_iqr() function from cell [5]; room R306 (a server closet).
# METHOD             add a flag column, then print only R306's row.
# CHECKS/INTERPRET   Expected: iqr_flag_energy is True for R306. If it is False, revisit
#                    cell [5] before continuing.

df["iqr_flag_energy"] = flag_iqr(df, "energy_kwh_m2_yr")

print(df.loc[df["room_id"] == "R306", ["room_id", "energy_kwh_m2_yr", "iqr_flag_energy"]])

# TODO: State the IQR bounds you computed (low, high) in your own words.

low_check, high_check = iqr_bounds(df["energy_kwh_m2_yr"])
r306_iqr = bool(df.loc[df["room_id"] == "R306", "iqr_flag_energy"].iloc[0])
if abs(low_check - 18.25) > 0.01 or abs(high_check - 134.25) > 0.01 or not r306_iqr:
    raise AssertionError(
        "OUTLIER CHECK FAILURE [cell 6]: expected fences 18.25/134.25 and R306 flagged True."
    )


# %% [7] Draw the boxplot: the IQR rule made visible
# QUESTION           Where do cell [6]'s two fence numbers actually fall, and which rooms land
#                    outside them?
# INPUTS/ASSUMPTIONS the iqr_flag_energy column from cell [6], plus the two 1.5*IQR fences
#                    recomputed in this cell from Q1/Q3; the same "zone" group key as cell [2].
#                    Only the 23 rooms with a recorded reading can be drawn - R206's missing
#                    energy value has no position on the axis.
# METHOD             ax.boxplot() with a list of three value Series (all rooms, North, South),
#                    ax.scatter() the individual rooms over each box with a small horizontal
#                    jitter, ax.axhline() the two fences from cell [6], then annotate Q1, Q3,
#                    the median, and each flagged room by room_id.
# CHECKS/INTERPRET   Expected: Q1 = 61.75, Q3 = 90.75, IQR = 29.0, fences 18.25 and 134.25.
#                    Expected TWO amber diamonds, not one - R306 (410.0, above the high fence)
#                    and R110 (12.0, below the low fence). Saves week05_iqr_boxplot.png.

import matplotlib.pyplot as plt
import numpy as np

BLUE, AMBER, GRAY = "#2E74B5", "#B5731A", "#5A5F66"

all_rooms = df.dropna(subset=["energy_kwh_m2_yr"])   # 23 rooms; R206 has no reading to draw
north = all_rooms[all_rooms["zone"] == "North"]
south = all_rooms[all_rooms["zone"] == "South"]
groups = [all_rooms, north, south]
spots = [1.0, 2.6, 3.7]                              # x position of each box

q1_e = all_rooms["energy_kwh_m2_yr"].quantile(0.25)
q3_e = all_rooms["energy_kwh_m2_yr"].quantile(0.75)
med_e = all_rooms["energy_kwh_m2_yr"].median()
# The same 1.5*IQR rule you wrote in cell [5], recomputed here so this figure is
# self-contained and you can see the two fence numbers it is about to draw.
iqr_e = q3_e - q1_e
low_fence_e = q1_e - 1.5 * iqr_e
high_fence_e = q3_e + 1.5 * iqr_e
print("Q1", q1_e, "Q3", q3_e, "IQR", iqr_e, "fences", round(low_fence_e, 2), round(high_fence_e, 2))

fig, ax = plt.subplots(figsize=(9, 5.5))
# TODO: draw the three boxes with ax.boxplot(). Pass a LIST of three Series - all_rooms,
# north, and south "energy_kwh_m2_yr" - plus positions=spots, widths=0.5, showfliers=False
# (you are drawing the points yourself below), and patch_artist=True.

rng = np.random.default_rng(5)          # a fixed seed keeps the jitter reproducible
for pos, group in zip(spots, groups):
    x = pos + rng.uniform(-0.13, 0.13, len(group))   # jitter so 12 rooms do not stack up
    y = group["energy_kwh_m2_yr"].to_numpy()
    plain = ~group["iqr_flag_energy"].to_numpy()
    # TODO: two ax.scatter() calls per group. First the NOT-flagged rooms, x[plain] against
    # y[plain], small and GRAY. Then the flagged rooms, x[~plain] against y[~plain], bigger,
    # AMBER, marker="D" - so a diamond means flag_iqr() returned True for that room.

# TODO: draw the two fences with ax.axhline(high_fence_e, ...) and ax.axhline(low_fence_e,
# ...), dashed and GRAY, then label each one with ax.text() so the reader can see that these
# lines ARE the two numbers the code just printed.

# TODO: annotate Q1 (q1_e), Q3 (q3_e), and the median (med_e) with ax.annotate() and a small
# arrow, so the box's own edges are tied to the three values you just printed.
# TODO: annotate the two flagged rooms by name - R306 Server at 410.0 above the high fence,
# and R110 Closet at 12.0 below the low fence.

ax.set_xticks(spots)
ax.set_xticklabels([f"All rooms\n(n = {len(all_rooms)})", f"North\n(n = {len(north)})",
                    f"South\n(n = {len(south)})"])
ax.set_xlim(0.0, 6.0)
ax.set_ylim(-18, 448)
ax.set_title("Which rooms land outside the 1.5*IQR fences the code computed "
             f"({low_fence_e:.2f} / {high_fence_e:.2f})?")
ax.set_xlabel("zone group (the same group key as cell [2])")
ax.set_ylabel("energy use intensity (kWh/m2/yr)")
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
if len(ax.collections) < 6 or len(ax.lines) < 2 or len(ax.texts) < 4:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 7]: finish boxes, point layers, both fences, and the "
        "required annotations before save; no placeholder PNG was written."
    )
fig.savefig("week05_iqr_boxplot.png", dpi=150, bbox_inches="tight")

print(all_rooms.loc[all_rooms["iqr_flag_energy"],
                    ["room_id", "room_type", "zone", "energy_kwh_m2_yr"]].to_string(index=False))
# WHY THIS MATTERS: this picture and cell [6]'s two printed numbers are ONE rule seen twice.
# The box runs from Q1 = 61.75 to Q3 = 90.75, the amber line is the median (75.0), the dashed
# lines are the 1.5*IQR fences (18.25 and 134.25), and every diamond past a fence is exactly a
# row where flag_iqr() returned True - the arithmetic and the drawing cannot disagree. Report a
# flagged room without looking at the picture and you cannot tell the two failure modes apart:
# a genuine 410.0 server closet gets deleted as a "typo," or a real measurement error gets
# defended as a "design signal." The picture also shows what cell [6]'s one-room printout hid -
# R110 at 12.0 is flagged too, below the LOW fence, and no cell before this one mentions it.
# COMMON ERROR: reading the whisker CAP as the fence. Matplotlib's default whis=1.5 IS this same
# 1.5*IQR rule, but a whisker stops at the last real reading INSIDE the fence (98.0 and 58.0
# here, not 134.25 and 18.25), so the fences are drawn separately with axhline(). Second error:
# calling ax.boxplot() on a column that still holds NaN - every quartile comes back NaN and
# matplotlib draws an empty frame with no error message, which is why all_rooms drops R206 first.


# %% [8] Chart the group means with the spread inside each group
# QUESTION           Is the North-South gap between the means bigger than the variation inside
#                    each zone - or does one flagged room carry the whole comparison?
# INPUTS/ASSUMPTIONS the same "zone" group key as cell [2]; mean, std, and count of
#                    energy_kwh_m2_yr per zone. North has 12 recorded readings, South 11
#                    (R206's is missing), so the two group means do NOT rest on equal n.
# METHOD             groupby().agg(["mean", "std", "count"]), then ax.bar(..., yerr=the std
#                    column, capsize=9) so every bar carries its own +/-1 SD error bar;
#                    annotate the gap between the means and South's mean without R306.
# CHECKS/INTERPRET   Expected: North mean 64.25, SD 19.90, n 12; South mean 115.68, SD 98.10,
#                    n 11; gap between the means 51.43. Expected South without R306: mean 86.25,
#                    SD 10.30, n 10. Saves week05_zone_means_spread.png.

GREEN = "#2E7D5B"

zone_spread = df.groupby("zone")["energy_kwh_m2_yr"].agg(["mean", "std", "count"]).round(2)
print(zone_spread)

gap = zone_spread.loc["South", "mean"] - zone_spread.loc["North", "mean"]
south_without_r306 = df.loc[(df["zone"] == "South") & (df["room_id"] != "R306"),
                            "energy_kwh_m2_yr"]
print("gap between the means:", round(gap, 2))
print("South without R306: mean", round(south_without_r306.mean(), 2),
      "SD", round(south_without_r306.std(), 2), "n", south_without_r306.count())

fig, ax = plt.subplots(figsize=(9, 5.5))
# TODO: draw the two bars with ax.bar([0, 1], zone_spread["mean"], ...). The one argument that
# makes this figure honest is yerr=zone_spread["std"] - pass the SD COLUMN, not the whole
# table and not the variance. Add width=0.5, color=[BLUE, AMBER], and capsize=9.

# TODO: label each bar with its own mean and SD using ax.text(), so the two numbers behind the
# error bar are readable and not just implied by the whisker length.

# TODO: draw a double-headed arrow between the two means with ax.annotate("", xy=..., xytext=...,
# arrowprops=dict(arrowstyle="<->", ...)) and label it with the gap, so the BETWEEN-group
# difference and the WITHIN-group spread are visible in the same frame.

# TODO: draw South's mean with R306 excluded as a GREEN dashed ax.hlines(), and label it. This
# is the version of the finding that survives setting the flagged server closet aside.

ax.set_xticks([0, 1])
ax.set_xticklabels([f"North\n(n = {zone_spread.loc['North', 'count']:.0f} readings)",
                    f"South\n(n = {zone_spread.loc['South', 'count']:.0f} readings)"])
ax.set_xlim(-0.55, 2.35)
ax.set_ylim(0, 245)
ax.set_title(f"Is the {gap:.2f} gap between the zone means bigger than the spread "
             "inside each zone?")
ax.set_xlabel("zone")
ax.set_ylabel("mean energy use (kWh/m2/yr), error bars = +/-1 SD within zone")
ax.grid(alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
if len(ax.patches) < 2 or len(ax.texts) < 3 or len(ax.collections) < 1:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8]: finish both bars, SD error bars, comparison "
        "annotations, and the R306-excluded line before save."
    )
fig.savefig("week05_zone_means_spread.png", dpi=150, bbox_inches="tight")
# WHY THIS MATTERS: cell [2]'s bare table says South's mean is 51.43 kWh/m2/yr above North's
# (about 80% higher). The error bars say the spread INSIDE South (SD 98.10) is about 1.9x that
# gap, and North's own +/-1 SD range (44.35 to 84.15) sits almost entirely inside South's
# (17.58 to 213.78) - so the two bare bars overstate how different the zones are. That is the
# whole difference between a claim and a defensible claim: "South uses 80% more" is a claim,
# "South's mean is 51.43 higher, but one flagged server closet makes South's own spread 1.9x
# that gap" is defensible. Set R306 aside and South's mean drops to 86.25 with SD 10.30 (green
# line): the 22.00 gap that survives is slightly larger than either zone's own SD (19.90 and
# 10.30), which is the version of this finding you can put in Project 1 Part II.
# COMMON ERROR: passing yerr the whole zone_spread table instead of one column, or passing the
# variance instead of the SD - matplotlib draws whatever length you hand it without complaint,
# so an error bar is only as honest as the column behind it. Also note n = 12 vs n = 11: the
# count of room_id and the count of readings that actually entered the mean are different
# numbers, and only the second one belongs in this figure.


# %% [9] Write the z-score-rule function
# QUESTION           Turn the z-score rule from Meeting A into one reusable function.
# INPUTS/ASSUMPTIONS any numeric Series; z = (x - mean) / std; default threshold 2.0.
# METHOD             complete flag_zscore() to compare |z| against threshold.
# CHECKS/INTERPRET   Cell [10] checks this function against room R306; expect True.

def flag_zscore(df: pd.DataFrame, col: str, threshold: float = 2.0) -> pd.Series:
    """True where |z-score| of df[col] exceeds threshold."""
    z = (df[col] - df[col].mean()) / df[col].std()
    # TODO: return z.abs() > threshold
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 9]: return the two-sided absolute z-score comparison."
    )


# %% [10] Studio 3 - apply the z-score rule and compare
# QUESTION           Confirm the z-score rule agrees with the IQR rule on this column.
# INPUTS/ASSUMPTIONS the flag_zscore() function from cell [9]; room R306.
# METHOD             add a flag column, then print R306's row with both flags.
# CHECKS/INTERPRET   Expected: both iqr_flag_energy and z_flag_energy are True for R306.

df["z_flag_energy"] = flag_zscore(df, "energy_kwh_m2_yr")

print(df.loc[df["room_id"] == "R306",
             ["room_id", "energy_kwh_m2_yr", "iqr_flag_energy", "z_flag_energy"]])

# TODO: Write one sentence: why does agreement between two differently-built rules increase
# your confidence more than either rule alone?

r306_two_rules = df.loc[df["room_id"] == "R306", ["iqr_flag_energy", "z_flag_energy"]].iloc[0]
if not bool(r306_two_rules["iqr_flag_energy"]) or not bool(r306_two_rules["z_flag_energy"]):
    raise AssertionError(
        "OUTLIER CHECK FAILURE [cell 10]: both rules should flag R306's energy intensity."
    )


# %% [11] Studio 4 - apply both rules to area_m2 (the disagreement)
# QUESTION           Run the SAME two functions on a different column and see whether they
#                    still agree.
# INPUTS/ASSUMPTIONS the same flag_iqr()/flag_zscore() functions; rooms R309 (a 120.0 m2
#                    double-height gallery) and R110 (a 3.0 m2 closet).
# METHOD             add both flag columns for area_m2, then print R309 and R110.
# CHECKS/INTERPRET   Expected: R309 - iqr_flag_area False, z_flag_area True. R110 -
#                    iqr_flag_area False, z_flag_area False. The two rules disagree on R309
#                    and agree (both miss) on R110.

df["iqr_flag_area"] = flag_iqr(df, "area_m2")
df["z_flag_area"] = flag_zscore(df, "area_m2")

print(df.loc[df["room_id"].isin(["R309", "R110"]),
             ["room_id", "room_type", "area_m2", "iqr_flag_area", "z_flag_area"]])

# TODO: Sort the whole dataset by area_m2 and look at the 3 largest and 3 smallest rows.
# Name one more room, other than R309 or R110, whose flag status you find debatable, and why.

area_check = df.set_index("room_id")[["iqr_flag_area", "z_flag_area"]]
expected_area_flags = {
    "R309": (False, True),
    "R110": (False, False),
}
for room_id, expected in expected_area_flags.items():
    actual = tuple(bool(value) for value in area_check.loc[room_id])
    if actual != expected:
        raise AssertionError(
            f"OUTLIER CHECK FAILURE [cell 11]: {room_id} flags should be {expected}, got {actual}."
        )


# %% [12] Studio 5 - keep / investigate / exclude decisions
# QUESTION           Write one graded decision sentence for each flagged room.
# INPUTS/ASSUMPTIONS results from cells [6], [10], and [11]: R306 (both flags True on energy),
#                    R309 (z-score only, on area), R110 (neither, on area).
# METHOD             fill in each dictionary value with a decision and the explanation it
#                    rests on: measurement error, genuine extreme, or missing variable.
# CHECKS/INTERPRET   A defensible sentence names the decision (keep/investigate/exclude) AND
#                    the reason - not just the room_id restated.

decisions = {
    "R306": "TODO: keep / investigate / exclude, and why",
    "R309": "TODO: keep / investigate / exclude, and why",
    "R110": "TODO: keep / investigate / exclude, and why",
}

for room_id, sentence in decisions.items():
    print(room_id, "-", sentence)

if any("TODO" in sentence.upper() or len(sentence.strip()) < 20 for sentence in decisions.values()):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 12]: write a substantive keep/investigate/exclude "
        "decision and reason for all three rooms."
    )


# %% [13] Bonus - merge the zone summary back onto every room
# QUESTION           Attach each room's own zone average onto its own row, so a room can be
#                    compared to its own group, not just the whole building.
# INPUTS/ASSUMPTIONS the zone_summary table from cell [2]; rename() and merge() from Meeting
#                    A.
# METHOD             reset_index() and rename() the summary, then merge() it back onto df on
#                    the shared "zone" key.
# CHECKS/INTERPRET   Once cell [2] is corrected, expect R306's zone_mean_energy to be 115.68
#                    and its energy_vs_zone_mean to be about 3.54 - still extreme against its
#                    own zone.

zone_lookup = zone_summary.reset_index()[["zone", "mean_energy"]].rename(
    columns={"mean_energy": "zone_mean_energy"}
)

merged = df.merge(zone_lookup, on="zone", how="left")
merged["energy_vs_zone_mean"] = (
    merged["energy_kwh_m2_yr"] / merged["zone_mean_energy"]
).round(2)

print(merged.loc[merged["room_id"] == "R306",
                 ["room_id", "zone", "energy_kwh_m2_yr", "zone_mean_energy",
                  "energy_vs_zone_mean"]])


# %% [14] Required transfer check - a different input than the one worked through live
# QUESTION           Prove, with your own assertions, that R306 is NOT an outlier on a
#                    DIFFERENT column than the one used live in cells [6] and [10].
# INPUTS/ASSUMPTIONS flag_iqr() and flag_zscore() from cells [5] and [9]; iqr_flag_area and
#                    z_flag_area already computed in cell [11]; room R306, area_m2 = 8.0.
# METHOD             write 2-4 assert statements checking R306's area_m2 flags, not its
#                    already-tested energy_kwh_m2_yr flags.
# CHECKS/INTERPRET   Expected: every assertion passes silently. R306 is a genuine outlier on
#                    energy_kwh_m2_yr but an entirely ordinary room on area_m2 - the same
#                    rule, the same row, a different verdict on a different variable.

r306_area_flags = df.loc[df["room_id"] == "R306", ["iqr_flag_area", "z_flag_area"]]

# TODO: Write 2-4 assert statements here proving R306's area_m2 status, for example:
#   assert bool(r306_area_flags["iqr_flag_area"].iloc[0]) is False

cell_14_assertions_complete = False  # TODO: True only after your transfer assertions pass
if not cell_14_assertions_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 14]: add 2-4 R306 area-flag assertions, then set "
        "cell_14_assertions_complete = True."
    )
print("Transfer check verified")


# %% [15] Studio 7 - apply this pipeline to YOUR Project 1 dataset
# QUESTION           This cell is both this week's studio assignment AND the Project 1
#                    dataset/question/provenance checkpoint - the same artifact, not two.
# INPUTS/ASSUMPTIONS your own Week 4 cleaned CSV; one of your own categorical columns; one
#                    of your own numeric columns. DATA_PATH starts at None on purpose: this
#                    cell must NOT be able to run silently against the shared Radley Hall
#                    file below - that practice happens in cells [1]-[14] above, not here.
# METHOD             replace DATA_PATH/GROUP_COL/VALUE_COL with your OWN dataset and column
#                    names; the None-guard raises immediately if you forget, so you cannot
#                    submit this cell still pointed at Radley Hall without an error telling
#                    you so. Once set, reuse flag_iqr()/flag_zscore() unchanged, then export
#                    Project 1 Part II's grouped_summary.csv with to_csv(..., index=False).
# CHECKS/INTERPRET   Running this cell unedited must raise ValueError, not print a result.
#                    Once DATA_PATH/GROUP_COL/VALUE_COL point at your own data, write one
#                    decision sentence per flagged row your dataset produces. The exported
#                    grouped_summary.csv must carry exactly five columns, in this order:
#                    group, n, mean, median, outlier_count.

DATA_PATH = None    # TODO: replace with your own Week 4 cleaned CSV path - NOT building_rooms.csv
GROUP_COL = None    # TODO: replace with your own categorical column
VALUE_COL = None    # TODO: replace with your own numeric column

if any(value is None for value in (DATA_PATH, GROUP_COL, VALUE_COL)):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 15]: "
        "Replace DATA_PATH with the path to YOUR OWN Week 4 cleaned CSV before running "
        "this cell - do not run this cell against the shared Radley Hall file. Set "
        "GROUP_COL and VALUE_COL to your own column names at the same time."
    )

DATA_PATH = Path(DATA_PATH)
if not DATA_PATH.exists():
    raise FileNotFoundError(f"PROJECT DATA ERROR [cell 15]: {DATA_PATH} does not exist.")
if DATA_PATH.name.lower() == "building_rooms.csv":
    raise AssertionError(
        "PROJECT DATA CHECK FAILURE [cell 15]: use your own Week 4 cleaned CSV, not the shared practice file."
    )

own_df = pd.read_csv(DATA_PATH)
if own_df.empty:
    raise AssertionError("PROJECT DATA CHECK FAILURE [cell 15]: the cleaned CSV has no rows.")
missing_columns = [column for column in (GROUP_COL, VALUE_COL) if column not in own_df.columns]
if missing_columns:
    raise KeyError(f"PROJECT SCHEMA ERROR [cell 15]: missing columns {missing_columns}.")
if own_df[GROUP_COL].isna().any() or own_df[VALUE_COL].isna().any():
    raise AssertionError(
        "PROJECT DATA CHECK FAILURE [cell 15]: clean or explicitly resolve missing group/outcome values first."
    )
if not pd.api.types.is_numeric_dtype(own_df[VALUE_COL]):
    raise TypeError(f"PROJECT SCHEMA ERROR [cell 15]: {VALUE_COL!r} must be numeric.")

own_summary = (
    own_df.groupby(GROUP_COL)[VALUE_COL]
    .agg(["mean", "median", "count"])
    .round(2)
    .sort_values("mean", ascending=False)
)
print(own_summary)

own_df["iqr_flag"] = flag_iqr(own_df, VALUE_COL)
own_df["z_flag"] = flag_zscore(own_df, VALUE_COL)
print(own_df.loc[own_df["iqr_flag"] | own_df["z_flag"]])

# Write one keep / investigate / exclude sentence for every flagged row printed above,
# keyed by that row's DataFrame index. Example: {17: "INVESTIGATE — verify sensor history."}
FLAGGED_ROW_DECISIONS = {  # TODO: complete for every printed row
}

flagged_indices = set(own_df.index[own_df["iqr_flag"] | own_df["z_flag"]].tolist())
missing_decisions = flagged_indices - set(FLAGGED_ROW_DECISIONS)
invalid_decisions = {
    index for index, sentence in FLAGGED_ROW_DECISIONS.items()
    if not isinstance(sentence, str)
    or len(sentence.strip()) < 20
    or not any(action in sentence.upper() for action in ("KEEP", "INVESTIGATE", "EXCLUDE"))
}
if missing_decisions or invalid_decisions:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 15]: complete one substantive KEEP / INVESTIGATE / "
        f"EXCLUDE sentence per flagged row. Missing={sorted(missing_decisions)}, "
        f"invalid={sorted(invalid_decisions)}."
    )


# Project 1 Part II's required export: one row per group, carrying the outlier count the
# keep / investigate / exclude decision rests on. The five column names and their order come
# straight from 01_PROJECT_BRIEF.txt: group, n, mean, median, outlier_count.
PROJECT_FOLDER = None        # TODO: Path to YOUR compiled Project 1 folder
if PROJECT_FOLDER is None:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 15]: set PROJECT_FOLDER before exporting grouped_summary.csv."
    )
PROJECT_FOLDER = Path(PROJECT_FOLDER)
if not PROJECT_FOLDER.exists():
    raise FileNotFoundError(f"PROJECT FOLDER ERROR [cell 15]: {PROJECT_FOLDER} does not exist.")
GROUPED_SUMMARY_PATH = PROJECT_FOLDER / "grouped_summary.csv"

grouped_summary = (
    own_df.groupby(GROUP_COL)[VALUE_COL]
    .agg(n="count", mean="mean", median="median")
    .round(2)
    .reset_index()
    .rename(columns={GROUP_COL: "group"})
)
outliers_per_group = own_df.groupby(GROUP_COL)["iqr_flag"].sum().astype(int)
grouped_summary["outlier_count"] = grouped_summary["group"].map(outliers_per_group)

assert list(grouped_summary.columns) == ["group", "n", "mean", "median", "outlier_count"]
if grouped_summary.empty or grouped_summary[["mean", "median"]].isna().any().any():
    raise AssertionError("EXPORT GATE FAILURE [cell 15]: grouped statistics must be finite and nonempty.")
if int(grouped_summary["n"].sum()) != len(own_df):
    raise AssertionError("EXPORT GATE FAILURE [cell 15]: group n values must account for every cleaned row.")
if int(grouped_summary["outlier_count"].sum()) != int(own_df["iqr_flag"].sum()):
    raise AssertionError("EXPORT GATE FAILURE [cell 15]: group outlier counts do not match the row flags.")

# The required filename is written only after data, decisions, schema, and counts pass.
grouped_summary.to_csv(GROUPED_SUMMARY_PATH, index=False)
reopened_summary = pd.read_csv(GROUPED_SUMMARY_PATH)
if list(reopened_summary.columns) != ["group", "n", "mean", "median", "outlier_count"]:
    raise AssertionError("EXPORT CHECK FAILURE [cell 15]: reopened CSV schema changed.")
print(reopened_summary.to_string(index=False))

# TODO: name the group whose outlier_count changes what you can claim, and say in one
# sentence what your comparison would have looked like if you had reported the means alone.
# WHY THIS MATTERS: grouped_summary.csv IS Project 1 Part II's required export, and it is the
# third row of Week 7B's compile checklist - written from YOUR OWN data, not Radley Hall's. A
# grouped summary without outlier_count hides the decision you were asked to defend: a mean
# over 12 rooms that includes one flagged extreme and a mean over 12 unremarkable rooms print
# identically, so a reader cannot tell whether your comparison rests on a genuine pattern or
# on one room you should have discussed by name.
# COMMON ERROR: calling grouped_summary.to_csv(path) without index=False. After .reset_index()
# the group key is already a real column named "group", so pandas writes an extra, meaningless
# row-number column and the exported header no longer matches the five names the brief asks
# for - the file looks fine in Spyder and fails the submission check.

# %% [16] AI-generated outlier-function audit
# QUESTION           Identify and repair the defects in an AI-generated outlier-flag
#                    function.
# INPUTS/ASSUMPTIONS ai_rule as shown text: a one-directional z-score check with no IQR
#                    cross-check.
# METHOD             list at least four specific defects, then compare with your own
#                    flag_iqr()/flag_zscore() functions from cells [5] and [9].
# CHECKS/INTERPRET   A defensible list names the missed-direction, missing-cross-check, and
#                    silent-delete defects - not merely that the code looks wrong.

ai_rule = """
def flag_outliers(df, col):
    z = (df[col] - df[col].mean()) / df[col].std()
    return df[z > 2]
"""

ai_defects = [
    # TODO: add at least four specific defects
]

print(ai_rule)
for defect in ai_defects:
    print("-", defect)

if len(ai_defects) < 4 or any("TODO" in defect.upper() for defect in ai_defects):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 16]: record at least four specific outlier-function defects."
    )


# %% [17] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the finished
#                    pipeline in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below.
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points.
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing the two
#                    outlier rules together still cannot decide.

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

exit_explanation = """
In 80-120 words, explain:
1. what your grouped, ranked summary compares,
2. how a function you wrote became an argument to .agg() or .apply(),
3. what the IQR rule and the z-score rule each test,
4. one column where they agreed and one where they disagreed, and
5. one design judgment the flags cannot make for you.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Transfer the same split–apply–combine logic to a material schedule: group by
# material_family; calculate total carbon, mean carbon, and n; sort by total;
# flag one IQR extreme without deleting it. Explain why total, mean, and count
# answer different questions and choose keep / investigate / correct.
