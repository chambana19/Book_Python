# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 4 studio · Data trustworthiness, cleaning, and documentation
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week04 module folder, with building_rooms.csv inside a
     data/ subfolder next to it (data/building_rooms.csv).
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict a shape, dtype, or count before running.
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A cleaned dataset is not "correct" until every dropped row or column - and every
  kept-but-flagged gap - has one written sentence explaining the decision. A silent
  drop is never acceptable, no matter how small the dataset.
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

# TODO: If your shape does not print (24, 12), check DATA_PATH before anything else.
if rooms.shape != (24, 12):
    raise AssertionError(
        f"DATA CHECK FAILURE [cell 1]: expected (24, 12), loaded {rooms.shape} from {DATA_PATH}."
    )


# %% [2] The trustworthiness interview
# QUESTION           What type is each column, really - and where exactly are the gaps?
# INPUTS/ASSUMPTIONS rooms from cell [1]
# METHOD             print rooms.dtypes, rooms.head(), rooms.info(), and
#                    rooms.isna().sum(), in that order
# CHECKS/INTERPRET   has_daylight should print as dtype object (not bool) because of one
#                    missing value. isna().sum() should show exactly 1 for has_daylight
#                    and 1 for energy_kwh_m2_yr, 0 everywhere else.
# VERSION NOTE       The has_daylight signal above is the same on any recent pandas. The
#                    OTHER text columns, though, print as dtype str on pandas 3.x and as
#                    object on pandas 2.x. That is a display change in pandas, not a
#                    difference in your data, so do not go hunting for a bug if your table
#                    says str where a slide says object (or the reverse).

print(rooms.dtypes)
print(rooms.head())
rooms.info()
print(rooms.isna().sum())

# TODO: Name, by room_id, which room is missing has_daylight and which is missing
# energy_kwh_m2_yr. (Hint: rooms[rooms["has_daylight"].isna()] shows the row.)


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
    "room_id": "text label - TODO: meaning",
    "floor": "1-3 - TODO: meaning",
    "zone": "North / South - TODO: meaning",
    "room_type": "category - TODO: meaning",
    "area_m2": "m2 - TODO: meaning",
    "orientation": "N/S/E/W - TODO: meaning",
    "has_daylight": "True/False - TODO: meaning",
    "energy_kwh_m2_yr": "kWh/m2/yr - TODO: meaning",
    "x_m": "m - TODO: meaning",
    "y_m": "m - TODO: meaning",
    "lat": "degrees (EPSG:4326) - TODO: meaning",
    "lon": "degrees (EPSG:4326) - TODO: meaning",
}

provenance_note = "TODO: state where Radley Hall's data came from and what it is not."

print(len(data_dictionary), "columns documented")
print(provenance_note)

# TODO: Replace every "TODO: meaning" with one short phrase after the dash. Replace
# provenance_note with your own one-to-two sentence statement.

if set(data_dictionary) != set(rooms.columns):
    raise AssertionError("DATA CHECK FAILURE [cell 3]: document every loaded column exactly once.")
if any("TODO" in meaning.upper() for meaning in data_dictionary.values()) or "TODO" in provenance_note.upper():
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 3]: finish all 12 meanings and the provenance note "
        "before treating this table as evidence."
    )


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

drop_justification = "TODO: one sentence explaining why R206 is dropped from cleaned."
keep_flag_note = "TODO: one sentence explaining why has_daylight stays, with R303 flagged."

print(drop_justification)
print(keep_flag_note)

# TODO: Confirm "R206" is NOT in cleaned["room_id"].tolist() and "R303" IS.

if cleaned.shape != (23, 12) or "R206" in cleaned["room_id"].tolist() or "R303" not in cleaned["room_id"].tolist():
    raise AssertionError(
        "CLEANING CHECK FAILURE [cell 4]: keep 23 rows, remove only R206 for the stated "
        "outcome, and retain R303 with its daylight gap."
    )
if "TODO" in drop_justification.upper() or "TODO" in keep_flag_note.upper():
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 4]: write both cleaning-decision sentences before continuing."
    )


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
    """TODO: one sentence describing what this function returns."""
    # TODO: return the vectorized NumPy conversion, rounded to `decimals` places, e.g.
    # return np.round(np.array(area_m2) * 10.7639, decimals)
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: implement the vectorized m²-to-ft² conversion."
    )


def estimate_annual_energy_kwh(energy_kwh_m2_yr: pd.Series, area_m2: pd.Series) -> pd.Series:
    """TODO: one sentence describing what this function returns."""
    # TODO: return energy_kwh_m2_yr * area_m2, rounded to the nearest whole kWh, e.g.
    # return (energy_kwh_m2_yr * area_m2).round(0)
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: implement annual energy as intensity × area."
    )


cleaned["area_ft2"] = convert_m2_to_ft2(cleaned["area_m2"])
cleaned["energy_kwh_yr"] = estimate_annual_energy_kwh(cleaned["energy_kwh_m2_yr"], cleaned["area_m2"])
print(cleaned[["room_id", "area_m2", "area_ft2", "energy_kwh_yr"]].head(3))

print()
print("Rooms whose TOTAL annual energy passes 5,000 kWh/yr - Boolean filtering, recalled:")
big_users = None  # TODO: filter cleaned to rows where energy_kwh_yr > 5000
# Then print
# room_id, room_type, area_m2, energy_kwh_m2_yr, energy_kwh_yr for those rows, e.g.
# big_users = cleaned[cleaned["energy_kwh_yr"] > 5000]
# print(big_users[["room_id", "room_type", "area_m2", "energy_kwh_m2_yr", "energy_kwh_yr"]])

r306 = None  # TODO: look up room R306 with cleaned.loc[...].iloc[0]
# and print its energy_kwh_m2_yr and energy_kwh_yr side by side. Is R306 on the list above?

if not np.allclose(cleaned["area_ft2"].head(3), [839.6, 475.8, 199.1]):
    raise AssertionError("MODEL CHECK FAILURE [cell 5]: the first three area_ft2 values are incorrect.")
if not np.allclose(cleaned["energy_kwh_yr"].head(3), [4836.0, 3160.0, 1073.0]):
    raise AssertionError("MODEL CHECK FAILURE [cell 5]: the first three annual-energy values are incorrect.")
expected_big_user_ids = {"R104", "R105", "R204", "R205", "R304", "R305", "R309"}
if (
    not isinstance(big_users, pd.DataFrame)
    or set(big_users["room_id"]) != expected_big_user_ids
    or not isinstance(r306, pd.Series)
    or r306["room_id"] != "R306"
    or abs(r306["energy_kwh_yr"] - 3280.0) > 0.01
):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: complete the >5,000 kWh/yr filter and the R306 "
        "lookup; check the seven qualifying room IDs and R306's 3,280 kWh/yr total."
    )


# %% [6] Export the cleaned dataset
# QUESTION           Save cleaned as a CSV a collaborator could reopen without clutter.
# INPUTS/ASSUMPTIONS cleaned from cells [4]-[5], now including area_ft2 and energy_kwh_yr
# METHOD             cleaned.to_csv(path, index=False), then reopen the file and confirm
#                    its shape
# CHECKS/INTERPRET   Expected reopened shape: (23, 14).

OUT_PATH = Path("radley_hall_cleaned.csv")
# TODO: export cleaned to OUT_PATH with index=False, e.g.
# cleaned.to_csv(OUT_PATH, index=False)

# TODO: after exporting, reopen the file and confirm its shape, e.g.
# check = pd.read_csv(OUT_PATH)
# print(check.shape)

cell_6_export_complete = False  # TODO: True only after exporting AND reopening the CSV
if not cell_6_export_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 6]: export with index=False, reopen the file, verify "
        "shape (23, 14), then set cell_6_export_complete = True."
    )
if not OUT_PATH.exists():
    raise AssertionError("EXPORT CHECK FAILURE [cell 6]: the expected CSV does not exist.")
check = pd.read_csv(OUT_PATH)
if check.shape != (23, 14) or any(str(column).startswith("Unnamed:") for column in check.columns):
    raise AssertionError(
        f"EXPORT CHECK FAILURE [cell 6]: expected a reopened (23, 14) table with no index column; got {check.shape}."
    )
print("Export verified:", OUT_PATH, check.shape)


# %% [7] One Matplotlib scatter
# QUESTION           Does a bigger room always mean a higher energy intensity?
# INPUTS/ASSUMPTIONS cleaned from cell [5], with area_ft2 and energy_kwh_m2_yr
# METHOD             fig, ax = plt.subplots(); ax.scatter(...); label both axes with
#                    units; save with fig.savefig(...)
# CHECKS/INTERPRET   One point should sit far above the rest (a server closet) - do not
#                    delete it to make the figure look tidier.

fig, ax = plt.subplots()
# TODO: ax.scatter(cleaned["area_ft2"], cleaned["energy_kwh_m2_yr"])
ax.set_xlabel("area_ft2")
ax.set_ylabel("energy_kwh_m2_yr")
ax.set_title("Radley Hall: area (ft2) vs. energy intensity")
if not ax.collections:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 7]: draw the scatter before save; no blank PNG was written."
    )
if "ft" not in ax.get_xlabel().lower() or "kwh" not in ax.get_ylabel().lower():
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 7]: label both axes with readable units before save."
    )
fig.savefig("radley_scatter.png", dpi=150, bbox_inches="tight")
print("scatter saved")


# %% [8] Self-check: prove the pipeline on a different room
# QUESTION           Does your pipeline hold up on a room you have not hand-checked yet?
# INPUTS/ASSUMPTIONS cleaned from cells [4]-[6]; room R204, NOT room R101 used above
# METHOD             write 2-4 assert statements checking area_ft2, energy_kwh_yr,
#                    missing-value counts, and shape for R204 and cleaned as a whole
# CHECKS/INTERPRET   If every assertion holds, the cell prints its confirmation message
#                    with no error. Expected R204 area_ft2: 699.7, energy_kwh_yr: 6370.0.

# TODO: Add 2-4 assert statements here, checking room R204 (not R101) and cleaned's
# shape/missing-value counts. Example to complete:
# r204 = cleaned[cleaned["room_id"] == "R204"].iloc[0]
# assert round(r204["area_m2"] * 10.7639, 1) == r204["area_ft2"]
# assert round(r204["energy_kwh_m2_yr"] * r204["area_m2"]) == r204["energy_kwh_yr"]

cell_8_assertions_complete = False  # TODO: True only after 2-4 transfer assertions pass
if not cell_8_assertions_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8]: add and pass the R204/shape/missingness assertions, "
        "then set cell_8_assertions_complete = True."
    )
print("Self-check verified")


# %% [8b] Studio - export Part I for YOUR OWN Project 1 dataset
# QUESTION           Do Project 1 Part I's two graded files - a cleaned CSV and a data
#                    dictionary - exist yet for YOUR OWN dataset, not just for Radley Hall?
# INPUTS/ASSUMPTIONS your own Week 4 dataset; the name of the one column a row must have
#                    recorded to be usable; your own column meanings and provenance note.
#                    DATA_PATH starts at None on purpose: this cell must NOT be able to run
#                    silently against the shared Radley Hall file from cell [1] - that
#                    practice happens in cells [1]-[8] above, not here. Cell [6]'s
#                    radley_hall_cleaned.csv stays exactly as it is; this cell writes YOUR
#                    two files next to it, under the submission names Project 1 requires.
# METHOD             replace DATA_PATH / OUTCOME_COL / OWN_COLUMN_MEANINGS / OWN_PROVENANCE
#                    with your own; the None-guard raises immediately if you forget, so you
#                    cannot submit this cell still pointed at Radley Hall without an error
#                    telling you so. Then reuse cell [4]'s targeted .notna() filter, export
#                    with to_csv(..., index=False) as cleaned_data.csv, and call
#                    write_data_dictionary() - one documented function, docstring and type
#                    hints included - to write data_dictionary.txt.
# CHECKS/INTERPRET   Running this cell unedited must raise ValueError, not print a result.
#                    The worked Radley Hall stand-in in the Instructor file prints: rows in
#                    24 -> rows kept 23, reopened cleaned_data.csv (23, 12), undocumented
#                    columns 0, and a first dictionary line reading "room_id: unique room
#                    identifier, e.g. R101 (text label)". Your own dataset's numbers will
#                    differ - but undocumented columns must read 0 before you submit.

PROJECT_FOLDER = None        # TODO: Path to YOUR compiled Project 1 folder
DATA_PATH = None             # TODO: replace with YOUR OWN Week 4 dataset - NOT building_rooms.csv
OUTCOME_COL = None           # TODO: replace with the column a row must have recorded to be usable
OWN_COLUMN_MEANINGS = None   # TODO: replace with your own {"column": "unit or values - meaning"} dict
OWN_PROVENANCE = None        # TODO: replace with your own one-to-two sentence provenance note

if any(value is None for value in (PROJECT_FOLDER, DATA_PATH, OUTCOME_COL, OWN_COLUMN_MEANINGS, OWN_PROVENANCE)):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8b]: "
        "Replace DATA_PATH with the path to YOUR OWN Week 4 dataset before running "
        "this cell - do not run this cell against the shared Radley Hall file from "
        "cell [1]. Set OUTCOME_COL, OWN_COLUMN_MEANINGS, and OWN_PROVENANCE to your "
        "own column name, your own column meanings, and your own provenance note at "
        "the same time."
    )


def write_data_dictionary(frame: pd.DataFrame, meanings: dict[str, str],
                          provenance: str, out_path: Path) -> int:
    """TODO: one or two sentences describing what this function writes and returns."""
    # TODO: build one "column: meaning (unit)" line per column of `frame`, count the
    # columns `meanings` does not document, append the provenance note, and write the
    # whole thing to out_path as plain text, e.g.
    # lines = ["DATA DICTIONARY - one line per column of cleaned_data.csv", ""]
    # undocumented = 0
    # for column in frame.columns:
    #     entry = meanings.get(column)
    #     if entry is None:
    #         unit, meaning = "unit not stated", "UNDOCUMENTED - describe this column"
    #         undocumented += 1
    #     elif " - " in entry:
    #         unit, meaning = entry.split(" - ", 1)
    #     else:
    #         unit, meaning = "unit not stated", entry
    #     lines.append(f"{column}: {meaning} ({unit})")
    # lines.append("")
    # lines.append("PROVENANCE")
    # lines.append(provenance)
    # out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # return undocumented
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8b]: implement write_data_dictionary(); no placeholder "
        "dictionary was exported."
    )


PROJECT_FOLDER = Path(PROJECT_FOLDER)
DATA_PATH = Path(DATA_PATH)
if not DATA_PATH.exists():
    raise FileNotFoundError(f"DATA FILE ERROR [cell 8b]: {DATA_PATH} does not exist.")
if DATA_PATH.name.lower() == "building_rooms.csv":
    raise AssertionError(
        "PROJECT DATA CHECK FAILURE [cell 8b]: use your approved Project 1 dataset, not the shared practice CSV."
    )
if not PROJECT_FOLDER.exists():
    raise FileNotFoundError(f"PROJECT FOLDER ERROR [cell 8b]: {PROJECT_FOLDER} does not exist.")

own_raw = pd.read_csv(DATA_PATH)
if OUTCOME_COL not in own_raw.columns:
    raise KeyError(f"PROJECT SCHEMA ERROR [cell 8b]: outcome column {OUTCOME_COL!r} is missing.")
if set(OWN_COLUMN_MEANINGS) != set(own_raw.columns):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8b]: OWN_COLUMN_MEANINGS must document every source column exactly once."
    )
if any("TODO" in str(value).upper() for value in OWN_COLUMN_MEANINGS.values()) or "TODO" in OWN_PROVENANCE.upper():
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8b]: replace every placeholder meaning and provenance phrase."
    )
own_cleaned = own_raw[own_raw[OUTCOME_COL].notna()].copy()
print("rows in:", own_raw.shape[0], "-> rows kept:", own_cleaned.shape[0])

OWN_CLEAN_PATH = PROJECT_FOLDER / "cleaned_data.csv"
OWN_DICT_PATH = PROJECT_FOLDER / "data_dictionary.txt"
OWN_DICT_DRAFT_PATH = PROJECT_FOLDER / ".data_dictionary_draft.txt"

undocumented_columns = write_data_dictionary(
    own_cleaned, OWN_COLUMN_MEANINGS, OWN_PROVENANCE, OWN_DICT_DRAFT_PATH
)

if undocumented_columns != 0:
    raise AssertionError(
        f"EXPORT GATE FAILURE [cell 8b]: {undocumented_columns} exported columns are undocumented."
    )
if not OWN_DICT_DRAFT_PATH.exists():
    raise AssertionError("EXPORT GATE FAILURE [cell 8b]: the dictionary function wrote no draft file.")
dictionary_text = OWN_DICT_DRAFT_PATH.read_text(encoding="utf-8")
if "TODO" in dictionary_text.upper() or "UNDOCUMENTED" in dictionary_text.upper():
    raise AssertionError("EXPORT GATE FAILURE [cell 8b]: the dictionary draft still contains placeholders.")
if any(f"{column}:" not in dictionary_text for column in own_cleaned.columns):
    raise AssertionError("EXPORT GATE FAILURE [cell 8b]: the dictionary draft omits an exported column.")

# Only submission-ready names are written after every gate above passes.
own_cleaned.to_csv(OWN_CLEAN_PATH, index=False)
OWN_DICT_DRAFT_PATH.replace(OWN_DICT_PATH)

own_check = pd.read_csv(OWN_CLEAN_PATH)
print("reopened cleaned_data.csv:", own_check.shape)
print("undocumented columns:", undocumented_columns, "- this must read 0 before you submit")
print("first lines of data_dictionary.txt:")
for line in OWN_DICT_PATH.read_text(encoding="utf-8").splitlines()[:5]:
    print("   ", line)

assert undocumented_columns == 0, "every exported column needs its own dictionary line"
assert list(own_check.columns) == list(own_cleaned.columns)
assert own_check[OUTCOME_COL].notna().all()
# WHY THIS MATTERS: cleaned_data.csv and data_dictionary.txt ARE Project 1 Part I's two
# graded deliverables, under exactly those names, and they are the first two rows Week 7B's
# compile checklist looks for. A cleaned CSV with no dictionary is not evidence: nobody
# downstream - a grader, a collaborator, or you six weeks from now - can tell what a column
# means, what unit it carries, or where the numbers came from, so no claim built on it can
# be checked. Cell [3] wrote the dictionary down in Python; this cell is where it becomes a
# file that ships alongside the data it describes.
# COMMON ERROR: exporting a cleaned CSV carrying derived columns (area_ft2, energy_kwh_yr)
# while leaving them out of the dictionary. The CSV still opens, so the gap is invisible on
# inspection - which is why write_data_dictionary() returns a count of undocumented columns
# and the printed line above must read 0.

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
    # TODO: add at least four specific defects
]

print(ai_cleaning)
for defect in ai_defects:
    print("-", defect)

if len(ai_defects) < 4 or any("TODO" in defect.upper() for defect in ai_defects):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 9]: record at least four specific cleaning/export defects."
    )


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
1. what the trustworthiness interview found (the dtype anomaly, two missing values),
2. why R206 was dropped but has_daylight was kept and flagged instead,
3. what area_ft2 measures and why it was computed with NumPy, not a loop,
4. what the scatter plot shows, and
5. one thing this cleaned dataset cannot yet tell you about Radley Hall.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# A material inventory has quantity_m3, density_kg_m3, and carbon_kgco2e_kg,
# with missing density/factor values. List the five DataFrame interview calls,
# decide what to calculate versus flag, and state how pandas, NumPy, and
# Matplotlib would each support a trustworthy embodied-carbon check.
