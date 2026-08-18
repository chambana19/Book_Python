# Self-Study Chapter Style Guide

## Visual system

- Body text uses the document's black text on a white page.
- Learning-outcome and part-summary boxes use orange frames and white
  backgrounds.
- `NoteBox`, `SyntaxBox`, `ExplainBox`, and `TryBox` share one neutral blue
  frame and near-white background. Their title text, not a different color,
  communicates purpose.
- Code examples use the existing `\code{label}{language}{body}{caption}`
  command. Labels begin with the two-digit chapter number.
- Tables use the existing document typography and avoid additional accent colors.
- Charts use a restrained Matplotlib palette: `tab:blue` for the primary
  series, `tab:orange` for a comparison, and `tab:green` only when a third
  series is needed. Labels, markers, or line styles repeat the distinction so
  meaning never depends on color alone.
- Explanatory box-and-arrow diagrams (pipelines, workflows, anatomy figures
  built with `rounded_box()` in `scripts/generate_book_figures.py`) use a
  single neutral dark outline (`DARK`) for every box by default. Reserve color
  for two cases only: one accent on the single box the diagram exists to
  highlight (e.g., the geometry column in a GeoDataFrame, the activation in a
  neuron), or two colors on an arrow/label pair that already states the
  distinction in adjacent text (e.g., push vs. pop, true vs. false). Never
  alternate colors across steps purely for visual variety -- the book's own
  color conventions (orange for outcomes/summary boxes, blue for explanatory
  boxes) train readers to expect box color to mean something, so decorative
  alternation reads as an unexplained code the reader is failing to crack.

The restrained orange, blue, black, and white palette keeps the pages readable
without assigning a new color to each kind of activity.

## Heading hierarchy

- `\h{}`: one chapter title per file.
- `\hh{}`: main instructional sections.
- `\hhh{}`: practice levels or a necessary subsection.
- `\hhhh{}`: avoided in the beginner chapters unless a later topic genuinely
  requires a fourth level.

Headings use sentence case, short descriptive wording, and no trailing period.
Numbering and typography remain controlled by the textbook class.

## Chapter order

1. Opening explanation
2. Prerequisites box
3. Learning outcomes box
4. Concept sections with short examples
5. Common mistakes
6. Practice ladder
7. Practice solutions
8. Checkpoint and answers
9. Summary box

Parts follow a cumulative sequence: foundations, reusable programs, numerical
analysis, visual communication, geospatial applications, and computational
methods including algorithms, optimization, and machine learning. New library
chapters must state which earlier concepts they extend.

## Concept-before-syntax standard

Before presenting the syntax for a foundational idea, establish its mental
model. A complete treatment answers the following questions where relevant:

1. What is the concept, in precise but beginner-readable language?
2. What information or relationship does it represent?
3. When should a programmer choose it, and when should they not?
4. Which operations or state changes does it support?
5. What result type, return value, or side effect should the reader expect?
6. Which preconditions, invariants, units, shapes, or schemas must hold?
7. What concrete output, trace, comparison, or counterexample provides evidence?
8. What common alternative looks similar but has a different meaning?
9. What failure occurs when the rule is violated, and how should it be diagnosed?

Definitions should be followed by at least one ordinary example and, when the
distinction is easy to misunderstand, one contrasting or intentionally failing
example. Do not ask students to memorize a command whose decision boundary has
not been explained.

## Writing conventions

- Address the student directly when giving an action.
- Prefer short paragraphs and concrete verbs.
- Introduce a term before using it in code.
- Use one stable name for each concept instead of cycling through synonyms.
- Put units in variable names when they prevent ambiguity.
- Avoid throat-clearing introductions and inflated claims.
- Use ASCII double hyphens in LaTeX source instead of em dashes.

## Example conventions

- Main examples run independently unless explicitly labeled interactive or
  intentionally incorrect.
- Expected output follows code when it materially helps prediction or checking.
- An advanced shortcut appears only after the ordinary form is understood.
- Practice levels remain: Read, Modify, Complete, Apply, Challenge.
- Hints support Apply and Challenge work without giving away the full solution.
- Plotting examples use the Figure/Axes pattern, label measurement units, keep
  grids light, and close completed figures.
- Every major or multi-step snippet is followed by syntax analysis that
  explains inputs, method calls, returned objects, and the role of indentation.
- Longer applications separate preparation, calculation, visualization, and
  export into visible stages with comments and descriptive names.
- Code listings use a print-readable footnote size. If a complete application
  remains too long for comfortable reading, retain its conceptual stages in
  the chapter and provide the runnable file in `examples`.
- Every instructional graphic has a descriptive caption that can also serve as
  alternative text. Charts use markers, line styles, direct labels, position,
  or texture so meaning never depends on color alone.
