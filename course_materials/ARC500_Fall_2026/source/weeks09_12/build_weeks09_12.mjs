// Builds the ARC 500 Weeks 9-12 A/B lecture decks from authored specs
// (Optimization: parameter sweeps, then linear/gradient/heuristic search).
//
//   node build_weeks09_12.mjs             # all specs found
//   node build_weeks09_12.mjs 09a 12b     # selected decks
//
// All layout/typography lives in the shared design system at
// ../_design/ so Weeks 1-3, 4-8, 9-12 and 13-15 stay visually identical.

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runBuilder } from "../_design/build.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");
const OUT = path.join(ROOT, "ARC500_2026_Expanded_Two_Meeting_Materials", "Weeks09-12_Optimization");
const SRC = JSON.parse(await fs.readFile(path.join(HERE, "sources.json"), "utf8"));

await runBuilder({ here: HERE, out: OUT, sources: SRC, pattern: /^week(\d\d[ab])\.json$/i });
