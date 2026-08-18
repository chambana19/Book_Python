# Part VI Revision Guide

Part VI extends programming syntax into foundational computational methods.

## Chapter 16: Algorithmic Thinking and Efficiency

- Begin with contracts, edge cases, traces, and invariants.
- Compare linear and binary search under the same specification.
- Introduce Big-O as growth, not stopwatch time.
- Use educational sorting to expose nested-loop reasoning while directing
  applications to Python's stable `sorted()` implementation.

## Chapter 17: Numerical Optimization with SciPy

- Separate decision variables, objective, bounds, data, and validation.
- Establish a transparent grid-search baseline before a numerical solver.
- Inspect complete result objects and verify feasibility and nearby behavior.
- Treat every optimum as conditional on model assumptions and sensitivity.

## Chapter 18: Machine Learning Foundations

- Choose regression, classification, or clustering from the required output.
- Protect test data before preprocessing or fitting.
- Compare every model with a simple training-only baseline.
- Pair metrics with diagnostic plots and document leakage, distribution shift,
  intended use, and prohibited claims.

## Validation targets

- All companion scripts run from the repository root.
- Generated figures use labels plus line style, markers, or position rather
  than color alone.
- Local and Overleaf builds compile without experimental structural tagging;
  figures retain descriptive captions and color-independent visual cues.
- Chapter applications separate preparation, algorithm, verification,
  communication, and interpretation.
