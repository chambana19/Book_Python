# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 7 studio · Spatial join and choropleth: merge, reproject, measure, map
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week07 module folder, alongside building_rooms.csv
     and zone_footprints.geojson (the same shared Radley Hall files from Weeks
     4-6 - this is fictional, illustrative data, not a real building).
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict the printed table or number before running.
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  Never trust an area, length, or distance computed in a geographic CRS
  (degrees). Always state which EPSG code you reprojected to, and why, before
  reporting any spatial measurement.

THIS WEEK'S ASSIGNMENT IS PROJECT 1's SPATIAL LAYER
  The reproducible script, the CRS-choice justification note, and the static
  choropleth map you build below ARE the Week 7 studio assignment AND the
  Project 1 Part IV milestone - one artifact, not two.
"""

# %% [0] Environment and working-folder check
# QUESTION           Confirm your Python version, executable, and working folder, and that
#                    both data files are visible.
# INPUTS/ASSUMPTIONS no inputs; building_rooms.csv and zone_footprints.geojson sit in this
#                    same folder
# METHOD             run the cell and read the printed environment lines and the two
#                    Path.exists() checks
# CHECKS/INTERPRET   You should see a Python version, an executable path, a folder path,
#                    and True for both data-file checks.

from pathlib import Path
import sys

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())
print("building_rooms.csv found:", Path("building_rooms.csv").exists())
print("zone_footprints.geojson found:", Path("zone_footprints.geojson").exists())

missing_inputs = [
    name for name in ("building_rooms.csv", "zone_footprints.geojson")
    if not Path(name).exists()
]
if missing_inputs:
    raise FileNotFoundError(f"DATA FILE ERROR [cell 0]: missing {missing_inputs}.")


# %% [1] Recall Week 5: one row of attributes per zone
# QUESTION           Rebuild the zone-level summary table from Week 5's groupby.
# INPUTS/ASSUMPTIONS building_rooms.csv; group by zone; mean energy, mean area, room count
# METHOD             pandas groupby().agg() with three named aggregations, then reset_index()
# CHECKS/INTERPRET   Expected: North mean_energy_kwh_m2_yr = 64.25, South = 115.68 (rounded);
#                    room_count = 12 for each zone.

import pandas as pd

rooms = pd.read_csv("building_rooms.csv")

zone_summary = rooms.groupby("zone").agg(
    mean_energy_kwh_m2_yr=("energy_kwh_m2_yr", "mean"),
    mean_area_m2=("area_m2", "mean"),
    room_count=("room_id", "count"),
).reset_index()

print(zone_summary)

# TODO: Before moving on, write one sentence: which zone uses more energy per square
# meter, and roughly by how much?

if not (
    zone_summary["zone"].tolist() == ["North", "South"]
    and abs(zone_summary.loc[0, "mean_energy_kwh_m2_yr"] - 64.25) < 0.01
    and abs(zone_summary.loc[1, "mean_energy_kwh_m2_yr"] - 115.68) < 0.01
    and zone_summary["room_count"].tolist() == [12, 12]
):
    raise AssertionError("GROUP CHECK FAILURE [cell 1]: the expected North/South summary changed.")


# %% [2] Load the zone geometry and inspect its CRS
# QUESTION           What CRS is zone_footprints.geojson stored in, and is it safe to
#                    measure area directly?
# INPUTS/ASSUMPTIONS zone_footprints.geojson; two polygons, North and South
# METHOD             gpd.read_file(), then print the GeoDataFrame and its .crs
# CHECKS/INTERPRET   Expected CRS: EPSG:4326 (geographic, degrees) - NOT safe to measure area
#                    directly yet.

import geopandas as gpd

zones = gpd.read_file("zone_footprints.geojson")
print(zones)
print("CRS:", zones.crs)

if zones.crs is None or zones.crs.to_epsg() != 4326 or len(zones) != 2:
    raise AssertionError("SPATIAL DATA CHECK FAILURE [cell 2]: expected two EPSG:4326 polygons.")


# %% [3] Merge the zone summary onto the geometry
# QUESTION           Attach mean_energy_kwh_m2_yr, mean_area_m2, and room_count to each
#                    zone polygon.
# INPUTS/ASSUMPTIONS zones from cell [2]; zone_summary from cell [1]; shared key: zone
# METHOD             an ordinary pandas .merge(), on="zone", how="left" - exactly like Week 5
# CHECKS/INTERPRET   Expected: type(zones_merged) is still GeoDataFrame; North shows 64.25,
#                    South shows 115.68 (rounded).

zones_merged = zones.merge(zone_summary, on="zone", how="left")

print(type(zones_merged).__name__)
print(zones_merged[["zone", "mean_energy_kwh_m2_yr", "mean_area_m2", "room_count"]])

# TODO: In one sentence, explain what would happen to this merge if one side's zone
# values were "north"/"south" (lowercase) instead of "North"/"South".

if len(zones_merged) != 2 or zones_merged["mean_energy_kwh_m2_yr"].isna().any():
    raise AssertionError("MERGE CHECK FAILURE [cell 3]: both polygons need matched zone attributes.")


# %% [4] The pitfall: measuring area before reprojecting
# QUESTION           What does .geometry.area return while zones_merged is still EPSG:4326?
# INPUTS/ASSUMPTIONS zones_merged from cell [3], still in its original EPSG:4326 CRS
# METHOD             call .geometry.area directly, with no .to_crs() first
# CHECKS/INTERPRET   Expected: a tiny, meaningless number close to 2.65e-08 (square degrees),
#                    NOT a usable area in square meters. Read the real UserWarning this
#                    produces at least once - do not suppress it your first time running this.

wrong_area = zones_merged.geometry.area
print("wrong (EPSG:4326) area, North:", f"{wrong_area.iloc[0]:.2e}")

# TODO: In one sentence, explain why this number cannot be trusted as an area in m2.


# %% [5] Reproject, then compute the real spatial metric
# QUESTION           What is each zone's footprint area, measured correctly?
# INPUTS/ASSUMPTIONS zones_merged from cell [3]; known ground truth: each zone is a
#                    24 m x 10 m rectangle = 240 m2 by construction
# METHOD             reproject to EPSG:32618 (UTM zone 18N - correct for Syracuse, NY, whose
#                    longitude falls in the 78W-72W band), then .geometry.area
# CHECKS/INTERPRET   Expected: both zones close to 239.74 m2 - within about 0.1% of the known
#                    240 m2 ground truth. This small gap is real projection distortion, not
#                    an error.

zones_utm = zones_merged  # TODO: replace with zones_merged.to_crs("EPSG:32618")
zones_utm["footprint_area_m2"] = 0.0  # TODO: replace 0.0 with zones_utm.geometry.area

print(zones_utm[["zone", "footprint_area_m2", "mean_energy_kwh_m2_yr"]])

# TODO: Once both lines above are fixed, footprint_area_m2 should print close to 239.74
# for both zones (known ground truth: 240.0 m2 each).

# CRS-choice justification note (required by Project 1 Part IV - write 1-2 sentences):
crs_choice_note = """
TODO: state the EPSG code you used above and justify it using Syracuse, NY's
longitude and the UTM zone band it falls inside.
"""

if zones_utm.crs is None or zones_utm.crs.to_epsg() != 32618:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: reproject to EPSG:32618 before measuring area."
    )
if not zones_utm["footprint_area_m2"].between(239.5, 240.1).all():
    raise AssertionError(
        "SPATIAL CHECK FAILURE [cell 5]: projected footprint areas should be about 239.74 m²."
    )
if "TODO" in crs_choice_note.upper() or "32618" not in crs_choice_note:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: finish the EPSG:32618 / Syracuse UTM-zone justification."
    )


# %% [6] Build the static, labeled choropleth
# QUESTION           Produce one map, shaded by mean_energy_kwh_m2_yr, with a title, labeled
#                    axes (units + CRS), and a color-scale legend.
# INPUTS/ASSUMPTIONS zones_utm from cell [5]
# METHOD             fig, ax = plt.subplots(); zones_utm.plot(column=..., ax=ax, legend=True);
#                    then ax.set_title/set_xlabel/set_ylabel; save with fig.savefig()
# CHECKS/INTERPRET   Inspect the saved PNG in Spyder's Plots pane: South should render
#                    visibly darker than North across the color scale.

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 5))
zones_utm.plot(
    column="mean_energy_kwh_m2_yr",
    cmap="OrRd",
    edgecolor="black",
    linewidth=1.2,
    legend=True,
    legend_kwds={"label": "Mean energy use intensity (kWh/m2/yr)"},
    ax=ax,
)
ax.set_title("TODO: a descriptive title naming Radley Hall as fictional")
ax.set_xlabel("TODO: Easting label with units and EPSG code")
ax.set_ylabel("TODO: Northing label with units and EPSG code")
fig.tight_layout()
map_labels = " ".join([ax.get_title(), ax.get_xlabel(), ax.get_ylabel()])
if "TODO" in map_labels.upper() or "32618" not in map_labels or not ax.collections:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 6]: finish the map, title, units, and EPSG labels "
        "before save; no placeholder PNG was written."
    )
fig.savefig("radley_hall_energy_choropleth.png", dpi=150, bbox_inches="tight")
print("Figure saved.")

# TODO: Fill in the title/xlabel/ylabel strings above, then check the saved PNG: South
# should render visibly darker than North.


# %% [6b] By floor, not just by zone: three in-code polygons
# QUESTION           Does the same merge-reproject-measure pipeline work on a different
#                    key, with geometry you build yourself instead of load from a file?
# INPUTS/ASSUMPTIONS rooms from cell [1], which has a "floor" column (1, 2, 3); three
#                    24m x 10m rectangles, one per floor, defined directly as shapely
#                    Polygon literals - not loaded from any file
# METHOD             a rect() helper builds each polygon; groupby("floor") summarizes
#                    energy the same way cell [1] grouped by zone; then reproject and
#                    measure area exactly like cell [5]
# CHECKS/INTERPRET   Expected: mean_energy_kwh_m2_yr of 66.29 (floor 1), 79.57 (floor 2),
#                    113.61 (floor 3); footprint_area_m2 near 240 for all three, but not
#                    identical - small projection distortion differs by latitude band.

from shapely.geometry import Polygon


def rect(lon0: float, lat0: float, lon1: float, lat1: float) -> Polygon:
    """Return an axis-aligned rectangle from two corner (lon, lat) pairs."""
    return Polygon([(lon0, lat0), (lon1, lat0), (lon1, lat1), (lon0, lat1)])


floors = gpd.GeoDataFrame(
    {"floor": [1, 2, 3]},
    geometry=[
        rect(-76.1361, 43.0392, -76.135805, 43.0392898),
        rect(-76.1361, 43.039362, -76.135805, 43.039452),
        rect(-76.1361, 43.039524, -76.135805, 43.039614),
    ],
    crs="EPSG:4326",
)

floor_summary = rooms.groupby("floor").agg(
    mean_energy_kwh_m2_yr=("energy_kwh_m2_yr", "mean"),
).round(2).reset_index()

floors_utm = floors  # TODO: replace with floors.to_crs("EPSG:32618")
floors_utm["footprint_area_m2"] = 0.0  # TODO: replace 0.0 with floors_utm.geometry.area
floors_merged = floors_utm.merge(floor_summary, on="floor", how="left")

print(floors_merged[["floor", "footprint_area_m2", "mean_energy_kwh_m2_yr"]])

# TODO: Once both lines above are fixed, footprint_area_m2 should print close to 240
# for all three floors (known ground truth: 240.0 m2 each).

if floors_utm.crs is None or floors_utm.crs.to_epsg() != 32618:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 6b]: reproject the three floor polygons before measuring."
    )
if not floors_merged["footprint_area_m2"].between(239.5, 240.1).all():
    raise AssertionError("SPATIAL CHECK FAILURE [cell 6b]: floor areas should be about 240 m².")

fig, ax = plt.subplots(figsize=(6, 5))
floors_merged.plot(
    column="mean_energy_kwh_m2_yr",
    cmap="OrRd",
    edgecolor="black",
    linewidth=1.2,
    legend=True,
    legend_kwds={"label": "Mean energy use intensity (kWh/m2/yr)"},
    ax=ax,
)
ax.set_title("TODO: a descriptive title naming Radley Hall as fictional, by floor")
ax.set_xlabel("TODO: Easting label with units and EPSG code")
ax.set_ylabel("TODO: Northing label with units and EPSG code")
fig.tight_layout()
floor_map_labels = " ".join([ax.get_title(), ax.get_xlabel(), ax.get_ylabel()])
if "TODO" in floor_map_labels.upper() or "32618" not in floor_map_labels or not ax.collections:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 6b]: finish the floor-map title, units, and EPSG labels "
        "before save."
    )
fig.savefig("radley_hall_floor_choropleth.png", dpi=150, bbox_inches="tight")
print("Figure saved.")

# TODO: Fill in the title/xlabel/ylabel strings above, then check the saved PNG: floor 3
# should render visibly darker than floor 1.


# %% [7] AI-audit: two bugs, one merged result
# QUESTION           An AI assistant wrote the function below. Find both defects before
#                    trusting its output.
# INPUTS/ASSUMPTIONS rooms and zones as loaded in cells [1]-[2]
# METHOD             run the function as given, inspect the (wrong) output, then name both
#                    defects in ai_defects below
# CHECKS/INTERPRET   A defensible list names the merge-key defect AND the CRS defect AND the
#                    missing-docstring/type-hint defect - not merely that the numbers "look wrong."

def ai_zone_area_report(rooms_df, zones_gdf):
    zone_summary = rooms_df.groupby("zone").agg(
        mean_energy_kwh_m2_yr=("energy_kwh_m2_yr", "mean")
    ).reset_index()
    zone_summary["zone"] = zone_summary["zone"].str.lower()
    merged = zones_gdf.merge(zone_summary, on="zone", how="left")
    merged["area_m2"] = merged.geometry.area
    return merged[["zone", "area_m2", "mean_energy_kwh_m2_yr"]]

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print(ai_zone_area_report(rooms, zones))

ai_defects = [
    # TODO: name the merge-key defect (what does .str.lower() break here?)
    # TODO: name the CRS defect (what CRS is merged.geometry.area actually using?)
    # TODO: name the missing-docstring/type-hint defect (required convention since Week 4 -
    #       does ai_zone_area_report have either one?)
]

for defect in ai_defects:
    print("-", defect)

if len(ai_defects) < 3 or any("TODO" in defect.upper() for defect in ai_defects):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 7]: name the merge-key, CRS, and documentation defects."
    )

# TODO: Write a corrected zone_area_report() function below, fixing both defects, and
# confirm it reproduces the 239.74 m2 / 64.25 / 115.68 values from cells [1] and [5].

def zone_area_report(rooms_df, zones_gdf):
    """TODO: one-line docstring describing what this function returns."""
    # TODO: implement the fixed version
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 7]: implement the corrected typed/documented zone report."
    )


corrected_report = zone_area_report(rooms, zones)
required_report_columns = {"zone", "area_m2", "mean_energy_kwh_m2_yr"}
if (
    not zone_area_report.__doc__
    or "TODO" in zone_area_report.__doc__.upper()
    or not {"rooms_df", "zones_gdf", "return"}.issubset(zone_area_report.__annotations__)
):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 7]: add a real docstring plus parameter and return type hints."
    )
if not required_report_columns.issubset(corrected_report.columns):
    raise AssertionError("FUNCTION CHECK FAILURE [cell 7]: corrected report schema is incomplete.")
if not corrected_report["area_m2"].between(239.5, 240.1).all():
    raise AssertionError("FUNCTION CHECK FAILURE [cell 7]: corrected report still measures in degrees.")


# %% [8] Self-check: perimeter length and a second 8 m pair (REQUIRED TRANSFER CHECK)
# QUESTION           Does the same projected-CRS rule hold for a different spatial metric
#                    (perimeter length) and a different pair of points?
# INPUTS/ASSUMPTIONS zones_utm from cell [5]; a second room pair, R102 and R103, also known
#                    to be 8.0 m apart (a different pair than the R101-R102 pair used in
#                    Meeting A)
# METHOD             compute zones_utm.geometry.length; separately build a two-point
#                    GeoDataFrame for R102/R103 in EPSG:4326 and reproject to EPSG:32618
# CHECKS/INTERPRET   Expected: both zones' perimeter_m close to 68.01 m (known truth: 68.0 m);
#                    R102-R103 close to 8.010 m in EPSG:32618 and 0.000098 in EPSG:4326 -
#                    the same pattern as Meeting A's demonstration, on new inputs.

from shapely.geometry import Point

zones_utm["perimeter_m"] = 0.0  # TODO: replace 0.0 with zones_utm.geometry.length
print(zones_utm[["zone", "perimeter_m"]])

if not zones_utm["perimeter_m"].between(67.9, 68.2).all():
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8]: calculate perimeter from the EPSG:32618 geometry."
    )

p_r102 = Point(-76.134977093003, 43.03940661157025)
p_r103 = Point(-76.13487876740541, 43.03940661157025)
pair = gpd.GeoDataFrame({"room_id": ["R102", "R103"]}, geometry=[p_r102, p_r103], crs="EPSG:4326")

d_deg = pair.geometry.iloc[0].distance(pair.geometry.iloc[1])
d_m = pair.to_crs("EPSG:32618").geometry.iloc[0].distance(pair.to_crs("EPSG:32618").geometry.iloc[1])
print(f"R102-R103 in EPSG:4326 (degrees): {d_deg:.6f}")
print(f"R102-R103 in EPSG:32618 (meters): {d_m:.3f}")

# TODO: Write 2-4 of your own assert statements below, applied to THESE values (a different
# metric and a different room pair than the ones worked through live), e.g.:
#   assert abs(zones_utm.loc[zones_utm["zone"] == "North", "perimeter_m"].iloc[0] - 68.0) < 0.1
#   assert abs(d_m - 8.0) < 0.1
#   assert d_deg < 0.001

cell_8_assertions_complete = False  # TODO: True only after 2-4 transfer assertions pass
if not cell_8_assertions_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8]: add the perimeter/distance assertions, then set "
        "cell_8_assertions_complete = True."
    )
if abs(d_m - 8.0) >= 0.1 or d_deg >= 0.001:
    raise AssertionError("SPATIAL CHECK FAILURE [cell 8]: projected/unprojected distance check failed.")
print("Self-check verified")


# %% [9] Compile Parts I-IV into one Project 1 folder (due at Week 8)
# QUESTION           Are Parts I-III, already produced in Weeks 4-6, and this week's new
#                    Part IV spatial layer, all sitting together in ONE folder under the
#                    names your Project 1 submission needs -- or is anything still missing?
# INPUTS/ASSUMPTIONS PROJECT_FOLDER is the one folder that should hold everything: Part I
#                    (cleaned_data.csv + data_dictionary.txt, both written by Week 4B cell
#                    [8b] from YOUR OWN dataset), Part II (grouped_summary.csv, written by
#                    Week 5B cell [15] from YOUR OWN dataset, plus your outlier decisions),
#                    Part III (Week 6B's two static figures), and Part IV (this week's map,
#                    or Week 6's animation .gif if you chose that extension instead). The row
#                    names below are the submission names from Project 1's brief, not Radley
#                    Hall's demo file names, so NOT all six defaults are files the weekly
#                    scripts hand you: a lone run of THIS script can satisfy only the Part IV
#                    row, plus Part III's two figure rows if Week 6B's script has been run in
#                    this same folder. Parts I and II are yours to export from your own data
#                    in Week 4B cell [8b] and Week 5B cell [15] and copy in here.
# METHOD             list every required deliverable as one Path per row, grouped by Part;
#                    check each with Path.exists(); print a PASS/MISSING report; count how
#                    many rows are missing.
# CHECKS/INTERPRET   Run in a folder holding only this script's own output: the Part IV row
#                    reads PASS (cell [6] saved the map earlier in this same run) and the
#                    other five read MISSING -- 5 of 6 missing. Run in the shared handouts
#                    folder, where Week 6B's script has also left week06_figures/ behind: the
#                    two Part III rows read PASS too -- 3 of 6 missing. Every row reads PASS
#                    only once YOUR OWN Part I and Part II exports sit in PROJECT_FOLDER;
#                    that is the "compile Parts I-III, then append Part IV" milestone this
#                    cell checks, one week before Week 8's clinic re-checks the same parts.

PROJECT_FOLDER = None        # TODO: Path to YOUR compiled Project 1 folder
if PROJECT_FOLDER is None:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 9]: set PROJECT_FOLDER to your compiled submission folder."
    )
PROJECT_FOLDER = Path(PROJECT_FOLDER)
if not PROJECT_FOLDER.exists():
    raise FileNotFoundError(f"PROJECT FOLDER ERROR [cell 9]: {PROJECT_FOLDER} does not exist.")

required_deliverables = {
    "Part I   (Wk4) cleaned CSV":         PROJECT_FOLDER / "cleaned_data.csv",  # TODO: your own Week 4B cell [8b] export
    "Part I   (Wk4) data dictionary":     PROJECT_FOLDER / "data_dictionary.txt",  # TODO: your own Week 4B cell [8b] export
    "Part II  (Wk5) grouped-summary CSV": PROJECT_FOLDER / "grouped_summary.csv",  # TODO: your own Week 5B cell [15] export
    "Part III (Wk6) distribution figure": PROJECT_FOLDER / "week06_figures" / "energy_distribution.png",  # TODO
    "Part III (Wk6) relationship figure": PROJECT_FOLDER / "week06_figures" / "area_vs_energy_relationship.png",  # TODO
    "Part IV  (Wk7) map or animation":    PROJECT_FOLDER / "radley_hall_energy_choropleth.png",  # TODO: your own map, or Week 6's .gif
}

print(f"{'Deliverable':38s} status")
missing = []
for label, path in required_deliverables.items():
    ok = path.exists()
    print(f"{label:38s} {'PASS' if ok else 'MISSING'}")
    if not ok:
        missing.append(label)

print()
print(len(missing), "of", len(required_deliverables), "deliverables missing")

if missing:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 9]: compile the remaining Project 1 deliverables: "
        f"{missing}."
    )

print("Compile check verified — now run Project01_Evidence_Before_Design/validate_submission.py")


# %% [10] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the finished
#                    workflow in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name at least two
#                    explicit limitations, per Project 1 Part IV's closing requirement.

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
1. why the merge required an exact-matching zone key,
2. why area/length had to be measured after reprojecting, not before,
3. what the 239.74 m2 vs 240 m2 gap does and does not mean,
4. what the choropleth shows and what design implication it supports, and
5. at least two explicit limitations of this spatial analysis.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Entrance points and shade polygons arrive in EPSG:4326. Describe the exact
# sequence for a 5 m entrance review buffer and point-in-polygon join: inspect
# geometry/CRS, reproject to EPSG:32618, predict within versus intersects for a
# boundary point, run the join, and verify every unmatched entrance.
