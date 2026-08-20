# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 2 lab · Values, units, and a transparent facade calculator · INSTRUCTOR SOLUTIONS
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Open this file in Spyder.
  2. Sections are marked with  # %%  — click inside one and press Ctrl+Enter
     to run just that cell. Press F9 to run only the highlighted lines.
  3. Watch the Variable Explorer after each cell. Confirm the value AND the type.
  4. Predict the output before you run. Then compare.

LEARNING TARGETS
  - Inspect a value's type and explain what operations that type allows.
  - Name variables so the architectural concept and its unit are visible.
  - Convert units and formats explicitly rather than silently.
  - Format results with f-strings without changing the stored value.

AI-USE RULE
  You may use generative AI. You may not submit code you cannot trace, test,
  and explain. Keep a short record (2-3 sentences per item): one suggestion
  you accepted, one you modified, one you rejected — and why.
"""

# %% [1] Inspect types
# QUESTION           Predict each type, run, and annotate the result.
# INPUTS/ASSUMPTIONS five literal values of five different types
# METHOD             print the value beside type(value) and annotate the result
# CHECKS/INTERPRET   Expected types: int, float, str, bool, and NoneType.

print(4, type(4))
print(3.6, type(3.6))
print("brick", type("brick"))
print(True, type(True))
print(None, type(None))

# %% [2] Unit-aware names
# QUESTION           Rename the variables so the architectural concept and unit are visible.
# INPUTS/ASSUMPTIONS a wall width and height with meaningless names
# METHOD             rename each variable to carry concept and unit, then recompute
# CHECKS/INTERPRET   Expected area: 36.0 m².

wall_width_m = 12
wall_height_m = 3.0
wall_area_m2 = wall_width_m * wall_height_m
print(wall_area_m2)

# %% [3] Operator and precedence check
# QUESTION           Predict, run, and explain both results, then add one assertion with a
#                    known answer for each (recall assert's syntax from earlier this week).
# INPUTS/ASSUMPTIONS two expressions differing only by parentheses
# METHOD             predict both, run both, explain what the grouping changes, then assert
#                    each known answer
# CHECKS/INTERPRET   Parentheses change the model, not merely the appearance; both assertions
#                    pass silently.

print(100 - 20 * 3)   # 40
print((100 - 20) * 3) # 240
assert 100 - 20 * 3 == 40
assert (100 - 20) * 3 == 240

# %% [4] Feet to meters
# QUESTION           Convert 25 feet to meters using a named factor and a plausibility check.
# INPUTS/ASSUMPTIONS a length in feet and the exact feet-to-meter factor
# METHOD             multiply by a named factor, then bracket-check the result
# CHECKS/INTERPRET   Expected length: 7.62 m; plausibility check: True.

length_ft = 25
feet_to_m = 0.3048
length_m = length_ft * feet_to_m
print(length_m)
print(7 < length_m < 8)

# %% [5] Format an architectural label
# QUESTION           Use an f-string to show the room, area to one decimal place, and unit.
# INPUTS/ASSUMPTIONS a room name and an unrounded area in m2
# METHOD             build an f-string with a .1f field and a unit suffix
# CHECKS/INTERPRET   Expected: Gallery: 44.2 m².

room = "Gallery"
area_m2 = 44.234
label = f"{room}: {area_m2:.1f} m²"
print(label)

# %% [6] Convert text
# QUESTION           Convert both strings and calculate area. Then try empty text, a word,
#                    zero, and a negative dimension; state which cases should be rejected and
#                    why.
# INPUTS/ASSUMPTIONS two dimensions that arrived as text, plus four edge-case inputs
# METHOD             convert each with float() before any arithmetic; test edge cases one at a
#                    time and comment on the outcome
# CHECKS/INTERPRET   Expected: 44.2. Empty text and a word both raise ValueError and must be
#                    rejected before arithmetic; zero and a negative number convert without
#                    error but are physically invalid dimensions.

length_text = "8.5"
width_text = "5.2"
length_m = float(length_text)
width_m = float(width_text)
area_m2 = length_m * width_m
print(area_m2)

# Edge case 1 -- empty text: float("") raises "ValueError: could not convert string to
# float: ''". Reject: there is no numeric value at all; the program must not guess one.

# Edge case 2 -- a word: float("abc") raises "ValueError: could not convert string to
# float: 'abc'". Reject: text that is not a number cannot become a measurement.

# Edge case 3 -- zero: converts without error.
print(float("0"))
# Reject anyway: a 0 m dimension describes a degenerate wall with no length or width, even
# though Python accepts it.

# Edge case 4 -- a negative number: converts without error.
print(float("-5"))
# Reject anyway: a negative length is not physically possible; float() has no concept of
# "physically valid," so that check must come from your own code, not from the conversion.

# %% [7] Boolean comparison
# QUESTION           Store whether the room meets a 40 m² minimum. Then test a case below,
#                    equal to, and above the threshold.
# INPUTS/ASSUMPTIONS a measured area and a programme minimum, both in m2
# METHOD             compare with >= and store the boolean result for three areas: below,
#                    equal to, and above the minimum
# CHECKS/INTERPRET   Expected: False, True, True (equal counts as meeting the minimum).

area_m2 = 44.2
minimum_m2 = 40.0
meets_minimum = area_m2 >= minimum_m2
print(meets_minimum)

area_below_m2 = 38.0
meets_minimum_below = area_below_m2 >= minimum_m2
print(meets_minimum_below)

area_equal_m2 = 40.0
meets_minimum_equal = area_equal_m2 >= minimum_m2
print(meets_minimum_equal)

# %% [8] Façade opening ratio
# QUESTION           Calculate and format the opening ratio as a percentage. Then test 0,
#                    half, full, and excessive opening areas; assert the three valid cases
#                    and flag the invalid one.
# INPUTS/ASSUMPTIONS facade dimensions in meters and a window area in m2
# METHOD             divide window area by facade area, format each as a percentage, assert
#                    the valid cases, and print a warning flag for the invalid case
# CHECKS/INTERPRET   The baseline result is approximately 25.9%; the four test ratios are
#                    0.0%, 50.0%, 100.0%, and 123.5% (invalid: exceeds 100%).

facade_width_m = 18.0
facade_height_m = 9.0
window_area_m2 = 42.0
facade_area_m2 = facade_width_m * facade_height_m
opening_ratio = window_area_m2 / facade_area_m2
print(f"Opening ratio: {opening_ratio:.1%}")

ratio_none = 0 / facade_area_m2
ratio_half = 81 / facade_area_m2
ratio_full = 162 / facade_area_m2
ratio_excess = 200 / facade_area_m2

print(f"No opening:        {ratio_none:.1%}")
print(f"Half facade:       {ratio_half:.1%}")
print(f"Full facade:       {ratio_full:.1%}")
print(f"Excessive opening: {ratio_excess:.1%}")

assert ratio_none == 0.0
assert ratio_half == 0.5
assert ratio_full == 1.0

is_invalid_geometry = ratio_excess > 1.0
print(f"WARNING -- opening exceeds facade area, invalid geometry: {is_invalid_geometry}")

# %% [9] A full elevation check: four facades, one code limit
# QUESTION           Apply cell [8]'s ratio pattern to all four elevations of the same
#                    building, then count how many meet a 40% maximum opening-ratio code.
# INPUTS/ASSUMPTIONS four facades (North, South, East, West), each with its own width_m,
#                    height_m, and window_area_m2; max_ratio = 0.40
# METHOD             repeat cell [8]'s two-line pattern (area, then ratio) for each facade,
#                    compare each ratio against max_ratio with <=, then add the four Boolean
#                    results together (True counts as 1, False as 0)
# CHECKS/INTERPRET   Expected ratios: North 25.9%, South 30.0%, East 16.7%, West 50.0%.
#                    Expected: 3 of 4 facades meet code (West does not).

max_ratio = 0.40

north_width_m = 18.0
north_height_m = 9.0
north_window_m2 = 42.0
north_area_m2 = north_width_m * north_height_m
north_ratio = north_window_m2 / north_area_m2
north_ok = north_ratio <= max_ratio

south_width_m = 20.0
south_height_m = 9.0
south_window_m2 = 54.0
south_area_m2 = south_width_m * south_height_m
south_ratio = south_window_m2 / south_area_m2
south_ok = south_ratio <= max_ratio

east_width_m = 12.0
east_height_m = 9.0
east_window_m2 = 18.0
east_area_m2 = east_width_m * east_height_m
east_ratio = east_window_m2 / east_area_m2
east_ok = east_ratio <= max_ratio

west_width_m = 12.0
west_height_m = 9.0
west_window_m2 = 54.0
west_area_m2 = west_width_m * west_height_m
west_ratio = west_window_m2 / west_area_m2
west_ok = west_ratio <= max_ratio

print(f'North: {north_ratio:.1%}  meets code: {north_ok}')
print(f'South: {south_ratio:.1%}  meets code: {south_ok}')
print(f'East:  {east_ratio:.1%}  meets code: {east_ok}')
print(f'West:  {west_ratio:.1%}  meets code: {west_ok}')

passing_count = north_ok + south_ok + east_ok + west_ok
print('Facades meeting code:', passing_count, 'of 4')

# COMMON ERROR: writing "if north_ok == True" out of habit. north_ok already
# IS the Boolean; comparing it to True is redundant, and comparing a Boolean
# to True with == is a common tell that a student hasn't yet trusted the
# value's own type.
# WHY THIS MATTERS: north_ok + south_ok + east_ok + west_ok works because
# Python treats True as 1 and False as 0 in arithmetic — this is a real,
# useful pattern for counting how many of several conditions passed, not a
# trick specific to this example. It will reappear whenever you need a count
# instead of four separate print statements.

# %% [10] AI-code audit
# QUESTION           Repair the code and add one known-answer test.
# INPUTS/ASSUMPTIONS plausible but defective AI-generated code
# METHOD             identify the type error, repair it, then add a known-answer test
# CHECKS/INTERPRET   The original code repeats text three times; it does not calculate area.

wall_width_m = float("12")
wall_height_m = 3.0
wall_area_m2 = wall_width_m * wall_height_m
print(f"{wall_area_m2:.1f} m²")
assert wall_area_m2 == 36.0

# %% [11] AI audit and AI-use record
# QUESTION           Did generative AI change what you submitted, and can you defend every
#                    retained line?
# INPUTS/ASSUMPTIONS your own prompts and the suggestions you received this week
# METHOD             record tool, prompt, what you kept, what you changed, and how you tested
#                    it
# CHECKS/INTERPRET   you must be able to trace and test every line you submit

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

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Repair a wall-finish takeoff with wall_length_m="12", height_m=3,
# openings_m2=6, and waste_percent=8. Expected: gross 36.0 m², net 30.0 m²,
# required 32.4 m² after multiplying net by 1.08. Require conversion, explicit
# grouping, units in the output, a known-answer assertion, and an invalid-input
# rule such as openings_m2 <= gross_area_m2.
