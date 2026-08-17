# Parts I and II Revision Guide

## Purpose

This edition is written for students who are learning Python independently.
It uses short explanations, small runnable examples, predictable chapter
structure, and several levels of practice.

## Learning sequence

1. **Your First Python Program**: install the tools, distinguish the editor,
   terminal, script, and REPL, then run simple output and calculations.
2. **Values, Variables, and Calculations**: learn basic types, variables,
   arithmetic, input, conversion, f-strings, comments, and common errors.
3. **Organizing Data**: move from single values to lists, dictionaries, tuples,
   and sets without requiring loops.
4. **Booleans and Decisions**: build conditions from comparisons, combine them,
   and use `if`, `elif`, and `else`.
5. **Loops and Repetition**: repeat known operations with `for` and `while`,
   then add accumulators, dictionary iteration, `enumerate`, `zip`, `break`,
   and `continue`.

Each chapter uses only ideas introduced earlier. A list comprehension appears
only as an optional extension after students have learned an ordinary loop.

## Common chapter pattern

Every chapter contains:

- prerequisites and measurable learning outcomes;
- plain-language explanations followed by short code;
- stop-and-predict prompts;
- common mistakes and corrections;
- a five-level practice ladder: Read, Modify, Complete, Apply, Challenge;
- hints and worked solutions; and
- a checkpoint with answers.

Examples use consistent variable names and small architecture-related contexts
without requiring outside data or a separate submission. Each activity can be
completed by one student with the material in the chapter.

## Assembly file

Use `main_parts_i_ii_self_study.tex` to assemble the revised edition. It loads
the following chapter files:

- `Chapters/01_Your_First_Python_Program.tex`
- `Chapters/02_Values_Variables_Calculations_Self_Study.tex`
- `Chapters/03_Organizing_Data.tex`
- `Chapters/04_Booleans_and_Decisions.tex`
- `Chapters/05_Loops_and_Repetition.tex`

The original chapter files remain unchanged.

## Validation

- Five chapters are present and referenced by the assembly file.
- All chapters contain the common learning and practice sections.
- All 112 code blocks have unique labels.
- All 97 Python blocks were checked for syntax. One deliberately incorrect
  block is retained to teach students how to read a `SyntaxError`.
- The remaining non-interactive Python examples were executed independently.
- The prose scan found no flagged formulaic phrases and no em dashes.

The repository's original typesetting setup depends on `lix.sty` and
`preamble.tex`. Those dependencies are not included in the repository copy, so
PDF compilation requires restoring them or replacing the typesetting layer.

