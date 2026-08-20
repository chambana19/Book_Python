# ARC 500 Fall 2026 release notes

Release date: 2026-08-20

## Outcome

The course now uses one shared visual/content system across 28 lecture decks and two project presentation templates. No deck is forced to 34 slides or any other common count. The final lecture decks range from 34 to 43 slides, with topic-driven variation and complete optional/self-application material retained.

## Major revisions

- Rebuilt all lecture decks with the shared 16:9 design system, consistent palette, typography, slide roles, source notes, and overflow diagnostics.
- Repaired visibly broken or clipped slides, including Week 1B mockups and dense code/table slides in later blocks.
- Restored the full authored Week 3A and Week 4A source inventories and expanded the Week 8 clinic with meaningful self-application checkpoints.
- Added additive 2026 practice-horizon material for Arrow/data contracts, IFC/IDS/Brick interoperability, accessible/declarative visualization, GeoParquet/OGC APIs, mixed-integer/multiobjective/Bayesian optimization, calibration/conformal uncertainty, EnergyPlus/BOPTEST verification, and lifecycle AI risk management.
- Added the rendered Week 9 sensitivity heatmap directly beside its generating code and worked reading exercise; plots are shown rather than merely described.
- Persisted all authored figure descriptions into PowerPoint's exported picture alt-text field and added an export-level accessibility check.
- Corrected linear-programming claims about existence, extreme points, uniqueness, and numerical tolerances.
- Reframed finite grid and heuristic results as best sampled/best known unless an exact finite baseline proves otherwise.
- Rebuilt Week 14 around 84-train / 28-validation / 28-untouched-final-test evaluation, validation-only threshold/specification choice, and development-only cross-validation.
- Removed the use of plus/minus RMSE as a prediction interval and required non-surrogate confirmation after optimization.
- Replaced the Spyder standalone-console installation workflow with one shared external `arc500-f26` environment and a preflight script.

## Handouts and projects

- Student scaffolds stop loudly at required TODO gates and cannot export plausible placeholder artifacts.
- Project 1 separates missing-value and statistical-outlier flags, gates exports, includes a submission validator, and provides a printable Weeks 4–7 evidence checklist.
- Project 2 uses the same 140-row/four-feature portfolio schema as Weeks 13–15, supports regression and classification branches, includes appropriate optimization starters, and requires surrogate-to-truth verification.
- Project 2 now requires its first model-inside-optimizer smoke test by the end of Week 14; Week 15 is confirmation and communication, with a scalable five-minute review format rather than first assembly.
- Project 1 and Project 2 presentation templates contain exactly six and eight slides respectively and use the same course visual system.

## Final lecture counts

| Block | Deck counts |
|---|---|
| Weeks 1–3 | 01A 34; 01B 34; 02A 36; 02B 34; 03A 38; 03B 36 |
| Weeks 4–8 | 04A 41; 04B 35; 05A 37; 05B 35; 06A 35; 06B 34; 07A 37; 07B 36; 08B 34 |
| Weeks 9–12 | 09A 35; 09B 36; 10A 35; 10B 35; 11A 36; 11B 35; 12A 43; 12B 41 |
| Weeks 13–15 | 13A 38; 13B 36; 14A 38; 14B 39; 15A 36 |

## Release control

- `course_manifest.yml` records every distributed file, byte size, SHA-256 hash, and PowerPoint slide count.
- `release_tools/course_release.py` generates the manifest, creates the Git repository mirror, and verifies local/repository parity.
- Generated inspect reports, render caches, Python caches, and ad-hoc outputs are excluded from the distribution.
- The week-specific Week 13, Week 14, and Week 15 folders are convenience mirrors of the consolidated `Weeks13-15_MachineLearning` authoring/build target.
