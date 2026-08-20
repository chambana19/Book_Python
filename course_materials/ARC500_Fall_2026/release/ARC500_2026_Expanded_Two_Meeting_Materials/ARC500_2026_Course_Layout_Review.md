# ARC 500 — Course Schedule and Topic Layout Review

> Historical planning snapshot, retained for provenance. Timing, deck counts,
> Week 14 evaluation, project scope, and the source-deck policy were revised
> after this review. The authoritative current files are
> `ARC500_2026_Semester_Restructure_Weeks01-15.txt`,
> `COURSE_DESIGN_SYSTEM.md`, `RELEASE_NOTES_2026-08-20.md`, and
> `course_manifest.yml`. In particular, standard meetings are nominally 80
> minutes and complete source decks are not cut to an exact time or slide count.

Prepared August 17, 2026. This is a planning/design document, not a
lecture-content revision — no slide, handout, or project content changes
are made here. It reviews the semester-level topic layout with the current
week structure treated as one candidate arrangement, not a fixed constraint,
per the official course-description document.

## 1. What the source-of-truth intro document actually says

Read directly from `ARC500_Brief_Description_SP26_CHUN.pdf` (the official,
LaTeX-formatted course description, Author: Junho Chun) and cross-checked
against `ARC500_Brief_Description_SP26.docx` (same body text, no schedule
detail):

- **Syracuse University, School of Architecture, Fall 2026, ARC 500, 3
  credit hours.**
- **Class meeting time: Monday/Wednesday 12:45–2:05 pm.** That is **80
  minutes**, not 85. `ARC500_2026_Semester_Restructure_Weeks01-15.txt` and
  every deck's per-slide timing note in this package are built on an
  assumed 85-minute meeting. This is a real, material discrepancy: it
  affects the time budget of all 29 weekly meetings, not one week. See
  Section 3.
- Location: Slocum Hall 307. Instructor: Junho Chun, PhD.
- **Audience, stated explicitly**: "Designed for beginners with no prior
  coding experience." Confirmed — this matches how the existing package is
  built (see prior audit findings: predict-before-run framing, deliberately
  broken debugging exercises, AI-use records, no closed-book syntax exam).
- **Six stated learning-objective areas** (verbatim groupings from the
  brief): Python fundamentals; AI-assisted coding; data analysis &
  visualization; applied optimization (objective functions and
  constraints, theory + application); machine learning principles
  (classification, regression, training, evaluation, theory +
  implementation); computational thinking for interdisciplinary
  problem-solving.
- **A notable signal in the flyer's own imagery**: the illustrated thumbnail
  grid includes parametric surfaces, "Architectural Parametric Forms &
  Structural Geometry," and "Generative & Computational Design Patterns" —
  alongside energy dashboards, classification/clustering, and statistical
  analysis. The current 15-week core teaches the data/optimization/ML side
  of that imagery in real depth, but does **not** teach any parametric or
  generative-geometry scripting (Grasshopper/Rhino.Python, Dynamo) — that
  material currently lives only in the new `Beyond ARC500` capstone handout
  as a **post-course** next step, not in the graded 15 weeks. This is a
  scope question worth a deliberate decision rather than a silent gap — see
  Section 4, Question 4.

## 2. Fresh review of the current 4-phase structure (not assumed fixed)

Current candidate structure, restated at the phase level rather than the
week level, to evaluate it as a *sequencing choice* rather than a fait
accompli:

| Phase | Weeks | Core question the phase answers | New abstraction introduced |
|---|---|---|---|
| 1. Foundations | 1–3 | Can I read, write, trace, and debug a short program? | Syntax, types, control flow, functions |
| 2. Data as Evidence | 4–8 | Can I turn a real dataset into a defensible claim? | Arrays/tables, cleaning, grouping, visual encoding, spatial reasoning |
| 3. Optimization | 9–12 | Can I formulate a design decision and solve it correctly? | Objective/constraints; exact -> gradient -> heuristic search |
| 4. Machine Learning | 13–14 | Can I predict an outcome and know when to distrust the prediction? | Statistical evaluation: baseline, split, leakage, cross-validation |
| 5. Integration | 15 | Can I chain prediction into optimization and defend the result? | None new — synthesis only |

**Why this ordering holds up, evaluated against two plausible alternatives:**

- *Alternative A — swap Phases 3 and 4 (teach ML right after Data-as-
  Evidence, optimization last):* ML would flow naturally out of Phase 2's
  "insight from data" framing. Rejected as the better option because ML
  introduces a genuinely new kind of abstraction the course hasn't asked
  for yet — statistical generalization (why a model that fits your data
  well can still be wrong on new data) — layered on top of the numerical
  mindset Phase 2 already built. Optimization (Phase 3) stays *inside* that
  numerical mindset (it's still "compute a number, check a constraint," no
  probability or generalization yet) and builds directly on Phase 2's
  vectorized-array habit (Week 9's sweeps are a one-step extension of
  Week 4-9's NumPy work). Sequencing the *smaller* new abstraction
  (optimization) before the *larger* one (statistical ML) is the more
  defensible difficulty ladder for a zero-experience cohort, and it also
  means the fitted model in Phase 4 is fresh when Week 15 plugs it into the
  optimizer built in Phase 3 — the reverse order would make that final
  integration reach back further in memory.

- *Alternative B — interleave optimization and ML weekly rather than
  block them:* rejected outright for this audience. A zero-experience
  cohort meeting only 160 (soon corrected: see below) minutes a week
  benefits from one theme sustained for 3-4 weeks with a stable vocabulary,
  not a topic switching every session — this is the same reasoning the
  existing master schedule already uses to justify blocking Weeks 4-8 as
  one continuous pandas/GeoPandas arc rather than splitting library
  introductions across non-adjacent weeks.

**Conclusion: keep the 5-phase backbone.** It is a sound, evidence-grounded
sequence — increasing-abstraction ladder, each phase feeds the next,
Project 1 and Project 2 sit at the two natural integration points (end of
Phase 2, end of everything). The adjustments below are refinements to load
and scope within that backbone, not a change to the backbone itself.

## 3. Concrete, evidence-based findings that warrant a decision

**Finding 1 — the meeting-length assumption is wrong by 5 minutes every
session (a ~6% overage compounded 29 times).** The actual meeting is 80
minutes; the master schedule and every deck's timing notes assume 85. Total
semester contact time, computed from the real Fall 2026 calendar (Labor Day
Mon Sep 7 off, Fall Break Mon Oct 12 off, Thanksgiving Mon Nov 23 AND Wed
Nov 25 both off, Week 15 has only the Monday meeting since Dec 9 is a
reading day, Week 3's Monday is the asynchronous primer not an in-person
meeting): **27 in-person 80-minute meetings = 2,160 minutes = 36 contact
hours** across the semester, not the ~2,295 minutes (38.25 hours) 27
meetings at 85 minutes would give. That's a real, if modest, standing
deficit against every slide deck's own pacing math — worth fixing at the
source (the master schedule's stated meeting length) rather than
re-discovering it deck by deck.

**Finding 2 — Week 4 carries the heaviest single-session cognitive load in
the semester**, and the load is in the *lecture*, not just the assignment
(the existing "lightest assignment" mitigation only softens the take-home
side). In one 80-minute Meeting A, students meet NumPy, pandas, *and*
Matplotlib for the first time, absorb a "trustworthiness interview"
(shape/dtypes/head/info/missing-counts), are introduced to the
docstring/type-hint convention, and learn Project 1 opens that same week.
This is five new things landing in one session for a zero-experience
cohort.

**Finding 3 — Week 7 (spatial data/CRS/GeoPandas) is the most specialized,
least-forward-connected topic in the required core.** Every other required
week's skill is used again later (pandas feeds everything; sweeps feed
optimization; optimization feeds Project 2; ML feeds Project 2). GIS/CRS
skills are used in Week 7 itself and as one optional Project 1 extension
path (map OR animation) — nothing downstream requires it. It is a
legitimate, architecture-relevant skill, but it is structurally different
from the other 13 required weeks in that removing it wouldn't break a later
week's prerequisite chain.

**Finding 4 — the flyer's own imagery implies a parametric/generative-
geometry interest area that the 15-week core doesn't currently teach at
all.** Not necessarily a problem — "data science and applied computation
for architects" is a coherent, complete course on its own — but it was
worth a conscious yes/no rather than leaving it as an unexamined gap
between what the course markets and what it teaches. Resolved below: no
parametric/geometry-scripting content anywhere in the course, including as
a post-course pointer.

## 4. Decisions (resolved August 17, 2026)

The instructor decided all four open questions from this review:

1. **Meeting length: re-baseline to 80 minutes — assumption corrected,
   content NOT to be trimmed.** 85 was wrong everywhere it appears, and
   that correction stands. However [UPDATED Aug 17]: the instructor will
   personally control in-room pacing against the real 80 minutes; no deck
   or handout content already designed against the 85-minute assumption
   should be cut or shortened on account of this correction. Content
   volume changes only happen when a specific, separately-decided change
   (like Decision 2 below) calls for one — never as a generic response to
   the 80-vs-85 gap.
2. **Week 4 load: split the toolchain introduction — IMPLEMENTED Aug 17.**
   Moved NumPy's first exposure into the end of Week 3B: a new handout cell
   [12] and a new deck slide (both validated, both build the same eight
   room areas from cell [9] into one array and convert it to square feet in
   one vectorized line, no loop) so Week 4 Meeting A now opens with a
   1-minute RECALL slide instead of a cold first look at NumPy, immediately
   before pandas/Matplotlib are introduced. Touched: `ARC500_Week03B_
   Spyder_Design_Rule_and_Function_Studio.pptx` (+1 slide, 36->37, plus
   speaker notes), `ARC500_Week03B_Student.py`/`_Instructor.py` (new cell
   [12], old AI-use-record cell renumbered [12]->[13]), the matching
   editable Word handout, `ARC500_Week04A_Toolchain_and_Data_as_Evidence.
   pptx` slide 6 (reframed PYTHON SYNTAX -> RECALL, same code/output kept
   for continuity with slide 8's "same three numbers" callback), and the
   Weeks 1-3 README, the master schedule's Week 3/4 entries, and the
   coverage map's Week 3/4 rows. No other slide or handout content in
   either deck was cut or altered — this was a pure content move, not a
   response to Decision 1's 80-minute correction.
3. **Week 7 (GIS/spatial): keep required.** No change to the core sequence.
4. **Geometry/parametric scripting: keep it OUT entirely, including as a
   post-course pointer.** Rejected even the "named next step" framing this
   review originally proposed. The `Beyond ARC500` capstone handout has
   been edited to remove all Grasshopper/Rhino/Dynamo/pyRevit/Galapagos/
   Wallacei references; its building-performance-simulation branch (Ladybug
   Tools/Honeybee) is kept but now described via its standalone Python
   packages rather than as a Grasshopper-native tool. The flyer's imagery
   should be read as illustrative of the broader field, not a scope
   commitment — no action needed on the flyer itself since that's a
   marketing asset outside this course package.

## 5. Proposed week-by-week topic layout (unchanged from the current
   package except where Section 4's decisions land — presented here as the
   layout for review, not as new content)

| Wk | Dates (MW) | Meeting A topic | Meeting B topic | New skill added | Builds directly on | Project tie-in |
|---|---|---|---|---|---|---|
| 1 | Aug 24/26 | Computational thinking; AI-collaborator protocol; Python execution model | Spyder IDE; `# %%` cells; tracebacks | Read/run/trace a script | — (entry point) | — |
| 2 | Aug 31/Sep 2 | Types, variables, units, expressions, f-strings | Unit-aware calculator with `assert` | Precise numeric expression + self-check | Week 1 execution model | — |
| 3 | Sep 7(*)/9 | *(async, ~40 min)* Booleans, if/else, boundary cases, functions | Compound conditions, `elif`, loops, accumulator, dict lookup, **+ a first look at NumPy arrays (shape, dtype, indexing) as the closing 10-15 min, per Decision 2** | Decision logic + reusable functions + first array contact | Week 2 expressions | — |
| 4 | Sep 14/16 | pandas Series/DataFrame building on Week 3B's arrays, then Matplotlib preview; trustworthiness interview; docstring convention | Clean a real dataset + one vectorized column + one plot | First real-data pipeline | Week 3B arrays (`df.method()`) | Project 1 assigned |
| 5 | Sep 21/23 | `groupby`; IQR/z-score outliers | Group + flag outliers on own dataset | Defensible aggregation & flagging | Week 4 cleaned data | P1 dataset/question checkpoint |
| 6 | Sep 28/30 | Question → encoding; `fig, ax`; animation | 3 static figures + 1 animated `.gif` | Honest visual argument | Week 5 grouped evidence | P1 visualization checkpoint |
| 7 | Oct 5/7 | Geometry, CRS, buffers, spatial join | Reproject + choropleth map | Spatial correctness | Week 4-6 pipeline habit | P1 spatial layer + compiled draft |
| 8 | Oct 12(*)/14 | *(no Meeting A — Fall Break)* | Peer clinic + Project 1 submission | — | Weeks 4-7 in full | **Project 1 due** |
| 9 | Oct 19/21 | Sensitivity question first, then NumPy sweep tools | 2D sweep + heatmap + assert-verified vectorization | Systematic "what matters most" exploration | Week 4-7 array/vector habit | Project 2 assigned |
| 10 | Oct 26/28 | Variables/objective/constraints; linear programs solved exactly | `linprog` on student's own P2 sub-problem | Exact formulation & solving | Week 9 sweep framing | P2 topic + linear-family proposal |
| 11 | Nov 2/4 | Gradient search; starting guess; local vs. global | `minimize` + multistart comparison | Continuous nonlinear search | Week 10 formulation habit | P2 nonlinear checkpoint |
| 12 | Nov 9/11 | Combinatorial search; hill-climbing; genetic algorithms | Hand-built GA/SA vs. brute-force baseline | Heuristic search + when it's worth it | Weeks 10-11 solver comparison habit | P2 heuristic-track checkpoint |
| 13 | Nov 16/18 | Regression; baseline; leakage | Fit + evaluate + fix an AI-drafted leakage bug | Honest predictive evaluation | Week 9-12 numerical fluency | P2 baseline-model checkpoint |
| 14 | Nov 30(**)/Dec 2 | Classification; confusion matrix; thresholds; model cards | Track-dependent: classifier OR refined regressor + model card | Decision-consequential evaluation | Week 13 evaluation habit | P2 model-card checkpoint |
| 15 | Dec 7 only | Predict→optimize→decide synthesis; presentations | *(no Meeting B — reading day)* | Chaining a fitted model into a solver | Everything above | **Project 2 due** + presentations |

(*) Labor Day / Fall Break — no in-person meeting that day.
(**) Thanksgiving break falls between Weeks 13 and 14 (Nov 23 & 25 both off).

## 6. Implementation status (updated August 17, 2026)

- **Decision 1** (meeting length): assumption corrected in this document
  and in the master schedule's framing language. Per the instructor's
  explicit instruction, no deck or handout content is being trimmed or cut
  because of the 80-vs-85 gap — the instructor will manage in-room pacing
  directly. Nothing further to implement for this decision.
- **Decision 2** (Week 4 load split): implemented. See Section 4 item 2 for
  exactly what changed, in which files, and how it was verified (deck
  validation, handout `py_compile` + a full run reproducing the exact
  numbers now printed in the CHECKS/INTERPRET line).
- **Decision 3** (Week 7 required): no change needed.
- **Decision 4** (geometry scripting removed): implemented — see the prior
  commit removing Grasshopper/Rhino/Dynamo/pyRevit/Galapagos/Wallacei
  references from the `Beyond ARC500` guide.

No lecture deck, handout, rubric, or starter code outside of Decisions 2
and 4's explicit scope was modified by this review or its implementation.
