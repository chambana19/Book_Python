# ARC 500 · Fall 2026 — Weeks 4-8 HISTORICAL revision record

> SUPERSEDED 2026-08-20. Numerical slide targets and exact 85-minute rules in
> this historical record must not be used. The current rule is a complete,
> topic-driven source deck with no slide-count cap; standard meetings are
> nominally 80 minutes and the instructor controls pacing. Follow
> `CONTRACT.md` and the package `COURSE_DESIGN_SYSTEM.md`.

You are revising an EXISTING, already-approved deck for ARC 500. This is a
revision pass, not a new build. **Read `CONTRACT.md` in this same directory
first** — it has the full concept ledger, the Project 1 cross-reference, and
the real-Python/pandas/GeoPandas verification protocol. Everything in it about
CONTENT still applies. This file governs the FORMAT/EXPANSION pass layered on
top of it.

## 0. What this pass is for

1. **Typography/layout consistency** — already fixed globally (§1). Do not
   reintroduce per-slide font overrides.
2. **Readability.**
3. **More content.** Target **32-36 slides per 85-minute meeting.** The
   instructor asked that new content be weighted toward worked examples /
   "predict before you run" checks, diagrams instead of prose columns, and
   dedicated vocabulary slides — NOT more `exercise` slides.

**The instructor specifically did NOT ask for more in-class practice/exercise
slides. Do not add new `exercise` slides beyond what is specified per-deck in
§4.** Every exercise/AI-audit slide that already exists must survive this pass
with its pedagogical content — title, prompt, scenario, numbers, steps —
UNCHANGED. You may re-typeset it onto the new layout system; you may NOT
reword, re-scope, or replace it.

**A confirmed failure mode from the Weeks 1-3 pass, read this before you
touch any exercise slide:** three separate revision agents on that pass
silently rewrote a protected exercise/AI-audit slide's entire scenario —
different prompt, different numbers, in one case introducing an untaught
construct — while genuinely believing they were "improving" it. All three were
caught by the verify pass and reverted. Do not repeat this. **Before you touch
any `exercise` slide, copy its exact `title`, `prompt`, and `steps` text into
your own scratch notes FIRST. When you finish the slide, diff your new JSON
field-by-field against that copy. Only layout/typography fields may differ.**

---

## 1. The design system

All layout and typography lives in:
`../_design/`
(`tokens.mjs`, `measure.mjs`, `layouts.mjs`, `build.mjs`) — the SAME system
already applied to Weeks 1-3. Read `tokens.mjs` and `layouts.mjs` before
authoring. **Do not set font sizes, colors, or positions in a spec.** Legacy
per-slide overrides (`headerFontSize`, `cellFontSize`, `calloutFontSize`) are
IGNORED by the builder — delete them if present.

A clean deck reports **10 distinct type sizes**. On overflow warnings, two
different situations apply — **do not treat them identically**:
- **`code` panel overflows are reliably real** — several existing slides in
  this block carry more lines of pandas/GeoPandas code than the fixed panel
  holds at the uniform font (some overshoot by 250+ points, roughly double
  what fits). Fix these by trimming shown code to its essential lines (mark
  elisions with `# ...`, matching this course's convention) or splitting the
  slide in two. Do not ship a code overflow unfixed.
- **`table` cell overflows are frequently FALSE POSITIVES**, especially in
  narrow (3-column, `callout`-present) tables. The estimate is a deliberately
  conservative average-character-width approximation and has already been
  confirmed wrong by rendering and looking (a cell flagged as needing 3 lines
  actually wrapped to 2 and fit with room to spare). **Before "fixing" a
  table-cell overflow, render the deck and Read the actual slide image.** If
  the text visibly fits, leave it — do not shorten good content to silence an
  estimate that isn't visually wrong. If it genuinely looks cramped or
  clipped, then shorten that cell.

### Layouts available

Existing: `title`, `statement`, `outcomes` (exactly 4), `agenda` (exactly 4),
`process` (2-4 steps), `twoColumn`, `code`, `chart`, `table`, `exercise`,
`closing` (exactly 4 takeaways). This block has never used `interface` (Spyder
IDE intro is Week 1) — do not introduce it.

**THREE NEW LAYOUTS — read `.codex_build/weeks01_03_expanded/CONTRACT.md`
section 1 for the full field schema of each, with examples:**
- **`definition`** — one term, one slide: term, plain-language definition,
  worked example, optional "common confusion" note. Use for `DataFrame`,
  `Series`, `groupby`, `IQR`, `z-score`, `fig`/`ax`, `FuncAnimation`,
  `GeoDataFrame`, `CRS`, and any other term currently buried in a shared
  `twoColumn`.
- **`anatomy`** — one line of code exploded, parts labeled by numbered chip
  (not leader lines — chips avoid the collisions leader lines caused in
  testing). `code` must be a single line, ≤ ~46 characters. Good candidates in
  this block: a `df.groupby(...).agg(...)` call, a `gdf.to_crs(...)` call, a
  `fig, ax = plt.subplots()` call.
- **`predict`** — code with no shown output, multiple choice, reveal strip.
  Place immediately BEFORE the `code` slide that shows the real output. Every
  wrong option must be a real pandas/GeoPandas beginner misconception (e.g.
  confusing `.loc` and `.iloc`, expecting `groupby` to return a DataFrame
  instead of a GroupBy object, forgetting a CRS reprojection changes the unit
  of `.area`) — verify the real behavior in the pinned course environment
  before writing the "why".

**A free source of expansion content, check this FIRST before writing brand
new slides:** `week04a.json`, `week04b.json`, `week05a.json`, and
`week05b.json` each author MORE slides than they render, via `includeSlides`.
The excluded slides (previously cut, presumably for time) are real,
already-written content sitting unused:
- 04a: authored slides 11, 14, 18, 20, 21 (all `code`) are excluded.
- 04b: authored slides 10 (`code`), 26 (`exercise`) are excluded.
- 05a: authored slides 14 (`code`), 15 (`table`), 16 (`code`), 20 (`twoColumn`) are excluded.
- 05b: authored slide 10 (`twoColumn`) is excluded.

Re-including previously-authored content is lower-risk than inventing new
material. If you re-include the excluded EXERCISE at 04b's authored slide 26,
it counts as restoring existing content, not adding a new exercise — the
"don't add exercises" rule is about inventing content that never existed, not
about surfacing something already written. Read each excluded slide before
deciding; some may be superseded by what's already rendered, in which case
leave them excluded and say so in your return summary.

---

## 2. Hard constraints

- Durations must total exactly **85 minutes** for every 85-minute meeting.
- Preserve all existing teaching content — see §0's protected-slide rule.
- Respect the concept ledger in `CONTRACT.md` §1 and the plan's Section 3 for
  your week. Never use a construct before the week it is taught.
- Spyder only. `# %%` cells, never Jupyter/notebooks.
- Compact JSON, one line per slide object — do not pretty-print.
- Handouts are NOT part of this pass. Do not modify anything in `handouts/`.
- Every pandas/NumPy/Matplotlib/GeoPandas output shown must be verified
  in the pinned course environment per `CONTRACT.md` §2 — this applies
  to `predict` answers and wrong options too, which are new to this pass.

---

## 3. Week 8 is special — read this if you are assigned 08b

`week08b.json` is a **13-slide, 85-minute peer-clinic-and-studio session**, not
a lecture — per the plan, Week 8 Meeting A does not exist (Fall Break), and
Meeting B is "Peer clinic on data provenance, reproducibility, and
interpretation, followed by Project 1 studio time and submission." Its two
`exercise` slides carry 12 and 46 minutes of unstructured/peer work
respectively — the deck is deliberately light on slide count because most of
the session is not slide-driven. **DO NOT expand this deck to 32-36 slides.**
Convert its existing layouts to the new system (e.g. its `table` slides may
benefit from a `callout`), fix its one real overflow warning, and stop. If you
believe a slide would genuinely help (e.g. a `definition` slide recapping
"reproducibility"), you may add up to 2-3 slides — but do not pad to hit a
target that does not apply to this session's structure. (Week 3A in the
Weeks 1-3 block is the same kind of exception, if you want to see the
precedent and how it was handled.)

---

## 4. Your specific deck

Slide counts below are RENDERED counts (respecting `includeSlides` where
present).

| deck | now | target | note |
|---|---|---|---|
| 04a | 25 | **33** | 10 `code` slides — several are strong `anatomy` candidates (the trustworthiness-interview calls). 5 authored-but-excluded `code` slides available, see §1. |
| 04b | 25 | **33** | 8 `exercise` already (do not add more) — expand via `definition`/`predict`/`anatomy` around the `code`/`twoColumn` slides. 1 excluded `code` + 1 excluded `exercise` available, see §1. |
| 05a | 26 | **34** | 5 `twoColumn` slides — IQR vs. z-score is a strong `twoColumn`-stays-`twoColumn` case (genuine two-sided comparison), but define `IQR` and `z-score` each on their own `definition` slide first. 4 excluded slides available, see §1. |
| 05b | 23 | **33** | 8 `exercise` already (do not add more). 1 excluded `twoColumn` available. |
| 06a | 28 | **34** | Static AND dynamic Matplotlib as co-equal — make sure `FuncAnimation` gets its own `definition` and consider an `anatomy` slide exploding a `FuncAnimation(...)` call. |
| 06b | 25 | **33** | 7 `exercise` already (do not add more). Fix the real code-panel overflow (see §1) as part of this pass. |
| 07a | 27 | **33** | GeoPandas-heavy — `CRS`, `EPSG`, `GeoDataFrame`, `reprojection`, `spatial join` are all strong `definition` candidates; a `gdf.to_crs(...)` or `.sjoin(...)` call is a strong `anatomy` candidate. |
| 07b | 24 | **33** | 6 `exercise` already (do not add more). |
| 08b | 13 | **13-16, DO NOT force to 32-36** | See §3. Studio/clinic session, not a lecture. |

## 5. How to work

1. Read this file, then `CONTRACT.md` in full, then `_design/tokens.mjs` and
   `_design/layouts.mjs`, then your deck's current spec.
2. Read the neighbouring decks' specs (the week before and after yours) so
   terminology matches.
3. Check §1's excluded-slide list for your deck before writing new content.
4. Revise the spec. Convert weak `twoColumn`s; insert `definition`/`anatomy`/
   `predict` slides; do not touch protected exercise/AI-audit content beyond
   re-typesetting it (see §0).
5. Rebuild and check the report:
   `cd "<builder dir>" && node build_weeks04_08.mjs <id>`
   Confirm slide count, exactly 85 minutes, 10 distinct sizes, no overflow
   warnings.
6. Render and look at it: `node montage.mjs <id>`, then Read
   `renders/week<id>_montage_full.png`. Fix anything that reads badly.
7. Verify every pandas/NumPy/Matplotlib/GeoPandas output and every `predict`
   answer/wrong-option in the pinned course environment.

## 6. Return value

Compact JSON: deck id, final slide count, total minutes, slides added, which
excluded slides you reused vs. left excluded and why, which new layouts you
used and where, the typography report's distinct-sizes number and overflow
count, and 2-3 real Python commands you ran with actual output.
