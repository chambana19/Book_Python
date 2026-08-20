# ARC 500 course design system

Last revised: 2026-08-20

## Governing principle

Every presentation is a complete source deck. There is no target, maximum, or normalization rule for slide count. Counts vary with the subject, the number of worked examples, and the amount of optional practice. The instructor decides what to hide, skip, or shorten for a particular meeting; the distributed source is not cut merely to make every deck the same length.

The semester should nevertheless feel like one course. Consistency comes from the visual language, learning sequence, evidence standards, and handout structure—not identical slide counts.

## Visual system

- Canvas: 16:9 widescreen.
- Primary typeface: Aptos/Arial-compatible sans serif; monospace for code and literal data.
- Shared projected type scale: 60, 48, 40, 28, 24, 20, 16, and 12 pt. Body text should normally remain at 20–24 pt; code should normally remain at 16–18 pt. Twelve-point text is reserved for footers, sources, and compact metadata.
- Palette: charcoal/ink and white for primary contrast; one course blue for structure and emphasis; light neutral panels for grouping; green/red only for semantically meaningful pass/risk distinctions. Color must never be the only carrier of meaning.
- Titles state the slide’s claim or question. Kicker labels identify the role: principle, method, vocabulary, predict-before-run, read-the-data, visual evidence, transfer, 2026 practice horizon, or closing.
- Dark slides are limited to openers and closings. Most explanatory slides use a white field so code, tables, figures, and diagrams remain readable when projected or printed.

The implementation lives in `.codex_build/_design/`. All lecture and project-template builders call the same design system.

## Repeated slide grammar

Use the smallest layout that makes the relationship visible:

- `statement`: one defensible principle plus its boundary.
- `process`: a three- or four-step workflow with explicit direction.
- `anatomy`: one expression decomposed into named parts.
- `twoColumn`: a contrast, distinction, or paired responsibility.
- `table`: exact comparisons, thresholds, schemas, or audit evidence.
- `code`: runnable code on the left; meaning, output, and limits on the right.
- `predict`: a commitment before execution, followed by a visible answer and explanation.
- `chart` or `figure`: the visual carries the evidence; text explains the bounded reading.
- `exercise`: a transfer task with an observable completion condition.
- `closing`: four or fewer durable takeaways and an exit prompt.

Do not convert a relationship into prose merely to save space. Split genuinely different ideas into separate slides. A complete deck may contain optional slides, additional worked cases, and state-of-practice extensions.

## Learning sequence across a meeting

The default sequence is:

1. Name the decision or evidence question.
2. Recall the smallest prerequisite.
3. Introduce one new term or method in plain language.
4. Predict a result before execution.
5. Run or inspect a complete worked example.
6. Verify with a known answer, boundary case, baseline, tolerance, or untouched test.
7. Transfer the pattern to a different architectural case.
8. State what the result supports and what it does not support.
9. Connect the core method to current professional practice when useful.

This sequence is more important than slide count. Optional slides should be labeled by role so the instructor can make pacing decisions without breaking the conceptual chain.

## Content depth

Each topic block should include four levels:

- Foundation: vocabulary, representation, and the smallest correct example.
- Application: one complete architecture/engineering case with units and context.
- Practice: easy, medium, and hard or core, practice, and extension tasks with explicit checks.
- Horizon: a concise 2026 professional or research connection, clearly distinguished from required beginner mastery.

Examples must be runnable and sufficiently complete to expose setup, input assumptions, intermediate state, output, verification, and interpretation. A short syntax fragment may introduce one line, but it cannot be the only example for a method used in an assignment or project.

## Visual evidence and accessibility

- Prefer native diagrams, plots, process flows, annotated tables, and code/output pairings over decorative stock imagery.
- Every figure needs a question, labeled axes, units, a readable legend when needed, and a bounded interpretation.
- Directly label the important outlier, threshold, optimum, residual pattern, or spatial mismatch when the visual claim depends on it.
- Use redundant cues: text labels, position, marker shape, line style, or pattern in addition to color.
- Add useful alternative text to raster figures and diagrams. Complex visuals also need a concise explanation in speaker notes or adjacent text.
- Verify that authored image descriptions survive export into PowerPoint's picture alt-text field; source-only metadata is not sufficient.
- Record source URLs in slide notes. A deck using external material should include an explicit sources/resource slide or companion resource document.

## Code and handout contract

All student scripts use Spyder cells and the same four headings:

`QUESTION` / `INPUTS/ASSUMPTIONS` / `METHOD` / `CHECKS/INTERPRET`

Instructor examples should include type hints and docstrings where those conventions are assessed, assertions or explicit checks, relative paths, reproducible seeds where randomness matters, and saved outputs with units. Unfinished student scaffolds must stop loudly at the first required TODO and must not export plausible placeholder CSV, PNG, GIF, or metric files.

## Evidence language

- A data audit does not prove the data are representative.
- An outlier flag does not prove a row is erroneous.
- A finite grid establishes the best sampled candidate, not a continuous global optimum.
- Linear programming guarantees that at least one optimal extreme point exists when a finite optimum exists; it does not guarantee uniqueness.
- A heuristic result is best-known under the stated budget and seeds unless an exact baseline proves otherwise.
- Cross-validation describes development variability; it is not an individual prediction interval.
- RMSE is not a prediction interval.
- Thresholds and feature specifications are selected on development/validation evidence; the final test is opened once.
- A surrogate proposes candidates. Adoption requires non-surrogate confirmation, measurement, simulation, or expert review.

## Required QA before release

1. Build every changed deck from its authored specification.
2. Require zero automated overflow warnings.
3. Render every changed deck and inspect both the full montage and any dense code/table slide at full size.
4. Confirm the closing slide remains last and optional horizon slides occur before it.
5. Compile and smoke-test instructor scripts; verify student scripts stop at intentional TODO gates with no misleading artifacts.
6. Validate project starters and complete synthetic fixtures.
7. Generate `course_manifest.yml` and compare local/repository hashes.
8. Exclude `.inspect.ndjson`, render caches, `__pycache__`, `.pyc`, and ad-hoc outputs from the student/GitHub release.
