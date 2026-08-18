"""Compare gradient descent and three metaheuristics on one facade model.

The smooth objective shows how a learning rate controls descent. The rugged
variant shows why a local method is not enough, and four global searches are
compared under one shared evaluation budget with a random-search baseline.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import differential_evolution, minimize

BOUNDS = [(0.10, 0.70), (0.00, 1.20)]
LOWS = np.array([low for low, _ in BOUNDS])
HIGHS = np.array([high for _, high in BOUNDS])
SPANS = HIGHS - LOWS
EVALUATION_BUDGET = 4000


# 1. Define the model, its analytic gradient, and a rugged variant.
def facade_cost(decisions):
    """Return one modeled cost; lower is better."""
    window_ratio, shading_depth_m = decisions
    energy = (
        90
        + 180 * (window_ratio - 0.22) ** 2
        + 60 * (shading_depth_m - 0.45) ** 2
        - 70 * window_ratio * shading_depth_m
    )
    daylight_penalty = 500 * max(0.0, 0.25 - window_ratio) ** 2
    shading_cost = 40 * shading_depth_m**2
    return energy + daylight_penalty + shading_cost


def facade_gradient(decisions):
    """Return the two partial derivatives of facade_cost."""
    window_ratio, shading_depth_m = decisions
    d_ratio = (
        360 * (window_ratio - 0.22)
        - 70 * shading_depth_m
        - 1000 * max(0.0, 0.25 - window_ratio)
    )
    d_depth = (
        120 * (shading_depth_m - 0.45) - 70 * window_ratio + 80 * shading_depth_m
    )
    return np.array([d_ratio, d_depth])


def rugged_facade_cost(decisions):
    """The same model plus a manufacturing-increment ripple."""
    window_ratio, shading_depth_m = decisions
    ripple = (
        6.0
        * np.sin(12 * np.pi * window_ratio)
        * np.sin(8 * np.pi * shading_depth_m)
    )
    return facade_cost(decisions) + ripple


def numerical_gradient(function, point, step=1e-5):
    """Estimate a gradient with central differences."""
    point = np.asarray(point, dtype=float)
    gradient = np.zeros_like(point)
    for index in range(point.size):
        forward = point.copy()
        backward = point.copy()
        forward[index] += step
        backward[index] -= step
        gradient[index] = (function(forward) - function(backward)) / (2 * step)
    return gradient


# 2. Implement the local method.
def gradient_descent(cost, gradient_of, start, learning_rate,
                     iterations=400, tolerance=1e-6):
    """Fixed-step descent that projects every step back into the bounds."""
    point = np.clip(np.array(start, dtype=float), LOWS, HIGHS)
    values = [cost(point)]
    converged = False
    for _ in range(iterations):
        moved = np.clip(point - learning_rate * gradient_of(point), LOWS, HIGHS)
        values.append(cost(moved))
        step_size = np.linalg.norm(moved - point)
        point = moved
        if step_size < tolerance:
            converged = True
            break
    return point, np.array(values), converged


# 3. Implement the global searches. Each takes (cost, seed) and returns
#    (design, cost, best-so-far history) so they can be swapped in one loop.
def random_search(cost, seed=7, evaluations=EVALUATION_BUDGET):
    rng = np.random.default_rng(seed)
    best = None
    best_cost = np.inf
    history = []
    for _ in range(evaluations):
        candidate = LOWS + rng.random(2) * SPANS
        value = cost(candidate)
        if value < best_cost:
            best, best_cost = candidate, value
        history.append(best_cost)
    return best, best_cost, np.array(history)


def simulated_annealing(cost, seed=7, evaluations=EVALUATION_BUDGET,
                        start_temperature=20.0, cooling=0.999, step_fraction=0.12):
    rng = np.random.default_rng(seed)
    current = LOWS + rng.random(2) * SPANS
    current_cost = cost(current)
    best, best_cost = current.copy(), current_cost
    history = [best_cost]
    temperature = start_temperature

    for _ in range(evaluations - 1):
        candidate = np.clip(
            current + rng.normal(0, step_fraction * SPANS), LOWS, HIGHS
        )
        candidate_cost = cost(candidate)
        change = candidate_cost - current_cost
        if change <= 0 or rng.random() < np.exp(-change / temperature):
            current, current_cost = candidate, candidate_cost
            if current_cost < best_cost:
                best, best_cost = current.copy(), current_cost
        temperature *= cooling
        history.append(best_cost)

    return best, best_cost, np.array(history)


def genetic_algorithm(cost, seed=7, population_size=40, generations=100,
                      mutation_probability=0.25, mutation_fraction=0.08,
                      elite_count=2):
    rng = np.random.default_rng(seed)

    def tournament(population, scores):
        contenders = rng.choice(len(population), 3, replace=False)
        return population[contenders[scores[contenders].argmin()]]

    population = LOWS + rng.random((population_size, 2)) * SPANS
    scores = np.array([cost(row) for row in population])
    history = list(np.minimum.accumulate(scores))

    for _ in range(generations - 1):
        order = scores.argsort()
        population, scores = population[order], scores[order]

        children = [population[index].copy() for index in range(elite_count)]
        while len(children) < population_size:
            parent_a = tournament(population, scores)
            parent_b = tournament(population, scores)
            weight = rng.random()
            child = weight * parent_a + (1 - weight) * parent_b
            if rng.random() < mutation_probability:
                child = child + rng.normal(0, mutation_fraction * SPANS)
            children.append(np.clip(child, LOWS, HIGHS))

        population = np.array(children)
        scores = np.array([cost(row) for row in population])
        history.extend(np.minimum(np.minimum.accumulate(scores), history[-1]))

    best_index = scores.argmin()
    return population[best_index], scores[best_index], np.array(history)


def particle_swarm(cost, seed=7, particle_count=30, iterations=134,
                   inertia=0.72, cognitive=1.5, social=1.5):
    rng = np.random.default_rng(seed)
    positions = LOWS + rng.random((particle_count, 2)) * SPANS
    velocities = rng.normal(0, 0.08, (particle_count, 2)) * SPANS

    personal_best = positions.copy()
    personal_cost = np.array([cost(row) for row in positions])
    global_best = personal_best[personal_cost.argmin()].copy()
    global_cost = personal_cost.min()
    history = list(np.minimum.accumulate(personal_cost))

    for _ in range(iterations - 1):
        toward_personal = rng.random((particle_count, 2))
        toward_global = rng.random((particle_count, 2))
        velocities = (
            inertia * velocities
            + cognitive * toward_personal * (personal_best - positions)
            + social * toward_global * (global_best - positions)
        )
        positions = np.clip(positions + velocities, LOWS, HIGHS)

        scores = np.array([cost(row) for row in positions])
        improved = scores < personal_cost
        personal_best[improved] = positions[improved]
        personal_cost[improved] = scores[improved]
        if personal_cost.min() < global_cost:
            global_best = personal_best[personal_cost.argmin()].copy()
            global_cost = personal_cost.min()

        history.extend(np.minimum(np.minimum.accumulate(scores), history[-1]))

    return global_best, global_cost, np.array(history)


# 4. Check the analytic gradient before relying on it.
probe = [0.55, 0.90]
if not np.allclose(facade_gradient(probe), numerical_gradient(facade_cost, probe)):
    raise ValueError("Analytic gradient disagrees with the finite-difference estimate")

# 5. Study the learning rate on the smooth objective.
START = [0.65, 0.60]
print("Smooth objective, projected gradient descent from", START)
for rate in (0.0005, 0.0025, 0.0060):
    design, values, converged = gradient_descent(
        facade_cost, facade_gradient, START, rate
    )
    status = "converged" if converged else "hit the iteration limit"
    print(f"  rate={rate:<7} steps={len(values) - 1:>4} cost={values[-1]:8.4f} {status}")

reference = minimize(
    facade_cost, x0=START, jac=facade_gradient, bounds=BOUNDS, method="L-BFGS-B"
)
print(f"  L-BFGS-B with jac: cost={reference.fun:.4f} after {reference.nfev} evaluations")

# 6. Show that a local method is not enough on the rugged objective.
local_design, local_values, local_converged = gradient_descent(
    rugged_facade_cost,
    lambda point: numerical_gradient(rugged_facade_cost, point),
    START,
    0.0025,
)
print("\nRugged objective")
print(f"  gradient descent stops at cost {local_values[-1]:.4f} "
      f"(converged={local_converged})")

# 7. Run every global search on the same budget and verify each result.
searches = {
    "random search": random_search,
    "simulated annealing": simulated_annealing,
    "genetic algorithm": genetic_algorithm,
    "particle swarm": particle_swarm,
}

results = {}
for name, search in searches.items():
    design, cost, history = search(rugged_facade_cost, seed=7)

    if not np.all((design >= LOWS) & (design <= HIGHS)):
        raise ValueError(f"{name} returned an infeasible design")
    if abs(rugged_facade_cost(design) - cost) > 1e-9:
        raise ValueError(f"{name} reported a cost it cannot reproduce")

    results[name] = (design, cost, history)

baseline_cost = results["random search"][1]
print(f"  budget: about {EVALUATION_BUDGET} objective evaluations each, seed 7")
for name, (design, cost, _) in sorted(results.items(), key=lambda item: item[1][1]):
    print(f"  {name:<20} cost={cost:8.4f} vs random search {baseline_cost - cost:+.4f} "
          f"ratio={design[0]:.3f} depth={design[1]:.3f} m")

library = differential_evolution(rugged_facade_cost, bounds=BOUNDS, seed=7)
print(f"  {'differential_evolution':<20} cost={library.fun:8.4f} "
      f"after {library.nfev} evaluations")

# 8. Report run-to-run stability rather than one lucky seed.
print("\nStability over seeds 1 to 8")
for name, search in searches.items():
    costs = [search(rugged_facade_cost, seed=seed)[1] for seed in range(1, 9)]
    print(f"  {name:<20} best={min(costs):.4f} worst={max(costs):.4f} "
          f"mean={np.mean(costs):.4f}")

# 9. Plot the convergence comparison.
styles = {
    "random search": ("0.35", ":"),
    "simulated annealing": ("tab:orange", "--"),
    "genetic algorithm": ("tab:blue", "-"),
    "particle swarm": ("tab:green", "-."),
}

fig, ax = plt.subplots(figsize=(8.4, 5.0), layout="constrained")
for name, (color, linestyle) in styles.items():
    history = results[name][2]
    ax.plot(
        np.arange(1, len(history) + 1),
        history,
        color=color,
        linestyle=linestyle,
        linewidth=1.9,
        label=f"{name}: {results[name][1]:.2f}",
    )
ax.axhline(
    local_values[-1],
    color="firebrick",
    linewidth=1.3,
    label=f"gradient descent: {local_values[-1]:.2f}",
)
ax.set(
    title="Best cost found per evaluation budget (rugged facade objective)",
    xlabel="Objective evaluations (log scale)",
    ylabel="Best cost so far (lower is better)",
    xscale="log",
)
ax.grid(alpha=0.2, which="both")
ax.legend()

output_folder = Path("study_figures")
output_folder.mkdir(exist_ok=True)
fig.savefig(
    output_folder / "facade_optimization_comparison.png", dpi=200, bbox_inches="tight"
)
plt.show()
plt.close(fig)
