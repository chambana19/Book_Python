# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 4 studio · INSTRUCTOR SOLUTIONS
Data trustworthiness, cleaning, and documentation
Syracuse University · School of Architecture · Fall 2026
"""

# %% [0] Environment and working-folder check
# QUESTION           Run the cell and confirm your Python version, executable, and working
#                    folder, and that a data/ subfolder holding building_rooms.csv sits
#                    next to this script.
# INPUTS/ASSUMPTIONS no inputs; Spyder is installed and this file is open
# METHOD             run the cell and read the three printed environment lines in the
#                    console
# CHECKS/INTERPRET   You should see a Python version, an executable path, and a folder
#                    path with no error.

from pathlib import Path
import sys

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())


# %% [1] Load Radley Hall with a keyword argument
# QUESTION           Load building_rooms.csv and confirm it has the size you expect.
# INPUTS/ASSUMPTIONS DATA_PATH points to data/building_rooms.csv; sep="," is the column
#                    separator, named explicitly as a keyword argument
# METHOD             pd.read_csv(DATA_PATH, sep=","), then print rooms.shape
# CHECKS/INTERPRET   Expected shape: (24, 12) - 24 rooms, 12 recorded columns.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = Path("data") / "building_rooms.csv"
rooms = pd.read_csv(DATA_PATH, sep=",")
print(rooms.shape)
# COMMON ERROR: a hardcoded absolute path (e.g. "C:/Users/yourname/Desktop/...") breaks
# the moment the file moves or the script runs on another machine. Path("data") / "..."
# is portable as long as the folder layout is preserved.


# %% [2] The trustworthiness interview
# QUESTION           What type is each column, really - and where exactly are the gaps?
# INPUTS/ASSUMPTIONS rooms from cell [1]
# METHOD             print rooms.dtypes, rooms.head(), rooms.info(), and
#                    rooms.isna().sum(), in that order
# CHECKS/INTERPRET   has_daylight should print as dtype object (not bool) because of one
#                    missing value. isna().sum() should show exactly 1 for has_daylight
#                    and 1 for energy_kwh_m2_yr, 0 everywhere else.

print(rooms.dtypes)
print(rooms.head())
rooms.info()
print(rooms.isna().sum())

missing_daylight_room = rooms.loc[rooms["has_daylight"].isna(), "room_id"].iloc[0]
missing_energy_room = rooms.loc[rooms["energy_kwh_m2_yr"].isna(), "room_id"].iloc[0]
print("Missing has_daylight:", missing_daylight_room)   # R303
print("Missing energy_kwh_m2_yr:", missing_energy_room)  # R206
# WHY THIS MATTERS: the dtype table (object instead of bool) told you SOMETHING was
# missing before you ran a single isna() call. A trustworthiness interview reads both
# signals - the shape of the dtype AND the count of the gap - because either one alone
# can be missed under deadline pressure.
# COMMON ERROR: printing rooms.info() and stopping there. info() shows non-null COUNTS,
# not which rows - you still need isna() (or a boolean filter) to name the room_id.


# %% [3] Data dictionary and provenance note
# QUESTION           Document every column before trusting a single exported number.
# INPUTS/ASSUMPTIONS the trustworthiness interview from cell [2]; Radley Hall is a
#                    fictional, instructor-built dataset for this course
# METHOD             fill in one dictionary entry per column (unit/values, then meaning,
#                    joined in a single string), then write a one-to-two sentence
#                    provenance note as a string
# CHECKS/INTERPRET   Every one of the 12 columns must appear as a key. The provenance
#                    note must state that Radley Hall is not a real measured building.

# One flat dictionary: column name -> "unit or values - meaning", the same
# name: value shape as Week 3's dictionaries, just with a longer string value.
data_dictionary = {
    "room_id": "text label - unique room identifier, e.g. R101",
    "floor": "1-3 - building floor level",
    "zone": "North / South - building half the room sits in",
    "room_type": "category - Lobby, Gallery, Office, Studio, Classroom, Server, or Closet",
    "area_m2": "m2 - measured room floor area",
    "orientation": "N/S/E/W - primary wall-facing direction",
    "has_daylight": "True/False - room has at least one exterior daylight opening",
    "energy_kwh_m2_yr": "kWh/m2/yr - modeled annual energy use intensity",
    "x_m": "m - local site-plan x coordinate",
    "y_m": "m - local site-plan y coordinate",
    "lat": "degrees (EPSG:4326) - geographic latitude, for Week 7 mapping",
    "lon": "degrees (EPSG:4326) - geographic longitude, for Week 7 mapping",
}

provenance_note = (
    "Radley Hall is a fictional 24-room building built for ARC 500 in Fall 2026. "
    "It is not a real measured building; all values were instructor-generated for "
    "this course and are reused, unchanged, across Weeks 4-7."
)

print(len(data_dictionary), "columns documented")
print(provenance_note)
# WHY THIS MATTERS: Project 1 Part I grades the data dictionary and provenance note as
# their own rubric line. A cleaned CSV with no dictionary is not yet evidence - it is
# just numbers nobody downstream can interpret or reproduce.
# COMMON ERROR: nesting a dictionary inside a dictionary (e.g. {"area_m2": {"unit":
# "m2", "meaning": "..."}}) to separate unit from meaning. That two-level lookup
# (data_dictionary["area_m2"]["unit"]) is never covered in this course - keep every
# entry a single flat string, exactly like the dictionaries from Week 3.


# %% [4] Build the cleaned, justified subset
# QUESTION           Which rows or columns get dropped, kept, or flagged - and why?
# INPUTS/ASSUMPTIONS rooms from cell [1]; one missing energy_kwh_m2_yr (room R206); one
#                    missing has_daylight (room R303)
# METHOD             filter to rows with a recorded energy_kwh_m2_yr using .notna(); do
#                    NOT drop has_daylight or its one missing row
# CHECKS/INTERPRET   Expected cleaned shape: (23, 12). Room R206 should be the one
#                    dropped; room R303 should still be present with has_daylight missing.

cleaned = rooms[rooms["energy_kwh_m2_yr"].notna()].copy()
print(cleaned.shape)

drop_justification = (
    "Room R206 is dropped from cleaned: its energy_kwh_m2_yr value was never recorded, "
    "and every downstream comparison in this pipeline (and next week's grouping) needs "
    "a real energy value - keeping a fabricated placeholder would misrepresent that room."
)
keep_flag_note = (
    "has_daylight is kept, not dropped, even though its dtype is object: 23 of 24 rooms "
    "have a valid True/False value, and dropping the whole column to fix one gap (room "
    "R303) would throw away far more evidence than it protects. R303's missing value "
    "stays flagged and must be excluded explicitly before any Boolean operation on it."
)

print(drop_justification)
print(keep_flag_note)

assert "R206" not in cleaned["room_id"].tolist()
assert "R303" in cleaned["room_id"].tolist()
# COMMON ERROR: calling rooms.dropna() here instead of a targeted .notna() filter. That
# would ALSO silently drop room R303 (missing has_daylight) even though the stated
# policy above is to keep and flag it, not drop it - two different columns' missingness
# get conflated into one blunt operation. See the AI-audit cell [9] for exactly this bug.


# %% [5] Two derived columns, two small documented functions
# QUESTION           Add area_ft2 AND energy_kwh_yr to cleaned, each its own documented
#                    function.
# INPUTS/ASSUMPTIONS cleaned from cell [4]; 1 m2 = 10.7639 ft2; energy_kwh_yr = each
#                    room's energy_kwh_m2_yr times its area_m2
# METHOD             write convert_m2_to_ft2(area_m2, decimals=1) AND
#                    estimate_annual_energy_kwh(energy_kwh_m2_yr, area_m2): each a
#                    docstring, a type hint on the parameter(s) and the return value, and
#                    a vectorized conversion inside - the docstring/type-hint convention
#                    from Monday, applied to real data twice, not once. Do not overwrite
#                    area_m2 or energy_kwh_m2_yr.
# CHECKS/INTERPRET   Expected first three area_ft2 values: 839.6, 475.8, 199.1. Expected
#                    first three energy_kwh_yr values: 4836.0, 3160.0, 1073.0.

def convert_m2_to_ft2(area_m2: pd.Series, decimals: int = 1) -> np.ndarray:
    """Convert a Series of room areas from square meters to square feet, rounded to
    `decimals` places."""
    return np.round(np.array(area_m2) * 10.7639, decimals)


def estimate_annual_energy_kwh(energy_kwh_m2_yr: pd.Series, area_m2: pd.Series) -> pd.Series:
    """Return each room's estimated total annual energy use (kWh/yr), rounded to the
    nearest whole kWh."""
    return (energy_kwh_m2_yr * area_m2).round(0)


cleaned["area_ft2"] = convert_m2_to_ft2(cleaned["area_m2"])
cleaned["energy_kwh_yr"] = estimate_annual_energy_kwh(cleaned["energy_kwh_m2_yr"], cleaned["area_m2"])
print(cleaned[["room_id", "area_m2", "area_ft2", "energy_kwh_yr"]].head(3))
# WHY THIS MATTERS: this is this week's "one clean function per pipeline stage" example
# required starting Week 4 - two documented functions, each with a docstring, type hints
# on its parameter(s) (pd.Series) and its return value, and a single vectorized line
# inside: no for loop, no accumulator, the same idea (one operation, every element) from
# Monday's lecture, now applied twice in the same pipeline.
# COMMON ERROR 1: cleaned["area_m2"] = convert_m2_to_ft2(cleaned["area_m2"]) - assigning
# the result back into area_m2 instead of a new area_ft2 column. The column would still
# be named area_m2 while silently holding square-foot values - a unit-label lie that
# breaks every later computation that trusts the name. Always derive into a new column.
# COMMON ERROR 2: writing either function with no docstring or no type hints because
# "it's just one line." Project 1 grades the docstring/type-hint convention on every
# function, regardless of how short the function's body is.

print()
print("Rooms whose TOTAL annual energy passes 5,000 kWh/yr - Boolean filtering, recalled:")
big_users = cleaned[cleaned["energy_kwh_yr"] > 5000]
print(big_users[["room_id", "room_type", "area_m2", "energy_kwh_m2_yr", "energy_kwh_yr"]])

r306 = cleaned.loc[cleaned["room_id"] == "R306"].iloc[0]
print("R306:", r306["energy_kwh_m2_yr"], "kWh/m2/yr (the highest intensity in the "
      "building), but only", r306["energy_kwh_yr"], "kWh/yr total - it does not clear "
      "the 5,000 kWh/yr bar above.")
# WHY THIS MATTERS: R306 (the Server closet) has the highest energy_kwh_m2_yr of any
# room - 410, more than four times its nearest rival - yet the same Boolean-filtering
# idea from the "South rooms" slide, applied to the new column, shows it never clears a
# 5,000 kWh/yr total-energy bar. At only 8.0 m2, its huge intensity multiplies into a
# modest annual total. Intensity and total answer different architectural questions; a
# derived column changes which question a filter can answer.


# %% [6] Export the cleaned dataset
# QUESTION           Save cleaned as a CSV a collaborator could reopen without clutter.
# INPUTS/ASSUMPTIONS cleaned from cells [4]-[5], now including area_ft2 and energy_kwh_yr
# METHOD             cleaned.to_csv(path, index=False), then reopen the file and confirm
#                    its shape
# CHECKS/INTERPRET   Expected reopened shape: (23, 14).

OUT_PATH = Path("radley_hall_cleaned.csv")
cleaned.to_csv(OUT_PATH, index=False)

check = pd.read_csv(OUT_PATH)
print(check.shape)
# COMMON ERROR: cleaned.to_csv(OUT_PATH) without index=False. pandas would then write
# its own row-number index as an extra "Unnamed: 0" column - every file you export this
# semester should carry index=False unless you have a specific, stated reason not to.


# %% [7] One Matplotlib scatter
# QUESTION           Does a bigger room always mean a higher energy intensity?
# INPUTS/ASSUMPTIONS cleaned from cell [5], with area_ft2 and energy_kwh_m2_yr
# METHOD             fig, ax = plt.subplots(); ax.scatter(...); label both axes with
#                    units; save with fig.savefig(...)
# CHECKS/INTERPRET   One point should sit far above the rest (a server closet) - do not
#                    delete it to make the figure look tidier.

fig, ax = plt.subplots()
ax.scatter(cleaned["area_ft2"], cleaned["energy_kwh_m2_yr"])
ax.set_xlabel("area_ft2")
ax.set_ylabel("energy_kwh_m2_yr")
ax.set_title("Radley Hall: area (ft2) vs. energy intensity")
fig.savefig("radley_scatter.png")
print("scatter saved")
# WHY THIS MATTERS: no two-room example here is the same size and zone by coincidence -
# this is the exact figure Project 1 Part III will ask you to build on your own data,
# and the one high point previews the outlier rule Week 5 names formally.
# COMMON ERROR: plotting area_m2 instead of the NumPy-derived area_ft2, which technically
# "works" but skips the required NumPy touch for this week's assignment.


# %% [8] Self-check: prove the pipeline on a different room
# QUESTION           Does your pipeline hold up on a room you have not hand-checked yet?
# INPUTS/ASSUMPTIONS cleaned from cells [4]-[6]; room R204, NOT room R101 used above
# METHOD             write 2-4 assert statements checking area_ft2, energy_kwh_yr,
#                    missing-value counts, and shape for R204 and cleaned as a whole
# CHECKS/INTERPRET   If every assertion holds, the cell prints its confirmation message
#                    with no error. Expected R204 area_ft2: 699.7, energy_kwh_yr: 6370.0.

r204 = cleaned.loc[cleaned["room_id"] == "R204"].iloc[0]
assert round(r204["area_m2"] * 10.7639, 1) == r204["area_ft2"]
assert round(r204["energy_kwh_m2_yr"] * r204["area_m2"]) == r204["energy_kwh_yr"]
assert cleaned["energy_kwh_m2_yr"].isna().sum() == 0
assert cleaned["has_daylight"].isna().sum() == 1
assert cleaned.shape[0] == 23

print("Self-check passed: R204 area_ft2 =", r204["area_ft2"], "energy_kwh_yr =", r204["energy_kwh_yr"])
# WHY THIS MATTERS: R101 was the room traced live in cells [1]-[5]; asserting on R204
# instead proves the area_ft2 formula and the cleaning decision both generalize, rather
# than only working for the one row already inspected by eye. This is this week's
# required transfer check.


# %% [9] AI-generated cleaning script audit
# QUESTION           Would you accept this AI-suggested cleaning script as-is?
# INPUTS/ASSUMPTIONS ai_cleaning as shown text
# METHOD             list at least four specific defects, then compare with your own
#                    cleaned pipeline from cells [4]-[6]
# CHECKS/INTERPRET   A defensible list names the factual, data-loss, provenance, and
#                    export defects - not merely that the code "looks wrong."

ai_cleaning = """
import pandas as pd

rooms = pd.read_csv("data/building_rooms.csv")

# has_daylight is already a clean bool column
rooms = rooms.dropna()

rooms["area_m2"] = rooms["area_m2"] * 10.7639

rooms.to_csv("cleaned_rooms.csv")
"""

ai_defects = [
    "Factual error: the comment claims has_daylight is 'already a clean bool column,' "
    "but the trustworthiness interview (cell [2]) showed its dtype is object because of "
    "one missing value (room R303).",
    "Uncontrolled data loss: rooms.dropna() with no arguments drops any row missing ANY "
    "column's value - here rooms R303 and R206, for two unrelated reasons - going from "
    "24 rows to 22 with no record of which rows or why.",
    "Destroyed provenance: rooms['area_m2'] = rooms['area_m2'] * 10.7639 overwrites the "
    "original measured column in place; it is still named area_m2 but now silently "
    "holds square-foot values, a unit-label lie for anyone reading the file later.",
    "Missing keyword argument: rooms.to_csv('cleaned_rooms.csv') omits index=False, "
    "adding a stray 'Unnamed: 0' column to the exported file.",
]

print(ai_cleaning)
for defect in ai_defects:
    print("-", defect)
# WHY THIS MATTERS: every one of these four defects is individually plausible and easy
# to miss under time pressure - which is exactly why an AI suggestion gets audited
# against your own trustworthiness interview, never accepted because it "runs."


# %% [10] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished pipeline in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five
#                    required points listed below
# METHOD             fill in the AI-use record honestly, then write the exit
#                    explanation addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing
#                    the script cannot judge.

ai_use_record = """
Tool/model: Example assistant
Prompt: Write a pandas script that cleans building_rooms.csv and exports it.
Suggestion received: A script using dropna() with no arguments, overwriting area_m2
in place, and calling to_csv() with no index argument.
What I accepted: The general shape - load, clean, derive, export.
What I modified and why: Replaced dropna() with a targeted .notna() filter on
energy_kwh_m2_yr only, kept has_daylight with its one flagged gap, derived a new
area_ft2 column instead of overwriting area_m2, and added index=False.
What I rejected and why: The claim that has_daylight was already a clean bool column -
contradicted by the trustworthiness interview.
How I tested it: Reopened the exported CSV and confirmed its shape, and asserted the
area_ft2 formula and missing-value counts on room R204, a room not used in the worked
example.
One limitation I found: The pipeline confirms internal consistency, not that Radley
Hall's numbers reflect any real building's performance - it can't, since the data is
fictional by design.
"""

exit_explanation = """
The trustworthiness interview found one real anomaly: has_daylight prints as dtype
object, not bool, because room R303's value was never recorded; energy_kwh_m2_yr had
a second gap, room R206, visible only once isna().sum() was checked. R206 is dropped
because every downstream energy comparison needs a real value; has_daylight is kept,
not dropped, since losing 23 good values to fix one gap would cost more than it
protects. area_ft2 converts every room's area at once using NumPy, no loop, and the
scatter plots it against energy intensity, showing most rooms clustered low except one
clear high point. This pipeline cannot yet say whether that point is a genuine outlier
or a measurement issue - Week 5's rules answer that, not this one.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# A material inventory has quantity_m3, density_kg_m3, and carbon_kgco2e_kg,
# with missing density/factor values. Expected policy: interview shape/dtypes/
# head/info/isna first; preserve incomplete rows with flags; derive carbon only
# where all factors exist; keep provenance. pandas organizes, NumPy supports the
# vectorized conditional, and Matplotlib reveals the resulting distribution.
