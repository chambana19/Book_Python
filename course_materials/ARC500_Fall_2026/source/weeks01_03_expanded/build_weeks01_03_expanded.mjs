// Builds the ARC 500 Weeks 1-3 A/B lecture decks from authored specs.
//
//   node build_weeks01_03_expanded.mjs             # all specs found
//   node build_weeks01_03_expanded.mjs 01a 02b     # selected decks
//   node build_weeks01_03_expanded.mjs --quiet     # suppress typography report
//
// All layout/typography lives in the shared design system at
// ../_design/ so Weeks 1-3, 4-8, 9-12 and 13-15 stay visually identical.

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { runBuilder } from "../_design/build.mjs";

// fileURLToPath (not URL.pathname) — the course path contains spaces, which
// stay percent-encoded in a file:// URL and break plain string handling.
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");
const OUT = path.join(ROOT, "ARC500_2026_Expanded_Two_Meeting_Materials", "Weeks01-03_Foundations");
const SRC = JSON.parse(await fs.readFile(path.join(HERE, "sources.json"), "utf8"));

await runBuilder({ here: HERE, out: OUT, sources: SRC });
