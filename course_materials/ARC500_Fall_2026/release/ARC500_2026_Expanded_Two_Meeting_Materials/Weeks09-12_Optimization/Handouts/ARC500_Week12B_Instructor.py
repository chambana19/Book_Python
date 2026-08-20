# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 12 studio · INSTRUCTOR SOLUTIONS
Genetic algorithm vs. brute force on a discrete panel-assignment problem
Syracuse University · School of Architecture · Fall 2026
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
    """Sum of squared mismatch between each bay's assigned panel and its ideal
    transmittance."""
    # NEW SYNTAX: "for i, p in enumerate(perm)" inside sum()'s parentheses is a
    # GENERATOR EXPRESSION -- it reads "for each bay i and its assigned panel p,"
    # producing one squared-mismatch term at a time and feeding it straight into
    # sum(), with no stored list. Equivalent to an explicit loop:
    #   total = 0
    #   for i, p in enumerate(perm):
    #       total += (panel_transmittance[p] - position_ideal[i]) ** 2
    #   return total
    # NOTE ON THE TYPE HINT: "perm: list" is written because every GA population
    # member and hill_climb's start is a list. Type hints are DOCUMENTATION, not
    # rules Python enforces -- so cost() also works on the TUPLES that
    # itertools.permutations produces in cell [2]. Both lists and tuples support
    # indexing and enumerate(), which is all cost() needs.
    return sum((panel_transmittance[p] - position_ideal[i]) ** 2
               for i, p in enumerate(perm))


print(round(cost((0, 1, 2, 3, 4, 5)), 4))
print(round(cost((0, 2, 4, 5, 3, 1)), 4))
# WHY THIS MATTERS: every method for the rest of this studio - hill climbing, the GA, the
# broken AI draft - is judged against the SAME cost() and the SAME verified number,
# 0.0125. If cost() is wrong here, every later "0.0125 confirmed" check downstream is
# meaningless, even if it happens to print the right-looking number.
# COMMON ERROR: writing sum((panel_transmittance[i] - position_ideal[p]) ** 2 ...) -
# swapping i and p reverses which list is being indexed by the PERMUTATION vs. by
# POSITION, silently changing the entire problem being solved.


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
# 720 of them into all_perms. costs = [cost(p) for p in all_perms] is a LIST
# COMPREHENSION -- the same "for each item, do something" idea as cell [1]'s
# generator expression, but built with square brackets so every result is
# collected into a new list right away, instead of fed straight into sum().
t0 = time.perf_counter()
all_perms = list(itertools.permutations(range(6)))
costs = [cost(p) for p in all_perms]
t1 = time.perf_counter()

best = all_perms[costs.index(min(costs))]
print(len(all_perms), "perms in", round((t1 - t0) * 1000, 2), "ms")
print("best:", best, "cost:", round(min(costs), 4))
print("worst cost:", round(max(costs), 4))
print("mean cost:", round(sum(costs) / len(costs), 4))
# WHY THIS MATTERS: 6! = 720 is small enough to check exhaustively - this number is the
# one guaranteed-correct answer everything else in this studio is compared against.
# Timing will differ machine to machine (about 1 ms is typical) - the number that
# actually matters is 720, not the millisecond count.
# COMMON ERROR: computing costs as a generator (costs = (cost(p) for p in all_perms))
# instead of a list. costs.index(...) and max(costs) both need to scan costs more than
# once; a generator is exhausted after the first pass and silently returns wrong or
# empty results the second time it is used.


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
            if cost(nb) < best_c:
                best_nb, best_c = nb, cost(nb)
        if best_nb is None:
            break
        cur, cur_c = best_nb, best_c
    return cur, cur_c


end, end_cost = hill_climb([0, 1, 2, 3, 4, 5])
print("stuck at:", end, "cost:", round(end_cost, 4))
# WHY THIS MATTERS: this is the exact result from Monday's Meeting A deck, reproduced
# here as a live check, not a new claim - 654 of the 720 possible starting arrangements
# get stuck the same way under this adjacent-swap neighborhood.
# COMMON ERROR: comparing `cost(nb) < best_c` using the ORIGINAL best_c from before the
# inner loop started, then updating best_c mid-loop but never re-reading it for
# subsequent neighbors - this code already reads best_c fresh each iteration, which is
# why it correctly finds the SINGLE best neighbor, not just the first improving one.


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
    for i in range(size):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child


rng = random.Random(7)
print(order_crossover([0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 1, 0], rng))
# WHY THIS MATTERS: rng picked cut points (1, 2), so the child keeps parent1's values 1,
# 2 there. `fill` is parent2 with 1 and 2 already removed - [5, 4, 3, 0] - dropped into
# the remaining slots left to right. This is the ONE mechanism that guarantees a valid
# permutation every single time, unlike the single-point crossover audited in cell [8].
# COMMON ERROR: writing `fill = [g for g in parent2 if g not in parent1]` instead of
# `if g not in child` - parent1 and child are NOT the same list at this point (child has
# None in most slots), so this filters against the wrong reference and silently produces
# a fill list of the wrong length, crashing later with an IndexError on `fill[idx]`.


# %% [5] Build swap_mutation
# QUESTION           Randomly perturb a child without ever breaking its permutation
#                    property.
# INPUTS/ASSUMPTIONS child from cell [4]; rng2 = random.Random(3)
# METHOD             complete the two-position swap
# CHECKS/INTERPRET   Expected mutated result: [5, 3, 2, 4, 1, 0].

def swap_mutation(perm: list, rng: random.Random) -> list:
    """Return a copy of perm with two random positions exchanged."""
    perm = perm[:]
    i, j = rng.sample(range(len(perm)), 2)
    perm[i], perm[j] = perm[j], perm[i]
    return perm


child = [5, 1, 2, 4, 3, 0]
rng2 = random.Random(3)
print(swap_mutation(child, rng2))
# WHY THIS MATTERS: rng2 picked positions (1, 4); swapping them turns [5,1,2,4,3,0] into
# [5,3,2,4,1,0] - still six distinct panel indices, just two exchanged. A swap can never
# create a duplicate or a gap, which is exactly why it is the safe mutation choice here.
# COMMON ERROR: rng.sample(range(len(perm)), 2) with replacement (e.g. two separate
# rng.randint(0, 5) calls) can pick the SAME position twice, "swapping" a value with
# itself - a silent no-op mutation that looks like it ran but never actually perturbed
# anything. rng.sample always returns two DISTINCT positions.


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
        elite = population[:survivors]
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
# WHY THIS MATTERS: `population.sort(key=cost)` before slicing is what makes
# `population[:survivors]` an actual ELITE (the 5 best), not 5 arbitrary individuals -
# compare directly to cell [8]'s AI draft, which slices without ever sorting. By
# generation 9 this reaches the identical true optimum verified in cells [1]-[2], and it
# never leaves that value again, because the best-5 are always kept.
# COMMON ERROR: forgetting `population.sort(key=cost)` before `population[:survivors]` -
# the loop would still run with no error, just silently keep 5 random individuals each
# generation instead of the fittest 5, and would very likely never converge to 0.0125 at
# all within 30 generations.


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
percent_of_brute_force = round(100 * individuals_evaluated / 720, 1)

print("GA individuals evaluated:", individuals_evaluated)
print("brute force individuals evaluated:", 720)
print("GA used", percent_of_brute_force, "% of brute force's evaluations")

when_worth_it = (
    "Not yet, at N=6: brute force is simpler, impossible to get wrong, and just as fast "
    "in wall-clock time here. The GA earns its cost once N grows past what brute force "
    "can check (12 panels alone is 12! = 479,001,600 permutations) or once each "
    "evaluation is expensive - a real daylighting or structural simulation instead of "
    "this cheap sum-of-squares formula, where evaluating 75 individuals instead of 720 "
    "would be the difference between a coffee break and an overnight run."
)
print(when_worth_it)
# WHY THIS MATTERS: 75 / 720 = 10.4% is the honest efficiency story - but it is an
# EVALUATION-COUNT story, not automatically a wall-clock-time story. On this machine,
# brute force (720 cheap evaluations, minimal Python overhead per permutation) actually
# finished in about the same time as, or slightly slower than, the GA once the GA is
# stopped as soon as it matches the known target - both land around a millisecond either
# way, because cost() itself is nearly free here. Evaluation count is the number that
# is the more transferable comparison for a REAL, expensive cost function; wall-clock
# time on THIS toy formula is not.
# COMMON ERROR: reporting only the evaluation-count comparison and implying the GA is
# unconditionally "faster" - state the wall-clock caveat explicitly, every time.


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
    "Crossover: ai_crossover slices at a FIXED point (cut=3), copied from a generic "
    "list-GA tutorial that never assumed a permutation. Combining two permutations this "
    "way produces an invalid child (a repeated panel index, another one missing) about "
    "94% of the time (verified separately: 188 of 200 test pairs) - order_crossover in "
    "cell [4] exists specifically to avoid this.",
    "Mutation: `if mutation_rate:` tests the TRUTHINESS of the number 0.35, which is "
    "always True - mutation fires on every single child, every generation, not at the "
    "stated 35% rate. The intended check is `if rng.random() < mutation_rate:`, as in "
    "cell [6].",
    "Selection: `survivors = population[:5]` slices the population without ever sorting "
    "it by cost first, so 'survivors' are 5 arbitrary individuals - the fittest are not "
    "actually being selected at all, unlike cell [6]'s `population.sort(key=cost)` "
    "before slicing.",
    "No validity check: `min(population, key=cost)` reports whatever has the lowest "
    "cost() value with no check that it is even a legal permutation. The reported "
    "'best,' [0, 3, 4, 5, 4, 1], assigns panel 4 to two different bays and never "
    "installs panel 2 anywhere - not a buildable facade at all, despite a plausible-"
    "looking cost number (0.0525).",
]
for defect in ai_defects:
    print("-", defect)
# WHY THIS MATTERS: every one of these four defects runs without raising a single
# error - the script executes cleanly and prints a number that LOOKS like progress
# (0.0525, better than the identity arrangement's 0.2325). Only checking the result
# against a known-valid structure (sorted(best) == list(range(6))) exposes the problem,
# exactly the same discipline Week 4's AI-audit first introduced for a pandas pipeline.
# COMMON ERROR: accepting an optimizer's reported "best cost" as trustworthy just because
# the number is low. A lower number is not evidence of a better - or even valid - answer
# unless the thing being scored was checked for validity first.


# %% [9] Self-check: does the GA transfer to one new seed?
# QUESTION           Does the GA reach the same true optimum with one DIFFERENT random
#                    seed than the live demo (seed=1)? This probes seed sensitivity; it
#                    does not prove performance for every seed.
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

assert history3[-1] == BEST_COST
assert len(history3) - 1 <= 9
assert population3[0] == [0, 2, 4, 5, 3, 1]
assert history3[0] != BEST_COST  # confirms real improvement happened, not a lucky gen-0 hit

print("Self-check passed: seed=3 reached the true optimum at generation",
      len(history3) - 1)
# WHY THIS MATTERS: seed=1 (cell [6]) reached 0.0125 at generation 9; seed=3 reaches the
# IDENTICAL true optimum at generation 4 - faster this time, same final answer, same
# exact permutation. This is the required different-scenario transfer check for this
# week - not a re-run of the seed=1 demo with a new label.
# COMMON ERROR: asserting only history3[-1] == BEST_COST and stopping there. Also
# asserting the FINAL PERMUTATION, not just its cost, matters - two different-looking
# permutations could coincidentally share a cost in general problems, though not in this
# particular one (0.0125 is uniquely achieved by (0, 2, 4, 5, 3, 1) here).


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
Tool/model: Example assistant
Prompt: Write a genetic algorithm in Python that assigns 6 glazing panels to 6 facade
bays to minimize squared mismatch to each bay's ideal transmittance.
Suggestion received: A script using a fixed-cut single-point crossover, an
`if mutation_rate:` truthiness check instead of a probability draw, and
population[:5] for "selection" with no sort beforehand (the ai_genetic_algorithm shown
in cell [8]).
What I accepted: The overall population/generations loop shape, and the idea of
tracking a best-cost-per-generation history.
What I modified and why: Replaced the crossover with order_crossover (segment-copy plus
ordered fill), which is the only one of the three that provably keeps every child a
valid permutation; fixed the mutation check to rng.random() < mutation_rate; added
population.sort(key=cost) before slicing so "survivors" are the actual fittest 5.
What I rejected and why: The AI script's implicit claim that a low cost() number is
automatically a good answer - min(population, key=cost) never checks that its own
"best" individual is even a legal permutation.
How I tested it: Compared the GA's final permutation and cost against the brute-force
baseline (cell [2]) and reran the entire GA with a second random seed (cell [9]),
requiring the identical permutation and cost both times before trusting either.
One limitation I found: This studio verifies that the GA finds the true optimum for
THIS problem, with THESE parameters and these two seeds - it does not prove a genetic
algorithm always finds the true optimum in general, and the seed-by-seed table from
Monday's deck shows real variation in how many generations it takes.
"""

exit_explanation = """
Every method here was judged against 0.0125, brute force's true optimum from
checking all 720 permutations. order_crossover and swap mutation keep every child a
valid permutation by construction - one keeps a real segment, the other only exchanges
existing values - while the AI draft's fixed-cut crossover broke that guarantee about
94% of the time. Evaluations (75 vs. 720, about 10%) showed a real efficiency gain;
timing did not, since this cost function is nearly free to evaluate either way. Seed=3
showed the result was not unique to seed=1; checking two seeds probes sensitivity but
does not prove generalization. This studio cannot yet say whether a real, 12-panel or
expensive-simulation version would behave the same way.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Expected representation: every candidate contains all six rooms exactly once;
# cost penalizes required adjacencies that are far apart and conflicts that are
# too close. Brute force verifies all 720 permutations. A GA claim requires
# permutation-preserving operators, validity assertions, multiple seeds, and
# comparison with the known small-case optimum.
