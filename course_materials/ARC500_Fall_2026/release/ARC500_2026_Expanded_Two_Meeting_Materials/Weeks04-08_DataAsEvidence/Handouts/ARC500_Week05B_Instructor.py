# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 5 studio · INSTRUCTOR SOLUTIONS
Grouping, dual-rule outlier audits, and your Project 1 checkpoint
Syracuse University · School of Architecture · Fall 2026
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

print(df.shape)  # (24, 12)
print(df[["room_id", "zone", "room_type", "area_m2", "energy_kwh_m2_yr"]].dtypes)
# COMMON ERROR: forgetting this file must sit in the SAME folder as the script -
# Path.cwd() from cell [0] shows exactly where Python is looking for it.


# %% [2] Recall: group by zone with multiple named aggregations
# QUESTION           Reproduce Meeting A's headline zone comparison before extending the
#                    pattern to a new category.
# INPUTS/ASSUMPTIONS energy_kwh_m2_yr, area_m2, room_id columns; group key is zone.
# METHOD             complete the three named aggregations below, then round to 2 decimals.
# CHECKS/INTERPRET   Expected: North mean_energy 64.25, South mean_energy 115.68; mean_area
#                    40.98 and 38.25; n = 12 for both zones.

zone_summary = df.groupby("zone").agg(
    mean_energy=("energy_kwh_m2_yr", "mean"),
    mean_area=("area_m2", "mean"),
    n=("room_id", "count"),
).round(2)

print(zone_summary)
# zone   mean_energy  mean_area   n
# North        64.25      40.98  12
# South       115.68      38.25  12
# WHY THIS MATTERS: this one .agg() call IS the "grouping, comparison, and outlier audit"
# milestone's starting table - South uses about 80% more energy per m2 than North, on equal
# sample sizes, exactly the kind of claim Project 1 Part II asks every student to produce.


# %% [3] Studio 1 - group by room_type and rank
# QUESTION           Build the same three-aggregation pattern for room_type instead of zone,
#                    then rank the result by mean energy.
# INPUTS/ASSUMPTIONS same columns as cell [2]; group key is now room_type (7 categories).
# METHOD             copy the pattern from cell [2], then sort_values on mean_energy.
# CHECKS/INTERPRET   Expected top of ranking: Server (410.0, n=1), Studio (94.0, n=6).
#                    Expected bottom: Closet (12.0, n=1).

room_type_summary = df.groupby("room_type").agg(
    mean_energy=("energy_kwh_m2_yr", "mean"),
    n=("room_id", "count"),
).round(2)

ranked = room_type_summary.sort_values("mean_energy", ascending=False)

print(ranked)
# room_type   mean_energy   n
# Server           410.00   1
# Studio            94.00   6
# Classroom         86.17   3
# Gallery           69.75   2
# Office            66.39  10
# Lobby             62.00   1
# Closet            12.00   1

# Server and Closet both have n = 1. Neither ranking extreme should be read with the same
# confidence as Office's n = 10 estimate - a single room can look like a whole category's
# "typical" value when it is really just one room.
# COMMON ERROR: sorting by the wrong column name (e.g. "energy_kwh_m2_yr" instead of the
# renamed "mean_energy") raises a KeyError - a useful, self-correcting error here.


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
# count     23.000000
# mean      88.847826
# std       72.543472
# min       12.000000
# 25%       61.750000
# 50%       75.000000
# 75%       90.750000
# max      410.000000

print(df["zone"].value_counts())
# zone
# North    12
# South    12
# WHY THIS MATTERS: describe()'s count (23) silently confirms room R206's missing value is
# still missing - a one-line trustworthiness check before any grouping or outlier work.


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
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def flag_iqr(df: pd.DataFrame, col: str) -> pd.Series:
    """True where df[col] sits outside the IQR bounds."""
    low, high = iqr_bounds(df[col])
    return (df[col] < low) | (df[col] > high)

# COMMON ERROR: writing q1 - 1.5 * iqr as (q1 - 1.5) * iqr - operator precedence matters;
# multiplication binds tighter than subtraction, but many beginners add the parentheses in
# the wrong place out of caution. Print iqr_bounds() on a known Series to sanity-check.
# COMMON ERROR: writing (df[col] < low) or (df[col] > high) with Python's or/and instead of
# |/& - pandas raises "ValueError: The truth value of a Series is ambiguous" because a
# multi-value Series has no single True/False for or/and to test. Use & and |, and keep the
# parentheses around each side - without them, operator precedence binds & tighter than <,
# which raises a different, equally confusing error.


# %% [6] Studio 2 - apply the IQR rule to energy_kwh_m2_yr
# QUESTION           Confirm your flag_iqr() function catches the room Meeting A flagged.
# INPUTS/ASSUMPTIONS the flag_iqr() function from cell [5]; room R306 (a server closet).
# METHOD             add a flag column, then print only R306's row.
# CHECKS/INTERPRET   Expected: iqr_flag_energy is True for R306. If it is False, revisit
#                    cell [5] before continuing.

df["iqr_flag_energy"] = flag_iqr(df, "energy_kwh_m2_yr")

print(df.loc[df["room_id"] == "R306", ["room_id", "energy_kwh_m2_yr", "iqr_flag_energy"]])
#    room_id  energy_kwh_m2_yr  iqr_flag_energy
# 17    R306             410.0             True

low_e, high_e = iqr_bounds(df["energy_kwh_m2_yr"])
print("IQR bounds (energy_kwh_m2_yr):", round(low_e, 2), round(high_e, 2))
# IQR bounds (energy_kwh_m2_yr): 18.25 134.25
# 410.0 is far above the high bound of 134.25 - R306 (a server closet running equipment
# around the clock) is a real, physically plausible genuine extreme, not obviously an error.


# %% [7] Write the z-score-rule function
# QUESTION           Turn the z-score rule from Meeting A into one reusable function.
# INPUTS/ASSUMPTIONS any numeric Series; z = (x - mean) / std; default threshold 2.0.
# METHOD             complete flag_zscore() to compare |z| against threshold.
# CHECKS/INTERPRET   Cell [8] checks this function against room R306; expect True.

def flag_zscore(df: pd.DataFrame, col: str, threshold: float = 2.0) -> pd.Series:
    """True where |z-score| of df[col] exceeds threshold."""
    z = (df[col] - df[col].mean()) / df[col].std()
    return z.abs() > threshold

# COMMON ERROR: writing z > threshold instead of z.abs() > threshold - this only catches
# high outliers and silently misses any value far BELOW the mean. See Studio 8's AI audit,
# which is built around exactly this mistake.


# %% [8] Studio 3 - apply the z-score rule and compare
# QUESTION           Confirm the z-score rule agrees with the IQR rule on this column.
# INPUTS/ASSUMPTIONS the flag_zscore() function from cell [7]; room R306.
# METHOD             add a flag column, then print R306's row with both flags.
# CHECKS/INTERPRET   Expected: both iqr_flag_energy and z_flag_energy are True for R306.

df["z_flag_energy"] = flag_zscore(df, "energy_kwh_m2_yr")

print(df.loc[df["room_id"] == "R306",
             ["room_id", "energy_kwh_m2_yr", "iqr_flag_energy", "z_flag_energy"]])
#    room_id  energy_kwh_m2_yr  iqr_flag_energy  z_flag_energy
# 17    R306             410.0             True           True

# z (R306) = 4.43, far past |z| > 2. Two independently-built rules - one from quartiles, one
# from mean/std - reaching the same conclusion is meaningfully stronger evidence than either
# rule alone, because they can fail in different ways and did not fail here.


# %% [9] Studio 4 - apply both rules to area_m2 (the disagreement)
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
#    room_id room_type  area_m2  iqr_flag_area  z_flag_area
# 19    R110    Closet      3.0          False        False
# 23    R309   Gallery    120.0          False         True

low_a, high_a = iqr_bounds(df["area_m2"])
print("IQR bounds (area_m2):", round(low_a, 2), round(high_a, 2))
# IQR bounds (area_m2): -47.25 123.95
# R309's 120.0 m2 fits inside this wide bound (Q1=16.95, Q3=59.75 - small offices and large
# studios both sit in this data, inflating the IQR), but z-score (2.82) still flags it. R110,
# a 3 m2 closet on a room schedule, is not extreme enough by either measure to stand out from
# Radley Hall's many genuinely small offices.

sorted_area = df.sort_values("area_m2")
print(sorted_area[["room_id", "room_type", "area_m2"]].head(3).to_string(index=False))
#  room_id room_type  area_m2
#     R110    Closet      3.0
#     R306    Server      8.0
#     R206    Office     15.5
print(sorted_area[["room_id", "room_type", "area_m2"]].tail(3).to_string(index=False))
#  room_id room_type  area_m2
#     R204    Studio     65.0
#     R101     Lobby     78.0
#     R309   Gallery    120.0
# A reasonable "one more debatable row": R306 itself is the 2nd-smallest room by area_m2
# (8.0 m2) yet is not flagged by either rule here - accept any answer defended by its
# position relative to nearby values in this sorted list, not a specific "correct" room_id.


# %% [10] Studio 5 - keep / investigate / exclude decisions
# QUESTION           Write one graded decision sentence for each flagged room.
# INPUTS/ASSUMPTIONS results from cells [6], [8], and [9]: R306 (both flags True on energy),
#                    R309 (z-score only, on area), R110 (neither, on area).
# METHOD             fill in each dictionary value with a decision and the explanation it
#                    rests on: measurement error, genuine extreme, or missing variable.
# CHECKS/INTERPRET   A defensible sentence names the decision (keep/investigate/exclude) AND
#                    the reason - not just the room_id restated.

decisions = {
    "R306": (
        "KEEP - a server closet running equipment continuously is a genuine extreme, not a "
        "measurement error; both rules agree, and the physical explanation is plausible."
    ),
    "R309": (
        "INVESTIGATE - z-score flags this 120.0 m2 double-height gallery as extreme, but "
        "IQR's bounds (inflated by the office/studio bimodal mix) do not; confirm the "
        "double-height program note before deciding whether it belongs in an area-only "
        "comparison at all."
    ),
    "R110": (
        "INVESTIGATE - neither rule flags this 3.0 m2 'room,' but that may be because "
        "labeling a closet as a room in the first place is the real data-quality question, "
        "not something an outlier rule on area_m2 alone can catch."
    ),
}

for room_id, sentence in decisions.items():
    print(room_id, "-", sentence)
# WHY THIS MATTERS: this is the exact written artifact Project 1 Part II grades - a
# defensible sentence per flagged row, not a silently dropped row.


# %% [11] Bonus - merge the zone summary back onto every room
# QUESTION           Attach each room's own zone average onto its own row, so a room can be
#                    compared to its own group, not just the whole building.
# INPUTS/ASSUMPTIONS the zone_summary table from cell [2]; rename() and merge() from Meeting
#                    A.
# METHOD             reset_index() and rename() the summary, then merge() it back onto df on
#                    the shared "zone" key.
# CHECKS/INTERPRET   Expect R306's zone_mean_energy to be 115.68 and its
#                    energy_vs_zone_mean to be about 3.54 - still extreme against its own
#                    zone.

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
#    room_id   zone  energy_kwh_m2_yr  zone_mean_energy  energy_vs_zone_mean
# 17    R306  South             410.0            115.68                 3.54
# WHY THIS MATTERS: this merge-a-summary-back-onto-per-row-data pattern is exactly what
# Project 1 Part II requires - a preview, not a new technique invented here.


# %% [12] Required transfer check - a different input than the one worked through live
# QUESTION           Prove, with your own assertions, that R306 is NOT an outlier on a
#                    DIFFERENT column than the one used live in cells [6] and [8].
# INPUTS/ASSUMPTIONS flag_iqr() and flag_zscore() from cells [5] and [7]; iqr_flag_area and
#                    z_flag_area already computed in cell [9]; room R306, area_m2 = 8.0.
# METHOD             write 2-4 assert statements checking R306's area_m2 flags, not its
#                    already-tested energy_kwh_m2_yr flags.
# CHECKS/INTERPRET   Expected: every assertion passes silently. R306 is a genuine outlier on
#                    energy_kwh_m2_yr but an entirely ordinary room on area_m2 - the same
#                    rule, the same row, a different verdict on a different variable.

r306_area_flags = df.loc[df["room_id"] == "R306", ["iqr_flag_area", "z_flag_area"]]

assert bool(r306_area_flags["iqr_flag_area"].iloc[0]) is False
assert bool(r306_area_flags["z_flag_area"].iloc[0]) is False

z_area_r306 = (
    df.loc[df["room_id"] == "R306", "area_m2"].iloc[0] - df["area_m2"].mean()
) / df["area_m2"].std()
assert abs(z_area_r306) < 2.0

print("Transfer-check cell reached")
print("z (R306, area_m2) =", round(z_area_r306, 2))  # -1.11


# %% [13] Studio 7 - apply this pipeline to YOUR Project 1 dataset
# QUESTION           This cell is both this week's studio assignment AND the Project 1
#                    dataset/question/provenance checkpoint - the same artifact, not two.
# INPUTS/ASSUMPTIONS your own Week 4 cleaned CSV; one of your own categorical columns; one
#                    of your own numeric columns. Defaults below still point at Radley Hall
#                    so this cell runs before you edit it.
# METHOD             set the three variables below, then reuse flag_iqr()/flag_zscore()
#                    unchanged.
# CHECKS/INTERPRET   With the defaults unchanged, expect exactly one flagged row: R309
#                    (z_flag True, iqr_flag False). On your own data, write one decision
#                    sentence per flagged row your dataset produces.

DATA_PATH = "building_rooms.csv"   # a student would replace this with their own Week 4 file
GROUP_COL = "zone"                  # a student would replace this with their own category
VALUE_COL = "area_m2"               # a student would replace this with their own numeric col

own_df = pd.read_csv(DATA_PATH)

own_summary = (
    own_df.groupby(GROUP_COL)[VALUE_COL]
    .agg(["mean", "median", "count"])
    .round(2)
    .sort_values("mean", ascending=False)
)
print(own_summary)
#         mean  median  count
# zone
# North  40.98    31.6     12
# South  38.25    37.6     12

own_df["iqr_flag"] = flag_iqr(own_df, VALUE_COL)
own_df["z_flag"] = flag_zscore(own_df, VALUE_COL)
flagged_rows = own_df.loc[own_df["iqr_flag"] | own_df["z_flag"]]
print(flagged_rows[["room_id", "area_m2", "iqr_flag", "z_flag"]].to_string(index=False))
#  room_id  area_m2  iqr_flag  z_flag
#     R309    120.0     False    True
# On the unmodified Radley Hall defaults this reproduces cell [9]'s single flagged row -
# confirming the three-variable template works before any student edits it for their own
# data. WHY THIS MATTERS: the only things that should ever need to change here are
# DATA_PATH, GROUP_COL, and VALUE_COL - the two flag functions generalize unchanged, which
# is the entire point of writing them as functions in cell [5] and [7] rather than as
# one-off inline code.


# %% [14] AI-generated outlier-function audit
# QUESTION           Identify and repair the defects in an AI-generated outlier-flag
#                    function.
# INPUTS/ASSUMPTIONS ai_rule as shown text: a one-directional z-score check with no IQR
#                    cross-check.
# METHOD             list at least four specific defects, then compare with your own
#                    flag_iqr()/flag_zscore() functions from cells [5] and [7].
# CHECKS/INTERPRET   A defensible list names the missed-direction, missing-cross-check, and
#                    silent-delete defects - not merely that the code looks wrong.

ai_rule = """
def flag_outliers(df, col):
    z = (df[col] - df[col].mean()) / df[col].std()
    return df[z > 2]
"""

ai_defects = [
    "Uses z > 2 instead of z.abs() > 2, so it can never catch a value far BELOW the mean "
    "(e.g. room R110's low energy reading would be invisible to this function).",
    "Runs only the z-score rule with no IQR cross-check, even though the two rules can "
    "disagree (see the area_m2 case) - a single rule's silence is not proof of no outlier.",
    "Returns df[z > 2], the filtered ROWS themselves, rather than a labeled Boolean flag "
    "column - the caller has no way to tell which rows were excluded from the returned data.",
    "The function name 'flag_outliers' implies a neutral flag, but the rows that pass "
    "through silently disappear from the returned data - a caller has no way to see that "
    "those rows were even checked, let alone that they passed.",
]

print(ai_rule)
for defect in ai_defects:
    print("-", defect)


def flag_outliers_repaired(df: pd.DataFrame, col: str) -> pd.Series:
    """Return a Boolean flag column - True means 'investigate', never auto-deleted."""
    return flag_zscore(df, col) | flag_iqr(df, col)


repaired = flag_outliers_repaired(df, "energy_kwh_m2_yr")
assert bool(repaired[df["room_id"] == "R306"].iloc[0]) is True
print("repaired function still flags R306:", bool(repaired[df["room_id"] == "R306"].iloc[0]))
# repaired function still flags R306: True


# %% [15] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the finished
#                    pipeline in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below.
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points.
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing the two
#                    outlier rules together still cannot decide.

ai_use_record = """
Tool/model: Example assistant
Prompt: Write a function that flags outliers in a pandas column using a z-score.
Suggestion received: A one-directional z > 2 filter that returns the flagged rows directly.
What I accepted: The overall z = (x - mean) / std structure.
What I modified and why: Changed to z.abs() > threshold so low outliers are not missed, and
returned a labeled Boolean column instead of a filtered, unlabeled subset of rows.
What I rejected and why: Using z-score alone as the only check - an IQR cross-check catches
cases (like area_m2) where the two rules disagree.
How I tested it: Asserted the repaired function still flags room R306 on energy_kwh_m2_yr,
and compared it against the hand-verified flag_iqr()/flag_zscore() functions from cells [5]
and [7].
One limitation I found: Neither rule can tell me whether a flagged room reflects a
measurement error, a genuine extreme, or a missing variable in the model - only a person can
make that call.
"""

exit_explanation = """
The grouped, ranked summary compares mean energy use per square meter across zone and
room_type, showing South-zone rooms use about 80% more energy per m2 than North-zone rooms on
equal sample sizes. flag_iqr and flag_zscore are ordinary functions, written once, then reused
unchanged as the comparison rule for every group here, the same function-as-argument idea
Meeting A extended toward .agg()/.apply(). On energy_kwh_m2_yr both rules agree that server
closet R306 is a genuine extreme; on area_m2 they disagree about gallery R309 and both miss
closet R110. Neither rule can decide whether a flagged row is a measurement error, a genuine
extreme, or evidence the grouping variable itself is incomplete - that judgment still belongs
to the analyst, not the code.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Transfer the same split–apply–combine logic to a material schedule. Expected
# interpretation: total identifies contribution, mean describes a typical row,
# and n exposes thin groups. An IQR flag means investigate quantity, factor,
# system boundary, or a genuine extreme—not automatically delete the assembly.
