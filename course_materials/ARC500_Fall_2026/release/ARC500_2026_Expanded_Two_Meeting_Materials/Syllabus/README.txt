ARC 500 · SYLLABUS · FALL 2026

FILES

  ARC500_Syllabus_FS26.tex   LaTeX source (the file to edit)
  ARC500_Syllabus_FS26.pdf   compiled output, US Letter

HOW TO COMPILE

  pdflatex ARC500_Syllabus_FS26.tex
  pdflatex ARC500_Syllabus_FS26.tex      (run twice so page totals settle)

Packages used, all in a standard TeX Live installation: geometry, microtype,
xcolor, fancyhdr, booktabs, longtable, array, tabularx, enumitem, titlesec,
ragged2e, hyperref, lmodern. No custom .cls or .sty file is needed.

OFFICIAL STATUS (AUGUST 20, 2026)

The student syllabus has been reconciled and contains no confirmation
placeholders. Course facts now state 3 credits, Mon/Wed 12:45-2:05pm in
Slocum 307, office hours Mon/Wed 10:30am-noon in Slocum 306A, the September
14 academic/financial drop deadline, the November 20 withdrawal deadline,
and the selected-topics elective role. Project 1 and Project 2 presentations
occur in class; their Blackboard packages are due at 11:59pm on October 14
and December 7, respectively.

The official distribution copy is maintained in the top-level Syllabus folder.

WHAT THIS DOCUMENT IS BUILT FROM

Structure and common course-policy sections follow the ARC 612 Fall 2026
syllabus so the two courses read as one instructor's consistent set. The five
required University statements were also checked against the current Office of
Academic Affairs syllabus guidance; ARC 500 uses the official Full Use with
Disclosure and Citation AI option rather than ARC 612's course-specific AI ban.

Every course-specific fact -- dates, deadlines, grade weights, rubric lines,
deliverables, milestones, and topic order -- is taken from the course's own
single source of truth:

  ../ARC500_2026_Semester_Restructure_Weeks01-15.txt

If that master schedule changes, this syllabus must be reconciled against it.

FOUR PLACES THIS SYLLABUS DELIBERATELY DIVERGES FROM ARC 612

These are intentional, not oversights. Do not "correct" them back toward the
ARC 612 template:

  1. LAPTOPS ARE REQUIRED, not prohibited. ARC 612's expectations table asks
     students to refrain from using laptops in class. ARC 500 is a hands-on
     course where the Wednesday studio deliverable is built in class, so a
     laptop at every meeting is a stated requirement, with a matching
     expectation that it is used for course work during class time. There is
     also a dedicated "Required Laptop and Software" section.

  2. GENERATIVE AI IS PERMITTED, not banned. ARC 612 prohibits all
     generative-AI tools. ARC 500 has generative AI in its title and teaches
     its use directly, so the AI policy instead sets six conditions
     (explain every line, keep an AI-use record, verify rather than trust,
     no substitution for assessed reasoning, no collaboration via AI, no
     uploading protected material) and enforces the record with a 70% cap on
     any submission whose disclosure is missing, incomplete, or fabricated.

  3. NO EXAMS. ARC 612 has two midterms and a final worth 50% combined.
     ARC 500 has no quiz or exam category at all: 40% weekly studio
     assignments (13 graded weeks, lowest 2 dropped), 25% Project 1, 35%
     Project 2. The syllabus states the reasoning for this.

  4. MONDAY/WEDNESDAY, 80-MINUTE MEETINGS. ARC 612 meets MWF for 55 minutes.
     ARC 500 meets Monday and Wednesday, 12:45-2:05pm, in Slocum Hall 307,
     and each week's two meetings have distinct roles (Monday = concepts,
     Wednesday = studio).

WHAT WAS CARRIED OVER FROM ARC 612

The university policy sections, which should stay aligned across courses: the
university attendance expectation, excused/non-excused determination, the
1.5%-per-unexcused-absence penalty, the grade scale, disability-related
accommodations, academic integrity, faith tradition observances, discrimination
or harassment, use of class materials, student work, the university email
policy, and Turnitin. The Turnitin section is scoped to this course's two
written deliverables (the Project 1 memo and the Project 2 report) rather than
to code files.

TWO PLACES THE ARC 612 TEXT WAS CORRECTED RATHER THAN COPIED

  - EXCUSED ABSENCES: ARC 612 excuses the first three absences. The ARC 500
    master schedule (Section 1) excuses the first TWO. The master wins, so
    this syllabus says two, and the worked example in the penalty section was
    recomputed to match. Do not restore "three" from the ARC 612 template.
    The 1.5% per-unexcused-absence figure itself is unchanged; it sits inside
    the master's stated "1-2 points" range.

  - GRADE SCALE BOUNDARY: ARC 612's scale reads ">93 = A" alongside
    "89-92 = A-", which leaves a rounded score of exactly 93 with no letter
    grade. This syllabus reads "93 and above" instead. No other boundary was
    touched.

VERIFICATION RECORD (Aug 18)

A full fact-check pass compared every claim in the syllabus against the master
schedule, the Spyder setup guide, the Weeks01-03 README, and both project
folders' briefs and rubrics. Results:

  - All 32 schedule dates verified, including day-of-week correctness against
    the real 2026 calendar (all 16 Mondays are Mondays, all 16 Wednesdays are
    Wednesdays, and Sep 5 / Oct 10 / Dec 5 are all Saturdays).
  - All 12 rubric percentages in both project tables match the master and both
    03_RUBRIC.txt files exactly.
  - All deadlines, the three Saturday exceptions, the Week 13 Thanksgiving
    shift, the 40/25/35 split, and the 70% AI-disclosure cap verified.
  - Zero occurrences of conda, Miniforge, Anaconda, Grasshopper, Rhino,
    Dynamo, pyRevit, Galapagos, or Wallacei.
  - Generative AI is affirmatively permitted, correctly inverting the ARC 612
    template.

Six defects were found and fixed in the syllabus (excused-absence count, the
grade-scale 93 gap, "one exception" where three weeks deviate from the
two-meeting pattern, credit hours stated as fact rather than TBD, Project 2's
omitted formulation memo and filenames, and Week 4's omitted NumPy/Matplotlib
deliverable).

The same pass also found three stale claims in the MASTER SCHEDULE itself,
which were corrected there (each marked [CORRECTED Aug 18] inline):

  - Section 2's list of weeks on the standard Monday deadline wrongly included
    Week 13, contradicting Week 13's own entry.
  - Section 2 and Week 3's entry both claimed the four-heading cell structure
    starts at Week 3B. All 14 instructor/student handout pairs were verified
    to carry all four headings, so it is universal from Week 1B. The 14 pairs
    are Weeks 1B-7B, Weeks 9B-13B, and the two Week 14B tracks; Week 8B and
    Week 15A are clinic/capstone materials rather than paired scaffolds.
  - The heading names were written with hyphens (INPUTS-ASSUMPTIONS); every
    actual handout uses slashes (INPUTS/ASSUMPTIONS).
