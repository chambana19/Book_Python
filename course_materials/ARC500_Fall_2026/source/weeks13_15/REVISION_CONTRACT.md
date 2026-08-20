# ARC 500 · Fall 2026 — Weeks 13-15 HISTORICAL revision record

> SUPERSEDED 2026-08-20. Numerical slide targets and exact 85-minute rules in
> this historical record must not be used. The current rule is a complete,
> topic-driven source deck with no slide-count cap; standard meetings are
> nominally 80 minutes and the instructor controls pacing. Follow
> `CONTRACT.md` and the package `COURSE_DESIGN_SYSTEM.md`.

You are revising an EXISTING, already-approved deck for ARC 500. This is a
revision pass, not a new build. **Read `CONTRACT.md` in this same directory
first** — full concept ledger, Project 2 cross-reference, and the real-Python
(scikit-learn) verification protocol still govern all CONTENT decisions. This
file governs the FORMAT/EXPANSION pass layered on top.

## 0. What this pass is for

1. **Typography/layout consistency** — fixed globally (§1).
2. **Readability.**
3. **More content.** Target **32-36 slides per 85-minute meeting**, all five
   decks including 15a (Meeting A only, but still a full 85-minute lecture/
   demo session — unlike Week 3A or Week 8B in earlier blocks, there is no
   density exception here). Weight new content toward worked examples /
   "predict before you run" checks, diagrams instead of prose columns, and
   dedicated vocabulary slides — NOT more `exercise` slides.

**Do not add new `exercise` slides beyond what already exists** (13a:1, 13b:2,
14a:2, 14b:4, 15a:0 — 15a has none by design, it carries no separate graded
assignment; do not add one). Every exercise/AI-audit slide must survive with
its title/prompt/steps/numbers UNCHANGED — re-typeset onto the new layout.

**A confirmed, repeated failure mode — read before touching any exercise
slide:** revision agents on ALL THREE prior passes (Weeks 1-3, Weeks 4-8, and
this pattern is now well-established enough to name explicitly) have silently
rewritten protected exercise/AI-audit slides' scenarios while genuinely
believing they were improving them. Every instance was caught by the verify
pass and reverted. **Before you touch any `exercise` slide, copy its exact
`title`/`prompt`/`steps` into your own scratch notes first. When you finish,
diff your new JSON against that copy field-by-field. Only layout/typography
fields may differ.**

---

## 1. The design system

Shared system: `../_design/`
(`tokens.mjs`, `measure.mjs`, `layouts.mjs`, `build.mjs`) — identical to every
other block. Read `tokens.mjs` and `layouts.mjs` first. Do not set font sizes,
colors, or positions in a spec — delete any legacy `headerFontSize`/
`cellFontSize`/`calloutFontSize` you find (week14a.json currently has one; the
builder already ignores it, but remove it while you're in that file).

A clean deck reports **10 distinct type sizes**. On overflow warnings:
- **`code` panel overflows are reliably real** in this block (several
  sklearn/pandas code slides carry more lines than the fixed panel holds —
  overshoots of 50-180+ points observed). Fix by trimming shown code to
  essential lines (`# ...` elision marker) or splitting the slide.
- **`table` cell overflows are frequently FALSE POSITIVES or trivial
  near-misses** (a handful of ~5pt-over warnings were confirmed cosmetically
  irrelevant on render). **Render and Read the actual slide image before
  "fixing" a table-cell overflow.** Only shorten text that visibly doesn't
  fit. The 8-column threshold-sweep table in `week14a.json` is a real
  candidate to double-check visually, since 8 narrow columns is the tightest
  case in this block.

### Layouts available

Existing: `title`, `statement`, `outcomes` (exactly 4), `agenda` (exactly 4),
`process`, `twoColumn`, `code`, `chart`, `table`, `exercise`, `closing`
(exactly 4 takeaways), `interface` (used once, in 13b — do not remove it).

**THREE NEW LAYOUTS — see `.codex_build/weeks01_03_expanded/CONTRACT.md`
section 1 for full field schemas and examples:**
- **`definition`** — one term, one slide. This block is FOURTEEN `twoColumn`
  slides deep in 13a alone — the richest deck in the whole course for this
  conversion. Strong candidates: `feature`/`target`, `train_test_split`,
  `naive baseline`, `MAE`/`RMSE`/`R²` (may need 2-3 separate slides — do not
  cram three metrics into one definition), `residual`,
  `overfitting`/`underfitting`, `data leakage`, `confusion matrix`,
  `precision`/`recall`/`F1`, `threshold`, `cross_val_score`, `model card`.
- **`anatomy`** — one line of code exploded, numbered chips. Strong
  candidates: a `train_test_split(X, y, test_size=0.25, random_state=42)`
  call, a `LinearRegression().fit(X_train, y_train)` call, a
  `confusion_matrix(y_test, y_pred)` call.
- **`predict`** — code with no shown output, multiple choice, reveal strip,
  placed immediately before the real reveal. This block's `data/README.md`
  has unusually rich verified material for this: "does the leakage-bug model
  beat the honest model's R² — by how much?", "which threshold gives zero
  false positives?", "does the 4-feature model's cross-validated R² match
  its single-split R²?" (verified answer: no — one fold is even negative,
  the block's single most important honest data point). Use those exact
  verified numbers, do not invent new ones.

---

## 2. Hard constraints

- Durations total exactly **85 minutes** per deck (15a has one meeting only —
  its 85 minutes are Meeting A's).
- Preserve all existing teaching content (see §0).
- Respect the concept ledger in `CONTRACT.md` and the plan's Section 3.
  Nothing from Weeks 1-12 needs re-teaching, but nothing may go BEYOND what
  each week introduces (14a's classifier concepts don't exist yet in 13a/13b).
- Every regression/classification/optimization number — every MAE/RMSE/R²,
  confusion-matrix cell, precision/recall/F1, cross_val_score fold, and the
  Week 15 surrogate-optimization result — MUST match `data/README.md`
  exactly, or be freshly verified in the pinned course environment
  (scikit-learn 1.9.0, pandas 3.0.5, scipy 1.17.1) if you introduce a
  genuinely new example. Do not invent different numbers or thresholds.
- Week 14b is TRACK-DEPENDENT (classification Track A + regression-refinement
  Track B) — preserve both tracks as clearly separated sections; do not merge
  or drop either.
- Week 15a has no Meeting B and no separate graded assignment — do not add
  either back in.
- Spyder only. Compact JSON, one line per slide object. Handouts are NOT part
  of this pass.

---

## 3. Your specific deck

| deck | now | target | note |
|---|---|---|---|
| 13a | 28 | **34** | 14 `twoColumn` slides — the richest single deck for `definition` conversion in this entire course. Convert the naive-baseline/MAE/RMSE/R²/residual/leakage vocabulary first. |
| 13b | 25 | **33** | 1 `exercise` — do NOT add more. Fix the 2 real code overflows (slides 12, 15 per current diagnostics). |
| 14a | 25 | **33** | 2 `exercise` — do NOT add more. Remove the legacy `calloutFontSize`/`headerFontSize`/`cellFontSize` on the threshold table; double-check that 8-column table renders cleanly after removal. |
| 14b | 29 | **34** | 4 `exercise` already (2 tracks × 2 each, roughly) — do NOT add more. Keep Track A and Track B clearly separated sections. |
| 15a | 24 | **33** | No `exercise` slides (by design — do not add one). 8 `twoColumn` slides to convert. The predict-optimize-decide worked demo (fitted model as `minimize` objective) is this deck's centerpiece — an `anatomy` slide exploding the `minimize(surrogate_eui, x0=..., bounds=...)` call would land well here. |

## 4. How to work

1. Read this file, then `CONTRACT.md`, then `_design/tokens.mjs` and
   `_design/layouts.mjs`, then `data/README.md` (every verified number lives
   there), then your deck's current spec.
2. Read the neighbouring decks' specs so terminology matches (especially the
   Week 13/14/15 shared dataset vocabulary).
3. Revise the spec per §3's notes.
4. Rebuild and check the report:
   `cd "<builder dir>" && node build_weeks13_15.mjs <id>`
   10 distinct sizes required; apply §1's code-vs-table distinction to any
   overflow warning before "fixing" it.
5. Render and look: `node montage.mjs <id>`, then Read
   `renders/week<id>_montage_full.png`.
6. Verify every numeric claim against `data/README.md` or in the pinned course
   environment.

## 5. Return value

Compact JSON: deck id, final slide count, minutes, slides added, new layouts
used and where, typography report numbers, and 2-3 real verification commands
with actual output.
