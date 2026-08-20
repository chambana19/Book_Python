# -*- coding: utf-8 -*-
"""
ARC 500 · Programming with Python and Generative AI
Week 3 studio · INSTRUCTOR SOLUTIONS
Design rules, control flow, loops, and functions
Syracuse University · School of Architecture · Fall 2026
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

print(39.9 >= minimum_m2)  # False
print(40.0 >= minimum_m2)  # True: equality is included by "at least"
print(40.1 >= minimum_m2)  # True


# %% [2] Two-branch status
# QUESTION           Complete the conditional with bounded evidence language.
# INPUTS/ASSUMPTIONS area_m2 = 35.0; minimum_m2 = 40.0 from cell [1]
# METHOD             replace each TODO string with bounded evidence language, then test
#                    one value per branch
# CHECKS/INTERPRET   area_m2 = 35.0 is below the minimum, so status should print review
#                    area.

area_m2 = 35.0

if area_m2 >= minimum_m2:
    status = "meets area criterion"
else:
    status = "review area"

print(status)


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
    daylight_status = "high"
elif daylight_pct >= 15.0:
    daylight_status = "moderate"
else:
    daylight_status = "low"

print(daylight_status)

for test_value in [10.0, 15.0, 24.9, 25.0, 30.0]:
    if test_value >= 25.0:
        test_status = "high"
    elif test_value >= 15.0:
        test_status = "moderate"
    else:
        test_status = "low"
    print(test_value, test_status)

# Reversed-branch defect (shown for demonstration only - do not keep this order).
# Checking the less restrictive threshold first makes the second condition
# unreachable for any value that already satisfies the first one.
print("--- reversed-branch defect ---")
for test_value in [10.0, 15.0, 24.9, 25.0, 30.0]:
    if test_value >= 15.0:          # BUG: less restrictive threshold checked first
        broken_status = "moderate"
    elif test_value >= 25.0:        # unreachable: anything >= 25 already matched above
        broken_status = "high"
    else:
        broken_status = "low"
    print(test_value, broken_status)  # 25.0 and 30.0 are wrongly reported as "moderate"


# %% [4] Compound logic and truth-table test
# QUESTION           A room is ready for the next review only when both criteria pass.
# INPUTS/ASSUMPTIONS area_m2 = 44.2; has_daylight = True; minimum_m2 = 40.0
# METHOD             replace the TODO with an and expression combining both criteria, then
#                    test all four True/False combinations
# CHECKS/INTERPRET   Expected baseline result: True. Only the True/True combination of
#                    both inputs should print True.

area_m2 = 44.2
has_daylight = True

ready_for_review = area_m2 >= 40.0 and has_daylight
print(ready_for_review)

for meets_area in [False, True]:
    for has_daylight_case in [False, True]:
        print(
            meets_area,
            has_daylight_case,
            meets_area and has_daylight_case,
        )


# %% [5] Loop through room areas
# QUESTION           Print each area beside a bounded status.
# INPUTS/ASSUMPTIONS room_areas_m2 = [35.0, 40.0, 62.5, 44.2, 28.0]; minimum_m2 = 40.0
# METHOD             inside the loop, compare area_m2 with minimum_m2 and choose a bounded
#                    status string
# CHECKS/INTERPRET   Expected meets sequence: False, True, True, True, False.

room_areas_m2 = [35.0, 40.0, 62.5, 44.2, 28.0]

for area_m2 in room_areas_m2:
    meets = area_m2 >= 40.0
    if meets:
        status = "meets area criterion"
    else:
        status = "review area"
    print(area_m2, meets, status)


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
        passing_count += 1  # += adds to the existing value: passing_count = passing_count + 1

print("Passing count:", passing_count)
assert passing_count == 3


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
    if area_m2 >= minimum_m2:
        return "meets area criterion"
    return "review area"


print(area_status(35.0))
print(area_status(40.0))
print(area_status(44.2))


# %% [8] Boundary assertions
# QUESTION           Turn the expected policy into executable checks.
# INPUTS/ASSUMPTIONS the area_status function from cell [7]; boundary values 39.9, 40.0,
#                    40.1; one non-default minimum_m2
# METHOD             write one assert per expected boundary result using ==, matching the
#                    outputs already confirmed in cell [7]
# CHECKS/INTERPRET   If every assertion holds, the cell prints its confirmation message
#                    with no error.

assert area_status(39.9) == "review area"
assert area_status(40.0) == "meets area criterion"
assert area_status(40.1) == "meets area criterion"
assert area_status(50.0, minimum_m2=60.0) == "review area"

print("Boundary tests passed")


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

for room in rooms:
    status = area_status(room["area_m2"])
    print(room["name"], status)

# This report addresses one area criterion only. It does not establish code
# compliance, program quality, accessibility, environmental performance, or
# architectural approval.

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
    if status == "review area":
        review_count += 1
    else:
        meets_count += 1

print("Review:", review_count, "Meets:", meets_count)
assert review_count + meets_count == len(rooms)
print("Every room accounted for")

# COMMON ERROR: forgetting that status must be recomputed inside THIS loop
# too — the counts cannot reuse whatever status held after cell [9]'s loop
# finished, because that only remembers the LAST room checked.
# WHY THIS MATTERS: the assertion is the actual check. If area_status ever
# returned a third, uncounted value, review_count + meets_count would stop
# equaling len(rooms), and the assertion would fail loudly instead of the
# report silently under-counting.


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
    "Uses > even though 'at least 40' includes equality.",
    "The threshold has no named variable or unit.",
    "'approved' overclaims what one area test can support.",
    "'bad room' is an unsupported design judgment.",
    "No docstring, boundary tests, invalid-input policy, or configurable minimum.",
]

print(ai_rule)
for defect in ai_defects:
    print("-", defect)


# %% [12] AI-use record and exit explanation
# QUESTION           Record how you used generative AI this week, then explain the
#                    finished workflow in 80-120 words.
# INPUTS/ASSUMPTIONS your own prompts and suggestions from this studio; the five required
#                    points listed below
# METHOD             fill in the AI-use record honestly, then write the exit explanation
#                    addressing all five required points
# CHECKS/INTERPRET   The exit explanation should be 80-120 words and name one thing the
#                    script cannot judge.

ai_use_record = """
Tool/model: Example assistant
Prompt: Propose a function that screens room area against an at-least-40-m² rule.
Suggestion received: Used > and returned approved/bad room.
What I accepted: The general function structure.
What I modified and why: Changed the boundary to >= and replaced verdicts with
bounded evidence language.
What I rejected and why: Unsupported design approval and judgment language.
How I tested it: Assertions at 39.9, 40.0, 40.1, and a non-default threshold.
One limitation I found: Area alone cannot establish room quality or compliance.
"""

exit_explanation = """
The function screens one recorded room area against a named 40 square-meter
minimum; that measurement and threshold are the evidence and criterion for this
rule. Because the criterion says at least 40 square meters, equality belongs in
the passing branch, and a boundary assertion protects that choice from silent
changes later. The function returns bounded language about the area criterion
instead of claiming design approval, since one measurement cannot certify an
entire room. A loop applies this same tested function to every room record in
the schedule, so the rule scales without copied code or inconsistent
thresholds. The result still cannot judge accessibility, proportion, use,
daylight quality, code compliance, context, or architectural experience; a
person must make that judgment.
"""

print(ai_use_record)
print(exit_explanation)

# %% ARCHITECTURAL TRANSFER — 4-minute exit check
# Adapt the tested function so a studio meets the screening rule only when
# area_m2 >= 40 AND has_daylight is True. Expected outcomes: False, True, False
# for (39.9, True), (40.0, True), and (45.0, False). Require a loop and bounded
# language; accessibility, egress, daylight quality, and program fit remain
# outside this simplified screen.
