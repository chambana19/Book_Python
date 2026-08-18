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
  built with `rounded_box()`/`arrow()` in `scripts/generate_book_figures.py`)
  are strictly monochrome: every box defaults to a black outline (`INK`) on
  white fill (`PAPER`), and every arrow defaults to solid black. This is
  deliberate, not merely restrained -- the book's other conventions already use
  orange and blue to mean specific things (summary boxes, explanatory boxes,
  chart series), so any color on a box or arrow reads as an unexplained code
  the reader is expected to crack. Two exceptions carry real information
  instead of decoration:
  - `fill=True` inverts a box to black fill with white text, reserved for the
    single element a diagram exists to highlight (the geometry column in a
    GeoDataFrame, the activation in a neuron). At most one per diagram, and
    check that the box is wide enough for its text at that fill, since
    overflow past a filled box renders as invisible white-on-white.
  - `linestyle="--"` marks the secondary path of a genuine two-outcome branch
    whose distinction is also stated in adjacent text (true vs. false, push
    vs. pop, matching error vs. no error); the primary/expected path stays
    solid. Never alternate line style or fill across steps for variety alone.
  - When two arrows share a start point and diverge only slightly at first
    (e.g., a parent box branching to two children), give them visibly
    different departure points along the parent's edge rather than one
    shared vertex, so they read as two lines rather than a crossing knot.
  - `rounded_box()`'s boxstyle `pad` (currently `0.003`) visually expands the
    rendered outline beyond the nominal `(x, y, width, height)` given to
    `FancyBboxPatch`, on every side -- confirmed empirically via
    `patch.get_extents()`. This expansion scales linearly with `pad` and was,
    at the old `pad=0.012`, larger than `arrow()`'s `shrink`, which is the
    real reason arrows could render as touching or overlapping a box outline
    even when their coordinates looked correct on paper. Any future increase
    to `pad` must stay well under `shrink`'s point value (converted to axis
    fraction) or this comes back.
  - `arrow()`'s `shrink` argument (points, default 9) pulls the tail and head
    back *along the line's own direction*, not perpendicular to whatever box
    edge they touch. For an arrow that meets a box edge head-on
    (perpendicular, e.g. a horizontal arrow into a vertical edge), shrink
    alone gives a clean gap. For a diagonal arrow meeting an edge at a
    shallow angle -- a branch or tree diagram is the usual case -- shrink's
    perpendicular component falls off with the sine of that angle and can
    round to zero, so the line still touches the box outline no matter how
    large `shrink` is. In that case, give the coordinate itself a small
    manual offset (about 0.012-0.015 in axis fraction) perpendicular to the
    edge it touches, in addition to the default shrink.
  - Verify arrow gaps and text-in-box fit by rendering the real figure and
    measuring actual artist geometry, not by hand-estimating from nominal
    figure/box dimensions. Two concrete traps this caught: (1) a zoomed,
    low-resolution crop can visually round a real gap down to nothing, or
    make a fine gap look like contact -- compare
    `FancyArrowPatch.get_window_extent(renderer)` against the box patch's
    `get_window_extent(renderer)` instead (both correctly reflect
    `shrinkA`/`shrinkB` and the `pad` expansion above); (2) `layout="constrained"`
    can shrink an axes well below the figure's nominal width (observed ~19%
    smaller in a five-box pipeline diagram), so a subtitle computed to "fit"
    against the nominal figure width can still overflow the box as actually
    rendered -- measure each title/subtitle `Text.get_window_extent(renderer)`
    against its box's real extent the same way, for every `rounded_box()`
    call including the ones built inside a loop from a `steps`/`groups` list
    rather than a literal string in the call itself.
  Chart-style figures (line plots, scatter plots, confusion matrices) are a
  separate convention and keep the `tab:blue`/`tab:orange`/`tab:green` palette
  described above.

The restrained orange, blue, black, and white palette keeps the pages readable
without assigning a new color to each kind of activity.

## Page furniture

- The running header shows `Chapter N` on the left and the chapter's title on
  the right (`\leftmark`, populated by `\chaptermark` in `textbook.cls`).
  Chapter-opening pages suppress the header and footer entirely
  (`\thispagestyle{empty}`) for a quiet first page.
- The footer shows a `Contents` link on the left and `Page X of Y` on the
  right, with a thin rule above it (`\footrulewidth`). It does not carry a
  standing link to the reader roadmap; that page remains reachable from the
  table of contents.
- From Part I onward, every page carries short corner marks at the four
  corners of the text block (`\pagecornermarks` in `preamble.tex`, activated
  in `main.tex`), matching the class's margins. The cover, imprint, table of
  contents, and reader roadmap are exempt so their bespoke layouts are
  undisturbed.

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
