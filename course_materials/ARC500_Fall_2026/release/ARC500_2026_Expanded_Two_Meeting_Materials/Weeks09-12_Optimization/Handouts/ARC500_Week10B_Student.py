# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 10 studio · Linear optimization with scipy.optimize.linprog
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week10 module folder. No data file is needed today -- the
     roof-allocation problem is defined directly in this script.
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict a result BEFORE running each cell -- especially cells [1]-[3].
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A linprog result is not verified until every constraint has been checked BY HAND.
  res.success == True only means the solver did its job on whatever numbers were typed
  in -- it does not mean those numbers were the right numbers. Hand-verify first.
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


# %% [1] Formulate Radley Hall's roof in standard form, and solve
# QUESTION           What is the exact best split of Radley Hall's 200 m2 roof between
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

# TODO: call linprog with c, A_ub, b_ub, bounds, method='highs' and store it as res, e.g.
# res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
raise NotImplementedError(
    "Cell [1] incomplete: solve with linprog, check status, then remove this gate."
)

print("res.x:", res.x if res is not None else "TODO")
print("res.fun:", res.fun if res is not None else "TODO")
print("res.success:", res.success if res is not None else "TODO")

# TODO: Before moving on, state in one sentence why res.fun should print as a NEGATIVE
# number here even though the roof problem is a maximize problem.


# %% [2] Hand-verify constraint 1: the area limit
# QUESTION           Does the solved (x1, x2) actually use all 200 m2 of roof, or less?
# INPUTS/ASSUMPTIONS res.x from cell [1]
# METHOD             x1, x2 = res.x; compute x1 + x2 by hand
# CHECKS/INTERPRET   Expected: area_used = 200.0, exactly at the limit (binding)

x1, x2 = res.x if res is not None else (None, None)
area_used = (x1 + x2) if x1 is not None else None
print("area used:", area_used, "<= 200 ?", (area_used <= 200) if area_used is not None else "TODO")

# TODO: Compute 80 + 120 on paper BEFORE trusting the printed value. Do they match?


# %% [3] Hand-verify constraint 2: the budget cap, then assert both
# QUESTION           Does the solved (x1, x2) actually spend all $50,000, or less?
# INPUTS/ASSUMPTIONS x1, x2 from cell [2]
# METHOD             compute 400*x1 + 150*x2 by hand; then assert both constraints bind
#                    exactly -- this IS the studio's required core exercise
# CHECKS/INTERPRET   Expected: budget_used = 50000.0, exactly at the limit (binding)

budget_used = (400 * x1 + 150 * x2) if x1 is not None else None
print("budget used:", budget_used, "<= 50000 ?", (budget_used <= 50000) if budget_used is not None else "TODO")

# TODO: Compute 400*80 + 150*120 on paper BEFORE trusting the printed value.

# TODO: Once cell [1]'s TODO is filled in (so area_used/budget_used are real numbers),
# add two assert statements confirming area_used == 200 and budget_used == 50000, then
# print a confirmation message, e.g.
# assert area_used == 200
# assert budget_used == 50000
# print("Both constraints bind exactly.")


# %% [4] Compare to the two "obvious" strategies
# QUESTION           Does the formulated-and-solved answer actually beat an "all-solar" or
#                    "all-green" guess?
# INPUTS/ASSUMPTIONS x1, x2 from cell [1]; all-solar capped at the same 120 m2 structural
#                    limit; all-green uses the full 200 m2
# METHOD             compute all three annual benefits with the same 60x1+25x2 formula
# CHECKS/INTERPRET   Expected: all-solar = 7200, all-green = 5000, optimal = 7800.0

benefit_allsolar = 60 * 120 + 25 * 0
benefit_allgreen = 60 * 0 + 25 * 200
benefit_opt = (60 * x1 + 25 * x2) if x1 is not None else None

print("all-solar:", benefit_allsolar)
print("all-green:", benefit_allgreen)
print("optimal:", benefit_opt if benefit_opt is not None else "TODO")

# TODO: State in one sentence which naive strategy you would have picked before this
# course, and by how many dollars per year the optimal formulation beats it.


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
    # TODO: add at least two specific defects, e.g. explain exactly why c_ai=[60, 25]
    # produces res_ai.x = [0, 0] even though res_ai.success is True
]

for defect in ai_defects:
    print("-", defect)

# TODO: Rewrite c_ai correctly (matching cell [1]'s c) and re-run linprog with the fixed
# coefficients. Confirm the repaired version reproduces [80. 120.] and -7800.0.


# %% [6] Self-check: a smaller approved budget (required transfer check)
# QUESTION           If the board approves only $40,000 this year instead of $50,000, what
#                    changes?
# INPUTS/ASSUMPTIONS same roof, same A_ub, same bounds; ONLY b_ub's budget entry changes,
#                    from 50000 to 40000
# METHOD             re-run linprog with the new b_ub, then hand-verify both constraints
#                    exactly as in cells [2]-[3]
# CHECKS/INTERPRET   Expected: res_new.x = [40. 160.], benefit = 6400.0; both constraints
#                    still bind exactly (40+160=200; 400*40+150*160=40000)

b_ub_new = [200, 40000]
# TODO: call linprog with c, A_ub, b_ub_new, bounds, method='highs', store as res_new, e.g.
# res_new = linprog(c, A_ub=A_ub, b_ub=b_ub_new, bounds=bounds, method='highs')
raise NotImplementedError(
    "Cell [6] incomplete: solve the transfer budget without overwriting res, then remove this gate."
)

print(res_new.x if res_new is not None else "TODO",
      -res_new.fun if res_new is not None else "TODO")

# TODO: Add 2-4 of your own assert statements here -- this week's required transfer
# safeguard, on a genuinely different input than the $50,000 case worked through above.
# Example to complete:
# assert res_new.x[0] + res_new.x[1] == 200
# assert 400 * res_new.x[0] + 150 * res_new.x[1] == 40000
# assert round(-res_new.fun, 2) == 6400.0


# %% [7] Capstone: wrap formulate -> solve -> verify in ONE reusable function
# QUESTION           Cells [1] and [6] typed the same four-array formulation twice,
#                    changing only the budget. Can one documented function solve and
#                    verify ANY roof area / approved budget pair?
# INPUTS/ASSUMPTIONS same $400/m2 solar and $150/m2 green-roof install costs, same
#                    $60/$25 per m2/yr benefits, same 120 m2 solar structural cap; ONLY
#                    the total roof area and the approved budget become parameters
# METHOD             finish solve_roof_allocation(area_limit_m2, budget_usd) -> dict, which
#                    already has its one-line docstring and type hints; build the arrays
#                    inside, solve, compute both hand-checks, and return the answer WITH
#                    its checks so no caller can read the answer without them
# CHECKS/INTERPRET   Expected once the TODOs are filled in: (200, 50000) -> 80/120,
#                    $7,800/yr; (200, 45000) -> 60/140, $7,100/yr; (200, 40000) -> 40/160,
#                    $6,400/yr; (160, 50000) -> 104/56, $7,640/yr; (200, 70000) -> 120/80,
#                    $9,200/yr with the BUDGET no longer binding.


def solve_roof_allocation(area_limit_m2: float, budget_usd: float) -> dict:
    """Solve one roof scenario; check both limits."""
    c = [-60, -25]                      # maximize -> minimize the negative
    A_ub = [[1, 1], [400, 150]]         # row 1 = area, row 2 = install cost
    b_ub = [area_limit_m2, budget_usd]
    bounds = [(0, 120), (0, None)]      # solar structurally capped at 120 m2
    # TODO: solve inside the function and unpack the answer, replacing the two placeholder
    # lines below, e.g.
    # res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    # x1, x2 = res.x
    # benefit_usd = round(-res.fun, 2)
    raise NotImplementedError(
        "Cell [7] incomplete: solve, verify status/slacks, and return the real allocation."
    )
    area_used = x1 + x2
    cost_used = 400 * x1 + 150 * x2
    return {"solar_m2": round(x1, 2),
            "green_m2": round(x2, 2),
            "benefit_usd": benefit_usd,
            "area_binds": area_used == area_limit_m2,
            "budget_binds": cost_used == budget_usd}


# Reuse 1: three approved budgets on the same 200 m2 roof, one call each.
for budget in [50000.0, 45000.0, 40000.0]:
    r = solve_roof_allocation(200.0, budget)
    print(budget, r["solar_m2"], r["green_m2"], r["benefit_usd"],
          r["area_binds"], r["budget_binds"])

# TODO: once the linprog call above is filled in, add ONE assert inside the loop above
# confirming both constraints bind in every scenario, e.g.
# assert r["area_binds"] and r["budget_binds"]

# TODO: confirm the function reproduces cells [1] and [6] without retyping the
# formulation -- call it at (200.0, 50000.0) and at (200.0, 40000.0), print both results,
# and add 2 asserts of your own that the benefits are 7800.0 and 6400.0.

# TODO: Reuse 2 -- call solve_roof_allocation(160.0, 50000.0) for a smaller 160 m2 roof on
# the same $50,000 budget. Print the result, then confirm BY HAND that 104 + 56 = 160 m2
# and 400*104 + 150*56 = $50,000 before adding 2 asserts of your own for those two facts.

# TODO: Reuse 3 -- call solve_roof_allocation(200.0, 70000.0) and print area_binds and
# budget_binds. Explain in one sentence why budget_binds comes back False here while
# area_binds is still True. (Hint: which limit stops solar from growing past 120 m2?)


# %% [8] Milestone: formulate and solve YOUR OWN Project 2 linear sub-problem
# QUESTION           What is the linear sub-component (or simplified linear relaxation)
#                    of your own Project 2 problem, and what does linprog say about it?
# INPUTS/ASSUMPTIONS your own Project 2 design variables, objective, constraints, and
#                    bounds -- an illustrative (NOT yours) example is shown for the
#                    pattern only
# METHOD             name your own variables/objective/constraints/bounds, translate to
#                    c/A_ub/b_ub/bounds, solve, then hand-verify every constraint exactly
#                    like cells [2]-[3]
# CHECKS/INTERPRET   No single expected answer -- your own hand-verified constraint table
#                    is the deliverable, matching this week's milestone.

# ILLUSTRATIVE example only (a window-retrofit budget) -- replace every line below with
# YOUR own Project 2 variables, objective, constraints, and bounds.
c_example = [-18, -30]
A_ub_example = [[1, 1], [250, 500]]
b_ub_example = [150, 50000]
bounds_example = [(0, None), (0, 80)]
res_example = linprog(c_example, A_ub=A_ub_example, b_ub=b_ub_example,
                       bounds=bounds_example, method="highs")
print("illustrative example:", res_example.x, -res_example.fun)

# TODO: Below this line, define YOUR OWN c, A_ub, b_ub, bounds for your Project 2 linear
# sub-problem (name the variables clearly, e.g. my_c, my_A_ub, my_b_ub, my_bounds), solve
# with linprog, print the result, and hand-verify every constraint by computing each
# A_ub row's value directly and comparing it to its b_ub limit, exactly like cells [2]-[3].


# %% [9] Required write-up: linear-formulation-family justification
# QUESTION           In 60-100 words, what does your own Project 2 formulation show?
# INPUTS/ASSUMPTIONS your own results from cell [8]
# METHOD             write linear_formulation_writeup addressing the four required points
#                    below
# CHECKS/INTERPRET   60-100 words, all four required points present

linear_formulation_writeup = """
TODO: in 60-100 words, state:
1. your own Project 2 problem's design variables, objective, and constraints, in one or
   two sentences,
2. which optimization family (linear, gradient-based, or heuristic) best fits your
   problem's overall structure and why, even if you solved only a linear relaxation
   today,
3. which of your constraints bind exactly at your solved optimum, and
4. one limitation of using a simplified linear relaxation, if that applies to your case.
"""

print(linear_formulation_writeup)


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
1. Radley Hall's optimal roof split and its annual benefit, with both binding constraints
   named,
2. why the all-solar and all-green strategies both lose money compared to the optimal mix,
3. what the AI-drafted formulation (cell [5]) got wrong, and why res_ai.success was still
   True despite the wrong answer,
4. what changed, and what stayed the same, in the $40,000-budget transfer check (cell
   [6]), and
5. one thing this script cannot tell you about whether $7,800/yr is the right amount to
   actually invest in Radley Hall's roof.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Formulate wall-versus-roof insulation allocation with $50,000 and 400 m²:
# wall costs $120/m² and saves $9/m²/yr; roof costs $80/m² and saves $7/m²/yr.
# Name variables/units, objective, constraints, bounds, and hand-check one
# feasible plus one infeasible candidate before asking linprog to solve it.
