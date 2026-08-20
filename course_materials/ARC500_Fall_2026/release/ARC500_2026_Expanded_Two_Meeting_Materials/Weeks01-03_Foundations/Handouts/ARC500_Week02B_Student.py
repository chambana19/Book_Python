# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 2 lab · Values, units, and a transparent facade calculator
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

a = 12
b = 3.0
c = a * b
print(c)

# %% [3] Operator and precedence check
# QUESTION           Predict, run, and explain both results, then add one assertion with a
#                    known answer for each (recall assert's syntax from earlier this week).
# INPUTS/ASSUMPTIONS two expressions differing only by parentheses
# METHOD             predict both, run both, explain what the grouping changes, then assert
#                    each known answer
# CHECKS/INTERPRET   Parentheses change the model, not merely the appearance; both assertions
#                    pass silently.

print(100 - 20 * 3)
print((100 - 20) * 3)
# TODO: add one assert statement for each known answer

# Set this to True only after both of your own assert statements pass. This deliberate
# NotImplementedError is an EXPECTED TODO STOP, not a mysterious Python failure.
cell_3_assertions_complete = False  # TODO: change to True after adding both assertions
if not cell_3_assertions_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 3]: add and run both known-answer assertions, "
        "then set cell_3_assertions_complete = True."
    )

# %% [4] Feet to meters
# QUESTION           Convert 25 feet to meters using a named factor and a plausibility check.
# INPUTS/ASSUMPTIONS a length in feet and the exact feet-to-meter factor
# METHOD             multiply by a named factor, then bracket-check the result
# CHECKS/INTERPRET   Expected length: 7.62 m; plausibility check: True.

length_ft = 25
feet_to_m = 0.3048
length_m = 0.0  # TODO: expect 7.62
print(length_m)

if abs(length_m - 7.62) > 1e-9:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 4]: calculate length_m with the named conversion factor."
    )

# %% [5] Format an architectural label
# QUESTION           Use an f-string to show the room, area to one decimal place, and unit.
# INPUTS/ASSUMPTIONS a room name and an unrounded area in m2
# METHOD             build an f-string with a .1f field and a unit suffix
# CHECKS/INTERPRET   Expected: Gallery: 44.2 m².

room = "Gallery"
area_m2 = 44.234
label = "TODO"
print(label)

if label != "Gallery: 44.2 m²":
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: replace label with the required one-decimal f-string."
    )

# %% [6] Convert text
# QUESTION           Convert both strings and calculate area. Then try empty text, a word,
#                    zero, and a negative dimension; state which cases should be rejected and
#                    why.
# INPUTS/ASSUMPTIONS two dimensions that arrived as text, plus four edge-case inputs
# METHOD             convert each with float() before any arithmetic; test edge cases one at a
#                    time and comment on the outcome
# CHECKS/INTERPRET   Expected: 44.2. State, in a comment, which of the four edge cases should
#                    be rejected and why.

length_text = "8.5"
width_text = "5.2"
length_value_m = None  # TODO: convert length_text with float()
width_value_m = None   # TODO: convert width_text with float()
text_area_m2 = None    # TODO: multiply the two converted values
print(text_area_m2)

# TODO: try each edge case in turn ("", "abc", "0", "-5") with float() and comment on what
# happens and whether it should be rejected

if (
    length_value_m is None
    or width_value_m is None
    or text_area_m2 is None
    or abs(text_area_m2 - 44.2) > 1e-9
):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 6]: convert both text values and calculate 44.2 m² "
        "before testing the edge cases."
    )

# %% [7] Boolean comparison
# QUESTION           Store whether the room meets a 40 m² minimum. Then test a case below,
#                    equal to, and above the threshold.
# INPUTS/ASSUMPTIONS a measured area and a programme minimum, both in m2
# METHOD             compare with >= and store the boolean result for three areas: below,
#                    equal to, and above the minimum
# CHECKS/INTERPRET   Expected: False, True, True (equal counts as meeting the minimum).

minimum_m2 = 40.0

# Print the three cases in the order the METHOD line names them: below, equal, above.
area_below_m2 = 38.0
meets_minimum_below = False  # TODO: compare area_below_m2 with minimum_m2 using >=
print(meets_minimum_below)

# TODO: complete and print the equal and above cases. The three printed lines should read
# False, True, True.
area_equal_m2 = 40.0
meets_minimum_equal = False  # TODO: compare with >=
print(meets_minimum_equal)

area_above_m2 = 44.2
meets_minimum_above = False  # TODO: compare with >=
print(meets_minimum_above)

if (meets_minimum_below, meets_minimum_equal, meets_minimum_above) != (False, True, True):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 7]: the below/equal/above results must be "
        "False, True, True."
    )

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
facade_area_m2 = 0.0       # TODO: facade_width_m * facade_height_m
opening_ratio = 0.0        # TODO: window_area_m2 / facade_area_m2
ratio_none = 0.0           # TODO: 0 / facade_area_m2
ratio_half = 0.0           # TODO: 81 / facade_area_m2
ratio_full = 0.0           # TODO: 162 / facade_area_m2
ratio_excess = 0.0         # TODO: 200 / facade_area_m2
is_invalid_geometry = False  # TODO: ratio_excess > 1.0

if (
    abs(opening_ratio - (42 / 162)) > 1e-9
    or (ratio_none, ratio_half, ratio_full) != (0.0, 0.5, 1.0)
    or ratio_excess <= 1.0
    or not is_invalid_geometry
):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8]: calculate the baseline and four test ratios, "
        "assert the three valid cases, and flag the excessive case."
    )

print(f"Opening ratio: {opening_ratio:.1%}")
print(f"Excessive opening: {ratio_excess:.1%}; invalid geometry: {is_invalid_geometry}")

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
north_ratio = 0.0  # TODO
north_ok = False  # TODO: compare north_ratio with max_ratio using <=

south_width_m = 20.0
south_height_m = 9.0
south_window_m2 = 54.0
south_ratio = 0.0  # TODO
south_ok = False  # TODO

east_width_m = 12.0
east_height_m = 9.0
east_window_m2 = 18.0
east_ratio = 0.0  # TODO
east_ok = False  # TODO

west_width_m = 12.0
west_height_m = 9.0
west_window_m2 = 54.0
west_ratio = 0.0  # TODO
west_ok = False  # TODO

print(f'North: {north_ratio:.1%}  meets code: {north_ok}')
print(f'South: {south_ratio:.1%}  meets code: {south_ok}')
print(f'East:  {east_ratio:.1%}  meets code: {east_ok}')
print(f'West:  {west_ratio:.1%}  meets code: {west_ok}')

passing_count = 0  # TODO: add all four _ok Booleans together
print('Facades meeting code:', passing_count, 'of 4')

expected_ratios = (42 / 162, 54 / 180, 18 / 108, 54 / 108)
actual_ratios = (north_ratio, south_ratio, east_ratio, west_ratio)
if any(abs(actual - expected) > 1e-9 for actual, expected in zip(actual_ratios, expected_ratios)):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 9]: calculate each facade ratio before interpreting code."
    )
if (north_ok, south_ok, east_ok, west_ok, passing_count) != (True, True, True, False, 3):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 9]: compare all four ratios with max_ratio and count "
        "the three passing facades."
    )

# %% [10] AI-code audit
# QUESTION           Repair the code and add one known-answer test.
# INPUTS/ASSUMPTIONS plausible but defective AI-generated code
# METHOD             identify the type error, repair it, then add a known-answer test
# CHECKS/INTERPRET   The original code repeats text three times; it does not calculate area.

ai_candidate = '''wall = "12"
height = 3
area = wall * height
print(area + " m²")
'''

try:
    exec(ai_candidate)
except TypeError as error:
    print(f"EXPECTED DEBUG ERROR [cell 10] — TypeError: {error}")
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 10]: repair ai_candidate, add a known-answer "
        "assertion, then rerun this cell."
    ) from error
else:
    if area != 36.0:
        raise AssertionError(
            "MODEL CHECK FAILURE [cell 10]: repaired code must calculate numeric area 36.0."
        )
    print("Cell 10 complete: the repaired program calculates 36.0 m².")

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
# openings_m2=6, and waste_percent=8. Use conversion, parentheses, unit-aware
# names, and an f-string. Predict the result, then add one assertion and one
# invalid-input check. Do not reuse the AI expression without tracing its types.
