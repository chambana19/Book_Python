import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildDeck } from "../_design/build.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..", "..");
const PACKAGE = path.join(ROOT, "ARC500_2026_Expanded_Two_Meeting_Materials");

await buildDeck({
  here: HERE,
  out: path.join(PACKAGE, "Project01_Evidence_Before_Design"),
  id: "p1",
  sources: {},
});

await buildDeck({
  here: HERE,
  out: path.join(PACKAGE, "Project02_Predict_Optimize_Decide"),
  id: "p2",
  sources: {},
});

console.log("Built consistent Project 1 and Project 2 presentation templates.");
