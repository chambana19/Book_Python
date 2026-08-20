# Shared teaching dataset for Weeks 4-7 (Radley Hall — fictional building)

**All Weeks 4-7 in-class examples should use this SAME dataset as the running
class demonstration**, the same way Weeks 1-3 kept reusing one Gallery/Lobby/
Studio room example. Do not invent a different in-class dataset per week —
continuity across weeks is part of what makes the sequence feel connected.
(Students' own Project 1 datasets, referenced in the weekly-assignment
sections of the plan, are separate and personal — this shared dataset is only
for the taught, in-class material.)

**This is fictional, illustrative data — explicitly say so on the first
slide that introduces it.** It is not real measured data about the actual
Slocum Hall or any real building. Call the building "Radley Hall" in slides
and handouts.

Files:
- `data/building_rooms.csv` — 24 rooms, the primary dataset for Weeks 4-6.
- `data/zone_footprints.geojson` — two zone polygons (North, South) for Week 7.

Both were generated and every number below was VERIFIED in the pinned course
environment with pandas 3.0.5 / geopandas 1.1.4 — do not
recompute these by hand or reasoning; if you need a value not listed here,
run it yourself against the same interpreter and the same CSV/GeoJSON files
(they will not change), and cite the exact code you ran.

## Columns (building_rooms.csv)

| column | dtype (as pandas 3.0.5 actually prints it) | meaning |
|---|---|---|
| room_id | str | e.g. "R101" |
| floor | int64 | 1, 2, or 3 |
| zone | str | "North" or "South" |
| room_type | str | Lobby, Gallery, Office, Studio, Classroom, Server, Closet |
| area_m2 | float64 | room floor area |
| orientation | str | N/S/E/W |
| has_daylight | **object** (not bool!) | True/False, but ONE missing value (room R303) forces pandas to store this column as `object` rather than a clean bool dtype — a real, useful "the dtype itself tells you something about data quality" moment for the Week 4 trustworthiness interview. Say this explicitly on slide. |
| energy_kwh_m2_yr | float64 | annual energy use intensity; ONE missing value (room R206) |
| x_m, y_m | float64 | simple local site-plan coordinates in meters |
| lat, lon | float64 | geographic coordinates (EPSG:4326), consistent with x_m/y_m via a fixed local reference point near Syracuse, NY (used only as a plausible geographic anchor, not a real building footprint). Exactly: `lat = 43.03944254401725 - y_m * (1/111320)` and `lon = -76.1351 + x_m * 1.22906997e-05`. **Note the sign on y_m: +y_m runs SOUTH**, because the site plan's origin is its north-west corner — so North-zone rooms (y_m=4.0) sit at a HIGHER latitude than South-zone rooms (y_m=22.0), which is what makes them land in the correct North/South polygons of `zone_footprints.geojson`. |

Verified with `df.isna().sum()`: exactly 1 null in `has_daylight`, 1 null in
`energy_kwh_m2_yr`, 0 elsewhere.

## Verified findings to reuse (do not re-derive different numbers)

**Outlier detection (Week 5) — a genuinely rich, real disagreement between
the two rules, not a manufactured one:**
- On `energy_kwh_m2_yr`: BOTH the IQR rule and the z-score rule cleanly flag
  room **R306** (a server closet at 410.0 kWh/m2/yr, z ≈ very large) as an
  unambiguous genuine extreme. Use this as the first, clean worked example.
- On `area_m2`: the two rules DISAGREE, which is a better teaching moment
  than a clean catch — z-score (threshold |z|>2) flags room **R309** (a
  120.0 m2 double-height gallery, z=2.82) as an outlier, but the IQR rule
  (Q1=16.95, Q3=59.75, bounds -47.25 to 123.95) does NOT flag it — the
  bimodal mix of small offices (~15-19 m2) and large studios/classrooms
  (~50-65 m2) inflates the IQR beyond usefulness here. Neither rule flags
  room **R110** (a 3.0 m2 "Closet" mislabeled as a room, z=-1.28 — not
  extreme enough by either measure because several genuine small offices
  sit nearby in the distribution). Use this to teach: outlier rules are
  tools, not verdicts — R110 is a real data-quality question (should a
  closet be in a room schedule at all?), and R309's status depends on which
  rule you trust and why.

**Groupby (Week 5) — the headline finding for the whole Weeks 4-7 arc:**
```
df.groupby("zone").agg(mean_energy=("energy_kwh_m2_yr","mean"), mean_area=("area_m2","mean"), n=("room_id","count"))
          mean_energy   mean_area   n
North        64.25        40.975   12
South       115.68        38.25    12
```
South-zone rooms use roughly **80% more energy per square meter** than
North-zone rooms, despite very similar average areas and identical room
counts — a genuine, dramatic, architecturally meaningful finding (plausible
story: south-facing exposure driving higher cooling/solar loads) worth
carrying through Week 5 (the grouping finding itself), Week 6 (visualize it),
and Week 7 (map it) as one continuous narrative, exactly modeling what
Project 1 asks students to do with their own dataset.

**Spatial (Week 7) — verified real geopandas behavior:**
- Measuring distance directly on the geographic CRS (EPSG:4326, degrees) for
  two points 8.0 m apart gives `0.000098` — a real, verified demonstration
  of why you cannot compute physical distance/area in a geographic CRS.
- Reprojecting to EPSG:32618 (UTM zone 18N — a real, correct projected CRS
  choice for the Syracuse, NY area) and re-measuring the same two points
  gives `8.010` m against a known ground truth of `8.000` m (the small
  difference is real projection distortion, not an error — worth naming).
- The two zone polygons in `zone_footprints.geojson` are each a simple
  24m x 10m rectangle (240 m2 by construction). Reprojected to EPSG:32618
  and measured with `.geometry.area`, both compute to approximately
  **239.74 m2** — matching the known 240 m2 ground truth to within ~0.1%,
  a good, honest "even a correct projected CRS has some distortion" note.
- A room-level point-in-polygon join of the rooms onto the two zone polygons
  is verified CORRECT: all 24 rooms fall strictly inside the polygon named by
  their own `zone` column, with a minimum clearance of 1.0 m from any polygon
  edge (no room sits on a boundary, so nothing returns NaN). Verified with:
  ```python
  rooms_gdf = gpd.GeoDataFrame(rooms, geometry=gpd.points_from_xy(rooms['lon'], rooms['lat']), crs='EPSG:4326')
  joined = gpd.sjoin(rooms_gdf, zones, how='left', predicate='within')
  (joined['zone_left'] == joined['zone_right']).sum()   # -> 24 of 24
  ```
  This does not change the recommended exercise below — that recommendation is
  about stacked-floor duplication, not about coordinate correctness — but it
  does mean a student who applies the Week 7 spatial workflow to this dataset
  on their own gets right answers rather than silently inverted ones.
- The recommended Week 7 spatial exercise: merge (a plain pandas attribute
  join, reusing the Week 5 groupby summary above) the zone-level energy/area
  summary onto `zone_footprints.geojson` by the shared `"zone"` key, then
  produce a 2-polygon choropleth colored by `mean_energy_kwh_m2_yr` — this
  is a clean, real, small example of exactly the workflow Project 1's
  Part IV asks students to build on their own site data. Avoid a room-level
  point-in-polygon or point-to-point spatial join exercise with this
  particular dataset — rooms are stacked at identical (x_m, y_m) across
  floors 1-3 (deliberately, to represent a real multi-story building
  footprint), so a room-to-room proximity join produces confusing
  same-location matches across floors; the zone-level join above avoids
  this entirely and is the intended exercise.
