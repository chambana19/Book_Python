"""Combine structured, semi-structured, and unstructured building data.

Three sources need three different kinds of work, and all three converge on one
rectangular feature table: the shape every later chapter consumes.
"""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Structured: the file carries the schema, so validate it and move on.
readings = pd.DataFrame(
    {
        "timestamp": pd.to_datetime(
            [
                "2026-03-01 08:00",
                "2026-03-01 09:00",
                "2026-03-01 10:00",
                "2026-03-01 11:00",
                "2026-03-01 12:00",
            ]
        ),
        "room_id": ["R101", "R101", "R101", "R101", "R101"],
        "temp_c": [20.4, 21.1, 24.8, 22.0, None],
        "co2_ppm": [612, 705, 1180, 890, 830],
    }
)

EXPECTED = {
    "timestamp": "datetime",
    "room_id": "string",
    "temp_c": "number",
    "co2_ppm": "number",
}
CHECKS = {
    "datetime": pd.api.types.is_datetime64_any_dtype,
    "string": lambda column: (
        pd.api.types.is_string_dtype(column) or pd.api.types.is_object_dtype(column)
    ),
    "number": pd.api.types.is_numeric_dtype,
}


def validate_schema(frame, expected):
    """Return a list of schema problems; an empty list means the frame passed."""
    problems = []
    for name, kind in expected.items():
        if name not in frame.columns:
            problems.append(f"missing column: {name}")
        elif not CHECKS[kind](frame[name]):
            problems.append(f"{name} is {frame[name].dtype}, expected {kind}")
    return problems


problems = validate_schema(readings, EXPECTED)
if problems:
    raise ValueError(f"sensor log failed validation: {problems}")

print("Structured source")
print(f"  shape {readings.shape}, missing values {int(readings.isna().sum().sum())}")
print(f"  schema problems: {problems}")

# 2. Semi-structured: self-describing but nested, so flatten to a stated grain.
asset = {
    "asset_id": "AHU-3",
    "location": {"building": "Link Hall", "floor": 2, "room": "M204"},
    "commissioned": "2019-06-14",
    "filters": [
        {"stage": 1, "type": "MERV8", "last_changed": "2026-01-10"},
        {"stage": 2, "type": "MERV13", "last_changed": "2025-11-02"},
    ],
}

filters = pd.json_normalize(
    asset,
    record_path="filters",
    meta=["asset_id", ["location", "building"]],
)

print("\nSemi-structured source")
print(f"  grain: one row per filter, shape {filters.shape}")
print(filters.to_string(index=False))

# 3a. Unstructured text: the vocabulary is the model, so it is stated here.
work_orders = [
    "Occupant reports room too warm all afternoon; VAV box not responding.",
    "Chilled water valve leaking near AHU-3, water on floor.",
    "Room too cold in the morning, occupants using space heaters.",
    "Filter change overdue; airflow reduced and room warm.",
]
VOCABULARY = ["warm", "cold", "leak", "filter", "valve", "airflow"]


def text_features(documents, vocabulary):
    """Return one row per document with a presence flag per vocabulary term."""
    rows = []
    for text in documents:
        tokens = re.findall(r"[a-z]+", text.lower())
        row = {
            f"has_{word}": int(any(token.startswith(word) for token in tokens))
            for word in vocabulary
        }
        row["word_count"] = len(tokens)
        rows.append(row)
    return pd.DataFrame(rows)


features = text_features(work_orders, VOCABULARY)
print("\nUnstructured text source")
print(f"  vocabulary: {VOCABULARY}")
print(f"  feature table shape {features.shape}")
print(features.to_string(index=False))

# 3b. Unstructured image: already an array, so reduce it to a few features.
rng = np.random.default_rng(7)
panel = np.zeros((48, 64, 3), dtype=np.int16)
panel[:, :, 0], panel[:, :, 1], panel[:, :, 2] = 40, 60, 90
rows, columns = np.ogrid[:48, :64]
hot_spot = ((rows - 14) ** 2 + (columns - 46) ** 2) < 90
panel[hot_spot] = [235, 175, 95]
panel = np.clip(panel + rng.integers(-8, 9, panel.shape), 0, 255).astype(np.uint8)

HOT_THRESHOLD = 140.0
grayscale = panel.mean(axis=2)
descriptor = {
    "mean_intensity": round(float(grayscale.mean()), 2),
    "max_intensity": round(float(grayscale.max()), 2),
    "hot_fraction": round(float((grayscale > HOT_THRESHOLD).mean()), 4),
}

print("\nUnstructured image source")
print(f"  array shape {panel.shape}, dtype {panel.dtype}")
print(f"  threshold {HOT_THRESHOLD} -> {descriptor}")

# 4. Converge: every path ends in the same rectangular shape.
combined = pd.DataFrame(
    [
        {
            "room_id": "R101",
            "mean_temp_c": round(float(readings["temp_c"].mean()), 2),
            "max_co2_ppm": int(readings["co2_ppm"].max()),
            "filter_stages": int(filters.shape[0]),
            "warm_reports": int(features["has_warm"].sum()),
            "hot_fraction": descriptor["hot_fraction"],
        }
    ]
)

print("\nConverged feature table")
print(combined.to_string(index=False))
print(f"  shape {combined.shape}")

# 5. Visualize the image path, which is the least obvious of the three.
fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.0), layout="constrained")
fig.suptitle(
    "From pixels to features: the unstructured path made visible",
    fontsize=14,
    weight="bold",
)

axes[0].imshow(panel)
axes[0].set(title="Synthetic thermal panel", xlabel="width: 64 pixels",
            ylabel="height: 48 pixels")
axes[0].set_xticks([0, 32, 63])
axes[0].set_yticks([0, 24, 47])

axes[1].imshow(grayscale, cmap="inferno")
axes[1].set(title="Mean of the three channels",
            xlabel=f"max intensity {descriptor['max_intensity']}")
axes[1].set_xticks([])
axes[1].set_yticks([])

axes[2].imshow(grayscale > HOT_THRESHOLD, cmap="gray")
axes[2].set(title=f"Above threshold {HOT_THRESHOLD:.0f}",
            xlabel=f"hot_fraction = {descriptor['hot_fraction']}")
axes[2].set_xticks([])
axes[2].set_yticks([])

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(output_folder / "building_data_pipeline.png", dpi=200, bbox_inches="tight")
plt.show()
plt.close(fig)
