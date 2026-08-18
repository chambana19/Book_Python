# Practical application scripts

These scripts accompany the long applications in Chapters 13--18. Each file
is self-contained and follows the same visible stages used in the textbook:
prepare data, calculate or transform, visualize, annotate, and export.

Install the project dependencies from the repository root:

```powershell
python -m pip install -r requirements-figures.txt
```

Then run one script at a time. Output is written to `study_figures` in the
repository root.

- `c13_building_performance_dashboard.py` creates a four-panel Matplotlib
  dashboard.
- `c14_site_service_areas.py` creates projected GeoPandas points and 400-meter
  buffers.
- `c15_chicago_mapping.py` retrieves teaching data, performs a spatial join,
  and combines a map with a ranked chart.
- `c16_search_algorithms.py` validates linear and binary search and compares
  operation growth.
- `c17_daylight_energy_optimization.py` compares an auditable grid search with
  bounded SciPy optimization.
- `c18_building_energy_ml.py` protects a test set, fits linear regression, and
  evaluates predictions against a baseline.
