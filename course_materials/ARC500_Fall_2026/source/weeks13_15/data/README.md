# Shared, pre-verified scenario for Weeks 13-15 (Machine Learning block)

One shared dataset drives all of Weeks 13, 14, and 15: `radley_portfolio_envelope.csv`
(140 rows), already generated and written to this folder. It is fictional (say so on
slide, same convention as Radley Hall in Weeks 4-8 and the Weeks 9-12 scenarios) but
every number below was verified in the pinned course environment
(numpy 2.4.6, pandas 3.0.5, scipy 1.17.1, scikit-learn
1.9.0). Do not recompute or alter these numbers — cite them exactly, or re-run the
scripts below yourself if you need a value not listed here.

**Continuity device:** Radley Hall's design team explored 140 envelope variants during
schematic design (this is the "portfolio," one row per variant). Two of the four design
variables — `wwr` (0.20-0.60) and `shade_m` (0.0-1.2) — are the EXACT SAME variables and
bounds as Weeks 9 and 11's swept/optimized nonlinear objective. Use this explicitly in
Week 13: "Weeks 9 and 11 gave you a clean analytic formula, `energy_proxy(wwr, shade_m)`,
and you swept or minimized it directly. Real buildings don't hand you a formula — you
only get measured/simulated outcomes for the variants someone actually tried. Fitting a
model FROM those outcomes is what Weeks 13-14 teach you to do." Week 15 closes the loop
by using the FITTED model (not the Week 9/11 analytic function) as the optimization
objective — predict, then optimize, then decide.

## Dataset schema (`data/radley_portfolio_envelope.csv`, n=140)

| column | type | meaning |
|---|---|---|
| `variant_id` | str | V001-V140, one row per explored design variant |
| `wwr` | float | window-to-wall ratio, 0.20-0.60 (same bounds as Weeks 9/11) |
| `shade_m` | float | shading overhang depth, meters, 0.0-1.2 (same bounds as Weeks 9/11) |
| `glazing_shgc` | float | glazing solar heat gain coefficient, 0.25-0.65 |
| `compactness` | float | surface-to-volume proxy (unitless), 0.8-1.4; LOWER = more compact/efficient |
| `orientation` | str | main facade orientation: N / E / S / W |
| `eui_kwh_m2yr` | float | **target** — simulated annual energy-use-intensity proxy, kWh/m2/yr-like, to MINIMIZE |
| `est_annual_cost_index` | float | a reporting-only utility-cost proxy, `= eui_kwh_m2yr * 0.14 + noise` — **LEAKAGE BAIT, see Week 13 below, never use as a predictive feature** |
| `meets_code` | int | **classification target** (Week 14), 1 if `eui_kwh_m2yr <= 27.0` else 0 |

Generating formula (already run, do not re-derive different coefficients):
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(7)
N = 140
wwr = rng.uniform(0.20, 0.60, N)
shade_m = rng.uniform(0.0, 1.2, N)
glazing_shgc = rng.uniform(0.25, 0.65, N)
compactness = rng.uniform(0.8, 1.4, N)
orientation = rng.choice(["N","E","S","W"], size=N, p=[0.25,0.25,0.25,0.25])
orient_offset = {"N": -1.0, "E": 0.0, "S": 1.0, "W": 0.5}
orient_vals = np.array([orient_offset[o] for o in orientation])
noise = rng.normal(0, 2.4, N)
eui = 15.0 + 18.0*wwr - 4.0*shade_m + 6.0*glazing_shgc + 5.0*compactness + orient_vals + noise
# est_annual_cost_index = eui_kwh_m2yr * 0.14 + rng.normal(0, 0.05, N)
# meets_code = (eui_kwh_m2yr <= 27.0).astype(int)
```
`eui_kwh_m2yr` distribution (n=140): mean 28.09, std 3.66, min 17.92, max 37.19,
25th pct 26.02, median 28.42, 75th pct 30.48.

Week 13's introductory regression examples use a fixed 105/35 split with
`test_size=0.25, random_state=42`. Week 14 then introduces the stronger three-way
84-train / 28-validation / 28-untouched-final-test protocol documented below. Keep the
roles and seeds explicit; never substitute the Week 13 evaluation split for Week 14's
selection-plus-final-test protocol.

## Week 13 — evaluated prediction (regression), naive baseline, and a real leakage bug

**Features used (the "AI-scaffolded" baseline model):** `wwr`, `shade_m`, `glazing_shgc`
(3 features — `compactness` and `orientation` are DELIBERATELY left out here; Week 14
adds `compactness` back in as the "refine a feature" studio task).

**Verified naive baseline** (`sklearn.dummy.DummyRegressor(strategy="mean")`, fit on
train, predicts the training mean 28.0836 for every test row): MAE=2.8906, RMSE=3.8154,
R²=-0.00003 (a naive mean predictor has R² essentially exactly 0 on its own training
distribution — use this to make the point concrete: R²=0 is not "bad," it is the
definition of "no better than guessing the average").

**Verified 3-feature `LinearRegression` fit** (`coef_` for `[wwr, shade_m, glazing_shgc]`
= `[17.6545, -3.3915, 3.4181]`, `intercept_`=21.6211): MAE=2.2680, RMSE=2.7146, R²=0.4937.
This beats the baseline (MAE drops ~21.5%, R² rises from ~0 to ~0.49) — real, but
imperfect; there is a genuine, honest reason for the leftover error (compactness and
orientation both have real effects and are missing from this model — this is not
manufactured, it sets up Week 14's refinement honestly).

**Verified worst 3 residuals in the test set** (use for "diagnose the largest residual"):
| variant | actual | predicted | residual | wwr | shade_m | shgc | compactness | orientation |
|---|---|---|---|---|---|---|---|---|
| V037 | 20.43 | 26.77 | -6.34 | 0.348 | 0.917 | 0.618 | 1.135 | N |
| V133 | 23.05 | 27.94 | -4.89 | 0.336 | 0.522 | 0.630 | 0.881 | E |
| V043 | 22.45 | 27.01 | -4.56 | 0.404 | 1.053 | 0.535 | 1.102 | E |

V037 is the single largest miss: the model over-predicts by 6.34 (thinks the design
performs worse than it actually does). Diagnosis available with only 3 features: V037
has high shading (0.917, among the deepest in the set) AND north orientation (the
coolest/lowest-gain offset, -1.0) — both real, verified effects the 3-feature model
cannot see (orientation isn't a numeric feature at all yet; only `compactness` gets
added in Week 14). This is a genuine, defensible answer to "why did the model miss this
one so badly," not a manufactured one.

**Full test-set actual/predicted/residual list** (35 rows, sorted by actual value, for
building the residual scatter chart) — regenerate via the script above plus
`train_test_split(..., random_state=42)` if you need it; do not hand-copy a shortened
version into a chart's `series` values without re-running, since transcription errors
are easy across 35 rows.

**THE LEAKAGE BUG (core Week 13 studio task — find AND FIX it):** an "AI-drafted"
version of this same regression additionally includes `est_annual_cost_index` as a
FOURTH predictive feature (alongside `wwr`, `shade_m`, `glazing_shgc`), reasoning
(plausibly, on the surface) that "cost is a design-relevant variable too." This is
leakage: `est_annual_cost_index` is deterministically derived FROM the target
(`= eui_kwh_m2yr * 0.14 + small noise`, verified correlation with `eui_kwh_m2yr` =
0.995574) — it is the answer, wearing a different unit.

**Verified leakage-version fit:** `coef_` = `[0.3310, 0.0374, 0.3054, 7.1264]`
(`wwr, shade_m, glazing_shgc, est_annual_cost_index` — note how small the first three
coefficients become, and how large the leaking feature's coefficient is, relative to the
honest 3-feature fit above), MAE=0.2852, RMSE=0.3342, **R²=0.9923**. Contrast directly
with the honest model's R²=0.4937 — an R² this close to 1.0 on a noisy, real-world-style
target is the "too good to be true" signal itself; teach students to be suspicious of a
suspiciously perfect metric, not just to hunt for leakage code patterns blindly. THE FIX:
drop `est_annual_cost_index` from the feature list entirely (it is a legitimate
reporting/output column, never a predictor); refit; confirm the metrics return to the
honest 3-feature numbers above.

**Optional extension — silent extrapolation** (mention, do not require): the 3-feature
model, asked to predict at `wwr=0.85` (training range is 0.201-0.598 — 0.85 is far
outside it, and also physically implausible), returns **37.15** with no warning, no
error, nothing visibly different from an in-range prediction. This is the "silent" part
of silent extrapolation — the number looks like a normal EUI value (within the
training data's own observed range, 17.9-37.2), not an obviously broken one. Good
one-line discussion prompt: "how would you even notice this without checking the input
ranges yourself?"

**Manual metric check for handout CHECKS/INTERPRET section:** with 35 test rows,
MAE = mean(|residual|) and RMSE = sqrt(mean(residual²)) are both directly hand-computable
from the printed residual list above; have students recompute at least MAE by hand from
the printed actual/predicted pairs and assert it matches the sklearn value to 2 decimals.

## Week 14 — classification (go/no-go track) AND regression refinement (continuous track)

Meeting B is TRACK-DEPENDENT (per the finalized plan, Section 3) — both tracks share the
Meeting A theory, then split for the studio task. Build two separate handout pairs.

### Track A — go/no-go classification

**Label:** `meets_code = 1` if `eui_kwh_m2yr <= 27.0` else `0`. **Verified class balance**
(full n=140): 92 "no" / 48 "yes" (34.3% meet code) — imbalanced enough to be realistic,
not so extreme the confusion matrix becomes degenerate.

**Fixed three-way protocol:** reserve 28 stratified rows as an untouched final test;
split the remaining 112 development rows into 84 training and 28 validation rows with
`random_state=42`; fit `LogisticRegression` only on training. Verified training fit:
`coef_ = [-1.4322, 1.6772, -0.1674, -0.6965]`, `intercept_ = -0.2802`.

**Verified validation threshold sweep** (same fitted model and the same 28 validation
rows; only the probability cutoff changes):
| threshold | TN | FP | FN | TP | precision | recall | F1 |
|---|---|---|---|---|---|---|---|
| 0.3 | 12 | 7 | 1 | 8 | 0.533 | 0.889 | 0.667 |
| 0.4 | 17 | 2 | 1 | 8 | 0.800 | 0.889 | 0.842 |
| 0.5 | 18 | 1 | 3 | 6 | 0.857 | 0.667 | 0.750 |
| 0.6 | 19 | 0 | 8 | 1 | 1.000 | 0.111 | 0.200 |
| 0.7 | 19 | 0 | 9 | 0 | 0.000 | 0.000 | 0.000 |

**Predeclared consequence rule:** a false positive (saying "go" when a design fails)
is the dangerous direction. Before opening the final test, require validation FPR ≤10%,
then maximize recall among qualifying thresholds. Threshold 0.4 narrowly fails
(2/19=10.5%); 0.5 qualifies (1/19=5.3%) and retains 6/9 positives; 0.6 also qualifies
but retains only 1/9. Therefore **freeze threshold 0.5**. It happens to match the software
default, but the justification is the validation-only consequence rule, not defaulting.

**Development-only 5-fold default-threshold accuracy:** `[0.7826, 0.6957, 0.8636,
0.6364, 0.8182]`, mean=0.7593. This is a variability check on the 112 development rows;
it does not validate the selected threshold and does not touch final-test rows.

**Final test, opened once after freezing model and threshold 0.5:** TN=16, FP=2, FN=8,
TP=2; precision=0.500, recall=0.200, F1=0.286. Report this performance drop honestly;
do not send it back into threshold selection.

**Manual validation check at 0.5:** from TN=18, FP=1, FN=3, TP=6, precision=6/7=0.8571,
recall=6/9=0.6667, and F1=0.7500, matching `sklearn.metrics`.

### Track B — continuous-outcome regression refinement (deepens Week 13, does not build a classifier)

Use the same fixed indices: both feature sets fit the 84 training rows and score the same
28 validation rows; the 28 final-test rows remain sealed. On validation, the 3-feature
model gives MAE=2.5583, RMSE=3.0016, R²=0.3903. Adding `compactness` gives
MAE=2.4733, RMSE=2.9129, R²=0.4258 (error reductions 0.0850 and 0.0888; R² gain 0.0355).

**Paired development-only 5-fold R²:** 3-feature `[0.4305, 0.3783, 0.0515, 0.0858,
0.2103]`, mean=0.2313; 4-feature `[0.4663, 0.4500, 0.2198, 0.3142, 0.1625]`,
mean=0.3225. The direction recurs on average, with substantial fold variation. Use this
alongside validation to freeze the 4-feature specification before final testing.

Refit the selected 4-feature model on all 112 development rows and open the 28-row final
test once: MAE=1.9881, RMSE=2.5210, R²=0.5167. The Week 15 baseline-design prediction
from this final refit is 31.2886.

### Model card (both tracks, one page)

State plainly: n=140 synthetic portfolio; 84 train / 28 validation / 28 untouched final;
feature ranges and non-extrapolation limit; no causal claim. Track A records threshold
0.5 selected on validation by FPR ≤10% then maximum recall, plus the one-time final-test
matrix. Track B records validation and paired development-CV selection evidence plus the
one-time final-test MAE/RMSE/R². Fold ranges and test RMSE are not individual prediction
intervals.

## Week 15 — predict-optimize-decide synthesis (worked demo, Meeting A only)

No Meeting B this week (Dec 9 is a reading day). This is a fully worked REFERENCE demo
for the instructor to narrate live, showing the exact integration pattern Project 2 Part
IV requires — not a graded studio task (Week 15 has none, per the plan).

**Baseline design** (a plausible "as-designed" starting point, held fixed except where
noted): `wwr=0.50, shade_m=0.20, glazing_shgc=0.45, compactness=1.10, orientation=S`.
**Verified surrogate-model (Week 14 Track B's 4-feature `LinearRegression`) predicted EUI
at baseline: 31.0982.**

**The integration move:** feed the FITTED regression model's `.predict()` call, wrapped
in a small Python function of `(wwr, shade_m)` only (holding `glazing_shgc`,
`compactness`, `orientation` fixed at the baseline values above), directly to
`scipy.optimize.minimize` as the objective — exactly Week 11's tool, but now the
objective is a fitted model instead of Week 9/11's analytic `energy_proxy` formula. This
is the project's central "predict, then optimize" move, made concrete and small enough to
narrate in one sitting.

**Verified result:** `minimize(..., x0=(0.50, 0.20), bounds=[(0.20,0.60),(0.0,1.2)])` →
`x=[0.20, 1.20]` (both variables land exactly on their lower/upper BOUND — worth
explaining explicitly: because the fitted surrogate is AFFINE in `wwr` and `shade_m`
holding the remaining features fixed, every local optimum on this bounded convex box is
global; at least one optimum lies on a boundary face or corner, while a flat face can
create multiple tied global optima), predicted EUI=**22.8698**, an improvement of **8.2284
kWh/m2/yr (26.46%)** over the baseline. **Verified from a second, very different starting
guess** (`x0=(0.22, 1.10)`): converges to the identical `x=[0.20, 1.20]`, EUI=22.8698 —
confirm and narrate this explicitly as a direct, honest CONTRAST with Week 11's two-basin
function, where most starting guesses landed in the higher local basin. Say plainly: "on
this bounded convex box, the linear surrogate has no SUBOPTIMAL local optimum; every
local optimum is global, and ties can create more than one. That is a property of THIS
model and domain, not a guarantee for nonlinear models or nonconvex feasible sets."

**Track A (go/no-go) integration pattern — describe conceptually, no separate full
numeric demo required to keep this single 80-minute session focused:** the
classifier's `predict_proba(...)[:, 1]` (predicted P(meets code)) is used as a
CONSTRAINT rather than the objective — e.g., "search over `(wwr, shade_m)` for the design
that minimizes cost/maximizes some other objective, SUBJECT TO predicted P(meets code) >=
0.5" (reusing Week 14 Track A's frozen validation-selected threshold). Name this explicitly as the
same predict-optimize-decide pattern, applied to a constraint instead of an objective.

**Decision framing to close the demo:** state the recommendation as bounded and
uncertain, not definitive — "the surrogate model predicts an EUI reduction of about 8.2
kWh/m2/yr (about 26%) at `wwr=0.20, shade_m=1.20`, holding shgc/compactness/orientation
fixed at baseline; this prediction inherits the fitted model's own honest uncertainty
(recall Week 14's cross-validated R² ranged from -0.20 to 0.57) and its training-range
limits (recall Week 13's silent-extrapolation note) — it is a recommendation to
investigate further at full simulation fidelity, not a guaranteed result." This sentence
IS the "predict, optimize, decide" synthesis the plan asks Week 15 to deliver.
