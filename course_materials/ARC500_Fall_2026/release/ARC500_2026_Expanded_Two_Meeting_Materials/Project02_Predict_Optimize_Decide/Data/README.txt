ARC 500 PROJECT 2 DATA

CANONICAL FILE
radley_portfolio_envelope.csv

- 140 synthetic course facade alternatives, one alternative per row.
- Same 140 records and schema used in the Week 13, Week 14, and Week 15 handouts.
- Identifier: variant_id.
- Numeric design features and units:
    wwr             window-to-wall ratio, dimensionless
    shade_m         exterior shade depth, metres
    glazing_shgc    solar heat-gain coefficient, dimensionless
    compactness     course compactness index, dimensionless
- Context-only categorical field: orientation (N/E/S/W).
- Continuous target: eui_kwh_m2yr, kWh/m2/year.
- Reporting-only derived field: est_annual_cost_index. It is intentionally highly
  correlated with EUI and MUST NOT be used as a predictor.
- Binary course label: meets_code = 1 when eui_kwh_m2yr <= 27.0, else 0.

PROVENANCE AND LIMITS

This is a synthetic teaching dataset, not measured Radley Hall performance and not a
calibrated EnergyPlus model. It supports practice with evaluation, optimization, and
audit trails; it cannot support a professional building-performance claim. Keep the
original file unchanged and record any approved replacement dataset and schema mapping.

LEGACY FILE
ARC500_facade_performance.csv is a 40-row, two-feature miniature retained only for
backward reference. The 2026 Project 2 starters do not load it. Do not mix its
alternative_id/eui_kwh_m2 schema or <=94 label with the canonical Week 13–15 model.
