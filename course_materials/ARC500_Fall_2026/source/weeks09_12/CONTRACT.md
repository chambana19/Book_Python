# ARC 500 · Fall 2026 — Weeks 9-12 Authoring Contract

You are authoring lecture decks and Spyder lab handouts for ARC 500,
Programming with Python and Generative AI, Syracuse University School of
Architecture. Audience: graduate architecture students with **zero prior
coding experience** (now 8 weeks into the semester). This contract governs
Weeks 9-12 only (Parameter Sweeps, then all three optimization algorithm
families: linear, gradient-based, heuristic).

**Read the finalized semester plan FIRST, in full, before writing anything:**
`../../ARC500_2026_Expanded_Two_Meeting_Materials/ARC500_2026_Semester_Restructure_Weeks01-15.txt`
Section 3 gives your week's exact Meeting A/B topics, assignment, and
milestone — follow it precisely. Section 5 (Project 2) is what Weeks 9-12
build toward — read it so your examples visibly serve it (Project 2 Part I
needs a sensitivity check from Week 9; Part II needs linprog AND minimize
from Weeks 10-11, both REQUIRED not conditional; Part III needs a heuristic
search from Week 12 on a genuinely discrete decision).

---

## 1. What already exists — read it, do not re-derive it

**Weeks 1-8 (built, verified, approved).** Specs live in
`.codex_build/weeks01_03_expanded/specs/` (Weeks 1-3) and
`.codex_build/weeks04_08/specs/` (Weeks 4-8). Read whichever matter for your
week's prerequisite ledger. By the end of Week 8, students additionally
know (beyond Weeks 1-3's core Python): third-party libraries (numpy, pandas,
matplotlib, geopandas) via import, method vs. function call, keyword
arguments at the call site, docstrings + basic type hints (routine since
Week 4), pandas DataFrame/Series, `.loc`/`.iloc`, tuple-unpacking, `&`/`|`
for combining Boolean Series (NOT `and`/`or`), groupby/agg, IQR and z-score
outlier rules, the `fig, ax` Matplotlib pattern, `FuncAnimation`, GeoDataFrame/
CRS/EPSG/reprojection/spatial join. They do NOT yet know: NumPy arrays in
depth (Week 9 is this), anything from `scipy.optimize`, anything from
`sklearn`, list/dict comprehensions, classes, or recursion.

**The layout/builder system (already proven, do not modify or invent a new
layout type):**
`build_weeks09_12.mjs`
Read it for the exact field schema of each of the ten-plus layout types
(title/statement/outcomes/agenda/process/twoColumn/code/table/exercise/
closing/interface/chart). Every new library, function, or piece of jargon
gets an explicit, VISIBLE (not speaker-notes-only) plain-language definition
with an example, at first use — no exceptions. This has been the single
most common defect across every prior audit of this course's material.

**Source keys** are in `sources.json`.

---

## 2. Numeric verification — REAL PYTHON, not reasoning

A pinned course Python environment is used for numeric verification,
with numpy 2.4.6, scipy 1.17.1, scikit-learn 1.9.0, pandas 3.0.5,
matplotlib 3.11.1, geopandas 1.1.4.

**You MUST verify every "output" field and every expected-value comment by
actually running the code** — solver results (`linprog`, `minimize`),
optimization trajectories, and GA convergence are NOT things you can
reliably predict by reasoning; small formula changes shift optima
non-obviously. Pattern:
```bash
cat > /tmp/check.py << 'EOF'
from scipy.optimize import linprog
res = linprog([-60,-25], A_ub=[[1,1],[400,150]], b_ub=[200,50000], bounds=[(0,120),(0,None)])
print(res.x, -res.fun)
EOF
python /tmp/check.py
```

**Three scenarios are already designed and fully verified for you — use
them exactly, do not invent different formulas/numbers:**
`data/README.md`
This covers: the Week 9/11 shared two-basin nonlinear objective (with a
verified table of which starting guesses land in the local vs. global
optimum), the Week 10 linear roof-allocation problem (verified optimal
mixed solution beats both naive pure strategies), and the Week 12 discrete
panel-assignment problem (verified brute-force optimum plus a tuned GA that
reliably reaches it — use `random.seed(1)` for the primary demo). Re-run the
exact scripts in that file yourself to confirm before using any number, but
do not change the underlying formulas/costs/bounds.

## 3. Weekly assignment / handout policy (from the finalized plan, Section 2)

- A "weekly assignment" IS that week's Meeting B Spyder studio handout.
- Every handout `# %%` cell needs the four headings (`# QUESTION`,
  `# INPUTS/ASSUMPTIONS`, `# METHOD`, `# CHECKS/INTERPRET`), matching the
  exact spacing/alignment convention already used in
  `.codex_build/weeks04_08/handouts/week04b_student.py` — read it first.
- Every handout's CHECKS/INTERPRET section must include at least one
  self-generated transfer check (a different input/parameter/scenario than
  the one worked through live) with 2-4 student-written `assert` statements.
- Student handout: scaffolded with `# TODO:` gaps stating the expected
  result. Never leave a version that crashes before any TODO is attempted.
- Instructor handout: complete, oracle-verified solutions, `# COMMON ERROR:`
  notes, `# WHY THIS MATTERS:` notes, and a REAL, concrete, filled-in
  AI-use-record and exit-reflection answer (not a blank template — this was
  a real, confirmed defect in an earlier week's material; do not repeat it).
- Include one AI-audit section per week: plausible but defective
  AI-generated code (matching that week's topic) for students to diagnose.
- Spyder only: `# %%` cells, Ctrl+Enter, Variable Explorer. Never mention
  notebooks/Jupyter.

## 4. Deck structure (matches Weeks 1-8's proven shape)

1. `title`, 2. `statement`, 3. `outcomes` (exactly 4), 4. `agenda` (exactly
4) — body slides — 1-2 `exercise` slides — `closing` (exactly 4 takeaways).
There is no target or maximum slide count. Standard meetings are nominally 80
minutes, but each distributed presentation is a complete source deck and may
carry additional practice or professional-horizon slides. Every new term
gets the established `"<Term>, defined"` treatment with a concrete example:
`ndarray`, `vectorization`, `meshgrid`, `objective function`, `constraint`,
`bounds`, `feasible region`, `linprog`, `minimize`, `initial guess`, `local
optimum` vs `global optimum`, `gradient`/`slope`, `heuristic`, `genetic
algorithm` (selection/crossover/mutation), `brute force` — no exceptions.

## 5. Week-specific notes (see the plan file Section 3 for full detail)

- **Week 9**: NumPy in application, not as a syntax catalog — pose the
  sensitivity question FIRST (which of two swept design variables moves the
  outcome most?), then introduce `ndarray`/`arange`/`linspace`/boolean
  mask/`meshgrid` only as needed to answer it (this ordering was a
  confirmed fix in an earlier week's audit — do not regress to a
  vocabulary-first structure). Use the Week 9/11 shared nonlinear objective
  from data/README.md as the swept function; visualize the full surface
  (heatmap) so both basins are visible.
- **Week 10**: linear/exact optimization as algorithm family #1 — design
  variables, objective, constraints, bounds, feasible region, why a linear
  problem solves EXACTLY (simplex/interior-point) rather than being
  searched. Use the verified roof-allocation LP from data/README.md; have
  students hand-verify both binding constraints.
- **Week 11**: nonlinear/gradient-based search as algorithm family #2 —
  `minimize` follows the slope downhill from a starting guess; initial
  guess, bounds, local vs. global optimum. Use the SAME nonlinear objective
  from Week 9 (continuity is the point — "you saw the whole surface last
  week; today the computer finds a minimum, but which one?"). The verified
  starting-guess table in data/README.md should drive the core worked
  example and the studio exercise — do not soften or hide that most
  plausible starting guesses land in the wrong (local) optimum; that is the
  entire lesson.
- **Week 12**: heuristic/metaheuristic search as algorithm family #3 — why
  gradient-based methods cannot handle a genuinely discrete/combinatorial
  decision; build from random search to hill-climbing to a small genetic
  algorithm. Use the verified panel-assignment problem from data/README.md;
  show the brute-force baseline (720 permutations, tractable here only
  because N=6 is small) and the GA reaching the identical true optimum in
  far fewer evaluations — but also name honestly that a GA does not
  guarantee finding the true optimum in general (it did here, verified,
  with the specified seed/parameters; do not claim this always happens).
  Briefly connect to generative-design tools students may already associate
  with "optimization."

## 6. Return value

Return only a compact JSON summary per week: files written, slide counts,
duration totals (must sum to 85 for each meeting), concepts introduced, and
2-3 of the real-Python verification commands you ran with their actual
output.
