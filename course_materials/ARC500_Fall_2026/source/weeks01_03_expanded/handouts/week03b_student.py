# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 3 studio · Design rules, control flow, loops, and functions
Syracuse University · School of Architecture · Fall 2026

HOW TO USE THIS FILE IN SPYDER
  1. Save this file in your Week03 module folder.
  2. Click inside one # %% cell and press Ctrl+Enter.
  3. Predict the value, type, or branch before running.
  4. Inspect the Console and Variable Explorer after every cell.
  5. Restart the kernel and run from the top before submission.

COURSE RULE
  A status describes evidence from one rule. It must not overclaim that a room
  is approved, good, compliant, or complete unless the program actually has
  sufficient evidence for that conclusion.
"""

# %% [0] Environment and working-folder check
# QUESTION           Run the cell and confirm your Python version, executable, and working
#                    folder.
# INPUTS/ASSUMPTIONS no inputs; Spyder is installed and this file is open
# METHOD             run the cell and read the three printed environment lines in the
#                    console
# CHECKS/INTERPRET   You should see a Python version, an executable path, and a folder
#                    path with no error.

from pathlib import Path
import sys

print("Python:", sys.version.split()[0])
print("Executable:", sys.executable)
print("Working folder:", Path.cwd())


# %% [1] Boundary comparison
# QUESTION           The criterion says "at least 40 m2." Predict all three results before
#                    running.
# INPUTS/ASSUMPTIONS minimum_m2 = 40.0; test areas of 39.9, 40.0, and 40.1 m2
# METHOD             compare each test area with minimum_m2 using >= and print each
#                    Boolean result
# CHECKS/INTERPRET   Expected results: False, True, True. Explain why >= matches "at
#                    least" and > would not.

minimum_m2 = 40.0

print(39.9 >= minimum_m2)
print(40.0 >= minimum_m2)
print(40.1 >= minimum_m2)

# TODO: Explain why >= matches "at least" better than >.


# %% [2] Two-branch status
# QUESTION           Complete the conditional with bounded evidence language.
# INPUTS/ASSUMPTIONS area_m2 = 35.0; minimum_m2 = 40.0 from cell [1]
# METHOD             replace each TODO string with bounded evidence language, then test
#                    one value per branch
# CHECKS/INTERPRET   area_m2 = 35.0 is below the minimum, so status should print review
#                    area.

area_m2 = 35.0

if area_m2 >= minimum_m2:
    status = "TODO"
else:
    status = "TODO"

print(status)

if status != "review area":
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 2]: use bounded 'meets area criterion' / 'review area' "
        "status text in the two branches."
    )


# %% [3] Three daylight ranges
# QUESTION           Complete the thresholds and test every range and boundary.
# INPUTS/ASSUMPTIONS daylight_pct = 18.0; three named ranges: high, moderate, low
# METHOD             fill in each status string, then rerun with daylight_pct set to 10.0,
#                    15.0, 24.9, 25.0, and 30.0
# CHECKS/INTERPRET   Expected baseline result: moderate. Also try reversing the first two
#                    branches once to see which values get misclassified, then restore the
#                    correct order.

daylight_pct = 18.0

if daylight_pct >= 25.0:
    daylight_status = "TODO"
elif daylight_pct >= 15.0:
    daylight_status = "TODO"
else:
    daylight_status = "TODO"

print(daylight_status)

# TODO: Set daylight_pct to 10.0, 15.0, 24.9, 25.0, and 30.0 (one value at a time) and
# rerun this cell for each, recording the status you get.

# TODO: Temporarily swap the two conditions below (test >= 15.0 before >= 25.0), rerun
# all five test values above, and note which values are misclassified. Then restore the
# original order shown here.

cell_3_boundary_tests_complete = False  # TODO: True only after recording all five tests
if daylight_status != "moderate" or not cell_3_boundary_tests_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 3]: complete the high/moderate/low labels and record "
        "all five boundary tests before setting cell_3_boundary_tests_complete = True."
    )


# %% [4] Compound logic and truth-table test
# QUESTION           A room is ready for the next review only when both criteria pass.
# INPUTS/ASSUMPTIONS area_m2 = 44.2; has_daylight = True; minimum_m2 = 40.0
# METHOD             replace the TODO with an and expression combining both criteria, then
#                    test all four True/False combinations
# CHECKS/INTERPRET   Expected baseline result: True. Only the True/True combination of
#                    both inputs should print True.

area_m2 = 44.2
has_daylight = True

ready_for_review = False  # TODO: replace with a compound Boolean expression
print(ready_for_review)

# TODO: Test all four combinations of the two Boolean criteria.

cell_4_truth_table_complete = False  # TODO: True only after testing all four combinations
if ready_for_review is not True or not cell_4_truth_table_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 4]: combine both criteria with 'and' and test the "
        "four-row truth table."
    )


# %% [5] Loop through room areas
# QUESTION           Print each area beside a bounded status.
# INPUTS/ASSUMPTIONS room_areas_m2 = [35.0, 40.0, 62.5, 44.2, 28.0]; minimum_m2 = 40.0
# METHOD             inside the loop, compare area_m2 with minimum_m2 and choose a bounded
#                    status string
# CHECKS/INTERPRET   Expected meets sequence: False, True, True, True, False.

room_areas_m2 = [35.0, 40.0, 62.5, 44.2, 28.0]

loop_results = []
for area_m2 in room_areas_m2:
    # TODO: calculate meets and choose a bounded status
    meets = False
    status = "TODO"
    loop_results.append((meets, status))
    print(area_m2, meets, status)

expected_loop_results = [
    (False, "review area"),
    (True, "meets area criterion"),
    (True, "meets area criterion"),
    (True, "meets area criterion"),
    (False, "review area"),
]
if loop_results != expected_loop_results:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 5]: calculate each Boolean and bounded status inside "
        "the loop; the expected pass pattern is False, True, True, True, False."
    )


# %% [6] Count passing records
# QUESTION           Complete the accumulator and verify it by hand.
# INPUTS/ASSUMPTIONS the same room_areas_m2 list as cell [5]; passing_count starts at 0
# METHOD             add 1 to passing_count inside the if branch, then add an assertion
#                    for the expected count
# CHECKS/INTERPRET   Expected passing_count: 3. The assertion should pass silently; no
#                    output means the claim held.

passing_count = 0

for area_m2 in room_areas_m2:
    if area_m2 >= minimum_m2:
        pass  # TODO: update passing_count

print("Passing count:", passing_count)

# TODO: Add an assertion for the expected count.

if passing_count != 3:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 6]: update passing_count inside the if branch and add "
        "your known-answer assertion for 3."
    )


# %% [7] Refactor the rule into a function
# QUESTION           Return status text; do not print inside the function.
# INPUTS/ASSUMPTIONS area_m2 and an optional minimum_m2 with default 40.0
# METHOD             implement the same boundary and two return values used in cells
#                    [1]-[2], keeping the default parameter
# CHECKS/INTERPRET   Expected calls: review area, meets area criterion, meets area
#                    criterion.

def area_status(area_m2, minimum_m2=40.0):
    """Return bounded evidence about one room-area criterion."""
    # A triple-quoted line right under def is a docstring - a short description of what
    # the function does; it doesn't affect what the function returns.
    # TODO: implement the boundary and two return values
    return "TODO"


print(area_status(35.0))
print(area_status(40.0))
print(area_status(44.2))

if [area_status(value) for value in (35.0, 40.0, 44.2)] != [
    "review area",
    "meets area criterion",
    "meets area criterion",
]:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 7]: implement the boundary and both bounded return values."
    )


# %% [8] Boundary assertions
# QUESTION           Turn the expected policy into executable checks.
# INPUTS/ASSUMPTIONS the area_status function from cell [7]; boundary values 39.9, 40.0,
#                    40.1; one non-default minimum_m2
# METHOD             write one assert per expected boundary result using ==, matching the
#                    outputs already confirmed in cell [7]
# CHECKS/INTERPRET   If every assertion holds, the cell prints its confirmation message
#                    with no error.

# TODO: Add assertions for 39.9, 40.0, 40.1, and a non-default minimum.

cell_8_assertions_complete = False  # TODO: True only after all four assertions pass
if not cell_8_assertions_complete:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 8]: add four boundary assertions, including one with "
        "a non-default minimum, then set cell_8_assertions_complete = True."
    )

print("Boundary-test cell reached")


# %% [9] Apply the function to a real room schedule
# QUESTION           Call the tested function for every room in an eight-room schedule, not
#                    a toy of three.
# INPUTS/ASSUMPTIONS rooms is a list of dictionaries; each dictionary stores one room name
#                    and area_m2
# METHOD             loop over rooms, call area_status(room["area_m2"]), and print
#                    room["name"] beside the result
# CHECKS/INTERPRET   Expected report: Lobby review area, Studio A/Gallery/Workshop/Studio
#                    B/Office meets area criterion, Seminar/Storage review area.

# A dictionary stores named fields as key: value pairs inside { }. rooms below is a list
# of dictionaries, so each entry is one room's record; room["name"] reads the value stored
# at the key "name" for that room.
rooms = [
    {"name": "Lobby", "area_m2": 35.0},
    {"name": "Studio A", "area_m2": 62.5},
    {"name": "Gallery", "area_m2": 44.2},
    {"name": "Workshop", "area_m2": 78.0},
    {"name": "Seminar", "area_m2": 28.5},
    {"name": "Studio B", "area_m2": 55.0},
    {"name": "Office", "area_m2": 40.0},
    {"name": "Storage", "area_m2": 18.0},
]

room_report = []
for room in rooms:
    # TODO: call area_status with the current room area
    status = "TODO"
    room_report.append((room["name"], status))
    print(room["name"], status)

# TODO: Explain why this report is screening evidence, not design approval.

expected_room_statuses = [
    "review area", "meets area criterion", "meets area criterion",
    "meets area criterion", "review area", "meets area criterion",
    "meets area criterion", "review area",
]
if [status for _, status in room_report] != expected_room_statuses:
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 9]: call area_status() once for every room in the schedule."
    )

# %% [10] Count the report, don't just print it
# QUESTION           Summarize the eight-room report from cell [9] as two counts.
# INPUTS/ASSUMPTIONS the same rooms list and area_status function from cells [7] and [9]
# METHOD             two accumulators (recall cell [6]), updated once per room inside the
#                    same loop shape, then an assertion that every room was counted exactly
#                    once
# CHECKS/INTERPRET   Expected: Review: 3 Meets: 5. The assertion should pass silently.

review_count = 0
meets_count = 0
for room in rooms:
    status = area_status(room["area_m2"])
    pass  # TODO: if status == "review area", add 1 to review_count; otherwise add 1 to meets_count

print("Review:", review_count, "Meets:", meets_count)

# TODO: Add an assertion confirming review_count + meets_count == len(rooms).

if (review_count, meets_count) != (3, 5):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 10]: classify every room exactly once; expect Review 3, "
        "Meets 5, then add the total-count assertion."
    )


# %% [11] AI-generated rule audit
# QUESTION           Identify and repair the defects in an AI-generated screening rule.
# INPUTS/ASSUMPTIONS ai_rule as shown text, using > instead of >= and the verdict words
#                    approved/bad room
# METHOD             list at least four specific defects, then compare them with the
#                    repaired area_status function
# CHECKS/INTERPRET   A defensible list names the boundary, wording, and missing-test
#                    defects, not merely that the code looks wrong.

ai_rule = """
def ai_area_status(area_m2):
    if area_m2 > 40:
        return "approved"
    return "bad room"
"""

ai_defects = [
    # TODO: add at least four specific technical or reasoning defects
]

print(ai_rule)
for defect in ai_defects:
    print("-", defect)

if len(ai_defects) < 4 or any("TODO" in defect.upper() for defect in ai_defects):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 11]: record at least four specific defects before "
        "accepting or repairing the AI-generated rule."
    )


# %% [12] Preview: the same rooms as one NumPy array
# QUESTION           The same eight room areas from cell [9], as one NumPy array instead of
#                    eight separate dictionaries — predict what shape, dtype, and areas_m2[0]
#                    will print before you run this cell.
# INPUTS/ASSUMPTIONS the same eight area_m2 values already used in cell [9]'s rooms list
# METHOD             build one array from the eight values, print its shape and dtype, print
#                    its first element, then convert the whole array to square feet in one
#                    line — no loop
# CHECKS/INTERPRET   Expected shape: (8,). Expected dtype: float64. Expected areas_m2[0]:
#                    35.0. Predict all four outputs before running. Week 4 starts here.

import numpy as np

# same eight rooms as cell [9]'s rooms list, now as one array instead of eight dictionaries
areas_m2 = np.array([35.0, 62.5, 44.2, 78.0, 28.5, 55.0, 40.0, 18.0])

# TODO: print the array's shape
# TODO: print the array's dtype
# TODO: print the first element with areas_m2[0]
# TODO: convert the whole array to square feet in one line (1 m2 = 10.7639 ft2), no loop
areas_ft2 = None  # TODO: replace with the vectorized conversion

if areas_ft2 is None or not isinstance(areas_ft2, np.ndarray) or areas_ft2.shape != (8,):
    raise NotImplementedError(
        "EXPECTED TODO STOP [cell 12]: inspect shape/dtype/first value and create the "
        "eight-value square-foot array without a loop."
    )
if not np.allclose(areas_ft2, areas_m2 * 10.7639):
    raise AssertionError(
        "MODEL CHECK FAILURE [cell 12]: areas_ft2 exists but does not match the known conversion."
    )


# %% [13] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished workflow in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing the
#                    script cannot judge.

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

exit_explanation = """
In 80-120 words, explain:
1. the evidence and criterion,
2. how equality is treated,
3. why the function returns bounded language,
4. how the loop scales the rule, and
5. one design judgment the script cannot make.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Adapt the tested function so a studio meets the screening rule only when
# area_m2 >= 40 AND has_daylight is True. Predict (39.9, True), (40.0, True),
# and (45.0, False); apply the function to all three with a loop; return bounded
# wording and name one architectural judgment this two-variable rule cannot make.
