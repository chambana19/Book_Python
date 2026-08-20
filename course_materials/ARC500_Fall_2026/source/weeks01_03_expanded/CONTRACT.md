# ARC 500 · Fall 2026 — Weeks 1-3 REVISION Contract (typography + content expansion)

You are revising an EXISTING, already-approved deck for ARC 500, Programming with
Python and Generative AI, Syracuse University School of Architecture. Audience:
graduate architecture students with **zero prior coding experience**. This is a
revision pass, not a new build.

## 0. What this pass is for

The instructor reviewed the Weeks 1-3 decks and asked for three things:

1. **Typography/layout consistency** — already fixed globally, see §1. You do not
   need to touch font sizes; you must simply not reintroduce per-slide overrides.
2. **Readability and learning sequence.**
3. **Complete, topic-driven source decks.** There is no numerical slide target
   or cap. Preserve the full foundation → application → practice → current-
   practice progression; the instructor will decide which slides to hide, skip,
   or shorten during an 80-minute meeting.

The instructor specifically asked that new content be weighted toward:
- **worked examples and "predict before you run" checks**,
- **diagrams / visual explanation** instead of prose columns,
- **dedicated vocabulary slides** for terms that currently share a crowded slide,
- **transfer exercises and self-application prompts** that let students reuse a
  complete workflow on an architectural or engineering problem.

Add `exercise` slides when they create meaningful practice, reflection, or
transfer. Do not add filler merely to reach a count; slide counts should vary
with the amount and difficulty of the topic.

---

## 1. The design system — read before you write a single slide

All layout and typography now lives in the shared design system at
`../_design/`
(`tokens.mjs`, `measure.mjs`, `layouts.mjs`, `build.mjs`). Read `tokens.mjs` and
`layouts.mjs` before authoring.

**Do not set font sizes, colors, or positions in a spec.** There is ONE type
scale (10 sizes, role-keyed). An audit of the old builder found 25 distinct sizes
with body text set 8 different ways depending only on which layout it landed in;
that is what this system removed. Legacy per-slide overrides — `headerFontSize`,
`cellFontSize`, `calloutFontSize` — are now IGNORED by the builder. Delete them
when you touch a slide; never add new ones.

The build prints a typography report per deck. **A clean deck reports 10 distinct
sizes and `no overflow warnings`.** If your deck reports an overflow, your text is
too long for its box — shorten it or move it to another slide. Do not ignore it:
an overflow means the renderer silently shrinks that text, which is exactly the
inconsistency this pass exists to remove.

### Layouts available

Existing (unchanged field schemas): `title`, `statement`, `outcomes` (exactly 4),
`agenda` (exactly 4), `process` (2-4 steps), `interface`, `twoColumn`, `code`,
`chart`, `table`, `exercise`, `closing` (exactly 4 takeaways).

**THREE NEW LAYOUTS — these are the main tool for this pass:**

**`definition`** — one term gets one slide. Use it for any term currently buried
in a shared `twoColumn`, and for every new term you introduce.
```json
{"layout":"definition","kicker":"Vocabulary","title":"<full sentence claim>",
 "term":"variable","termMono":true,
 "definition":"<plain language, 2-4 sentences, no jargon that isn't already taught>",
 "example":{"head":"area_m2 = length_m * width_m","body":"<why this example shows it>"},
 "exampleMono":true,"exampleLabel":"In practice",
 "note":"<optional: the single most common student misconception>","noteLabel":"Common confusion",
 "duration":2,"teaching":"<speaker notes>"}
```
`term` renders monospace by default (right for `int`, `f-string`, `def`); set
`"termMono":false` for prose terms like `abstraction`. `note` is optional but
strongly encouraged — it is where the real teaching lands.

**`anatomy`** — ONE line of code, exploded, with each part labeled. This is the
diagram layout the instructor asked for. Labels are positioned by monospace
character index, so each bracket lands exactly under its substring.
```json
{"layout":"anatomy","kicker":"Anatomy","title":"<claim>",
 "code":"area_m2 = length_m * width_m","codeSize":34,
 "parts":[{"match":"area_m2","label":"The name being created","body":"<1-2 short sentences>"},
          {"match":"=","label":"Assignment","body":"..."}],
 "duration":3,"teaching":"..."}
```
Rules: `code` must be a SINGLE line and should be ≤ 46 characters (longer lines
shrink below the readable size). `match` must appear in `code` — the build throws
if it does not; for a repeated character give `"at": <char index>` instead. Keep
`body` to about 60 characters; 4-6 parts is the sweet spot. Label rows are packed
automatically and cannot collide.

**`predict`** — commit before you run. The code shows NO output; students choose
an answer, then the instructor reveals the strip at the bottom.
```json
{"layout":"predict","kicker":"Predict before you run","title":"<claim>",
 "code":"length_m = 12\nwidth_m = 5\n\nprint(length_m / width_m)",
 "question":"What does this print?",
 "options":["2","2.4","2.0","an error"],"answer":1,
 "why":"<why the right answer is right AND why the tempting wrong one is tempting>",
 "duration":2,"teaching":"..."}
```
`answer` is a 0-based index. 3-4 options. Keep `why` to ~200 characters or it
overflows. Options render monospace by default; `"optionsMono":false` for prose.
**Every wrong option must be a real misconception a beginner would actually
hold** — not filler. The `predict` slide is most effective placed immediately
BEFORE the `code` slide that shows the same construct with its real output.

---

## 2. Hard constraints

- Standard meetings are nominally 80 minutes, but every presentation is a
  complete source deck with no slide-count cap. Do not remove or compress
  authored content merely to force an exact duration. The build prints the
  authored total; the instructor controls live pacing by hiding, skipping, or
  shortening optional slides.
- **Preserve all existing teaching content.** This material has already been
  through audit passes. You may split a slide, convert it to a better layout, or
  reword for clarity — you may NOT delete a concept, a worked example, an
  `exercise`, or an AI-audit section. If you think something should be cut, keep
  it and say so in your return summary instead.
- **Respect the concept ledger** (§3). Never use a construct before the week it is
  taught. This is the single most common defect found in past audits of this
  course.
- **Spyder only.** `# %%` cells, Ctrl+Enter, Variable Explorer, Editor/Console.
  Never mention Jupyter or notebooks.
- **Spec format:** compact JSON, ONE LINE PER SLIDE OBJECT (see any existing
  spec). Do not pretty-print the file — that has been reverted by hand before.
- Handouts are NOT part of this pass. Do not modify anything in `handouts/`.

---

## 3. Concept ledger — what students know, and when

Cumulative. Nothing may appear before the meeting that introduces it.

- **1A** — computational thinking; decomposition/abstraction/representation;
  algorithm; automation vs. judgment; the AI evidence trail; script/statement/
  comment; `print()`; arithmetic operators; expressions; literals; variables and
  assignment; types named informally (number/text/Boolean); syntax vs. runtime vs.
  logic error; state tracing by hand.
- **1B** — the Spyder IDE (Editor/Console/Variable Explorer); project folder and
  working directory; `import`; the kernel; `# %%` cells; reading a traceback.
- **2A** — `type()`; `int`/`float`/`str`/`bool`/`None` formally; naming with
  units; operator precedence; unit conversion; string concatenation; f-strings
  (including `:.1f` and `:.1%`); `float()`/`int()` conversion; comparison
  operators; `round()`; floating-point display quirks; `assert` (first use).
- **2B** — studio application of all 2A material. No new constructs.
- **3A** (asynchronous primer, 40 min) — Boolean recall; `if`/`else`; boundary
  cases; `def`, parameters, function call, `return`.
- **3B** — compound conditions (`and`/`or`/`not`); `elif`; `for` over a list
  (list/`[]` syntax defined at first use); the accumulator pattern; a minimal
  dictionary lookup; default arguments; `assert`-based tests.

**Not available anywhere in Weeks 1-3:** any third-party library (no numpy,
pandas, matplotlib), `while`, list/dict comprehensions, classes, recursion,
`try`/`except`, file I/O, slicing beyond simple indexing.

---

## 4. Your specific deck

Slide counts are topic-driven, not targets. Current complete source counts are:

| deck | current source slides | note |
|---|---:|---|
| 01a | 34 | computational thinking and the evidence loop |
| 01b | 34 | installation, Spyder, debugging, and environment preflight |
| 02a | 36 | values, types, expressions, and assertions |
| 02b | 34 | full Spyder studio progression |
| 03a | 38 | full asynchronous source deck; instructor selects pacing |
| 03b | 36 | live decisions, loops, and functions studio |

### Week 3A is special — read this if you are assigned 03a

Labor Day removes the in-person Meeting A. The distributed Week 3A file is
nevertheless the complete 38-slide source deck so asynchronous and self-directed
learners retain every explanation and example. Do not restore an `includeSlides`
subset or cut it to a numerical target. Use speaker notes and the delivery guide
to select the path appropriate to the cohort.

---

## 5. How to work

1. Read this contract, `_design/tokens.mjs`, `_design/layouts.mjs`, and your
   deck's current spec in full.
2. Read the two neighbouring decks' specs so your terminology matches theirs.
3. Revise the spec. Convert weak `twoColumn` slides to `definition`/`anatomy`;
   insert `predict` slides before code reveals; add worked examples.
4. Rebuild and CHECK THE REPORT:
   `cd "<builder dir>" && node build_weeks01_03_expanded.mjs <id>`
   Confirm: all authored slides are present, the closing remains last, the
   shared type scale is used, and the report says `no overflow warnings`.
5. Render and LOOK at it: `node montage.mjs <id>`, then Read
   `renders/week<id>_montage_full.png`. Fix anything that reads badly.
6. Any Python you put on a slide must be real. Run every snippet whose output
   you show—and every `predict` answer—in the declared course environment
   before claiming a result.

## 6. Return value

Compact JSON only: deck id, final slide count, total minutes, count of slides
added, which layouts you introduced and where, the typography report's "distinct
sizes" number and overflow count, and 2-3 real Python commands you ran with their
actual output.
