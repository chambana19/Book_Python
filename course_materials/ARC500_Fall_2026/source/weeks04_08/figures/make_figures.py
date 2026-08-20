# -*- coding: utf-8 -*-
"""Generate every figure the Weeks 4-8 decks embed.

Run from the activated course environment:  python make_figures.py

Each figure is built from the REAL shared dataset (../data/building_rooms.csv,
../data/zone_footprints.geojson) using the SAME operations the week's handout teaches --
not decorative stand-ins. If a number on a slide changes, re-running this regenerates the
matching picture, so the two cannot drift apart.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "_design"))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from figstyle import apply_style, save, ACCENT, RED, GREEN, MUTED, INK, AMBER, ACCENT_DEEP

apply_style()

DATA = HERE.parent / "data"
rooms = pd.read_csv(DATA / "building_rooms.csv")
cleaned = rooms[rooms["energy_kwh_m2_yr"].notna()].copy()
cleaned["area_ft2"] = np.round(np.array(cleaned["area_m2"]) * 10.7639, 1)
cleaned["energy_kwh_yr"] = (cleaned["energy_kwh_m2_yr"] * cleaned["area_m2"]).round(0)

print("Weeks 4-8 figures")


# ---------------------------------------------------------------- Week 4
def w04_missingness():
    """Where the gaps are — the .isna().sum() interview, as a picture."""
    counts = rooms.isna().sum()
    counts = counts[counts.index != "geometry"]
    fig, ax = plt.subplots()
    colors = [RED if v > 0 else ACCENT for v in counts.values]
    ax.barh(counts.index[::-1], counts.values[::-1], color=colors[::-1])
    ax.set_xlabel("missing values (of 24 rooms)")
    ax.set_xlim(0, 2)
    ax.set_xticks([0, 1, 2])
    ax.grid(axis="y", visible=False)
    for i, v in enumerate(counts.values[::-1]):
        if v:
            ax.text(v + 0.05, i, f"{v}", va="center", color=RED, fontweight="bold")
    return save(fig, HERE, "w04_missingness.png")


def w04_scatter_area_energy():
    """The exact scatter the Week 4 handout builds in cell [7]."""
    fig, ax = plt.subplots()
    ax.scatter(cleaned["area_ft2"], cleaned["energy_kwh_m2_yr"], color=ACCENT, s=70,
               edgecolor="white", linewidth=1.2, zorder=3)
    r306 = cleaned.loc[cleaned["room_id"] == "R306"].iloc[0]
    ax.annotate("R306 (Server, 8.0 m2)\n410 kWh/m2/yr",
                xy=(r306["area_ft2"], r306["energy_kwh_m2_yr"]),
                xytext=(320, 330), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.6))
    ax.set_xlabel("area_ft2")
    ax.set_ylabel("energy_kwh_m2_yr")
    return save(fig, HERE, "w04_scatter_area_energy.png")


def w04_intensity_vs_total():
    """Why a derived column changes the question: intensity vs. annual total."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 4.2))
    top_i = cleaned.nlargest(6, "energy_kwh_m2_yr")
    a1.barh(top_i["room_id"][::-1], top_i["energy_kwh_m2_yr"][::-1],
            color=[RED] + [ACCENT] * 5)
    a1.set_title("by intensity (kWh/m2/yr)")
    a1.set_xlabel("energy_kwh_m2_yr")
    a1.grid(axis="y", visible=False)

    top_t = cleaned.nlargest(6, "energy_kwh_yr")
    cols = [RED if r == "R306" else ACCENT for r in top_t["room_id"]]
    a2.barh(top_t["room_id"][::-1], top_t["energy_kwh_yr"][::-1], color=cols[::-1])
    a2.set_title("by annual total (kWh/yr)")
    a2.set_xlabel("energy_kwh_yr")
    a2.grid(axis="y", visible=False)
    return save(fig, HERE, "w04_intensity_vs_total.png")


# ---------------------------------------------------------------- Week 5
def w05_zone_means():
    """The headline Week 5 finding, as a comparison chart."""
    zs = cleaned.groupby("zone").agg(mean_energy=("energy_kwh_m2_yr", "mean")).reset_index()
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    bars = ax.bar(zs["zone"], zs["mean_energy"], color=[ACCENT, RED], width=0.5)
    for b, v in zip(bars, zs["mean_energy"]):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.2f}",
                ha="center", fontweight="bold", color=INK)
    ax.set_ylabel("mean energy_kwh_m2_yr")
    ax.set_ylim(0, 140)
    ax.grid(axis="x", visible=False)
    return save(fig, HERE, "w05_zone_means.png")


def w05_iqr_fences():
    """The IQR rule drawn on the actual distribution, with both flagged rooms."""
    v = cleaned["energy_kwh_m2_yr"]
    q1, q3 = v.quantile(0.25), v.quantile(0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    flagged_ids = {"R306", "R110"}
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    ax.axvspan(q1, q3, color=ACCENT, alpha=0.10, zorder=1)
    # One row of points, no jitter: jitter reads as extra observations that do not exist.
    keep = cleaned[~cleaned["room_id"].isin(flagged_ids)]
    ax.scatter(keep["energy_kwh_m2_yr"], np.zeros(len(keep)), color=ACCENT, s=70,
               edgecolor="white", linewidth=1.0, zorder=3)
    for x, lbl in [(low, f"low fence  {low:.2f}"), (high, f"high fence  {high:.2f}")]:
        ax.axvline(x, color=AMBER, linestyle="--", linewidth=1.8, zorder=2)
        ax.text(x, 0.55, lbl, ha="center", va="bottom", color=AMBER, fontsize=11, fontweight="bold")
    ax.annotate("", xy=(q1, -0.42), xytext=(q3, -0.42),
                arrowprops=dict(arrowstyle="<->", color=MUTED, linewidth=1.2))
    ax.text((q1 + q3) / 2, -0.62, f"IQR   Q1={q1:.2f}   Q3={q3:.2f}",
            ha="center", va="top", color=MUTED, fontsize=11)
    for rid, side in [("R110", -1), ("R306", 1)]:
        r = cleaned.loc[cleaned["room_id"] == rid].iloc[0]
        ax.scatter([r["energy_kwh_m2_yr"]], [0], color=RED, s=150, zorder=4,
                   edgecolor="white", linewidth=1.4)
        ax.annotate(f"{rid}  {r['energy_kwh_m2_yr']:.0f}",
                    xy=(r["energy_kwh_m2_yr"], 0), xytext=(r["energy_kwh_m2_yr"], 0.30),
                    ha="center", color=RED, fontweight="bold", fontsize=12)
    ax.set_yticks([])
    ax.set_ylim(-0.95, 0.95)
    ax.set_xlim(-25, 445)
    ax.set_xlabel("energy_kwh_m2_yr")
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    return save(fig, HERE, "w05_iqr_fences.png")


def w05_rules_disagree():
    """IQR and z-score reaching different verdicts on area_m2 — the honest hard case."""
    a = cleaned["area_m2"]
    q1, q3 = a.quantile(0.25), a.quantile(0.75)
    iqr = q3 - q1
    hi = q3 + 1.5 * iqr
    z = (a - a.mean()) / a.std()
    fig, ax = plt.subplots()
    ax.scatter(a, z, color=ACCENT, s=65, edgecolor="white", zorder=3)
    ax.axhline(2, color=GREEN, linestyle="--", linewidth=1.8)
    ax.text(3, 2.06, "z-score rule: |z| > 2", color=GREEN, fontsize=11)
    ax.axvline(hi, color=AMBER, linestyle="--", linewidth=1.8)
    ax.text(hi - 2, -1.35, f"IQR high fence {hi:.2f}", color=AMBER, fontsize=11,
            rotation=90, va="bottom", ha="right")
    r309 = cleaned.loc[cleaned["room_id"] == "R309"].iloc[0]
    z309 = (r309["area_m2"] - a.mean()) / a.std()
    ax.annotate("R309: z flags it,\nIQR does not",
                xy=(r309["area_m2"], z309), xytext=(72, 1.15), color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.6))
    ax.set_xlabel("area_m2")
    ax.set_ylabel("z-score of area_m2")
    return save(fig, HERE, "w05_rules_disagree.png")


# ---------------------------------------------------------------- Week 6
def w06_three_encodings():
    """Distribution / comparison / relationship — one question each, side by side."""
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.5))
    a, b, c = axes
    a.hist(cleaned["energy_kwh_m2_yr"], bins=8, color=ACCENT, edgecolor="white")
    a.set_title("distribution")
    a.set_xlabel("energy_kwh_m2_yr")
    a.set_ylabel("rooms")

    zs = cleaned.groupby("zone")["energy_kwh_m2_yr"].mean()
    b.bar(zs.index, zs.values, color=[ACCENT, RED], width=0.5)
    b.set_title("comparison")
    b.set_ylabel("mean energy_kwh_m2_yr")
    b.grid(axis="x", visible=False)

    for zone, col in [("North", ACCENT), ("South", RED)]:
        sub = cleaned[cleaned["zone"] == zone]
        c.scatter(sub["area_m2"], sub["energy_kwh_m2_yr"], color=col, s=45,
                  edgecolor="white", label=zone)
    c.set_title("relationship")
    c.set_xlabel("area_m2")
    c.legend()
    return save(fig, HERE, "w06_three_encodings.png")


def w06_animation_frames():
    """Four frames of the progressive-reveal animation, laid out as a strip."""
    plot_df = cleaned.sort_values("energy_kwh_m2_yr").reset_index(drop=True)
    n = len(plot_df)
    picks = [3, 10, 17, n - 1]
    fig, axes = plt.subplots(1, 4, figsize=(10.2, 3.0), sharey=True)
    for ax, frame in zip(axes, picks):
        shown = plot_df.iloc[: frame + 1]
        cols = [RED if r == "R306" else ACCENT for r in shown["room_id"]]
        ax.bar(range(len(shown)), shown["energy_kwh_m2_yr"], color=cols)
        ax.set_xlim(-0.5, n - 0.5)
        ax.set_ylim(0, 430)
        ax.set_title(f"frame {frame + 1} of {n}", fontsize=12)
        ax.set_xticks([])
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel("energy_kwh_m2_yr")
    return save(fig, HERE, "w06_animation_frames.png")


# ---------------------------------------------------------------- Week 7
def w07_crs_matters():
    """The same two zones measured in degrees vs. metres — why CRS is not cosmetic."""
    import geopandas as gpd
    zones = gpd.read_file(DATA / "zone_footprints.geojson")
    zs = cleaned.groupby("zone").agg(mean_energy_kwh_m2_yr=("energy_kwh_m2_yr", "mean")).reset_index()
    merged = zones.merge(zs, on="zone", how="left")
    utm = merged.to_crs("EPSG:32618")

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 4.0))
    merged.plot(ax=a1, facecolor=ACCENT, alpha=0.35, edgecolor=INK, linewidth=1.4)
    a1.set_title("EPSG:4326 — degrees")
    a1.set_xlabel("longitude")
    a1.set_ylabel("latitude")
    a1.ticklabel_format(useOffset=False, style="plain")
    a1.tick_params(labelsize=9, labelrotation=30)
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        bad = merged.geometry.area.iloc[0]
    a1.text(0.5, -0.34, f".area -> {bad:.2e} (square degrees)", transform=a1.transAxes,
            ha="center", color=RED, fontsize=11, fontweight="bold")

    utm.plot(ax=a2, facecolor=GREEN, alpha=0.35, edgecolor=INK, linewidth=1.4)
    a2.set_title("EPSG:32618 — metres")
    a2.set_xlabel("easting (m)")
    a2.set_ylabel("northing (m)")
    a2.ticklabel_format(useOffset=False, style="plain")
    a2.tick_params(labelsize=9, labelrotation=30)
    a2.text(0.5, -0.34, f".area -> {utm.geometry.area.iloc[0]:.2f} m2 (truth: 240)",
            transform=a2.transAxes, ha="center", color=GREEN, fontsize=11, fontweight="bold")
    return save(fig, HERE, "w07_crs_matters.png")


def w07_choropleth():
    """The Week 7 deliverable map, exactly as the handout builds it."""
    import geopandas as gpd
    zones = gpd.read_file(DATA / "zone_footprints.geojson")
    zs = cleaned.groupby("zone").agg(mean_energy_kwh_m2_yr=("energy_kwh_m2_yr", "mean")).reset_index()
    utm = zones.merge(zs, on="zone", how="left").to_crs("EPSG:32618")
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    utm.plot(column="mean_energy_kwh_m2_yr", cmap="OrRd", edgecolor="black",
             linewidth=1.2, legend=True,
             legend_kwds={"label": "Mean energy use intensity (kWh/m2/yr)"}, ax=ax)
    for _, row in utm.iterrows():
        c = row.geometry.centroid
        ax.annotate(f"{row['zone']}\n{row['mean_energy_kwh_m2_yr']:.2f}",
                    xy=(c.x, c.y), ha="center", va="center", fontweight="bold", fontsize=12)
    ax.set_xlabel("Easting (m, EPSG:32618)")
    ax.set_ylabel("Northing (m, EPSG:32618)")
    ax.ticklabel_format(useOffset=False, style="plain")
    ax.tick_params(labelsize=9, labelrotation=30)
    ax.grid(False)
    return save(fig, HERE, "w07_choropleth.png")


for fn in [w04_missingness, w04_scatter_area_energy, w04_intensity_vs_total,
           w05_zone_means, w05_iqr_fences, w05_rules_disagree,
           w06_three_encodings, w06_animation_frames,
           w07_crs_matters, w07_choropleth]:
    fn()

print("done.")


# ---------------------------------------------------------------- concept diagrams
from figstyle import concept_fig, box, arrow, PANEL


def w05_split_apply_combine():
    """The grammar behind groupby(), drawn rather than described."""
    fig, ax = concept_fig(width=8.0, height=4.0)
    for x, lbl in [(30, "SPLIT"), (61, "APPLY"), (87, "COMBINE")]:
        ax.text(x, 95, lbl, color=MUTED, fontsize=12, fontweight="bold", ha="center")
    box(ax, 10, 55, 17, 20, "24 rooms\none table", face="white", edge=MUTED, fontsize=12)
    for yy, zone, col in [(76, "North\n12 rooms", ACCENT), (34, "South\n12 rooms", RED)]:
        box(ax, 36, yy, 20, 18, zone, face=PANEL, edge=col, fontsize=12)
        arrow(ax, 19, 55 + (yy - 55) * 0.20, 26, yy)
        box(ax, 62, yy, 18, 15, ".mean()", face="white", edge=col, fontsize=12)
        arrow(ax, 46, yy, 53, yy)
        arrow(ax, 71, yy, 77, 55 + (yy - 55) * 0.22)
    box(ax, 88, 55, 20, 24, "one row\nper zone", face=PANEL, edge=GREEN, fontsize=12)
    return save(fig, HERE, "w05_split_apply_combine.png")


def w04_trustworthiness_interview():
    """The five questions of the Week 4 interview, as one sequence."""
    fig, ax = concept_fig(width=8.0, height=3.6)
    steps = [("shape", "how big?"), (".dtypes", "what types?"), (".head()", "what rows?"),
             (".info()", "all at once"), (".isna()", "gaps where?")]
    for i, (call, q) in enumerate(steps):
        x = 11 + i * 19.5
        box(ax, x, 62, 18, 20, f"{call}\n\n{q}", face="white", edge=ACCENT, fontsize=12)
        if i:
            arrow(ax, x - 18, 62, x - 9.5, 62)
    box(ax, 50, 20, 62, 15, "only now: filter, derive, export", face=PANEL, edge=GREEN)
    # Descend from the END of the sequence, not from whichever box happens to sit at the
    # centre -- otherwise the arrow reads as "after .head()" instead of "after all five".
    arrow(ax, 89, 52, 74, 28, color=GREEN)
    return save(fig, HERE, "w04_trustworthiness_interview.png")


for fn in [w05_split_apply_combine, w04_trustworthiness_interview]:
    fn()
