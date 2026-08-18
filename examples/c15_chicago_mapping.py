"""Create the Chapter 15 Chicago spatial-join application."""

from pathlib import Path

import geopandas as gpd
import geodatasets
import matplotlib.pyplot as plt


# 1. Retrieve and load the two documented layers.
community_path = geodatasets.get_path("geoda.chicago_commpop")
grocery_path = geodatasets.get_path("geoda.groceries")

chicago = gpd.read_file(community_path)
groceries = gpd.read_file(grocery_path)

# 2. Inspect the minimum assumptions used later.
required_columns = {"community", "POP2010", "geometry"}
missing = required_columns.difference(chicago.columns)
if missing:
    raise ValueError(f"Missing Chicago columns: {sorted(missing)}")
if chicago.crs is None or groceries.crs is None:
    raise ValueError("Both layers must have a CRS")

# 3. Align the layers in a projected Chicago-area CRS.
chicago = chicago.to_crs("EPSG:26916")
groceries = groceries.to_crs(chicago.crs)

# 4. Attach a community name to each grocery point.
joined = gpd.sjoin(
    groceries,
    chicago[["community", "geometry"]],
    how="left",
    predicate="within",
)

# 5. Calculate the ten largest mapped-location counts.
top_counts = (
    joined.dropna(subset=["community"])
    .groupby("community")
    .size()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

# 6. Coordinate a map and a comparison chart.
fig, axes = plt.subplots(
    1,
    2,
    figsize=(10.8, 5.4),
    layout="constrained",
)

chicago.plot(
    column="POP2010",
    cmap="Blues",
    legend=True,
    edgecolor="white",
    linewidth=0.35,
    legend_kwds={"label": "Population in 2010", "shrink": 0.72},
    ax=axes[0],
)
groceries.plot(
    ax=axes[0],
    color="tab:orange",
    edgecolor="black",
    linewidth=0.25,
    markersize=9,
    zorder=3,
)
axes[0].set_title("Population and grocery locations")
axes[0].set_axis_off()

top_counts.plot.barh(ax=axes[1], color="tab:blue")
axes[1].set(
    title="Communities with the most mapped groceries",
    xlabel="Mapped grocery locations",
    ylabel="Community",
)
axes[1].grid(axis="x", alpha=0.2)

# 7. Record the source and export the complete Figure.
fig.text(
    0.5,
    0.01,
    "Source: GeoDa Center datasets distributed through geodatasets",
    ha="center",
    fontsize=8,
)
output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "chicago_population_groceries.png",
    dpi=200,
    bbox_inches="tight",
)
plt.show()
plt.close(fig)
