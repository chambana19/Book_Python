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

## Chapter 19: Gradient-Based and Metaheuristic Optimization

- Build the derivative and gradient as local slopes before showing any solver
  call, and check every analytic gradient against a central difference.
- Treat the learning rate as an empirical choice: show a rate that is too small,
  one that works, and one that oscillates without raising an error.
- Distinguish "the step became small" from "the loop ran out of iterations";
  only the first is convergence.
- Motivate metaheuristics with measured failure of a local method on a rugged
  objective, not with assertion.
- Implement simulated annealing, a genetic algorithm, and particle swarm from
  scratch, then map each to its SciPy equivalent.
- Compare every method at one shared evaluation budget against a random-search
  baseline, and report seeds and run-to-run spread.

## Chapter 20: Classification and Model Selection

- Open with class balance and a majority-class baseline so accuracy is
  discredited before any model is fitted.
- Name both errors in the language of the problem before selecting a metric.
- Keep preprocessing inside a `Pipeline` so cross-validation refits it per fold.
- Separate predicted probability, decision threshold, and predicted label.
- Use cross-validation for every comparison; open the test set once and report
  the cross-validated score beside it.
- Read validation curves for over- and underfitting, and treat `best_score_` as
  optimistically biased.
- Present permutation importance as reliance of the fitted model, never as
  causation, and check it against the known generating rule.

## Chapter 21: Neural Networks

- Present a network as the previous two chapters combined: gradient descent
  fits it, cross-validation selects it.
- Prove numerically that stacked linear layers collapse; do not assert it.
- Compare activations by their slope, not only their shape, so the vanishing
  gradient is visible rather than named.
- Derive backpropagation for one hidden layer and gradient-check it against
  finite differences before any training result is shown.
- Present feature scaling as mandatory, with the measured cost of omitting it.
- Benchmark the network against a linear model and a tree ensemble, and state
  plainly when the extra complexity is not repaid.

## Validation targets

- All companion scripts run from the repository root.
- Generated figures use labels plus line style, markers, or position rather
  than color alone.
- Local and Overleaf builds compile without experimental structural tagging;
  figures retain descriptive captions and color-independent visual cues.
- Chapter applications separate preparation, algorithm, verification,
  communication, and interpretation.
