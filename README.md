# Introduction to Programming with Python

This repository contains the LaTeX source for an independent-study Python
textbook covering programming foundations, algorithms, NumPy, pandas,
Matplotlib, structured and unstructured data handling, GeoPandas, numerical
optimization including gradient descent and metaheuristics, and machine
learning from regression through classification, model selection, and neural
networks. Compile `main.tex` in Overleaf or with a compatible LaTeX engine.

## Learning figures

The book includes source-code diagrams, Matplotlib results, dashboards, and
geospatial maps in `Figures/Generated`. The generated PDF files are used by
LaTeX; PNG companions make the outputs easy to preview on GitHub. The first
`geodatasets` run downloads and caches the referenced educational datasets.

To regenerate the figures from the repository root:

```powershell
python -m pip install -r requirements-figures.txt
python scripts/generate_book_figures.py
```

The script is deterministic and replaces the generated files with the same
named outputs.

## Runnable applications

The longer applications printed in Chapters 13--22 are also available as
complete scripts in `examples`. Run them from the repository root after
installing `requirements-figures.txt`:

```powershell
python examples/c13_building_performance_dashboard.py
python examples/c14_building_data_pipeline.py
python examples/c15_site_service_areas.py
python examples/c16_chicago_mapping.py
python examples/c17_search_algorithms.py
python examples/c18_daylight_energy_optimization.py
python examples/c19_building_energy_ml.py
python examples/c20_facade_optimization.py
python examples/c21_comfort_complaint_classification.py
python examples/c22_neural_network_comfort.py
```

Each script writes a high-resolution PNG to the ignored `study_figures`
folder. The Chapter 16 script may download its documented teaching datasets on
the first run.

## Accessibility

The source includes visible navigation, document-language metadata, Unicode
text mapping, descriptive figure captions, and color-independent chart cues.
Experimental structural PDF tagging is disabled in the standard build because
the current LaTeX tagging toolchain can conflict with the book's code listings
and boxed teaching environments. This keeps local and Overleaf builds reliable.

## Compile locally

With Tectonic installed:

```powershell
tectonic main.tex --outdir output/pdf --keep-logs
```

The finished textbook is written to `output/pdf/main.pdf`. Local build output
and Python dependency folders are excluded from Git.
