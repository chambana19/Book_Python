# ARC 500 · Fall 2026 — Weeks 4-8 Authoring Contract

You are authoring lecture decks and Spyder lab handouts for ARC 500,
Programming with Python and Generative AI, Syracuse University School of
Architecture. Audience: graduate architecture students with **zero prior
coding experience**. This contract governs Weeks 4-8 only.

**Read the finalized semester plan FIRST, in full, before writing anything:**
`../../ARC500_2026_Expanded_Two_Meeting_Materials/ARC500_2026_Semester_Restructure_Weeks01-15.txt`

Section 3 of that file gives your week's exact Meeting A topic, Meeting B
topic, assignment, and milestone — follow it precisely, do not improvise a
different topic list. Sections 1-2 explain the grading/weekly-assignment
policy your handout's structure must match. Sections 4-5 are the two
projects; Weeks 4-8 build directly toward Project 1 ("Evidence Before
Design"), whose full spec (Section 4) your week's content and handout
should visibly serve — read it so your examples aren't accidentally
mismatched to what Project 1 will actually ask students to do.

---

## 1. What already exists — read it, do not re-derive it

**Weeks 1-3 (built, fixed, approved).** Specs:
`../weeks01_03_expanded/specs/week01a.json` through `week03b.json`.
Read whichever ones matter for establishing your own week's prerequisite
ledger — do not assume a summary is accurate; verify by reading the actual
JSON. By the end of Week 3, students know: print/comments/arithmetic/
variables/expressions, IDE/kernel/traceback/import/module, types (int,
float, str, bool, None), naming with units, precedence, unit conversion,
f-strings (`:.1f`, `:.1%`), `round()`, comparison operators, Boolean logic,
`if/elif/else`, compound conditions, `for` loops over a **list** (defined
at first use), the accumulator pattern, `def`/parameters/return/default
arguments, a first minimal **dictionary**, and `assert`. They do NOT yet
know: any third-party library, `try/except`, file I/O beyond `pathlib`/
`sys` already covered, comprehensions, classes, or lambda.

**The layout/builder system (already proven, do not modify or invent a new
layout type):**
`build_weeks04_08.mjs`
Read it to see the exact field schema for each of the ten layout types
(title/statement/outcomes/agenda/process/twoColumn/code/table/exercise/
closing, plus interface/chart). Every new library, function, or piece of
jargon gets an explicit, VISIBLE (not speaker-notes-only) plain-language
definition with an example, at first use — this is the single most
consistent standard across every already-built week, and the single most
common defect the four-agent Weeks 1-3 audit found when it wasn't followed.

**Source keys** (for the `"sources"` field) are in
`sources.json` —
use only keys that exist there.

---

## 2. Numeric/output verification — REAL PYTHON, not reasoning

Unlike Weeks 1-3 (plain arithmetic, verifiable with a Node oracle), Weeks
4-7 are pandas/NumPy/Matplotlib/GeoPandas-heavy. DataFrame formatting,
dtype display, groupby output alignment, and float precision in this
context are genuinely hard to get right by reasoning alone — pandas 3.0
(the real installed version) already prints string-column dtypes as `str`,
not the `object` you may expect from older pandas docs or training data.

**Use the activated, pinned course Python environment** with pandas 3.0.5,
numpy 2.4.6, matplotlib 3.11.1, geopandas 1.1.4, scipy 1.17.1, and
scikit-learn 1.9.0.

**You MUST verify every single "output" field on every code slide, and
every expected-value comment in both handouts, by actually running the
code** — do not trust your own mental model of what pandas/numpy prints.
Pattern:
```bash
cat > /tmp/check.py << 'EOF'
import pandas as pd
df = pd.DataFrame({"area_m2": [35.0, 62.5, 44.2]})
print(df.describe())
EOF
python /tmp/check.py
```
Copy the ACTUAL stdout into your slide's `"output"` field verbatim (trim to
fit the slide's space budget, but never alter a value, alignment, or
dtype line to make it "look cleaner" than what real Python produced — if
real output is inconveniently long, choose a smaller/simpler example
instead, exactly as Weeks 1-3 chose binary-exact numbers to avoid float
noise **except** where the noise itself was the teaching point).

For plain Python-only arithmetic (rare in these weeks, but if it comes up),
verify the expression directly in the same pinned course environment.

**Matplotlib figures on slides**: you cannot embed a live chart image into
a `code` layout slide's output field (it's a text panel). Show the plotting
CODE on the code panel, and in `explainBody` describe precisely what the
figure shows/looks like (axes, what's plotted, one specific readable
feature) rather than fabricating a text "output" for a plot command that
produces no stdout. If you want to verify a plotting call doesn't error,
run it against the real matplotlib with a non-interactive backend:
```bash
cat > /tmp/check_plot.py << 'EOF'
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1,2,3],[4,5,6])
fig.savefig("/tmp/check_plot.png")
print("ok")
EOF
python /tmp/check_plot.py
```
This confirms the code actually runs without error — genuinely useful,
since a typo'd Matplotlib call is otherwise easy to miss until class.

**GeoPandas (Week 7)**: no live internet/basemap services are available to
students in class, and none should be assumed in your examples. Build
small geometries in-code (e.g., `shapely.geometry.Point`/`Polygon`
literals, or a tiny in-memory GeoDataFrame) rather than downloading
shapefiles. Verify CRS/reprojection/area calculations against the real
geopandas the same way as pandas above.

---

## 3. Weekly assignment / handout policy (from the finalized plan, Section 2)

- A "weekly assignment" IS that week's Meeting B Spyder studio handout,
  not a separate task.
- Every handout `# %%` cell needs the four headings, exactly matching the
  style already used in `handouts/week01b_student.py` and
  `handouts/week02b_student.py` (read one of those files first for the
  exact spacing/alignment convention): `# QUESTION`, `# INPUTS/ASSUMPTIONS`,
  `# METHOD`, `# CHECKS/INTERPRET`.
- **Starting Week 4, every handout's CHECKS/INTERPRET section must include
  at least one self-generated check applied to a slightly different input
  than the one worked through live** (a different row, case, parameter, or
  small scenario tweak), with 2-4 `assert` statements the student writes
  and runs themselves. This is the plan's "lightweight transfer safeguard"
  — do not skip it, it is a required, graded element every week from here
  on, not an optional nicety.
- Student handout: working scaffolding plus `# TODO:` gaps, each stating
  the expected result so students can self-check. Never leave a student
  version that crashes before any TODO is attempted.
- Instructor handout: complete, oracle-verified solutions, a
  `# COMMON ERROR:` note at each place beginners predictably slip, and a
  `# WHY THIS MATTERS:` line tying the exercise to design practice.
- Include one AI-audit section per week: a short block of plausible but
  defective AI-generated code (matching that week's library) for students
  to diagnose; instructor version names each defect. (Weeks 1-3 already
  established this pattern — follow it, don't reinvent it.)
- Spyder only: `# %%` cells, Ctrl+Enter, Variable Explorer, IPython
  console. Never mention notebooks/Jupyter.

## 4. Deck structure (per meeting, matching Weeks 1-3's proven shape)

1. `title`, 2. `statement`, 3. `outcomes` (exactly 4), 4. `agenda` (exactly
4) — then body slides (worked examples, trace/summary tables, process
slides, twoColumn concept-with-example slides) — then one or two `exercise`
slides — then `closing` (exactly 4 takeaways). There is no target or maximum
slide count. Standard meetings are nominally 80 minutes, while the distributed
file preserves the complete authored sequence and optional practice; the
instructor controls pacing locally. Week 8 Meeting A does not exist because of
Fall Break, so Week 8 is Meeting B only. Every new term gets the
established `"<Term>, defined"` treatment (a twoColumn or an inline gloss
in an existing slide's body/explainBody) with a concrete example — this
applies to `DataFrame`, `Series`, `method`, `keyword argument`, `groupby`,
`IQR`, `z-score`, `fig`/`ax`, `FuncAnimation`, `GeoDataFrame`, `CRS`, and
every other piece of new vocabulary your week introduces, no exceptions.

## 5. Week-specific notes (see the plan file for full detail — this is a
   quick-reference, not a substitute for reading Section 3)

- **Week 4**: opens with the "meet the toolchain" segment (NumPy, pandas,
  Matplotlib first contact together) — keep this to roughly the first
  third of Meeting A, then move into the pandas trustworthiness interview.
  Also teach a short docstring + basic type-hint convention here (this is
  a critique-driven fix — earlier drafts required these at Project 1
  without ever teaching them; you are the week that closes that gap).
  Meeting B needs the one small NumPy-derived-column + Matplotlib-scatter
  touch the plan specifies, not just a pure pandas deep-dive.
- **Week 5**: grouping AND outlier detection (IQR rule + z-score rule) as
  two explicitly named, separately taught skills, plus passing a function
  IN as an argument (`.agg()`, `.apply()`) as a named function-concept
  extension. Per the plan, Meeting B should have students apply this to
  their OWN Project 1 dataset from Week 4, not a generic shared one.
- **Week 6**: static AND dynamic (animated) Matplotlib as two co-equal
  modes of evidence — both weighted real content, not dynamic-as-an-aside.
- **Week 7**: GeoPandas fundamentals — geometry vs. attributes, CRS/EPSG,
  why area/length need a projected CRS, spatial join, static choropleth.
  No live downloads/basemap dependency (see Section 2 above).
- **Week 8**: Fall Break removes Meeting A entirely — there is no Week 8
  Meeting A deck. Build ONLY a Meeting B deck: a peer-clinic-and-studio
  session, not new content delivery. Keep it short and structural (how to
  give/receive a data-provenance critique, a submission checklist tied
  directly to Project 1's rubric, in-class work time) rather than
  introducing any new library or concept. No separate weekly assignment
  this week — Project 1 itself is due.

## 6. Return value

Return only a short JSON summary per week/meeting: file paths written,
slide count, duration total, concepts introduced, and any oracle-verified
outputs you're not fully confident about (flag rather than silently guess).
