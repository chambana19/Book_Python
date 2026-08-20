ARC 500 · EXPANDED WEEKS 1-3 FOUNDATIONS
Fall 2026 · two meetings per week · 80 minutes per meeting

WEEK 1

Meeting A
  ARC500_Week01A_Computational_Thinking_and_Responsible_AI.pptx
  Computational problem formulation, algorithms, decomposition,
  representation, abstraction, Python reading, tracing, model limitations,
  and responsible generative-AI use.

Meeting B
  ARC500_Week01B_Spyder_Installation_and_First_Program.pptx
  Handouts/ARC500_Week01B_Student.py
  Handouts/ARC500_Week01B_Instructor.py
  Installation choices, environment verification, Spyder interface, project
  folders, # %% cells, Console, Variable Explorer, first program, debugging,
  clean restart, and AI-use record.

WEEK 2

Meeting A
  ARC500_Week02A_Values_Variables_Units_and_Expressions.pptx
  Types, variables, names, arithmetic, precedence, units, conversion, strings,
  formatted output, Booleans, comparisons, floating-point display, and tests.

Meeting B
  ARC500_Week02B_Spyder_Architectural_Quantity_Studio.pptx
  Handouts/ARC500_Week02B_Student.py
  Handouts/ARC500_Week02B_Instructor.py
  Guided Spyder work culminating in a tested facade opening-ratio calculator.

WEEK 3

Meeting A (asynchronous primer, ~40 minutes — Mon Sep 7 is Labor Day, so this
week has no in-person Meeting A; completed before Wednesday)
  ARC500_Week03A_Asynchronous_Decisions_and_Functions_Primer.pptx
  Boolean/comparison recall, if/else, boundary cases, and def/parameters/
  function calls/return, closing with one short room-screening rule. Does
  not attempt to replace an 80-minute meeting; compound conditions, elif,
  for loops, the accumulator pattern, and dictionary lookup are introduced
  and practiced live in Meeting B instead.

Meeting B
  ARC500_Week03B_Spyder_Design_Rule_and_Function_Studio.pptx
  Handouts/ARC500_Week03B_Student.py
  Handouts/ARC500_Week03B_Instructor.py
  A room-schedule screening workflow built from one tested comparison into a
  reusable function applied across records. Closes with a 1-3 minute preview
  (cell [12]) that puts the same eight room areas into one NumPy array —
  shape, dtype, indexing, one vectorized conversion, no new grading — so
  Week 4 Meeting A opens from a recall instead of a cold first exposure to
  NumPy, pandas, and Matplotlib all at once.

COMPANION TEXT

  Weeks 1-3 track chapters 1 (Your First Python Program), 8 (Errors and
  Exceptions), 2 (Values, Variables, Calculations), 3 (Organizing Data), 4
  (Booleans and Decisions), 5 (Loops and Repetition), and 6 (Functions and
  Reusable Code) of the course companion text, "Introduction to
  Programming with Python" (J. Chun, chambana19/Book_Python) -- see the
  master schedule's Section 0 for the full chapter map and what
  "companion" does and does not mean here. [Chapter numbers corrected
  Aug 18 -- the book was reorganized/expanded since this reference was
  first written; verify against Section 0 before citing a chapter number
  anywhere else.] The one intentional divergence: the book installs and
  edits in VS Code; these weeks use Spyder instead (see SPYDER SETUP
  below).

SPYDER SETUP

  Spyder_Installation_and_Course_Environment_Guide.txt

Every student uses the shared arc500-f26 Conda environment created from
ARC500_environment.yml and verifies it with ARC500_environment_preflight.py.
Spyder is installed with its official standalone installer and connected to
that external environment. Course packages are not installed into Spyder's
internal environment from the IPython Console. This workflow follows current
Spyder 6 and GeoPandas guidance and keeps Weeks 7, 10, and 13 from becoming
unplanned installation labs.

FS25 REUSE AND REVISION

- Reused: computational-thinking prompts, input-process-output examples,
  short code traces, first-run/debug demonstrations, architectural quantities,
  and selected room/material examples from the 2025 foundation lectures and
  worksheets.
- Added explicitly defined beginner vocabulary: script, statement, comment,
  literal, variable, assignment, expression, function call, data type, int,
  float, string, Boolean, comparison, conditional, logical operator, loop,
  function, parameter, argument, and return. These explanations are adapted
  from the FS25 L3 Basics, L4 Data Type, L7 Boolean, L8 Control Flow,
  L10 Function, and Operator lectures.
- Revised: VS Code/Jupyter references are replaced with Spyder and .py files;
  syntax catalogs are reduced; every concept is connected to assumptions,
  units, expected output, tests, interpretation, and student activity.
- Reorganized: the previous collections-heavy Week 3 is reduced to only the
  list/dictionary structure required by the room-schedule example. Control
  flow and functions now appear in Week 3 because they are prerequisites for
  later data analysis, optimization, and machine learning.

COURSE WORKFLOW

Students may use generative AI for coding support, but must preserve an AI-use
record and be able to trace, test, modify, and explain every submitted line.
Before submission, each completed .py file should run from the top after a
Spyder kernel restart.
