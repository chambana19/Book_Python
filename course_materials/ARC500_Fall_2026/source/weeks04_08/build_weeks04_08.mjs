// Builds the ARC 500 Weeks 4-8 A/B lecture decks from authored specs.
//
//   node build_weeks04_08.mjs             # all specs found
//   node build_weeks04_08.mjs 04a 05b     # selected decks
//
// All layout/typography lives in the shared design system at
// ../_design/ so Weeks 1-3, 4-8, 9-12 and 13-15 stay visually identical.

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runBuilder } from "../_design/build.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");
const OUT = path.join(ROOT, "ARC500_2026_Expanded_Two_Meeting_Materials", "Weeks04-08_DataAsEvidence");
const SRC = JSON.parse(await fs.readFile(path.join(HERE, "sources.json"), "utf8"));

await runBuilder({ here: HERE, out: OUT, sources: SRC, pattern: /^week(\d\d[ab])\.json$/i });
