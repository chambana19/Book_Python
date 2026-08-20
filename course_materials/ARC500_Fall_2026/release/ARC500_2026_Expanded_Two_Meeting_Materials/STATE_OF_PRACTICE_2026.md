# ARC 500 state of practice — Fall 2026

Reviewed: 2026-08-20

This guide keeps current professional and research connections visible without turning an introductory course into a survey of tools. The core course remains Python reasoning, trustworthy data, visual evidence, optimization, evaluated prediction, and bounded decision-making. The items below are optional horizon modules and next steps.

## Weeks 1–3: reproducible AI-assisted programming

Current practice is environment-first and test-first: one declared environment, a connected IDE/interpreter, relative paths, restart-and-run verification, and an AI-use record that distinguishes accepted, modified, rejected, and independently checked suggestions. Spyder 6 should connect to the shared external `arc500-f26` environment rather than receive ad-hoc installs inside a standalone internal console.

Primary references: [Spyder installation and environment guidance](https://docs.spyder-ide.org/current/installation.html), [Python control flow](https://docs.python.org/3/tutorial/controlflow.html).

## Weeks 4–5: typed analytical data and data contracts

CSV remains useful for small transparent exchanges, but current analytical systems increasingly use typed columnar storage and in-memory interchange. Apache Arrow defines a language-independent columnar memory format; Parquet stores typed columns efficiently. Neither replaces the evidence contract: row meaning, identifiers, units, null policy, provenance, and validation checks.

Built-environment data adds a semantic layer. IFC 4.3 is the open, vendor-neutral asset data model; IDS 1.0 expresses machine-checkable IFC information requirements; Brick 1.4 describes operational equipment, spaces, points, and relationships for portable building analytics. A DataFrame extracted from any of these is an analysis view, not the authority: retain stable identity, units, provenance, and validation results.

Primary references: [Apache Arrow overview](https://arrow.apache.org/overview/), [pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html), [buildingSMART IFC](https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/), [buildingSMART IDS](https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/), [Brick Schema](https://brickschema.org/).

## Week 6: accessible explanatory visualization

The professional direction is declarative and reproducible visual specification, direct annotation, accessible color use, and descriptions for complex images. Interactive or animated output is justified only when change, sequence, or exploration adds evidence. A static figure remains preferable when it answers the question more directly.

Primary references: [Matplotlib quick start](https://matplotlib.org/stable/users/explain/quick_start.html), [WCAG use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), [W3C complex images tutorial](https://www.w3.org/WAI/tutorials/images/complex/), [Vega-Lite](https://vega.github.io/vega-lite/).

## Week 7: open geospatial files and APIs

GeoParquet 1.1 specifies geometry encoding and geospatial metadata in Parquet, including CRS metadata and optional bounding-box coverage. OGC API standards provide modular, OpenAPI-based access to geospatial collections and features. These delivery mechanisms do not relax the core checks: geometry validity, CRS, axis order, extent, predicates, unmatched features, and projected measurement.

Primary references: [GeoParquet 1.1 specification](https://geoparquet.org/releases/v1.1.0/), [OGC API Features](https://ogcapi.ogc.org/features/overview.html).

## Weeks 9–12: optimization beyond one smooth objective

The course core covers sweeps, linear programming, bounded nonlinear minimization, discrete search, and metaheuristics. Current extensions should be selected from the decision structure:

- mixed-integer linear programming for counts, selections, and on/off choices;
- multiobjective optimization for a Pareto set when energy, carbon, cost, and quality conflict;
- Bayesian optimization when each simulation or experiment is expensive;
- mixed-variable and uncertainty-aware methods when continuous, categorical, and noisy inputs interact.

Modern methods still require an explicit problem, fair evaluation budget, baseline, feasibility audit, repeated seeds where relevant, and independent confirmation.

Primary references: [SciPy `milp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html), [pymoo multiobjective optimization](https://pymoo.org/), [BoTorch introduction](https://botorch.org/docs/introduction).

## Weeks 13–14: honest evaluation, calibration, and uncertainty

A current prediction workflow separates training, validation/policy selection, and an untouched final test. Classification decisions require both discrimination and probability calibration; threshold choice belongs to a stated consequence rule. Conformal prediction is an important horizon for model-agnostic prediction sets or intervals with coverage guarantees under stated assumptions. It does not make every subgroup or shifted case certain.

Primary references: [scikit-learn probability calibration](https://scikit-learn.org/stable/modules/calibration.html), [scikit-learn threshold tuning example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_tuned_decision_threshold.html), [Angelopoulos and Bates, conformal prediction tutorial](https://arxiv.org/abs/2107.07511).

## Week 15: simulation confirmation, benchmarking, and lifecycle risk

A surrogate and optimizer propose; a higher-fidelity simulator, measurement, or expert review confirms. EnergyPlus is a domain simulation engine for building and system performance. BOPTEST provides repeatable building-controls test cases, KPIs, baselines, and an API; it is not a universal truth model for every design decision. The NIST AI Risk Management Framework supplies a lifecycle vocabulary—govern, map, measure, and manage—for technical and organizational responsibility.

Primary references: [EnergyPlus](https://energyplus.net/), [IBPSA BOPTEST](https://github.com/ibpsa/project1-boptest), [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework).

## Update rule

Review this document before each semester. Prefer primary standards, official documentation, and peer-reviewed methods. Add a horizon item only when it changes what students should verify, disclose, compare, or refuse—not because a tool is fashionable.
