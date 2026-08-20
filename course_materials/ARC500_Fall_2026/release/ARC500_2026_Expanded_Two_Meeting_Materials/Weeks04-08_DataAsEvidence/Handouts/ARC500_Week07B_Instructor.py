# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 7 studio · INSTRUCTOR SOLUTIONS
Spatial join and choropleth: merge, reproject, measure, map
Syracuse University · School of Architecture · Fall 2026
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
# COMMON ERROR: forgetting .reset_index() leaves "zone" as the index rather than a normal
# column - the later merge on="zone" would then raise a KeyError because "zone" would not
# be a column anymore.


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
# COMMON ERROR: merging with mismatched capitalization or spelling on either side (e.g.
# "north" vs "North") produces silent NaN rows instead of an error - see cell [7]'s AI-audit
# for exactly this bug.


# %% [4] The pitfall: measuring area before reprojecting
# QUESTION           What does .geometry.area return while zones_merged is still EPSG:4326?
# INPUTS/ASSUMPTIONS zones_merged from cell [3], still in its original EPSG:4326 CRS
# METHOD             call .geometry.area directly, with no .to_crs() first
# CHECKS/INTERPRET   Expected: a tiny, meaningless number close to 2.65e-08 (square degrees),
#                    NOT a usable area in square meters. Read the real UserWarning this
#                    produces at least once - do not suppress it your first time running this.

wrong_area = zones_merged.geometry.area
print("wrong (EPSG:4326) area, North:", f"{wrong_area.iloc[0]:.2e}")
# Real geopandas raises: "UserWarning: Geometry is in a geographic CRS. Results from 'area'
# are likely incorrect. Use 'GeoSeries.to_crs()' to re-project geometries to a projected
# CRS before this operation." This number is real math (degrees squared), applied to the
# wrong physical unit - not a crash, which is exactly why it is dangerous.


# %% [5] Reproject, then compute the real spatial metric
# QUESTION           What is each zone's footprint area, measured correctly?
# INPUTS/ASSUMPTIONS zones_merged from cell [3]; known ground truth: each zone is a
#                    24 m x 10 m rectangle = 240 m2 by construction
# METHOD             reproject to EPSG:32618 (UTM zone 18N - correct for Syracuse, NY, whose
#                    longitude falls in the 78W-72W band), then .geometry.area
# CHECKS/INTERPRET   Expected: both zones close to 239.74 m2 - within about 0.1% of the known
#                    240 m2 ground truth. This small gap is real projection distortion, not
#                    an error.

zones_utm = zones_merged.to_crs("EPSG:32618")
zones_utm["footprint_area_m2"] = zones_utm.geometry.area

print(zones_utm[["zone", "footprint_area_m2", "mean_energy_kwh_m2_yr"]])

pct_diff = (zones_utm["footprint_area_m2"] - 240.0).abs() / 240.0 * 100
print("percent difference from known 240 m2:")
print(pct_diff.round(3))

# CRS-choice justification note (required by Project 1 Part IV):
crs_choice_note = """
Reprojected to EPSG:32618 (UTM zone 18N) because Radley Hall's fictional site sits
at approximately 76.13 degrees W, 43.04 degrees N (Syracuse, NY), and UTM zone 18N
covers the 78W-72W longitude band. UTM gives coordinates in meters on a locally
accurate flat projection, which is required before computing area or length.
"""
print(crs_choice_note)


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
ax.set_title("Radley Hall (fictional): mean energy use intensity by zone")
ax.set_xlabel("Easting (m, EPSG:32618)")
ax.set_ylabel("Northing (m, EPSG:32618)")
fig.tight_layout()
fig.savefig("radley_hall_energy_choropleth.png", dpi=150)
print("Figure saved.")
# WHY THIS MATTERS: a map without labeled units and a stated CRS is not reproducible
# evidence - a reviewer (or your own Project 1 grader) cannot tell what the colors or axes
# mean without them. This is the same fig/ax labeling discipline from Week 6, just applied
# to a GeoDataFrame instead of a plain scatter plot.


# %% [6b] By floor, not just by zone: three in-code polygons
# QUESTION           Does the same merge-reproject-measure pipeline work on a different
#                    key, with geometry you build yourself instead of load from a file?
# INPUTS/ASSUMPTIONS rooms from cell [1], which has a "floor" column (1, 2, 3); three
#                    24m x 10m rectangles, one per floor, defined directly as shapely
#                    Polygon literals - not loaded from any file
# METHOD             write a small rect() helper, build a 3-row GeoDataFrame from it,
#                    groupby("floor") for a per-floor energy summary, merge, reproject,
#                    measure area, exactly like cells [1], [3], and [5]
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

floors_utm = floors.to_crs("EPSG:32618")
floors_utm["footprint_area_m2"] = floors_utm.geometry.area
floors_merged = floors_utm.merge(floor_summary, on="floor", how="left")

print(floors_merged[["floor", "footprint_area_m2", "mean_energy_kwh_m2_yr"]])
# COMMON ERROR: assuming shapely.geometry.Polygon needs a file to exist - it does not;
# any list of (x, y) coordinate pairs in order defines a valid polygon in code, which is
# exactly how zone_footprints.geojson itself was originally authored for this course.

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
ax.set_title("Radley Hall (fictional): mean energy use intensity by floor")
ax.set_xlabel("Easting (m, EPSG:32618)")
ax.set_ylabel("Northing (m, EPSG:32618)")
fig.tight_layout()
fig.savefig("radley_hall_floor_choropleth.png", dpi=150)
print("Figure saved.")
# WHY THIS MATTERS: the exact same four-step shape (groupby, merge, reproject, measure)
# that mapped zone now maps floor - a real second key, built from geometry you wrote
# yourself rather than downloaded. Project 1 Part IV credits exactly this kind of second
# evidence extension, on a key of your own choosing.


# %% [7] AI-audit: two bugs, one merged result
# QUESTION           An AI assistant wrote the function below. Find both defects before
#                    trusting its output.
# INPUTS/ASSUMPTIONS rooms and zones as loaded in cells [1]-[2]
# METHOD             run the function as given, inspect the (wrong) output, then name both
#                    defects in ai_defects below
# CHECKS/INTERPRET   A defensible list names the merge-key defect AND the CRS defect - not
#                    merely that the numbers "look wrong."

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
    "zone_summary['zone'] = zone_summary['zone'].str.lower() lowercases the join key to "
    "'north'/'south', but zones_gdf still has 'North'/'South' - the merge silently finds "
    "no matches, so mean_energy_kwh_m2_yr comes back NaN for every row instead of raising "
    "an error.",
    "merged['area_m2'] = merged.geometry.area runs before any .to_crs() call, so the "
    "column named area_m2 actually holds square-DEGREE values (about 2.65e-08) - a "
    "misleadingly named, physically meaningless number.",
    "No CRS-choice justification anywhere in the function - Project 1 Part IV requires "
    "one, and there is no comment or docstring stating what CRS the geometry is even in.",
    "No docstring and no type hints on ai_zone_area_report, despite that convention being "
    "required starting Week 4.",
]

for defect in ai_defects:
    print("-", defect)


def zone_area_report(rooms_df: pd.DataFrame, zones_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Return each zone's projected footprint area (m2) beside its mean energy use intensity."""
    zone_summary = rooms_df.groupby("zone").agg(
        mean_energy_kwh_m2_yr=("energy_kwh_m2_yr", "mean")
    ).reset_index()
    merged = zones_gdf.merge(zone_summary, on="zone", how="left")
    merged_utm = merged.to_crs("EPSG:32618")
    merged_utm["area_m2"] = merged_utm.geometry.area
    return merged_utm[["zone", "area_m2", "mean_energy_kwh_m2_yr"]]


fixed_result = zone_area_report(rooms, zones)
print(fixed_result)
assert abs(fixed_result.loc[fixed_result["zone"] == "North", "area_m2"].iloc[0] - 239.74) < 0.05
assert abs(fixed_result.loc[fixed_result["zone"] == "South", "area_m2"].iloc[0] - 239.74) < 0.05
print("Fixed function reproduces cell [5]'s known-good values.")


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

zones_utm["perimeter_m"] = zones_utm.geometry.length
print(zones_utm[["zone", "perimeter_m"]])

p_r102 = Point(-76.134977093003, 43.03940661157025)
p_r103 = Point(-76.13487876740541, 43.03940661157025)
pair = gpd.GeoDataFrame({"room_id": ["R102", "R103"]}, geometry=[p_r102, p_r103], crs="EPSG:4326")

d_deg = pair.geometry.iloc[0].distance(pair.geometry.iloc[1])
d_m = pair.to_crs("EPSG:32618").geometry.iloc[0].distance(pair.to_crs("EPSG:32618").geometry.iloc[1])
print(f"R102-R103 in EPSG:4326 (degrees): {d_deg:.6f}")
print(f"R102-R103 in EPSG:32618 (meters): {d_m:.3f}")

assert abs(zones_utm.loc[zones_utm["zone"] == "North", "perimeter_m"].iloc[0] - 68.0) < 0.1
assert abs(zones_utm.loc[zones_utm["zone"] == "South", "perimeter_m"].iloc[0] - 68.0) < 0.1
assert abs(d_m - 8.0) < 0.1
assert d_deg < 0.001

print("Self-check assertions passed")
# COMMON ERROR: comparing d_m to 8.0 with == instead of a tolerance (abs(d_m - 8.0) < 0.1)
# fails every time - real projected-CRS measurements carry small, honest distortion and will
# almost never equal a ground-truth value exactly.


# %% [9] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the finished
#                    workflow in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name at least two
#                    explicit limitations, per Project 1 Part IV's closing requirement.

ai_use_record = """
Tool/model: Example assistant
Prompt: Merge a zone-level energy summary onto zone_footprints.geojson and map it.
Suggestion received: A function that lowercased the join key and computed area
before reprojecting.
What I accepted: The overall merge-then-plot structure.
What I modified and why: Removed the .str.lower() call so the join key matched
exactly, and reprojected to EPSG:32618 before computing area.
What I rejected and why: The unreprojected area_m2 column - it held square-degree
values that would have silently misreported every zone's footprint size.
How I tested it: Compared the fixed function's output against cell [5]'s
known-good 239.74 m2 values with two assert statements.
One limitation I found: Two zones is too few to generalize a citywide energy
pattern; the CRS choice (UTM 18N) is only correct for this specific Syracuse, NY
location.
"""

exit_explanation = """
The merge attaches Week 5's zone energy/area summary to each zone polygon using an
exact-matching zone key; a capitalization mismatch would silently drop every row
to NaN instead of raising an error. Area and length both require a projected CRS,
not the file's original EPSG:4326 degrees - reprojecting to EPSG:32618 (justified
by Syracuse, NY's longitude falling inside UTM zone 18N) turns a meaningless
2.65e-08 into a trustworthy 239.74 m2, within 0.1% of the known 240 m2 ground
truth, small honest distortion, not an error. The choropleth shows South shaded
far darker than North, spatializing Week 5's roughly 80% higher energy finding.
This cannot judge construction quality or occupant behavior, and two zones cannot
generalize beyond this one fictional building.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Entrance points and shade polygons arrive in EPSG:4326. Expected sequence:
# inspect both layers; reproject to EPSG:32618 before the 5 m buffer/distance;
# state a within/intersects boundary rule; run the join; inspect unmatched rows
# and plot the result. A shared CRS is necessary, but projected units are what
# make the five-meter claim meaningful.
