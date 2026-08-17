# Part III Revision Guide

## Purpose

Part III moves students from short scripts to reusable and reliable programs.
The chapters retain the independent-study pattern established in Parts I and
II while introducing one new responsibility at a time.

## Learning sequence

1. **Functions and Reusable Code**: define, call, parameterize, and compose
   focused functions before using them in error-handling examples.
2. **Useful Built-in Functions**: organize familiar built-ins, add numeric and
   boolean summaries, and introduce focused standard-library imports.
3. **Errors and Exceptions**: classify errors, read tracebacks, catch specific
   exceptions, validate input, and raise clear errors from functions.
4. **Copying Data Safely**: distinguish equality from identity, recognize
   aliases, and choose shallow, targeted, or deep copies.
5. **Files and Paths**: work with paths, text, CSV, and JSON after functions and
   exception handling are available.

This order removes the earlier prerequisite inversion in which exceptions were
presented before functions. It also replaces the large jump into advanced file
processing with a gradual path from small text files to structured formats.

## Content boundaries

- Variable-length parameters, custom classes, and advanced copying hooks are
  deferred.
- `map()` and `filter()` are omitted because ordinary loops and comprehensions
  are clearer at this stage.
- Spreadsheet libraries, large binary-file processing, and bulk folder
  operations remain in later specialized material.
- Every main example is self-contained. Interactive and deliberately failing
  examples are clearly identified.

## Common chapter pattern

Every chapter contains prerequisites, measurable outcomes, short examples,
prediction prompts, common mistakes, five practice levels, solutions, a
checkpoint with answers, and a summary box.

## Assembly file

Use `main_part_iii_self_study.tex` to assemble Part III by itself. The active
`main.tex` places these chapters after Parts I and II and before the numerical
and data-analysis chapters.

## Validation targets

- one chapter heading and a consistent heading hierarchy per file;
- orange frames, white backgrounds, and 2 mm corners for learning and summary boxes;
- unique code labels and syntactically valid Python examples;
- independent execution for non-interactive examples;
- no references to semester-specific deliverables; and
- a stable Read, Modify, Complete, Apply, Challenge practice ladder.

