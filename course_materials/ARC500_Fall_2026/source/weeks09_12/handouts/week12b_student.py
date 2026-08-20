# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 12 studio · Genetic algorithm vs. brute force on a discrete panel-assignment problem
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week12 module folder. No data file is needed this week -
     the 6-bay, 6-panel problem is generated entirely in code.
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict a cost, a permutation, or a generation count before running.
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A genetic algorithm's result is not "correct" until checked against a brute-force
  baseline (or some other known answer) on the same problem. A GA that runs without
  error and is never checked against anything is not yet evidence of anything.
"""

# %% [0] Environment check
# QUESTION           Run the cell and confirm your Python version, executable, and working
#                    folder.
# INPUTS/ASSUMPTIONS no inputs; Spyder is installed and this file is open
# METHOD             run the cell and read the three printed environment lines in the
#                    console
# CHECKS/INTERPRET   You should see a Python version, an executable path, and a folder
#                    path with no error.

from pathlib import Path
import sys

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())


# %% [1] Define the problem, confirm two known costs
# QUESTION           Define Radley Hall's south-facade panel-assignment problem and
#                    confirm two example costs match Monday's deck.
# INPUTS/ASSUMPTIONS position_ideal and panel_transmittance as given; perm is a
#                    permutation of panel indices 0-5, one panel per bay
# METHOD             complete cost(perm) as a sum of squared mismatch between each bay's
#                    assigned panel and its ideal transmittance
# CHECKS/INTERPRET   Expected: 0.2325 for (0,1,2,3,4,5), 0.0125 for (0,2,4,5,3,1) -
#                    Monday's verified true optimum.

position_ideal = [0.15, 0.25, 0.45, 0.55, 0.35, 0.20]        # bay 1..6
panel_transmittance = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60]   # 6 distinct panels


def cost(perm: list) -> float:
    """TODO: one sentence describing what this function returns."""
    # NEW SYNTAX: the finished return line uses a GENERATOR EXPRESSION -- the
    # "for i, p in enumerate(perm)" part inside sum()'s parentheses means "for each
    # bay i and its assigned panel p." Each squared-mismatch term is produced one at
    # a time and fed straight into sum(), with no stored list. It is exactly
    # equivalent to writing: total = 0
    #                         for i, p in enumerate(perm):
    #                             total += (panel_transmittance[p]-position_ideal[i])**2
    #                         return total
    # NOTE ON THE TYPE HINT: "perm: list" is written because every GA population
    # member and hill_climb's start is a list. Type hints are DOCUMENTATION, not
    # rules Python enforces -- so cost() also works on the TUPLES that
    # itertools.permutations produces in cell [2]. Both lists and tuples support
    # indexing and enumerate(), which is all cost() needs.
    # TODO: return the sum of squared mismatch between each bay's assigned panel and
    # its ideal transmittance, e.g.
    # return sum((panel_transmittance[p] - position_ideal[i]) ** 2
    #            for i, p in enumerate(perm))
    raise NotImplementedError(
        "Cell [1] incomplete: implement the squared-mismatch cost before continuing."
    )


print(round(cost((0, 1, 2, 3, 4, 5)), 4))
print(round(cost((0, 2, 4, 5, 3, 1)), 4))

# TODO: If both numbers above do not print 0.2325 and 0.0125, fix cost() before
# continuing to any later cell.


# %% [2] Brute-force baseline, re-confirmed and timed
# QUESTION           Re-confirm Monday's brute-force true optimum, and time it.
# INPUTS/ASSUMPTIONS cost() from cell [1]; itertools.permutations generates all 720
#                    orderings of range(6)
# METHOD             list all permutations, compute every cost, find best/worst/mean;
#                    time the whole block with time.perf_counter()
# CHECKS/INTERPRET   Expected: 720 permutations, best (0, 2, 4, 5, 3, 1) cost 0.0125,
#                    worst cost 0.5825, mean cost 0.2975.

import itertools
import time

# NEW SYNTAX: itertools.permutations(range(6)) is a standard-library function that
# generates every possible ordering of 0-5, one at a time; list(...) collects all
# 720 of them into all_perms. The TODO below asks for a LIST COMPREHENSION --
# [cost(p) for p in all_perms] -- the same "for each item, do something" idea as
# cell [1]'s generator expression, but built with square brackets so every result
# is collected into a new list right away, instead of fed straight into sum().
t0 = time.perf_counter()
all_perms = list(itertools.permutations(range(6)))
# TODO: build a list `costs` holding cost(p) for every p in all_perms, e.g.
# costs = [cost(p) for p in all_perms]
raise NotImplementedError(
    "Cell [2] incomplete: evaluate cost(p) for every permutation before continuing."
)
t1 = time.perf_counter()

best = all_perms[costs.index(min(costs))]
print(len(all_perms), "perms in", round((t1 - t0) * 1000, 2), "ms")
print("best:", best, "cost:", round(min(costs), 4))
print("worst cost:", round(max(costs), 4))
print("mean cost:", round(sum(costs) / len(costs), 4))


# %% [3] Recap: hill climbing gets stuck (from Monday)
# QUESTION           Confirm Monday's hill-climbing result still gets stuck the same way.
# INPUTS/ASSUMPTIONS cost() from cell [1]; neighbors() swaps two ADJACENT bays only
# METHOD             complete the improvement check inside hill_climb(), then run from
#                    the identity arrangement
# CHECKS/INTERPRET   Expected: stuck at [0, 1, 2, 5, 4, 3], cost 0.0925 - NOT the true
#                    optimum, 0.0125.

def neighbors(perm: list):
    """Yield every arrangement reachable by swapping two ADJACENT bays."""
    # NOTE ON THE TYPE HINT: this is the one function in the file with no
    # "-> ..." return hint. neighbors() is a GENERATOR (it uses yield, not
    # return), so it does not hand back a list -- it hands back one list at a
    # time. Annotating that correctly needs typing tools this course does not
    # use, so the honest choice is to leave the return hint off and say why.
    for i in range(len(perm) - 1):
        nb = perm[:]
        nb[i], nb[i + 1] = nb[i + 1], nb[i]
        yield nb


def hill_climb(start: list) -> tuple:
    """Move to the best improving neighbor until none improves; return (perm, cost)."""
    cur, cur_c = start[:], cost(start)
    while True:
        best_nb, best_c = None, cur_c
        for nb in neighbors(cur):
            # TODO: if this neighbor's cost is better than best_c so far, keep it, e.g.
            # if cost(nb) < best_c:
            #     best_nb, best_c = nb, cost(nb)
            raise NotImplementedError(
                "Cell [3] incomplete: implement the improving-neighbor comparison."
            )
        if best_nb is None:
            break
        cur, cur_c = best_nb, best_c
    return cur, cur_c


end, end_cost = hill_climb([0, 1, 2, 3, 4, 5])
print("stuck at:", end, "cost:", round(end_cost, 4))


# %% [4] Build order_crossover
# QUESTION           Combine two parent arrangements into one VALID child - no repeated
#                    panel index, no skipped one.
# INPUTS/ASSUMPTIONS two demo parents, [0,1,2,3,4,5] and [5,4,3,2,1,0]; rng =
#                    random.Random(7)
# METHOD             keep one parent's segment (already given), then complete the loop
#                    that fills every remaining slot from the other parent, in order
# CHECKS/INTERPRET   Expected child: [5, 1, 2, 4, 3, 0].

import random

# NEW VOCABULARY: a random SEED (the 7 in random.Random(7), below) is a fixed
# starting number that makes "randomness" reproducible -- the same seed always
# produces the exact same sequence of shuffles/samples, which is why everyone in
# class sees identical output here. random.Random(7) run twice gives identical
# results; random.Random(8) would shuffle differently.


def order_crossover(parent1: list, parent2: list,
                    rng: random.Random) -> list:
    """Keep a segment of parent1, fill the rest from parent2's order."""
    size = len(parent1)
    a, b = sorted(rng.sample(range(size), 2))
    child = [None] * size
    child[a:b + 1] = parent1[a:b + 1]
    # NEW SYNTAX: fill = [g for g in parent2 if g not in child] is another LIST
    # COMPREHENSION (see cell [2]) -- "for each gene g in parent2, keep it only if
    # it is not already somewhere in child."
    fill = [g for g in parent2 if g not in child]
    idx = 0
    # TODO: fill every remaining None slot, left to right, from `fill`, e.g.
    # for i in range(size):
    #     if child[i] is None:
    #         child[i] = fill[idx]
    #         idx += 1
    return child


rng = random.Random(7)
print(order_crossover([0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 1, 0], rng))

# TODO: If the printed child is not [5, 1, 2, 4, 3, 0], trace the fill loop by hand
# before moving on.


# %% [5] Build swap_mutation
# QUESTION           Randomly perturb a child without ever breaking its permutation
#                    property.
# INPUTS/ASSUMPTIONS child from cell [4]; rng2 = random.Random(3)
# METHOD             complete the two-position swap
# CHECKS/INTERPRET   Expected mutated result: [5, 3, 2, 4, 1, 0].

def swap_mutation(perm: list, rng: random.Random) -> list:
    """Return a copy of perm with two random positions exchanged."""
    perm = perm[:]
    # TODO: pick two distinct positions and swap them, e.g.
    # i, j = rng.sample(range(len(perm)), 2)
    # perm[i], perm[j] = perm[j], perm[i]
    return perm


child = [5, 1, 2, 4, 3, 0]
rng2 = random.Random(3)
print(swap_mutation(child, rng2))


# %% [6] The full GA loop, run with seed=1
# QUESTION           Run the complete genetic algorithm and confirm it reaches Monday's
#                    true optimum.
# INPUTS/ASSUMPTIONS order_crossover, swap_mutation, cost() from earlier cells;
#                    population 12, 5 survivors, mutation rate 0.35, seed=1
# METHOD             complete the elite-selection line, then let crossover + mutation
#                    fill the rest of each new generation
# CHECKS/INTERPRET   Expected: gen 0 -> 0.1025, gen 5 -> 0.0225, gen 9 -> 0.0125; best
#                    permutation (0, 2, 4, 5, 3, 1).

def genetic_algorithm(seed: int, pop_size: int = 12, survivors: int = 5,
                      mutation_rate: float = 0.35, generations: int = 30) -> list:
    """Evolve pop_size permutations for `generations`; return the best one found."""
    # seed reproducibility: same idea as cell [4]'s random.Random(7) -- fixing
    # seed=1 below means this exact GA run is reproducible for everyone.
    rng = random.Random(seed)
    population = [list(range(6)) for _ in range(pop_size)]
    for ind in population:
        rng.shuffle(ind)
    checkpoints = (0, 5, 9)
    for gen in range(generations + 1):
        population.sort(key=cost)
        if gen in checkpoints:
            print("gen", gen, "-> best cost", round(cost(population[0]), 4))
        # TODO: keep the best `survivors` individuals (population is already sorted
        # above) as the elite, e.g.
        # elite = population[:survivors]
        raise NotImplementedError(
            "Cell [6] incomplete: select exactly the requested elite survivors."
        )
        next_gen = elite[:]
        while len(next_gen) < pop_size:
            p1, p2 = rng.sample(elite, 2)
            child = order_crossover(p1, p2, rng)
            if rng.random() < mutation_rate:
                child = swap_mutation(child, rng)
            next_gen.append(child)
        population = next_gen
    return population[0]


best = genetic_algorithm(seed=1)
print("best permutation:", best, "cost:", round(cost(best), 4))


# %% [7] Compare the GA to brute force: evaluations and timing
# QUESTION           How many individuals did the GA evaluate to reach the true optimum,
#                    and how does that compare to brute force?
# INPUTS/ASSUMPTIONS the GA reaches the true optimum at generation 9 (cell [6]);
#                    population 12, 7 new individuals created per generation
# METHOD             compute individuals evaluated by hand from the generation number,
#                    then compare to brute force's 720
# CHECKS/INTERPRET   Expected: 75 individuals evaluated, about 10% of brute force's 720.

generation_reached = 9
individuals_evaluated = 12 + generation_reached * 7
# TODO: compute what percentage `individuals_evaluated` is of brute force's 720, e.g.
# percent_of_brute_force = round(100 * individuals_evaluated / 720, 1)
raise NotImplementedError(
    "Cell [9] incomplete: compute and label the comparison quantity before continuing."
)

print("GA individuals evaluated:", individuals_evaluated)
print("brute force individuals evaluated:", 720)
print("GA used", percent_of_brute_force, "% of brute force's evaluations")

when_worth_it = (
    "TODO: one paragraph - when is a GA worth the extra code, versus just using brute "
    "force? Name a specific N or a specific kind of expensive cost function."
)
print(when_worth_it)


# %% [8] AI-audit: a plausible but broken genetic algorithm
# QUESTION           Would you accept this AI-drafted genetic algorithm as-is?
# INPUTS/ASSUMPTIONS ai_genetic_algorithm as shown; cost() from cell [1]
# METHOD             run it, observe the result, then list at least four specific
#                    defects
# CHECKS/INTERPRET   A defensible list names the crossover, mutation, selection, AND
#                    validity-checking defects - not merely that the result "looks
#                    wrong."

def ai_crossover(parent1, parent2):
    cut = 3
    return parent1[:cut] + parent2[cut:]


def ai_mutate(perm, mutation_rate, rng):
    perm = perm[:]
    if mutation_rate:
        i, j = rng.sample(range(len(perm)), 2)
        perm[i], perm[j] = perm[j], perm[i]
    return perm


def ai_genetic_algorithm(seed):
    rng = random.Random(seed)
    population = [list(range(6)) for _ in range(12)]
    for ind in population:
        rng.shuffle(ind)
    for gen in range(10):
        survivors = population[:5]
        next_gen = survivors[:]
        while len(next_gen) < 12:
            p1, p2 = rng.sample(survivors, 2)
            child = ai_mutate(ai_crossover(p1, p2), 0.35, rng)
            next_gen.append(child)
        population = next_gen
    best = min(population, key=cost)
    return best, round(cost(best), 4)


ai_result = ai_genetic_algorithm(seed=1)
print(ai_result)
print("valid permutation?", sorted(ai_result[0]) == list(range(6)))

ai_defects = [
    # TODO: add at least four specific defects
]
for defect in ai_defects:
    print("-", defect)


# %% [9] Self-check: does the GA transfer to one new seed?
# QUESTION           Does the GA reach the same true optimum with a DIFFERENT random
#                    seed than the live demo (seed=1)?
# INPUTS/ASSUMPTIONS order_crossover, swap_mutation, cost() from earlier cells; seed=3,
#                    NOT seed=1
# METHOD             re-run the GA loop with seed=3, tracking best cost per generation
#                    until it matches the known true optimum; write 2-4 assert
#                    statements
# CHECKS/INTERPRET   Expected: reaches 0.0125 by generation 4 - faster than seed=1's
#                    generation 9, but the SAME final answer.

BEST_COST = 0.0125
rng3 = random.Random(3)
population3 = [list(range(6)) for _ in range(12)]
for ind in population3:
    rng3.shuffle(ind)
history3 = []
for gen in range(31):
    population3.sort(key=cost)
    history3.append(round(cost(population3[0]), 4))
    if history3[-1] == BEST_COST:
        break
    elite3 = population3[:5]
    next_gen3 = elite3[:]
    while len(next_gen3) < 12:
        p1, p2 = rng3.sample(elite3, 2)
        child = order_crossover(p1, p2, rng3)
        if rng3.random() < 0.35:
            child = swap_mutation(child, rng3)
        next_gen3.append(child)
    population3 = next_gen3

print("seed=3 history:", history3)
print("reached true optimum at generation:", len(history3) - 1)

# TODO: Add 2-4 assert statements here, checking seed=3's result (NOT seed=1's from
# cell [6]). Example to complete:
# assert history3[-1] == BEST_COST
# assert len(history3) - 1 <= 9
# assert population3[0] == [0, 2, 4, 5, 3, 1]

print("Self-check cell reached")


# %% [10] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished pipeline in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five
#                    required points listed below
# METHOD             fill in the AI-use record honestly, then write the exit
#                    explanation addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing
#                    the script cannot judge.

ai_use_record = """
Tool/model:
Prompt:
Suggestion received:
What I accepted:
What I modified and why:
What I rejected and why:
How I tested it:
One limitation I found:
"""

exit_explanation = """
In 80-120 words, explain:
1. what number every method in this studio was judged against, and where it came from,
2. why order crossover and swap mutation, specifically, keep every child a valid
   permutation, when the AI-drafted version in cell [8] did not,
3. what evaluations-vs-720 and timing both told you, and why they told different
   stories,
4. what seed=3's result in cell [9] proves that seed=1 alone could not, and
5. one thing this studio cannot yet tell you about a REAL 12-panel or 20-zone version
   of this same problem.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Represent six rooms along a corridor as a permutation. Define an adjacency
# penalty, explain why the problem has no useful slope, use 6! = 720 as the
# brute-force truth baseline, and state the validity checks crossover/mutation
# must preserve before a multi-seed GA comparison can be trusted.
