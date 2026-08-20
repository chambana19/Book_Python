# -*- coding: utf-8 -*-
"""ARC 500 Project 1 starter: load, audit, clean, group, and flag evidence."""

# %% 0 — QUESTION
# Question:
# INPUTS/ASSUMPTIONS
# What one row means:
# METHOD
# Load local files relative to this project folder.
# CHECKS/INTERPRETATION
# State the expected rows, columns, and units before running.

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "Data" / "building_rooms.csv"
OUTPUT_DIR = PROJECT_DIR / "Submission"


def export_table(table: pd.DataFrame, path: Path) -> None:
    """Validate and save a nonempty DataFrame to CSV without the pandas row index."""
    if table.empty:
        raise AssertionError(f"EXPORT GATE FAILURE: {path.name} would be empty.")
    if any(str(column).startswith("Unnamed:") for column in table.columns):
        raise AssertionError(f"EXPORT GATE FAILURE: {path.name} contains an accidental index column.")
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(path, index=False)


# %% 1 — QUESTION
# Are the rows, columns, types, missing values, duplicates, and ranges plausible?
# INPUTS/ASSUMPTIONS
# The course CSV is the original evidence; do not overwrite it.
# METHOD
# Load and interview the DataFrame.
# CHECKS/INTERPRETATION
# Replace the expected values only after verifying them from the data dictionary.

data = pd.read_csv(DATA_FILE)
print(data.head())
print("shape:", data.shape)
print(data.dtypes)
print("missing:\n", data.isna().sum())
print("duplicate rows:", int(data.duplicated().sum()))
print(data.describe(include="all"))

# TODO: add at least four assert statements tied to expected evidence.

audit_assertions_complete = False  # TODO: True only after at least four evidence checks pass
if not audit_assertions_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 1]: add at least four data-specific assertions, run "
        "them, then set audit_assertions_complete = True."
    )


# %% 2 — QUESTION
# Which cleaning decisions are necessary for the project question?
# INPUTS/ASSUMPTIONS
# Every removed or changed row needs a written reason.
# METHOD
# Copy first, then make explicit cleaning/filtering decisions.
# CHECKS/INTERPRETATION
# Compare row counts and important ranges before and after.

def clean_rooms(raw: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw rooms table; raw itself is never modified."""
    # TODO: implement only justified cleaning steps.
    # cleaned = cleaned.loc[...].copy()
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 2]: implement only the cleaning decisions you can justify."
    )


clean = clean_rooms(data)

print("rows before:", len(data), "rows after:", len(clean))
cleaning_decisions = [
    # TODO: one sentence per removed, changed, or deliberately retained gap
]
if clean is data or clean.empty or list(clean.columns) != list(data.columns):
    raise AssertionError(
        "CLEANING CHECK FAILURE [cell 2]: return a nonempty copy with the documented source schema."
    )
if not cleaning_decisions or any("TODO" in sentence.upper() for sentence in cleaning_decisions):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 2]: record the reason for every cleaning/retention decision."
    )


# %% 3 — QUESTION
# How do at least two meaningful groups compare?
# INPUTS/ASSUMPTIONS
# Select one group column and one numerical outcome with stated units.
# METHOD
# groupby plus named aggregations.
# CHECKS/INTERPRETATION
# Confirm group counts add to the cleaned row count.

GROUP_COLUMN = "orientation"   # TODO: confirm or replace
OUTCOME_COLUMN = "energy_kwh_m2_yr"  # TODO: confirm or replace
grouping_choice_confirmed = False  # TODO: True after confirming question, groups, and units


def summarize_by_group(rooms: pd.DataFrame, group_column: str, outcome_column: str) -> pd.DataFrame:
    """Return one row per group_column value with n, mean, and median of outcome_column."""
    # "size" counts rows, including a row whose outcome is missing; mean/median
    # independently skip a missing outcome. Using the group column keeps this function
    # reusable for an approved dataset that has no room_id field.
    result = (
        rooms.groupby(group_column, dropna=False)
        .agg(
            n=(group_column, "size"),
            mean=(outcome_column, "mean"),
            median=(outcome_column, "median"),
        )
        .reset_index()
        .rename(columns={group_column: "group"})
    )
    return result[["group", "n", "mean", "median"]]


summary = summarize_by_group(clean, GROUP_COLUMN, OUTCOME_COLUMN)
print(summary.round(2))
assert int(summary["n"].sum()) == len(clean)
if not grouping_choice_confirmed:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 3]: confirm the group/outcome choice and its units, "
        "then set grouping_choice_confirmed = True."
    )
if summary["group"].nunique(dropna=False) < 2:
    raise AssertionError("GROUP CHECK FAILURE [cell 3]: compare at least two meaningful groups.")


# %% 4 — QUESTION
# Which rows are flagged by the IQR rule, and what should happen to each one?
# INPUTS/ASSUMPTIONS
# A flag begins an investigation; it is not automatic permission to delete.
# METHOD
# Calculate Q1, Q3, IQR, fences, and a Boolean mask.
# CHECKS/INTERPRETATION
# Inspect flagged rows in their full architectural context.

def iqr_bounds(values: pd.Series) -> tuple[float, float]:
    """Return (low, high) IQR fence bounds for a numeric Series."""
    q1, q3 = values.quantile(0.25), values.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def flag_outliers(values: pd.Series) -> pd.Series:
    """Return True for recorded values outside the IQR fences; missing values stay separate."""
    low, high = iqr_bounds(values)
    return values.notna() & ((values < low) | (values > high))


low_fence, high_fence = iqr_bounds(clean[OUTCOME_COLUMN])
analysis_table = clean.copy()
analysis_table["missing_flag"] = analysis_table[OUTCOME_COLUMN].isna()
analysis_table["outlier_flag"] = flag_outliers(analysis_table[OUTCOME_COLUMN])
flagged_rows = analysis_table.loc[analysis_table["outlier_flag"]].copy()
print("IQR fences:", low_fence, high_fence)
print(flagged_rows[[GROUP_COLUMN, OUTCOME_COLUMN, "missing_flag", "outlier_flag"]])

# Record one decision per flagged DataFrame index. Example:
# {17: ("INVESTIGATE", "Verify whether the server reading is representative.")}
OUTLIER_DECISIONS = {  # TODO: complete for every flagged row
}

allowed_actions = {"KEEP", "INVESTIGATE", "EXCLUDE"}
missing_decisions = set(flagged_rows.index) - set(OUTLIER_DECISIONS)
invalid_decisions = {
    index for index, decision in OUTLIER_DECISIONS.items()
    if not isinstance(decision, tuple)
    or len(decision) != 2
    or str(decision[0]).upper() not in allowed_actions
    or len(str(decision[1]).strip()) < 20
}
if missing_decisions or invalid_decisions:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 4]: record a valid action and substantive reason for "
        f"every outlier. Missing={sorted(missing_decisions)}, invalid={sorted(invalid_decisions)}."
    )
if (analysis_table["missing_flag"] & analysis_table["outlier_flag"]).any():
    raise AssertionError(
        "FLAG CHECK FAILURE [cell 4]: a missing value must not also be labeled an outlier."
    )

decision_rows = [
    {
        "row_index": index,
        "action": str(OUTLIER_DECISIONS[index][0]).upper(),
        "reason": str(OUTLIER_DECISIONS[index][1]).strip(),
    }
    for index in flagged_rows.index
]
decision_table = pd.DataFrame(decision_rows, columns=["row_index", "action", "reason"])

outlier_counts = (
    analysis_table.groupby(GROUP_COLUMN, dropna=False)["outlier_flag"]
    .sum()
    .astype(int)
    .reset_index()
    .rename(columns={GROUP_COLUMN: "group", "outlier_flag": "outlier_count"})
)
summary = summary.merge(outlier_counts, on="group", how="left")
summary["outlier_count"] = summary["outlier_count"].fillna(0).astype(int)
summary[["mean", "median"]] = summary[["mean", "median"]].round(2)

if list(summary.columns) != ["group", "n", "mean", "median", "outlier_count"]:
    raise AssertionError("SUMMARY CHECK FAILURE [cell 4]: grouped-summary schema is incorrect.")
if int(summary["outlier_count"].sum()) != int(analysis_table["outlier_flag"].sum()):
    raise AssertionError("SUMMARY CHECK FAILURE [cell 4]: group outlier counts do not match row flags.")


# %% 5 — QUESTION
# What is the bounded evidence claim?
# INPUTS/ASSUMPTIONS
# Use only outputs verified above.
# METHOD
# Print a short result statement with a numerical comparison and units.
# CHECKS/INTERPRETATION
# Name at least two limitations and one next evidence-gathering step.

EVIDENCE_STATEMENT = "TODO: one bounded numerical comparison with units"
LIMITATIONS = [
    # TODO: at least two specific limitations
]
NEXT_EVIDENCE_STEP = "TODO: one concrete next evidence-gathering step"
export_approved = False  # TODO: True only after the claim and all checks above are complete

if "TODO" in EVIDENCE_STATEMENT.upper() or len(EVIDENCE_STATEMENT.strip()) < 30:
    raise NotImplementedError("EXPECTED TODO STOP [cell 5]: write the bounded evidence statement.")
if len(LIMITATIONS) < 2 or any("TODO" in item.upper() for item in LIMITATIONS):
    raise NotImplementedError("EXPECTED TODO STOP [cell 5]: record at least two limitations.")
if "TODO" in NEXT_EVIDENCE_STEP.upper() or len(NEXT_EVIDENCE_STEP.strip()) < 20:
    raise NotImplementedError("EXPECTED TODO STOP [cell 5]: name a concrete next evidence step.")
if not export_approved:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: review every check, then set export_approved = True. "
        "No submission-like CSV has been written."
    )

if summary[["mean", "median"]].isna().any().any() or not np.isfinite(
    summary[["mean", "median"]].to_numpy(dtype=float)
).all():
    raise AssertionError("EXPORT GATE FAILURE [cell 5]: grouped means/medians must be finite.")

# Submission filenames are created only after audit, cleaning, grouping, flag, decision,
# claim, limitation, and next-step gates all pass.
export_table(analysis_table, OUTPUT_DIR / "cleaned_data.csv")
export_table(summary, OUTPUT_DIR / "grouped_summary.csv")
if not decision_table.empty:
    export_table(decision_table, OUTPUT_DIR / "outlier_decisions.csv")

print(EVIDENCE_STATEMENT)
print("Limitations:", LIMITATIONS)
print("Next evidence step:", NEXT_EVIDENCE_STEP)
print("Verified exports written to:", OUTPUT_DIR)
