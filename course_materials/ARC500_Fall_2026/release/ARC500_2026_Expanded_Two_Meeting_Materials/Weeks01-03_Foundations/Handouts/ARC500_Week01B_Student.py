# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 1 lab · Spyder, the .py workflow, and your first calculations
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Open this file in Spyder.
  2. Sections are marked with  # %%  — click inside one and press Ctrl+Enter
     to run just that cell. Press F9 to run only the highlighted lines.
  3. Watch the Variable Explorer after each cell. Confirm the value AND the type.
  4. Predict the output before you run. Then compare.

LEARNING TARGETS
  - Run a .py file one # %% cell at a time and read the IPython console.
  - Use print, comments, expressions, and unit-bearing variable names.
  - Trace a short program by hand before running it.
  - Tell a syntax error from a runtime error from a modelling error.

AI-USE RULE
  You may use generative AI. You may not submit code you cannot trace, test,
  and explain. Keep a short record: one suggestion you accepted, one you
  modified, one you rejected — and why.
"""

# %% [1] Environment check
# QUESTION           Run the cell. Then change the message so it identifies you and one
#                    architectural interest.
# INPUTS/ASSUMPTIONS no inputs; Spyder is installed and this file is open
# METHOD             run the cell, read the console, then edit the printed text
# CHECKS/INTERPRET   You should see two readable lines and no error.

from pathlib import Path
import sys

print("ARC 500 script is running in Spyder")
print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())

# %% [2] Comments carry assumptions
# QUESTION           Add comments identifying units and the rectangular-room assumption.
# INPUTS/ASSUMPTIONS length and width in meters; the room is rectangular
# METHOD             state the units in comments, then multiply
# CHECKS/INTERPRET   The output remains 44.2; comments change interpretation, not execution.

length = 8.5
width = 5.2
print(length * width)

# %% [3] Predict expressions
# QUESTION           Before running, predict all four outputs. Then explain the effect of
#                    parentheses.
# INPUTS/ASSUMPTIONS four arithmetic expressions; no variables involved
# METHOD             predict each value, run, then compare against your prediction
# CHECKS/INTERPRET   Expected outputs: 14, 30, 4.0, 16.

print(8 + 2 * 3)
print((8 + 2) * 3)
print(12 / 3)
print(2 ** 4)

# %% [4] Room-area model
# QUESTION           Replace the TODO values with dimensions for a room. Use meaningful names
#                    and print the area.
# INPUTS/ASSUMPTIONS room name as text; length and width in meters
# METHOD             name each quantity with its unit, multiply, then print
# CHECKS/INTERPRET   For the example values, area is 44.2 m².

room_name = "TODO"
length_m = 0.0
width_m = 0.0
area_m2 = 0.0  # TODO
print(room_name)
print(area_m2)

# %% [5] Studio 2: trace values through cells
# QUESTION           Complete the trace table below BEFORE running this cell. Predict
#                    length_m, width_m, and area_m2 after each statement, then run and
#                    compare with the Variable Explorer.
# INPUTS/ASSUMPTIONS length_m and width_m in meters; area_m2 is calculated once, then
#                    width_m changes afterward
# METHOD             fill in every TODO cell in the table, run, then compare
# CHECKS/INTERPRET   Decide whether area_m2 updates automatically when width_m changes.

# TRACE TABLE (fill in each TODO before running)
# statement                     | length_m | width_m | area_m2
# length_m = 8.5                |   TODO   |   TODO  |   TODO
# width_m = 5.2                 |   TODO   |   TODO  |   TODO
# area_m2 = length_m * width_m  |   TODO   |   TODO  |   TODO
# width_m = 6.0                 |   TODO   |   TODO  |   TODO
# print(area_m2)   -> prints:   TODO

length_m = 8.5
width_m = 5.2
area_m2 = length_m * width_m

width_m = 6.0
print(area_m2)

# %% [6] Material allowance
# QUESTION           Calculate required flooring with a 15% cutting allowance. Estimate the
#                    result first.
# INPUTS/ASSUMPTIONS floor area in m2; an allowance expressed as a decimal fraction
# METHOD             multiply the area by (1 + rate) and keep the rate named
# CHECKS/INTERPRET   Expected raw result: 50.83 m².

area_m2 = 44.2
waste_rate = 0.15
required_m2 = 0.0  # TODO: expect 50.83
print(required_m2)

# %% [7] Scale up: a three-room takeoff
# QUESTION           Repeat cell [4] and [6]'s pattern for three rooms instead of one, then
#                    total the material required across all three.
# INPUTS/ASSUMPTIONS three named rooms (Gallery, Studio, Lobby) with length_m/width_m each;
#                    the same 15% waste_rate from cell [6]
# METHOD             for each room: compute area, then required material; total the three
#                    required amounts
# CHECKS/INTERPRET   Expected areas: 44.2, 30.0, 20.0 m². Expected required: 50.83, 34.5,
#                    23.0 m². Expected total required: 108.33 m².

gallery_length_m = 8.5
gallery_width_m = 5.2
gallery_area_m2 = 0.0  # TODO

studio_length_m = 6.0
studio_width_m = 5.0
studio_area_m2 = 0.0  # TODO

lobby_length_m = 5.0
lobby_width_m = 4.0
lobby_area_m2 = 0.0  # TODO

waste_rate = 0.15
gallery_required_m2 = 0.0  # TODO: expect 50.83
studio_required_m2 = 0.0  # TODO: expect 34.5
lobby_required_m2 = 0.0  # TODO: expect 23.0
total_required_m2 = 0.0  # TODO: expect 108.33

print(gallery_area_m2, studio_area_m2, lobby_area_m2)
print(gallery_required_m2, studio_required_m2, lobby_required_m2)
print(total_required_m2)

# %% [8] Debug a small program
# QUESTION           Run this cell. Fix ONLY the error it reports, then rerun. Repeat until
#                    it executes, then check whether the arithmetic model is correct.
# INPUTS/ASSUMPTIONS a deliberately broken program, stored as text so this handout itself
#                    remains valid Python, modeling a 10 m x 5 m room
# METHOD             predict the first failure, repair one defect at a time, rerun, and
#                    add a comment classifying each repaired defect (syntax, runtime, or
#                    modeling)
# CHECKS/INTERPRET   Expected result after all fixes: 50.

broken_program = '''room = "Studio
length_m = 10
width_m = five
area_m2 = length_m + width_m
print(area_m2)
'''

# Edit the program INSIDE broken_program, not the harness below. exec() asks Python to run
# that text as code. The harness labels the deliberately expected debug failure so it is
# not confused with an accidental error elsewhere in this handout.
try:
    exec(broken_program)
except (SyntaxError, NameError, TypeError) as error:
    print(f"EXPECTED DEBUG ERROR [cell 8] — {type(error).__name__}: {error}")
    print("Repair only that defect inside broken_program, then rerun this cell.")
else:
    if area_m2 != 50:
        print(
            "EXPECTED MODEL CHECK FAILURE [cell 8] — the code ran, but area_m2 is not 50. "
            "Repair the arithmetic model."
        )
    else:
        print("Cell 8 complete: syntax, runtime names, and the 50 m² model all check out.")

# %% [9] Exit challenge
# QUESTION           Create a three-line input-process-output description for one studio
#                    task, then implement the smallest possible Python version.
# INPUTS/ASSUMPTIONS one studio task of your choosing
# METHOD             write input, process, and output as comments before any code
# CHECKS/INTERPRET   Expected area: 36.0 m². Your explanation should reveal at least one
#                    assumption.

# INPUT:
# PROCESS:
# OUTPUT:

# Write your code below

# %% [10] AI audit and AI-use record
# QUESTION           Did generative AI change what you submitted, and can you defend every
#                    retained line?
# INPUTS/ASSUMPTIONS your own prompts and the suggestions you received this week
# METHOD             record tool, prompt, what you kept, what you changed, and how you tested
#                    it
# CHECKS/INTERPRET   you must be able to trace and test every line you submit

# Text between three quote marks can span multiple lines; Python treats it as one string.
ai_use_record = """
Tool/model:
Prompt:
Suggestion received:
What I accepted:
What I modified and why:
What I rejected and why:
How I tested it:
One limitation I found:
"""
print(ai_use_record)

# If you did not use generative AI, replace the record with:
# ai_use_record = "No generative AI used."

# %% ARCHITECTURAL TRANSFER — 3-minute exit check
# Reuse today's input → process → output → check workflow for this new case:
# 420 m² gross floor area; reserve 18% for circulation/services; test whether
# twelve 24 m² studios fit. Predict first, print the usable/requested/surplus
# areas with units, add one known-answer check, and name one omitted condition.
