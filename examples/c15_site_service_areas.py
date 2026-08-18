"""Create the Chapter 15 projected site-service map."""

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


# 1. Store attributes and source coordinates.
sites = pd.DataFrame(
    {
        "name": ["Main Hall", "Design Studio", "Transit Stop", "Library"],
        "longitude": [-76.1355, -76.1318, -76.1372, -76.1286],
        "latitude": [43.0386, 43.0371, 43.0410, 43.0395],
    }
)

# 2. Create point geometry in the source CRS.
points = gpd.GeoDataFrame(
    sites,
    geometry=gpd.points_from_xy(sites["longitude"], sites["latitude"]),
    crs="EPSG:4326",
)

# 3. Transform to a meter-based CRS before measuring.
points = points.to_crs("EPSG:32618")

# 4. Build a polygon GeoDataFrame from 400 m buffers.
service_areas = gpd.GeoDataFrame(
    points[["name"]].copy(),
    geometry=points.buffer(400),
    crs=points.crs,
)

# 5. Draw polygons first and points second.
fig, ax = plt.subplots(figsize=(7.4, 5.2), layout="constrained")
service_areas.plot(
    ax=ax,
    color="tab:blue",
    alpha=0.16,
    edgecolor="tab:blue",
    linewidth=1.2,
)
points.plot(
    ax=ax,
    color="tab:orange",
    edgecolor="black",
    markersize=48,
    zorder=3,
)

# 6. Label each point using its projected x and y coordinates.
for row in points.itertuples():
    ax.annotate(
        row.name,
        (row.geometry.x, row.geometry.y),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8,
    )

# 7. Add map context and export.
ax.set(
    title="Four 400 m site-service areas",
    xlabel="Easting (m), UTM zone 18N",
    ylabel="Northing (m), UTM zone 18N",
)
ax.set_aspect("equal")
ax.grid(alpha=0.18)

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "site_service_areas.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)
