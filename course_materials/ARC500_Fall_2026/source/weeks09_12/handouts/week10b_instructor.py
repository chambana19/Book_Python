# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 10 studio · INSTRUCTOR SOLUTIONS
Linear optimization with scipy.optimize.linprog
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
from math import isclose
import sys

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())


# %% [1] Formulate Radley Hall's roof in standard form, and solve
# QUESTION           What split does the LP solver find, to numerical tolerance, for
#                    Radley Hall's 200 m2 roof between
#                    solar panels and green roof?
# INPUTS/ASSUMPTIONS solar: $400/m2 install, $60/m2/yr benefit, structurally capped at
#                    120 m2; green roof: $150/m2 install, $25/m2/yr benefit, no extra
#                    cap; 200 m2 total roof; $50,000 approved budget
# METHOD             maximize 60*x1 + 25*x2 -> minimize the negative; write area and
#                    budget as A_ub/b_ub rows; write the structural cap as a bound
# CHECKS/INTERPRET   Expected: res.x = [80. 120.], res.fun = -7800.0, res.success = True

from scipy.optimize import linprog

# maximize 60x1 + 25x2  ->  minimize the negative
c = [-60, -25]
A_ub = [[1, 1],       # area:   x1 + x2 <= 200
        [400, 150]]   # budget: 400x1 + 150x2 <= 50000
b_ub = [200, 50000]
bounds = [(0, 120),   # solar: structural cap
          (0, None)]  # green roof: no extra bound

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

if not res.success:
    raise RuntimeError(f"linprog failed (status={res.status}): {res.message}")
print("res.x:", res.x)
print("res.fun:", res.fun)
print("res.success:", res.success)
print("res.message:", res.message)
# WHY THIS MATTERS: res.fun prints -7800.0, not 7800.0, because linprog always minimizes.
# Maximizing 60x1+25x2 was rewritten as minimizing its negative back in c = [-60, -25] --
# the sign lives in c, not in linprog itself. Negate res.fun to read the real benefit.
# COMMON ERROR: reading res.fun directly as "the answer" without negating it back. A
# positive-looking -7800.0 is easy to misreport as a small number or a loss instead of an
# $7,800/yr gain.


# %% [2] Hand-verify constraint 1: the area limit
# QUESTION           Does the solved (x1, x2) actually use all 200 m2 of roof, or less?
# INPUTS/ASSUMPTIONS res.x from cell [1]
# METHOD             x1, x2 = res.x; compute x1 + x2 by hand
# CHECKS/INTERPRET   Expected: area_used is 200.0 to the stated tolerance (binding)

x1, x2 = res.x
area_used = x1 + x2
print("area used:", area_used, "<= 200 ?", area_used <= 200)
# WHY THIS MATTERS: 200.0 is not merely "within" the 200 m2 limit -- it is active to the
# stated tolerance. Recognizing a binding constraint (rather than one with slack left
# over) is what Meeting A's feasible-region-corner argument looks like in real numbers.


# %% [3] Hand-verify constraint 2: the budget cap, then assert both
# QUESTION           Does the solved (x1, x2) actually spend all $50,000, or less?
# INPUTS/ASSUMPTIONS x1, x2 from cell [2]
# METHOD             compute 400*x1 + 150*x2 by hand; then assert both constraints bind
#                    exactly -- this IS the studio's required core exercise
# CHECKS/INTERPRET   Expected: budget_used is 50000.0 to the stated tolerance (binding)

budget_used = 400 * x1 + 150 * x2
print("budget used:", budget_used, "<= 50000 ?", budget_used <= 50000)

AREA_ATOL_M2 = 1e-7
BUDGET_ATOL_USD = 1e-5
assert isclose(area_used, 200.0, rel_tol=0.0, abs_tol=AREA_ATOL_M2)
assert isclose(budget_used, 50000.0, rel_tol=0.0, abs_tol=BUDGET_ATOL_USD)
print("Both constraints bind within the stated numerical tolerances.")
# COMMON ERROR: checking only one of the two constraints and stopping there. A roof
# allocation could satisfy the area limit with room to spare while quietly overspending
# the budget (or vice versa) -- every constraint gets its own hand-check, every time.
# WHY THIS MATTERS: this cell IS the studio's required core exercise. 80+120=200 and
# 400*80+150*120=50000 are the two hand computations every student must produce on paper
# before trusting res.x, not merely read the printed numbers.


# %% [4] Compare to the two "obvious" strategies
# QUESTION           Does the formulated-and-solved answer actually beat an "all-solar" or
#                    "all-green" guess?
# INPUTS/ASSUMPTIONS x1, x2 from cell [1]; all-solar capped at the same 120 m2 structural
#                    limit; all-green uses the full 200 m2
# METHOD             compute all three annual benefits with the same 60x1+25x2 formula
# CHECKS/INTERPRET   Expected: all-solar = 7200, all-green = 5000, optimal = 7800.0

benefit_allsolar = 60 * 120 + 25 * 0
benefit_allgreen = 60 * 0 + 25 * 200
benefit_opt = 60 * x1 + 25 * x2

print("all-solar:", benefit_allsolar)
print("all-green:", benefit_allgreen)
print("optimal:", benefit_opt)
# WHY THIS MATTERS: most students (and most intuitive designers) pick all-solar first,
# since $60/m2/yr beats $25/m2/yr. That per-m2 comparison alone is misleading once a
# shared budget is involved -- solar's $400/m2 install cost also eats the budget four
# times faster than it would if cost were ignored. This table is the numeric proof that
# formulating (not intuition) decides the winning mix.
# COMMON ERROR: comparing strategies by benefit PER UNIT AREA instead of TOTAL annual
# benefit under the real constraints. Per-unit comparisons ignore that area and budget are
# both shared, limited resources being split between two competing uses.


# %% [5] AI-audit: a plausible but wrong formulation
# QUESTION           Would you accept this AI-suggested setup for the SAME roof problem?
# INPUTS/ASSUMPTIONS c_ai, A_ub, b_ub, bounds as shown; A_ub/b_ub/bounds are identical to
#                    cell [1]
# METHOD             run it, read res_ai.x and res_ai.fun, then diagnose
# CHECKS/INTERPRET   A defensible diagnosis names the sign/negation defect, not merely
#                    that the printed answer "looks wrong."

c_ai = [60, 25]     # "maximize benefit"
res_ai = linprog(c_ai, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
print(res_ai.x, res_ai.fun)

ai_defects = [
    "Sign/negation error: c_ai = [60, 25] tells linprog to MINIMIZE 60x1+25x2, not "
    "maximize it. Since linprog always minimizes, a maximize objective must be negated "
    "first (c = [-60, -25], cell [1]) -- c_ai skips that step entirely.",
    "The result looks clean, not broken: res_ai.success is True and res_ai.x = [0, 0] is "
    "a perfectly valid, constraint-satisfying point -- there is no error message anywhere "
    "to flag the mistake. Minimizing a POSITIVE-coefficient objective with only <= "
    "constraints and lower bound 0 always drives the variables toward zero.",
    "Misleading comment: the code comment '\"maximize benefit\"' states the intended goal "
    "in English but the coefficients do the opposite -- a comment describing INTENT is not "
    "a substitute for verifying the ACTUAL formula matches that intent.",
]

for defect in ai_defects:
    print("-", defect)

c_ai_fixed = [-60, -25]
res_ai_fixed = linprog(c_ai_fixed, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
print("fixed:", res_ai_fixed.x, -res_ai_fixed.fun)

assert list(res_ai_fixed.x) == list(res.x)
assert -res_ai_fixed.fun == 7800.0
# WHY THIS MATTERS: res_ai.success == True is exactly why Cell [1]'s own success check is
# not sufficient by itself -- a successfully solved WRONG formulation still reports
# success. This is the sharpest possible illustration of this week's course rule.
# COMMON ERROR: assuming a generative-AI suggestion that "runs without error" must be
# correct. Every one of this cell's three defects is individually plausible, and none of
# them raises a Python exception -- exactly why this formulation gets audited against the
# hand-verified result from cells [1]-[3], never accepted on its own.


# %% [6] Self-check: a smaller approved budget (required transfer check)
# QUESTION           If the board approves only $40,000 this year instead of $50,000, what
#                    changes?
# INPUTS/ASSUMPTIONS same roof, same A_ub, same bounds; ONLY b_ub's budget entry changes,
#                    from 50000 to 40000
# METHOD             re-run linprog with the new b_ub, then hand-verify both constraints
#                    exactly as in cells [2]-[3]
# CHECKS/INTERPRET   Expected: res_new.x = [40. 160.], benefit = 6400.0; both constraints
#                    still bind within tolerance (analytic equalities: 40+160=200;
#                    400*40+150*160=40000)

b_ub_new = [200, 40000]
res_new = linprog(c, A_ub=A_ub, b_ub=b_ub_new, bounds=bounds, method="highs")

print(res_new.x, -res_new.fun)

assert res_new.x[0] + res_new.x[1] == 200
assert 400 * res_new.x[0] + 150 * res_new.x[1] == 40000
assert round(-res_new.fun, 2) == 6400.0

print("Self-check passed: transfer budget confirms both constraints still bind.")
# WHY THIS MATTERS: only b_ub's second entry changed (50000 -> 40000); nothing else about
# the problem did. The optimal mix shifted from (80, 120) to (40, 160), and BOTH
# constraints still bind within tolerance -- evidence that the pattern from cells [2]-[3]
# is a property of this problem's structure, not a coincidence of one specific budget
# number.
# COMMON ERROR: re-running cells [1]-[3] with the new budget and overwriting res/x1/x2 in
# place, losing the original $50,000 answer needed for comparison. Store the transfer
# result under a new name (res_new), exactly as done here.


# %% [7] Capstone: wrap formulate -> solve -> verify in ONE reusable function
# QUESTION           Cells [1] and [6] typed the same four-array formulation twice,
#                    changing only the budget. Can one documented function solve and
#                    verify ANY roof area / approved budget pair?
# INPUTS/ASSUMPTIONS same $400/m2 solar and $150/m2 green-roof install costs, same
#                    $60/$25 per m2/yr benefits, same 120 m2 solar structural cap; ONLY
#                    the total roof area and the approved budget become parameters
# METHOD             define solve_roof_allocation(area_limit_m2, budget_usd) -> dict with
#                    a one-line docstring and type hints; build c/A_ub/b_ub/bounds inside,
#                    solve, compute both hand-checks, and return the answer WITH its
#                    checks so no caller can read the answer without them
# CHECKS/INTERPRET   Expected: (200, 50000) -> 80/120, $7,800/yr; (200, 45000) -> 60/140,
#                    $7,100/yr; (200, 40000) -> 40/160, $6,400/yr; (160, 50000) -> 104/56,
#                    $7,640/yr; (200, 70000) -> 120/80, $9,200/yr with the BUDGET no
#                    longer binding.


def solve_roof_allocation(area_limit_m2: float, budget_usd: float) -> dict:
    """Solve one roof scenario; check both limits."""
    c = [-60, -25]                      # maximize -> minimize the negative
    A_ub = [[1, 1], [400, 150]]         # row 1 = area, row 2 = install cost
    b_ub = [area_limit_m2, budget_usd]
    bounds = [(0, 120), (0, None)]      # solar structurally capped at 120 m2
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success:
        raise RuntimeError(
            f"linprog failed for area={area_limit_m2}, budget={budget_usd} "
            f"(status={res.status}): {res.message}"
        )
    x1, x2 = res.x
    area_used = x1 + x2
    cost_used = 400 * x1 + 150 * x2
    return {"solar_m2": round(x1, 2),
            "green_m2": round(x2, 2),
            "benefit_usd": round(-res.fun, 2),
            "area_binds": isclose(area_used, area_limit_m2,
                                   rel_tol=0.0, abs_tol=AREA_ATOL_M2),
            "budget_binds": isclose(cost_used, budget_usd,
                                     rel_tol=0.0, abs_tol=BUDGET_ATOL_USD),
            "solver_status": int(res.status),
            "solver_message": str(res.message)}


# Reuse 1: three approved budgets on the same 200 m2 roof, one call each.
for budget in [50000.0, 45000.0, 40000.0]:
    r = solve_roof_allocation(200.0, budget)
    assert r["area_binds"] and r["budget_binds"]
    print(budget, r["solar_m2"], r["green_m2"], r["benefit_usd"])

# The function reproduces cells [1] and [6] within the verification tolerances -- no
# retyped formulation.
approved = solve_roof_allocation(200.0, 50000.0)
assert approved["solar_m2"] == 80.0 and approved["green_m2"] == 120.0
assert approved["benefit_usd"] == 7800.0
assert solve_roof_allocation(200.0, 40000.0)["benefit_usd"] == 6400.0

# Reuse 2: a genuinely different scenario -- a smaller 160 m2 roof, full budget.
smaller_roof = solve_roof_allocation(160.0, 50000.0)
print("160 m2 roof:", smaller_roof["solar_m2"], smaller_roof["green_m2"],
      smaller_roof["benefit_usd"])
assert smaller_roof["solar_m2"] == 104.0 and smaller_roof["green_m2"] == 56.0
assert smaller_roof["benefit_usd"] == 7640.0

# Reuse 3: a budget so large it stops binding -- the structural cap takes over.
rich = solve_roof_allocation(200.0, 70000.0)
print("$70,000 budget:", rich["solar_m2"], rich["green_m2"], rich["benefit_usd"],
      "| area binds?", rich["area_binds"], "| budget binds?", rich["budget_binds"])
assert rich["area_binds"] and not rich["budget_binds"]
print("Capstone function verified on five scenarios.")
# WHY THIS MATTERS: this is the whole week in one place. The four standard-form arrays,
# the linprog call, and BOTH hand-checks from cells [2]-[3] now live in a single
# documented function, so the formulation was written once and audited once instead of
# retyped per scenario. Returning the checks alongside the answer is the real design
# decision here: a caller physically cannot read solar_m2 without also seeing whether the
# limits were used up, which is exactly the habit cell [5]'s AI-audit shows is needed.
# COMMON ERROR: making everything a parameter. The $400/m2 install cost, the $60/m2/yr
# benefit, and the 120 m2 structural cap never change in this problem, so hard-coding them
# inside is correct; only area_limit_m2 and budget_usd actually vary between scenarios.
# Over-parameterizing a function makes every call site longer and every call easier to get
# wrong.
# COMMON ERROR: assuming every constraint always binds because it did in cells [1]-[6].
# The $70,000 scenario above returns budget_binds = False -- solar hits its 120 m2
# structural cap first, so $10,000 of budget is left unspent. A function that reports
# which limits bind makes that visible instead of leaving it assumed.


# %% [8] Milestone: formulate and solve YOUR OWN Project 2 linear sub-problem
# QUESTION           What is the linear sub-component (or simplified linear relaxation)
#                    of your own Project 2 problem, and what does linprog say about it?
# INPUTS/ASSUMPTIONS your own Project 2 design variables, objective, constraints, and
#                    bounds -- an illustrative (NOT yours) example is shown for the
#                    pattern only
# METHOD             name your own variables/objective/constraints/bounds, translate to
#                    c/A_ub/b_ub/bounds, solve, then hand-verify every constraint against
#                    a stated numerical tolerance
#                    like cells [2]-[3]
# CHECKS/INTERPRET   No single expected answer -- your own hand-verified constraint table
#                    is the deliverable, matching this week's milestone.

# ILLUSTRATIVE example only (a window-retrofit budget) -- a DIFFERENT fictional problem
# than the roof, shown only so the four-array pattern is visible once more before writing
# your own. A real student submission replaces every line below with their own Project 2
# variables, objective, constraints, and bounds.
# x1 = m2 of standard low-E glazing retrofit, x2 = m2 of triple-pane glazing retrofit
c_example = [-18, -30]                  # maximize 18x1+30x2 annual savings
A_ub_example = [[1, 1], [250, 500]]     # glazing area <= 150 m2 ; budget <= $50,000
b_ub_example = [150, 50000]
bounds_example = [(0, None), (0, 80)]   # triple-pane supply capped at 80 m2 this year
res_example = linprog(c_example, A_ub=A_ub_example, b_ub=b_ub_example,
                       bounds=bounds_example, method="highs")
print("illustrative example:", res_example.x, -res_example.fun)

x1_ex, x2_ex = res_example.x
area_used_ex = x1_ex + x2_ex
budget_used_ex = 250 * x1_ex + 500 * x2_ex
print("glazing area used:", area_used_ex, "(<=150)")
print("budget used:", budget_used_ex, "(<=50000)")
print("triple-pane used:", x2_ex, "(<=80, has slack -- not every constraint must bind)")

assert area_used_ex == 150
assert budget_used_ex == 50000
assert x2_ex < 80
# WHY THIS MATTERS: this illustrative example deliberately shows a constraint that does
# NOT bind (the 80 m2 triple-pane supply cap, actual use 50 m2) alongside two that do
# (glazing area, budget) -- real problems do not always have every constraint bind, and
# claiming otherwise without checking would be its own kind of error.
# COMMON ERROR: submitting this illustrative window-retrofit example AS your own Project 2
# milestone. It exists only to demonstrate the pattern -- your own submission must use
# your own Project 2 problem's real variables, objective, and constraints.


# %% [9] Required write-up: linear-formulation-family justification
# QUESTION           In 60-100 words, what does your own Project 2 formulation show?
# INPUTS/ASSUMPTIONS your own results from cell [8]
# METHOD             write linear_formulation_writeup addressing the four required points
#                    below
# CHECKS/INTERPRET   60-100 words, all four required points present

linear_formulation_writeup = (
    "This studio's illustrative problem allocates a fixed glazing budget between "
    "standard and triple-pane window retrofits (x1, x2) to maximize annual energy "
    "savings, 18x1+30x2, subject to a 150 m2 glazing-area limit and a $50,000 budget. "
    "The problem is naturally linear, so linprog -- not minimize or a heuristic search -- "
    "is the correct deterministic LP family here. Area and budget bind within the solver "
    "and verification tolerances at the "
    "optimum (150 m2, $50,000); the 80 m2 triple-pane supply cap does not. Its "
    "limitation: it assumes fixed unit costs, ignoring any bulk-purchase discount a real "
    "contract might offer."
)
print(linear_formulation_writeup)
print(len(linear_formulation_writeup.split()), "words")
# WHY THIS MATTERS: this write-up IS the Week 10 linear-formulation-family checkpoint
# named in the semester plan and Project 2 Part I's required algorithm-family
# justification -- graded as this week's ordinary studio task, not an additional artifact.


# %% [10] AI-use record and exit reflection
# QUESTION           Record how you used generative AI this week, then explain today's
#                    roof-allocation result in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing this
#                    script cannot tell you.

ai_use_record = """
Tool/model: Example assistant
Prompt: Write a scipy.optimize.linprog setup that maximizes Radley Hall's roof benefit
across solar panels and a green roof, given the area/budget/structural limits.
Suggestion received: A c/A_ub/b_ub/bounds setup structurally identical to cell [1], but
with c = [60, 25] (the un-negated benefit coefficients) and no success or constraint
check afterward -- essentially the cell [5] AI-audit bug, offered as if it were final.
What I accepted: The general standard-form shape (c, A_ub, b_ub, bounds) and the choice
of method='highs'.
What I modified and why: Negated c to [-60, -25], since linprog always minimizes and the
roof problem is a maximize problem; added the two hand-verification cells (area, budget)
and their asserts, since res.success alone does not confirm the formulation is correct;
added the naive-strategy comparison table to show the mixed answer actually wins.
What I rejected and why: The un-negated c = [60, 25] suggestion -- it runs cleanly and
reports success, but silently solves "minimize benefit," not "maximize benefit," landing
at (0, 0) with zero benefit.
How I tested it: Hand-computed both binding constraints (80+120=200;
400*80+150*120=50000) before trusting res.x; re-ran the identical script with only the
budget changed to $40,000 (cell [6]) and reproduced the same binding-constraint pattern
on a new pair of numbers.
One limitation I found: This script confirms the formulated LP is solved to numerical
tolerance and its
constraints hand-verified; it cannot confirm that $400/m2, $150/m2, $60/m2/yr, and
$25/m2/yr are themselves accurate real-world costs -- that would need real vendor quotes,
not this fictional teaching scenario.
"""

exit_explanation = """
Radley Hall's roof is best split as 80 m2 of solar and 120 m2 of green roof, earning
$7,800/yr -- both the 200 m2 area limit and the $50,000 budget bind within the stated
solver/verification tolerances
(80+120=200; 400*80+150*120=50000). All-solar earns only $7,200/yr and all-green just
$5,000/yr, because per-m2 return alone ignores that area and budget are shared, limited
resources. The AI-drafted formulation in cell [5] forgot to negate the objective
(c=[60,25] instead of [-60,-25]); linprog still reported success, but had actually solved
"minimize benefit," returning (0, 0). The $40,000-budget check shifted the mix to 40 m2
solar, 160 m2 green roof, $6,400/yr, with the identical binding pattern. This script
cannot say whether $7,800/yr justifies the $50,000 upfront cost against other capital
priorities.
"""

print(ai_use_record)
print(exit_explanation)
print(len(exit_explanation.split()), "words")

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Expected formulation: maximize 9*x_wall + 7*x_roof; x_wall+x_roof <= 400;
# 120*x_wall+80*x_roof <= 50000; both variables >= 0. Verified optimum is
# (400, 0), $3,600/yr: surface binds and budget has slack. Require a manual
# feasibility check before the solver result is interpreted.
