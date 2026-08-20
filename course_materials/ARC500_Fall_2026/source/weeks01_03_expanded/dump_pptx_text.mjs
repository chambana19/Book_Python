// Dumps all slide text from an FS25 archive .pptx, shape by shape, for review.
import { PresentationFile } from "@oai/artifact-tool";
import fs from "node:fs/promises";

const srcPath = process.argv[2];
const buf = new Uint8Array(await fs.readFile(srcPath));
const deck = await PresentationFile.importPptx(buf);
console.log(`FILE: ${srcPath}`);
console.log(`SLIDES: ${deck.slides.items.length}\n`);
deck.slides.items.forEach((slide, i) => {
  console.log(`===== slide ${i + 1} =====`);
  for (const sh of slide.shapes.items) {
    let t;
    try { t = sh.text?.toString?.() ?? sh.text; } catch { t = null; }
    if (t && String(t).trim()) console.log(String(t).trim());
  }
  console.log("");
});
