// ARC 500 deck design system — shared build harness.
//
// One buildDeck() used by every week's builder, so a change to the design
// system reaches all decks instead of being re-implemented per block. Emits
// typography/overflow diagnostics per deck (see measure.mjs) so layout drift is
// caught by the build rather than by reading slides one at a time.

import fs from "node:fs/promises";
import fsSync from "node:fs";
import path from "node:path";
import JSZip from "jszip";
import { Presentation, PresentationFile } from "@oai/artifact-tool";
import { G } from "./tokens.mjs";
import { makeCtx, makeLayouts } from "./layouts.mjs";
import { Diagnostics } from "./measure.mjs";

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

function escapeXmlAttribute(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll('"', "&quot;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("'", "&apos;");
}

/**
 * Persist authored figure descriptions in the field PowerPoint exposes as Alt
 * Text. The current artifact exporter preserves `image.alt` in inspection
 * metadata but omits p:cNvPr/@descr from the serialized PPTX. Treating that as
 * a post-export invariant keeps the release accessible and makes any future
 * exporter change safe: existing descriptions are replaced deterministically.
 */
async function persistPictureAltText(pptxPath, slides) {
  const zip = await JSZip.loadAsync(await fs.readFile(pptxPath));
  let pictureCount = 0;

  for (const [index, specSlide] of slides.entries()) {
    const slidePath = `ppt/slides/slide${index + 1}.xml`;
    const entry = zip.file(slidePath);
    if (!entry) throw new Error(`missing exported slide XML: ${slidePath}`);
    let xml = await entry.async("string");
    const pictures = xml.match(/<p:pic\b[\s\S]*?<\/p:pic>/g) || [];
    if (!pictures.length) continue;

    if (specSlide.layout !== "figure") {
      throw new Error(`slide ${index + 1} exports ${pictures.length} picture(s) without a figure-layout alt-text contract`);
    }
    if (pictures.length !== 1) {
      throw new Error(`slide ${index + 1} exports ${pictures.length} pictures; expected exactly one described figure`);
    }

    const description = escapeXmlAttribute(specSlide.alt || specSlide.title);
    let updated = false;
    xml = xml.replace(/<p:pic\b[\s\S]*?<\/p:pic>/, (pictureXml) =>
      pictureXml.replace(/<p:cNvPr\b([^>]*?)(?:\sdescr="[^"]*")?\s*\/>/, (_match, attrs) => {
        updated = true;
        const cleanAttrs = attrs.replace(/\sdescr="[^"]*"/g, "").trimEnd();
        return `<p:cNvPr${cleanAttrs} descr="${description}"/>`;
      })
    );
    if (!updated) throw new Error(`slide ${index + 1} picture is missing a writable p:cNvPr node`);
    zip.file(slidePath, xml);
    pictureCount += 1;
  }

  if (pictureCount) {
    const bytes = await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
    await fs.writeFile(pptxPath, bytes);
  }
}

/** Resolve a spec's effective slide list, honouring includeSlides/durationOverrides. */
export function resolveSlides(spec) {
  const numbers = Array.isArray(spec.includeSlides) ? spec.includeSlides : spec.slides.map((_, i) => i + 1);
  return numbers.map((n) => {
    const slide = spec.slides[n - 1];
    if (!slide) throw new Error(`includeSlides references missing slide ${n}`);
    const override = spec.durationOverrides?.[String(n)];
    return override === undefined ? slide : { ...slide, duration: override };
  });
}

/**
 * @param {object} opts
 * @param {string} opts.here      builder directory (holds specs/ and handouts/)
 * @param {string} opts.out       .pptx output directory
 * @param {string} opts.id        deck id, e.g. "01a"
 * @param {object} opts.sources   source-key map for speaker notes
 * @param {boolean} [opts.render] also render per-slide PNGs (default true)
 */
export async function buildDeck({ here, out, id, sources, render = true }) {
  const specPath = path.join(here, "specs", `week${id}.json`);
  const spec = JSON.parse(await fs.readFile(specPath, "utf8"));
  const deck = Presentation.create({ slideSize: { width: G.stageW, height: G.stageH } });
  const W = spec.weekLabel;

  const diag = new Diagnostics();
  const ctx = makeCtx(diag);
  // `figure` slides name a file; resolve it against this block's figures/ directory so
  // specs stay portable and a missing figure fails loudly at build time.
  //
  // Images are inlined as data URLs rather than handed over as a `path`: the renderer's
  // path lookup silently produced a zero-byte media entry here (the slide rendered as an
  // empty grey panel and the build still reported success), which is exactly the kind of
  // failure that ships unnoticed. Reading the bytes ourselves makes a missing or
  // unreadable figure a hard build error instead.
  const figuresDir = path.join(here, "figures");
  const figureCache = new Map();
  const L = makeLayouts(ctx, sources, diag, {
    resolveFigure: (f) => {
      if (!f) throw new Error("figure slide is missing its `figure` filename");
      if (figureCache.has(f)) return figureCache.get(f);
      const abs = path.join(figuresDir, f);
      let bytes;
      try {
        bytes = fsSync.readFileSync(abs);
      } catch {
        throw new Error(`figure not found: ${abs} — run figures/make_figures.py for this block`);
      }
      if (!bytes.length) throw new Error(`figure is empty: ${abs}`);
      const contentType = f.endsWith(".svg") ? "image/svg+xml" : "image/png";
      const src = { dataUrl: `data:${contentType};base64,${bytes.toString("base64")}`, contentType };
      figureCache.set(f, src);
      return src;
    },
  });

  const slides = resolveSlides(spec);
  for (const [i, s] of slides.entries()) {
    const fn = L[s.layout];
    if (!fn) throw new Error(`week ${id} slide ${i + 1}: unknown layout "${s.layout}"`);
    try {
      fn(deck, W, s);
    } catch (e) {
      throw new Error(`week ${id} slide ${i + 1} (${s.layout}): ${e.message}`);
    }
  }

  const pptxPath = path.join(out, spec.fileName);
  const pptx = await PresentationFile.exportPptx(deck);
  await pptx.save(pptxPath);
  await persistPictureAltText(pptxPath, slides);

  const renderDir = path.join(here, "renders", `week${id}`);
  if (render) {
    await fs.rm(renderDir, { recursive: true, force: true });
    await fs.mkdir(renderDir, { recursive: true });
    for (const [i, slide] of deck.slides.items.entries()) {
      const png = await deck.export({ slide, format: "png", scale: 1 });
      await writeBlob(path.join(renderDir, `slide-${String(i + 1).padStart(2, "0")}.png`), png);
    }
  }
  try {
    await fs.mkdir(renderDir, { recursive: true });
    await fs.rename(`${pptxPath}.inspect.ndjson`, path.join(renderDir, "inspect.ndjson"));
  } catch (e) {
    if (e?.code !== "ENOENT") throw e;
  }

  for (const item of spec.handouts || []) {
    await fs.copyFile(path.join(here, "handouts", item.source), path.join(out, "Handouts", item.fileName));
  }

  const minutes = slides.reduce((a, b) => a + (b.duration || 0), 0);
  return { id, file: spec.fileName, slides: deck.slides.items.length, minutes, diag };
}

/** CLI wrapper shared by every week's builder. */
export async function runBuilder({ here, out, sources, pattern = /^week(\d\d[ab])\.json$/i }) {
  await fs.mkdir(out, { recursive: true });
  await fs.mkdir(path.join(out, "Handouts"), { recursive: true });
  await fs.mkdir(path.join(here, "renders"), { recursive: true });

  const argv = process.argv.slice(2).filter((a) => !a.startsWith("--"));
  const quiet = process.argv.includes("--quiet");
  const ids = argv.length
    ? argv
    : (await fs.readdir(path.join(here, "specs")).catch(() => []))
        .map((f) => f.match(pattern)?.[1])
        .filter(Boolean)
        .sort();

  const built = [];
  let failed = 0;
  for (const id of ids) {
    try {
      const r = await buildDeck({ here, out, id, sources });
      built.push(r);
      console.log(`built week ${r.id}: ${r.slides} slides, ${r.minutes} min -> ${r.file}`);
      if (!quiet) console.log(r.diag.report());
    } catch (e) {
      failed += 1;
      console.error(`FAILED week ${id}: ${e.message}`);
      process.exitCode = 1;
    }
  }
  console.log(`\n${built.length}/${ids.length} decks built into ${out}`);
  if (failed) console.log(`${failed} failed`);
  return built;
}
