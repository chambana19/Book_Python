# Delivering the complete ARC 500 source decks

Last revised: 2026-08-20

## The decks are menus with a protected spine

Every deck contains the full authored explanation, examples, practice, and optional professional horizon. Different topics therefore have different slide counts. Do not delete material simply to make a deck resemble another deck or meet a numerical target.

Protect this spine when pacing a class:

`question → prerequisite → new idea → prediction → worked example → verification → transfer → bounded claim`

Hide, skip, or shorten optional elaborations around that spine. Keep the source file complete so a later cohort, asynchronous learner, engineer, or self-directed student can use the fuller path.

## Three practical delivery modes

### Core meeting

Use the opener, outcomes, prerequisite recall, first complete worked case, at least one predict-before-run item, one verification/transfer activity, and the closing. Assign the remaining worked examples and the 2026 horizon as follow-up reading.

### Full workshop

Use the complete conceptual sequence, multiple worked examples, live code tracing, and the handout. Pause after each prediction and require students to state the expected value, type, unit, or error before execution.

### Self-application or asynchronous study

Students read speaker notes, run the instructor example once, restart the kernel, complete the student scaffold, and answer the transfer prompt on a different row or parameter. A valid completion includes the check—not only the output.

## How to use optional horizon slides

Slides labeled `2026 PRACTICE HORIZON` are additive. Their purpose is to show where the core method leads in current practice, not to create surprise prerequisites. Use them to:

- name a current standard or tool;
- identify the decision structure that would justify it;
- state what additional evidence would be required;
- give advanced students a credible next step.

They may be discussed briefly, assigned for self-study, or hidden in a beginner-paced meeting. Keep them in the source deck.

## Teaching code without turning the lecture into typing

- Read the question and expected check before reading syntax.
- Trace only the lines that change state or implement the decision rule.
- Use complete code for the final example; avoid leaving students with disconnected snippets.
- Make units, dtypes, shapes, bounds, labels, seeds, and paths visible.
- Restart and run top-to-bottom before calling a script reproducible.
- When AI produces code, require the student to predict, test, explain, modify, and disclose. Fast authorship is not evaluation.

## Project 1: Evidence Before Design

Weeks 4–8 form one feasible evidence pipeline:

`question + provenance → cleaning + flags → grouping + outlier decision → two static figures → map OR animation → bounded recommendation`

The project intentionally separates missingness from statistical outliers. Students export exact-schema files only after all TODO gates and checks pass. The final six-slide pin-up is a cover plus five content slides. Use `validate_submission.py` before submission; the untouched starter is expected to fail with actionable messages.

The visual narrative should show data trust, grouped evidence, two purposeful figures, one extension, and a recommendation with limits. The map/animation is evidence only when it answers an additional question.

## Project 2: Predict, Optimize, Decide

Weeks 9–15 form one cumulative decision pipeline:

`bounded design space → evaluated prediction → justified optimizer → baseline/fair comparison → non-surrogate confirmation → recommendation + refusal boundary`

Students choose a regression or classification track but use the same 140-row, four-feature portfolio schema. Evaluation uses development, validation, and an untouched final test. A classifier’s threshold is chosen on validation evidence; a regressor’s feature specification is chosen before final testing. The fitted model may become an optimizer objective or a modeled constraint, but the final candidate must be rechecked in a higher-fidelity simulator, measurement process, or documented expert audit.

The first model-inside-objective/constraint smoke test is due by the end of Week 14: freeze the exact fitted artifact, verify feature order, run the support gate, and evaluate the wrapper at the baseline plus one candidate. Week 15 is for independent confirmation, synthesis, and communication—not first assembly.

The eight-slide final template protects the integration: decision/formulation, evaluated prediction, primary optimization, fair comparison, predict–optimize–verify connection, baseline versus candidate, and a bounded recommendation with next validation. Live review is capped at five minutes per student: a four-minute decision brief plus one-minute evidence/code trace. Reserve 15 minutes for selective source-deck synthesis; for more than 12 students, use parallel gallery/code-review rounds before reconvening.

## What to look for while circulating

- Does the student know what one row/candidate means?
- Are units and bounds visible?
- Is the output regenerated by the script?
- Is the comparison fair—same subproblem, data split, evaluation budget, and metric?
- Is a final test, validation set, or truth model being reused improperly?
- Does the claim stop where the evidence stops?
- Is the student able to name the next measurement, simulation, or stakeholder review?

## Semester-wide consistency check

Before teaching a block, inspect the coverage map, the Meeting A deck, the Meeting B deck, the student handout, and the project milestone together. If a convention or number changes, update the authored specification, builder source, active handout, convenience mirrors, and repository release in the same change.
