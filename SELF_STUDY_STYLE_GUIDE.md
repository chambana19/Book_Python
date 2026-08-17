# Self-Study Chapter Style Guide

## Visual system

- Body text uses the document's black text on a white page.
- Learning-outcome and summary boxes use `colframe=orange`, `colback=white`,
  and `arc=2mm`.
- `NoteBox` is reserved for prerequisites, stop-and-predict prompts, and short
  cautions.
- Code examples use the existing `\code{label}{language}{body}{caption}`
  command. Labels begin with the two-digit chapter number.
- Tables use the existing document typography and avoid additional accent colors.

The restrained orange, black, and white palette keeps the pages readable and
matches the established cover accent without assigning a different color to
each chapter.

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

