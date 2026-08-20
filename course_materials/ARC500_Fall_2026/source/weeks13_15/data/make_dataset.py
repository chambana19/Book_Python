"""Regenerates radley_portfolio_envelope.csv exactly (random_state fixed).
Reference only -- the CSV in this folder is already the authoritative output;
re-run this only to confirm reproducibility, never to produce a different file."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
N = 140

wwr = rng.uniform(0.20, 0.60, N)
shade_m = rng.uniform(0.0, 1.2, N)
glazing_shgc = rng.uniform(0.25, 0.65, N)
compactness = rng.uniform(0.8, 1.4, N)
orientation = rng.choice(["N", "E", "S", "W"], size=N, p=[0.25, 0.25, 0.25, 0.25])
orient_offset = {"N": -1.0, "E": 0.0, "S": 1.0, "W": 0.5}
orient_vals = np.array([orient_offset[o] for o in orientation])
noise = rng.normal(0, 2.4, N)

eui = (15.0
       + 18.0 * wwr
       - 4.0 * shade_m
       + 6.0 * glazing_shgc
       + 5.0 * compactness
       + orient_vals
       + noise)

df = pd.DataFrame({
    "variant_id": [f"V{i+1:03d}" for i in range(N)],
    "wwr": wwr.round(3),
    "shade_m": shade_m.round(3),
    "glazing_shgc": glazing_shgc.round(3),
    "compactness": compactness.round(3),
    "orientation": orientation,
    "eui_kwh_m2yr": eui.round(2),
})
df["est_annual_cost_index"] = (df["eui_kwh_m2yr"] * 0.14 + rng.normal(0, 0.05, N)).round(3)
df["meets_code"] = (df["eui_kwh_m2yr"] <= 27.0).astype(int)

if __name__ == "__main__":
    df.to_csv("radley_portfolio_envelope.csv", index=False)
    print("wrote radley_portfolio_envelope.csv, n =", len(df))
