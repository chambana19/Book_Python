// Text measurement + vertical-rhythm helpers.
//
// The renderer's `autoFit: "shrinkText"` silently rescales any box whose text
// overflows. That is what made the decks look typographically random: two
// slides using the same nominal role rendered at different actual sizes purely
// because one had more words. The fix is to MEASURE first — estimate how tall a
// block will render, then (a) position it deliberately and (b) warn at build
// time when it genuinely will not fit, instead of letting it shrink in silence.

import { LS } from "./tokens.mjs";

// Average glyph advance as a fraction of point size. Consolas is a fixed 0.55
// advance. Arial regular-weight was measured empirically against a real
// render (a table cell wrapped to 2 lines in practice; 0.5 predicted 3 and
// produced a false-positive overflow warning) and calibrated to 0.42. Bold
// Arial glyphs are measurably wider than regular at the same point size —
// three independent revision passes (Weeks 4-8, 9-12, 13-15) each hit the
// SAME bug before this constant existed: a bold heading estimated at N lines
// actually wrapped to N+1, and the extra line's body text collided with
// whatever was positioned right below it (a chart's explain body, an
// anatomy chip's body, a code slide's explain body). 0.46 (~10% wider) is
// calibrated from those confirmed real-render mismatches, not a guess.
// sansBold bumped again (0.46 -> 0.50) after a THIRD confirmed real-render
// collision (a code-slide explainHead this time, in the shared column()
// panel every code/chart/twoColumn slide across all four course blocks
// uses) -- 0.46 still under-predicted wrapping for bold headings. This one
// applies to bold text only; regular sans (0.42, driving all the
// already-confirmed-good table/predict-box estimates) is untouched.
// sans recalibrated 0.42 -> 0.465 against a real render: the chart-explain body on
// Week 6A slide 21 rendered 10 lines with a longest line of 35 characters in a 376pt
// column at 23pt, implying an advance of 376/35/23 = 0.467. At 0.42 the estimator
// predicted 38 characters per line — i.e. FEWER lines than reality — which is why body
// text positioned beneath a measured heading could still collide with it.
const ADVANCE = { sans: 0.465, sansBold: 0.54, mono: 0.55 };

export function charWidth(fontSize, mono = false, bold = false) {
  return fontSize * (mono ? ADVANCE.mono : bold ? ADVANCE.sansBold : ADVANCE.sans);
}

/** Estimated rendered line count for `text` inside a box `boxW` wide. */
export function estimateLines(text, boxW, fontSize, mono = false, bold = false) {
  if (text == null || text === "") return 0;
  const perLine = Math.max(1, Math.floor(boxW / charWidth(fontSize, mono, bold)));
  let lines = 0;
  for (const para of String(text).split("\n")) {
    if (para.length === 0) {
      lines += 1;
      continue;
    }
    // Proportional text wraps on WORD boundaries. Dividing the character count by the
    // line capacity ignores that and systematically UNDER-counts lines in narrow
    // columns: the heading "The raw relationship, before color and annotation" (49
    // chars, 25-char capacity) measured as 2 lines but rendered as 3, and the body
    // positioned directly beneath it overlapped that third line on a shipped slide.
    // Monospace stays character-based on purpose — code panels are hard-wrapped by the
    // author at explicit newlines, and their budgets are calibrated to that.
    if (mono) {
      lines += Math.ceil(para.length / perLine);
      continue;
    }
    let used = 1;
    let cur = 0;
    for (const word of para.split(/\s+/).filter(Boolean)) {
      const candidate = cur === 0 ? word.length : cur + 1 + word.length;
      if (candidate <= perLine) {
        cur = candidate;
        continue;
      }
      if (cur !== 0) used += 1;
      cur = word.length;
      // A single word wider than the box breaks mid-word rather than overflowing.
      while (cur > perLine) {
        used += 1;
        cur -= perLine;
      }
    }
    lines += used;
  }
  return lines;
}

/** Estimated rendered height in points. */
export function estimateHeight(text, boxW, fontSize, lineSpacing = LS.body, mono = false, bold = false) {
  return estimateLines(text, boxW, fontSize, mono, bold) * fontSize * lineSpacing;
}

/**
 * Vertically place a block of known height inside a band.
 * Short blocks are optically centred (see G.centerBias) so they read as
 * deliberate rather than as content that ran out halfway down the slide.
 * Blocks at least as tall as the band are simply top-anchored.
 */
export function blockTop(blockH, bandTop, bandH, bias) {
  if (blockH >= bandH) return bandTop;
  return Math.round(bandTop + (bandH - blockH) * bias);
}

/**
 * Collects build-time typography/overflow diagnostics so layout problems are
 * reported as numbers rather than discovered by eye, slide by slide.
 */
export class Diagnostics {
  constructor() {
    this.overflows = [];
    this.sizes = new Map();
    this.fills = [];
  }

  /** Record every font size actually emitted, to prove the scale is respected. */
  noteSize(fontSize, role = "?") {
    if (!Number.isInteger(fontSize) || fontSize % 4 !== 0) {
      throw new Error(`font size ${fontSize}px for ${role} will not export as a whole-point PowerPoint size`);
    }
    const key = `${fontSize}`;
    const entry = this.sizes.get(key) || { size: fontSize, count: 0, roles: new Set() };
    entry.count += 1;
    entry.roles.add(role);
    this.sizes.set(key, entry);
  }

  noteOverflow(slideNo, name, needed, available) {
    this.overflows.push({
      slideNo,
      name,
      needed: Math.round(needed),
      available: Math.round(available),
      over: Math.round(needed - available),
    });
  }

  noteFill(slideNo, layout, usedH, bandH) {
    this.fills.push({ slideNo, layout, pct: Math.round((usedH / bandH) * 100) });
  }

  report() {
    const sizes = [...this.sizes.values()].sort((a, b) => b.size - a.size);
    const lines = [];
    lines.push(`  type scale in use: ${sizes.length} distinct sizes`);
    lines.push(
      "    " + sizes.map((s) => `${s.size}pt x${s.count}`).join("  "),
    );
    if (this.overflows.length) {
      lines.push(`  OVERFLOW WARNINGS (${this.overflows.length}) — revise content or geometry before delivery:`);
      for (const o of this.overflows.slice(0, 12)) {
        lines.push(`    slide ${o.slideNo} "${o.name}": needs ${o.needed}pt in ${o.available}pt (+${o.over})`);
      }
      if (this.overflows.length > 12) lines.push(`    ...and ${this.overflows.length - 12} more`);
    } else {
      lines.push("  no overflow warnings");
    }
    const low = this.fills.filter((f) => f.pct < 55);
    if (low.length) {
      lines.push(`  LOW FILL (<55% of content band): ${low.map((l) => `${l.slideNo}(${l.pct}%)`).join(" ")}`);
    }
    return lines.join("\n");
  }
}
