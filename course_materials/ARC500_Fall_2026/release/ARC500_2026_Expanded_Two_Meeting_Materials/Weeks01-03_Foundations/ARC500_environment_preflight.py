"""ARC 500 Fall 2026 environment preflight.

Run once from a system terminal and once from the Spyder console connected to
the ``arc500-f26`` environment. The script writes no course deliverables.
"""

from __future__ import annotations

import platform
import sys
from pathlib import Path


def require(condition: bool, message: str) -> None:
    """Raise a readable setup error when one preflight condition fails."""
    if not condition:
        raise RuntimeError(message)


print("ARC500 ENVIRONMENT PREFLIGHT")
print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Platform:", platform.platform())
print("Working folder:", Path.cwd())

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import shapely
import sklearn
from scipy.optimize import linprog
from shapely.geometry import Point
from sklearn.linear_model import LinearRegression

versions = {
    "NumPy": np.__version__,
    "pandas": pd.__version__,
    "Matplotlib": matplotlib.__version__,
    "SciPy": scipy.__version__,
    "scikit-learn": sklearn.__version__,
    "GeoPandas": gpd.__version__,
    "Shapely": shapely.__version__,
}
for package, version in versions.items():
    print(f"{package}: {version}")

values = np.array([12.0, 18.0, 30.0])
frame = pd.DataFrame({"area_m2": values})
require(float(frame["area_m2"].mean()) == 20.0, "NumPy/pandas check failed")

fig, ax = plt.subplots(figsize=(2.0, 1.2))
ax.plot([0, 1], [0, 1])
plt.close(fig)

point = gpd.GeoSeries([Point(-76.135, 43.039)], crs="EPSG:4326").to_crs("EPSG:32618")
require(point.crs is not None and point.crs.to_epsg() == 32618, "GeoPandas CRS check failed")

lp = linprog(c=[1.0, 1.0], bounds=[(1.0, None), (2.0, None)], method="highs")
require(lp.success and np.allclose(lp.x, [1.0, 2.0]), "SciPy linprog check failed")

X = np.array([[0.0], [1.0], [2.0]])
y = np.array([1.0, 3.0, 5.0])
prediction = LinearRegression().fit(X, y).predict([[3.0]])[0]
require(np.isclose(prediction, 7.0), "scikit-learn fit/predict check failed")

print("ARC500 PREFLIGHT: PASS")
