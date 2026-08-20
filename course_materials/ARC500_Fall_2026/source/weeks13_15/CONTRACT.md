# ARC 500 · Fall 2026 — Weeks 13-15 Authoring Contract

You are authoring lecture decks and Spyder lab handouts for ARC 500, Programming with
Python and Generative AI, Syracuse University School of Architecture. Audience: graduate
architecture students with **zero prior coding experience** (now 12 weeks into the
semester). This contract governs Weeks 13-15 only: Machine Learning I (regression),
Machine Learning II (classification, model cards, decisions), and the Project 2 capstone
clinic/presentation/synthesis session.

**Read the finalized semester plan FIRST, in full, before writing anything:**
`../../ARC500_2026_Expanded_Two_Meeting_Materials/ARC500_2026_Semester_Restructure_Weeks01-15.txt`
Section 3 gives your week's exact Meeting A/B topics, assignment, and milestone — follow
it precisely. Section 5 (Project 2) is what Weeks 13-15 build toward — read it in full so
your examples visibly serve it (Part IV needs a naive baseline + evaluated model +
model card, track-dependent; the whole project's central move is Part IV's fitted model
feeding Part II/III's optimization, which is exactly what Week 15 demonstrates).

---

## 1. What already exists — read it, do not re-derive it

**Weeks 1-12 (built, verified, approved).** Specs live in
`.codex_build/weeks01_03_expanded/specs/` (Weeks 1-3), `.codex_build/weeks04_08/specs/`
(Weeks 4-8), and `.codex_build/weeks09_12/specs/` (Weeks 9-12). By the end of Week 12,
students know: numpy/pandas/matplotlib/geopandas via import, docstrings + basic type
hints (routine since Week 4), groupby/agg, IQR/z-score outlier rules, the `fig, ax`
Matplotlib pattern, `FuncAnimation`, GeoDataFrame/CRS/reprojection/spatial join, `ndarray`/
`arange`/`linspace`/boolean masks/`meshgrid`, `scipy.optimize.linprog` (design variables,
objective, constraints, bounds, feasible region), `scipy.optimize.minimize` (initial
guess, local vs. global optimum), and a small genetic algorithm (selection, crossover,
mutation) vs. brute-force baseline. They do NOT yet know: anything from `sklearn`,
`train_test_split`, any regression/classification metric, `cross_val_score`, list/dict
comprehensions, classes, or recursion.

**This week's shared objective function callback, Week 9/11's `energy_proxy(wwr,
shade_m)`, is DIRECTLY relevant continuity** — see `data/README.md` for exactly how to
use it (Week 13 contrasts "a clean formula you swept/optimized directly" against "a
fitted model built from data," and Week 15 replaces the Week 9/11 analytic function with
the Week 13/14 FITTED model as the optimization objective — the same `minimize` call
site, a different objective function inside it).

**The layout/builder system (already proven, do not modify or invent a new layout
type):**
`build_weeks13_15.mjs`
Read it for the exact field schema of each layout type (title/statement/outcomes/agenda/
process/twoColumn/code/table/exercise/closing/interface/chart). There is no dedicated
"confusion matrix" layout — build it with the `table` layout (rows = actual class,
columns = predicted class; use the `callout` field for the accuracy/precision headline if
useful). Every new library, function, or piece of jargon gets an explicit, VISIBLE (not
speaker-notes-only) plain-language definition with an example, at first use — no
exceptions. This has been the single most common defect across every prior audit of this
course's material.

**Source keys** are in `sources.json`
(includes `sklStart`, `sklSplit`, `sklMetrics`, `sklCV`, `sklLinear`, `sklDummy`,
`sklLogistic`, `sklConfusion`, `sklPrecisionRecall`).

---

## 2. Numeric verification — REAL PYTHON, not reasoning

A pinned course Python environment is used for verification, with numpy 2.4.6,
scipy 1.17.1, scikit-learn 1.9.0, pandas 3.0.5, and matplotlib 3.11.1.

**You MUST verify every "output" field and every expected-value comment by actually
running the code** — regression metrics, confusion matrices, cross_val_score folds, and
the Week 15 optimization result are NOT things you can reliably predict by reasoning.

**The entire dataset, every model fit, every metric, every confusion matrix, and the
Week 15 optimization result are already designed and fully verified for you — use them
exactly, do not invent different numbers, coefficients, or thresholds:**
`data/README.md`
This covers: the shared `radley_portfolio_envelope.csv` dataset (140 rows, already
written to `data/`), the Week 13 baseline-vs-3-feature regression fit plus a real,
verified leakage bug (`est_annual_cost_index`) students must find and fix, the Week 14
Track A classifier (confusion matrix + threshold sweep + consequences argument) and
Track B regression refinement (adding `compactness`, plus an honestly-reported negative
cross-validation fold), and the Week 15 predict-optimize-decide worked demo (fitted model
as `minimize` objective). Re-run the exact scripts in that file yourself to confirm
before using any number, but do not change the underlying formula/coefficients/seed
(`random_state=42` everywhere a split occurs).

## 3. Weekly assignment / handout policy (from the finalized plan, Section 2)

- A "weekly assignment" IS that week's Meeting B Spyder studio handout.
- Every handout `# %%` cell needs the four headings (`# QUESTION`,
  `# INPUTS/ASSUMPTIONS`, `# METHOD`, `# CHECKS/INTERPRET`), matching the exact
  spacing/alignment convention already used in
  `.codex_build/weeks04_08/handouts/week04b_student.py` — read it first.
- Every handout's CHECKS/INTERPRET section must include at least one self-generated
  transfer check (a different input/parameter/scenario than the one worked through live)
  with 2-4 student-written `assert` statements.
- Student handout: scaffolded with `# TODO:` gaps stating the expected result. Never
  leave a version that crashes before any TODO is attempted.
- Instructor handout: complete, oracle-verified solutions, `# COMMON ERROR:` notes,
  `# WHY THIS MATTERS:` notes, and a REAL, concrete, filled-in AI-use-record and
  exit-reflection answer (not a blank template).
- Include one AI-audit section per week: plausible but defective AI-generated code
  (matching that week's topic) for students to diagnose. **Week 13's AI-audit section IS
  the graded studio task itself** (the leakage bug in `data/README.md`) — do not also
  invent a second, separate AI-audit snippet for Week 13; one real bug, found and fixed,
  is the whole point.
- Spyder only: `# %%` cells, Ctrl+Enter, Variable Explorer. Never mention
  notebooks/Jupyter.
- **Week 14 Meeting B is TRACK-DEPENDENT** — write TWO separate handout pairs:
  `week14b_student_classification.py` / `week14b_instructor_classification.py` (Track A,
  go/no-go) and `week14b_student_regression.py` / `week14b_instructor_regression.py`
  (Track B, continuous-outcome refinement). Both must exist; a student picks one based on
  their own Project 2 framing (per the plan).
- **Week 15 has NO Meeting B and NO separate graded weekly assignment** (this week's
  deliverable IS Project 2 itself, per the plan). Still write ONE reference/demo script,
  `week15a_demo_predict_optimize_decide.py` — a fully worked, non-graded, instructor-
  narrated walkthrough of the Week 15 integration demo in `data/README.md` (not scaffolded
  with `# TODO:` gaps like a studio handout; it is a complete, runnable reference the
  instructor projects/narrates live and students may keep). It still uses the four-heading
  `# %%` convention for consistency, but label it clearly as a reference demo, not an
  assignment, in its own header comment.

## 4. Deck structure (matches Weeks 1-12's proven shape)

1. `title`, 2. `statement`, 3. `outcomes` (exactly 4), 4. `agenda` (exactly 4) — body
slides — 1-2 `exercise` slides — `closing` (exactly 4 takeaways). There is no target
or maximum slide count. Standard meetings are nominally 80 minutes, but every
distributed presentation retains the complete authored sequence, worked examples,
and optional horizon material. Every new term gets the established `"<Term>,
defined"` treatment with a concrete example: `feature`/`target`, `train_test_split`,
`naive baseline`, `MAE`/`RMSE`/`R²`, `residual`, `overfitting`/`underfitting`, `data
leakage`, `confusion matrix`, `precision`/`recall`/`F1`, `threshold`, `cross_val_score`,
`model card` — no exceptions.

## 5. Week-specific notes (see the plan file Section 3 for full detail)

- **Week 13 (Meeting A + B):** Open Meeting A with features vs. target and why a naive
  baseline (predict the mean) comes first — a model that cannot beat "just guess the
  average" has told you something real. Use an AI coding assistant to scaffold the
  `LinearRegression` fit/predict pipeline QUICKLY (this is explicitly where the plan
  wants AI-assisted scaffolding, not a hand-typed-from-scratch pipeline), then spend the
  remaining time on MAE/RMSE/R², a residual plot, and naming over/underfitting and data
  leakage IN the AI-drafted code — the leakage bug from `data/README.md`
  (`est_annual_cost_index`) is the core artifact, not a bonus. Meeting B: verify the
  split, calculate a metric manually, diagnose the largest residual (V037, see
  `data/README.md`), find AND FIX the leakage bug, explain why it was wrong. Polynomial
  feature engineering is an optional extension only — do not make it load-bearing.
- **Week 14 (Meeting A + B, Meeting B is TRACK-DEPENDENT):** Meeting A is shared theory —
  confusion matrix, precision vs. recall, choosing a threshold from real consequences
  (use the verified threshold-sweep table + the false-positive-is-dangerous argument in
  `data/README.md` — do not just show the arithmetic, teach the reasoning), `cross_val_score`
  as "does this hold up on data it hasn't seen," and the model card as a deliverable
  stating scope and limits. Meeting B forks: Track A students build the go/no-go
  classifier (confusion matrix + model card); Track B students deepen Week 13's
  regression (add `compactness`, re-evaluate, update the model card) rather than building
  an unrelated classifier — do NOT make Track B feel like a lesser consolation path; its
  cross-validation result (including the honestly negative fold) is one of this block's
  most important teaching moments. Both tracks hand-compute their track's metrics from
  raw counts (precision/recall/F1 from the confusion matrix, or ΔMAE/ΔRMSE from Week 13's
  baseline).
- **Week 15 (Meeting A ONLY, no Meeting B, Dec 7):** This is a closing SYNTHESIS session,
  not new-content lecture — say so explicitly on an early slide, and keep the deck's
  balance of "new content" light. Structure: brief predict-optimize-decide framing recap
  (2-3 slides), the fully worked Week 15 demo from `data/README.md` (fitted model as
  `minimize` objective, contrast explicitly with Week 11's local-trap behavior — THIS
  surrogate has none, and explain why in terms of its own linear shape, not as a general
  claim about all fitted models), a short conceptual note on the Track A constraint
  pattern (predicted P(meets code) >= threshold as a constraint, no separate full numeric
  demo required), then in-class presentation logistics: a 4-minute decision brief plus
  a 1-minute evidence/code trace, hard-capped at 5 minutes per student; reserve 15 minutes
  for selective source-deck synthesis, and use parallel gallery/code-review rounds when
  enrollment exceeds 12. Include a reproducibility/AI-use-record reminder and closing
  takeaways. No `exercise` slide is required this week (there is no
  studio time to run one in) — an `agenda` item can note "instructor available to advise
  case by case" instead.

## 6. Return value

Return only a compact JSON summary per week: files written, slide counts, duration
totals (must sum to 85 for each meeting — Week 15 has only one meeting, Meeting A),
concepts introduced, and 2-3 of the real-Python verification commands you ran with their
actual output.
