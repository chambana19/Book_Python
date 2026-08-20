# ARC 500 · Fall 2026 — Weeks 9-12 HISTORICAL revision record

> SUPERSEDED 2026-08-20. Numerical slide targets and exact 85-minute rules in
> this historical record must not be used. The current rule is a complete,
> topic-driven source deck with no slide-count cap; standard meetings are
> nominally 80 minutes and the instructor controls pacing. Follow
> `CONTRACT.md` and the package `COURSE_DESIGN_SYSTEM.md`.

You are revising an EXISTING, already-approved deck for ARC 500. This is a
revision pass, not a new build. **Read `CONTRACT.md` in this same directory
first** — full concept ledger, Project 2 cross-reference, and the real-Python
verification protocol (numpy/scipy/scikit-learn) still govern all CONTENT
decisions. This file governs the FORMAT/EXPANSION pass layered on top.

## 0. What this pass is for

1. **Typography/layout consistency** — fixed globally (§1). Do not
   reintroduce per-slide font overrides.
2. **Readability.**
3. **More content.** Target **32-36 slides per 85-minute meeting** (all eight
   decks in this block are normal 85-minute meetings — there is no Week 3A/
   Week 8B-style exception in this block). Weight new content toward worked
   examples / "predict before you run" checks, diagrams instead of prose
   columns, and dedicated vocabulary slides — NOT more `exercise` slides.

**Do not add new `exercise` slides beyond what already exists.** Every
exercise/AI-audit slide must survive with its title/prompt/steps/numbers
UNCHANGED — re-typeset onto the new layout only.

**A confirmed failure mode from the Weeks 1-3 and Weeks 4-8 passes, read this
before touching any exercise slide:** revision agents on both prior passes
silently rewrote protected exercise/AI-audit slides' scenarios (different
numbers, different prompts, in one case an untaught construct) while
genuinely believing they were improving them. Every instance was caught by
the verify pass and reverted — but it keeps happening, so: **before you touch
any `exercise` slide, copy its exact `title`/`prompt`/`steps` into your own
scratch notes first. When you finish, diff your new JSON against that copy
field-by-field. Only layout/typography fields may differ.**

---

## 1. The design system

Shared system: `../_design/`
(`tokens.mjs`, `measure.mjs`, `layouts.mjs`, `build.mjs`) — identical to Weeks
1-3 and 4-8. Read `tokens.mjs` and `layouts.mjs` first. Do not set font sizes,
colors, or positions in a spec.

A clean deck reports **10 distinct type sizes**. On overflow warnings, two
different situations apply — **do not treat them identically**:
- **`code` panel overflows are reliably real** in this block (this is the
  scipy.optimize / genetic-algorithm block; several existing slides carry
  more lines of code than the fixed panel holds at the uniform font — some by
  a factor of 2-3x). Fix these by trimming the shown code to its essential
  lines (mark elisions with `# ...`, matching this course's convention) or
  splitting into two slides. Do not ship a code overflow unfixed.
- **`table` cell overflows are frequently FALSE POSITIVES**, especially in
  narrow (3-column, `callout`-present) tables. The overflow estimate uses an
  average character width and is deliberately conservative; it has already
  been confirmed wrong by rendering and looking (a cell it flagged as needing
  3 lines actually wrapped to 2 and fit with room to spare). **Before
  "fixing" a table-cell overflow, render the deck and Read the actual slide
  image.** If the text visibly fits, leave it — do not shorten good content
  to silence an estimate that isn't visually wrong. If it genuinely looks
  cramped or clipped, then shorten that cell's text.

### Layouts available

Existing: `title`, `statement`, `outcomes` (exactly 4), `agenda` (exactly 4),
`process`, `twoColumn`, `code`, `chart`, `table`, `exercise`, `closing`
(exactly 4 takeaways). No `interface` in this block.

**THREE NEW LAYOUTS — see `.codex_build/weeks01_03_expanded/CONTRACT.md`
section 1 for full field schemas and examples:**
- **`definition`** — one term, one slide. Strong candidates in this block:
  `objective function`, `constraint`, `bounds`, `feasible region`, `linprog`,
  `minimize`, `initial guess`, `local optimum` vs `global optimum`,
  `gradient`, `heuristic`, `genetic algorithm` (as an umbrella term, with
  selection/crossover/mutation as its worked example), `brute force`,
  `meshgrid`, `vectorization`.
- **`anatomy`** — one line of code exploded, numbered chips (not leader
  lines — chips avoid collisions). `code` single line, ≤ ~46 characters.
  Strong candidates: a `linprog(c, A_ub=..., b_ub=..., bounds=...)` call, a
  `minimize(f, x0=..., bounds=...)` call, a `meshgrid` call.
- **`predict`** — code with no shown output, multiple choice, reveal strip.
  Place immediately BEFORE the `code` slide that reveals the real result.
  This block is unusually well-suited to `predict`: "which starting guess
  lands in the local trap?", "does the GA reach the same optimum as brute
  force?", "which constraint binds first?" are all real, verified,
  non-obvious answers already documented in `data/README.md` — use those
  exact numbers, do not invent new scenarios.

---

## 2. Hard constraints

- Durations total exactly **85 minutes** per deck.
- Preserve all existing teaching content (see §0).
- Respect the concept ledger in `CONTRACT.md` and the plan's Section 3.
  Nothing from Weeks 13-15 (regression/classification/sklearn) may appear
  here — this block ends at heuristic search.
- Every numeric claim — every `linprog`/`minimize` result, every GA
  convergence value, every sweep/sensitivity number — MUST match
  `data/README.md` exactly, or be freshly verified in the pinned course
  environment if you introduce a genuinely new example.
  Do not invent different numbers, coefficients, or seeds. This block's
  numbers were tuned carefully (e.g. the GA's seed=1 was chosen for its
  teaching-clean convergence curve, NOT because it's fastest — an earlier
  draft of this course's own materials got that specific claim wrong and had
  to correct it; do not reintroduce the error).
- Spyder only. Compact JSON, one line per slide object. Handouts are NOT part
  of this pass.

---

## 3. Your specific deck

Slide counts are current authored/rendered counts (no `includeSlides` tricks
in this block — all authored slides currently render).

| deck | now | target | note |
|---|---|---|---|
| 09a | 29 | **34** | 7 `twoColumn` — several are strong `definition` candidates (`ndarray`, `meshgrid`, boolean mask). Pose the sensitivity question before vocabulary, per CONTRACT.md's existing ordering fix — do not regress this. |
| 09b | 25 | **33** | 7 `exercise` already — do NOT add more. |
| 10a | 24 | **33** | 8 `twoColumn` — `objective function`/`constraint`/`bounds`/`feasible region` are strong `definition` candidates; a `linprog(...)` call is a strong `anatomy` candidate. |
| 10b | 24 | **33** | 6 `exercise` already — do NOT add more. |
| 11a | 24 | **33** | 7 `twoColumn` — `initial guess`, `local optimum` vs `global optimum`, `gradient` are strong `definition` candidates. The starting-guess table in `data/README.md` is an excellent `predict` source (5 of 8 plausible guesses land in the wrong optimum). |
| 11b | 24 | **33** | 5 `exercise` already — do NOT add more. |
| 12a | 28 | **34** | 6 `twoColumn` — `heuristic`, `genetic algorithm`, `brute force` are strong `definition` candidates. The verified per-seed generations-to-reach-optimum table in `data/README.md` is a strong `predict` source. |
| 12b | 26 | **33** | 6 `exercise` already — do NOT add more. |

## 4. How to work

1. Read this file, then `CONTRACT.md`, then `_design/tokens.mjs` and
   `_design/layouts.mjs`, then `data/README.md` (every verified number lives
   there), then your deck's current spec.
2. Read the neighbouring decks' specs so terminology matches.
3. Revise the spec per §3's notes.
4. Rebuild and check the report:
   `cd "<builder dir>" && node build_weeks09_12.mjs <id>`
   Confirm slide count, exactly 85 minutes, 10 distinct sizes. For any
   overflow warning, apply §1's code-vs-table distinction before "fixing"
   anything.
5. Render and look: `node montage.mjs <id>`, then Read
   `renders/week<id>_montage_full.png`.
6. Verify every numeric claim against `data/README.md` or in the pinned course
   environment.

## 5. Return value

Compact JSON: deck id, final slide count, minutes, slides added, new layouts
used and where, typography report numbers (distinct sizes, real overflow
count after applying §1's code-vs-table filter), and 2-3 real verification
commands with actual output.
