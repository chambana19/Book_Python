// ARC 500 deck design system — layout library.
//
// Every layout draws from the shared scale in tokens.mjs. No layout defines its
// own font size. Where a layout needs to fit a variable amount of content it
// MEASURES (measure.mjs) and either optically centres the block or reports an
// overflow at build time — it never leaves the renderer to silently shrink text
// to an arbitrary size, which was the root cause of the "many different font
// sizes" problem this system replaces.

import { T, LS, G, C, FONT } from "./tokens.mjs";
import { estimateHeight, estimateLines, blockTop, charWidth } from "./measure.mjs";

// PowerPoint stores 0.75 points per CSS pixel. Snap any spec-level override
// (for example anatomy/code sizes) to four-pixel steps so the exported file
// contains whole-point font sizes.
const exportSafeFontSize = (value) => Math.max(4, Math.round(value / 4) * 4);

// ------------------------------------------------------------- primitives
export function makeCtx(diag) {
  let slideNo = 0;

  function addText(slide, text, position, style = {}, name = undefined) {
    const fontSize = exportSafeFontSize(style.fontSize ?? T.body);
    diag?.noteSize(fontSize, name || "unnamed");
    const shape = slide.shapes.add({
      geometry: "textbox",
      name,
      position,
      fill: "none",
      line: { style: "solid", fill: "none", width: 0 },
    });
    shape.text = text;
    shape.text.style = {
      typeface: style.typeface ?? FONT.sans,
      fontSize,
      color: style.color ?? C.ink,
      bold: style.bold ?? false,
      alignment: style.alignment ?? "left",
      verticalAlignment: style.verticalAlignment ?? "top",
      // Fixed-size text is intentional: silent shrink-to-fit creates fractional
      // effective sizes and makes equivalent ideas look inconsistently ranked.
      // addFitted measures every variable block and reports overflow instead.
      autoFit: style.autoFit ?? "none",
      wrap: "square",
      lineSpacing: style.lineSpacing ?? LS.body,
      insets: style.insets ?? { top: 0, right: 0, bottom: 0, left: 0 },
    };
    return shape;
  }

  /** addText + build-time overflow check against the box height. */
  function addFitted(slide, text, position, style = {}, name = undefined, mono = false) {
    const fs = exportSafeFontSize(style.fontSize ?? T.body);
    const ls = style.lineSpacing ?? LS.body;
    // style.bold flows into the estimate automatically -- bold Arial wraps
    // sooner than regular at the same width, and the overflow check must
    // reflect that or it silently under-reports real risk on every bold head.
    const needed = estimateHeight(text, position.width, fs, ls, mono, style.bold ?? false);
    if (needed > position.height + 2) diag?.noteOverflow(slideNo, name || "unnamed", needed, position.height);
    return addText(slide, text, position, { ...style, fontSize: fs }, name);
  }

  function addPanel(slide, position, fill = C.panel2, line = C.rule, radius = 0, name = undefined) {
    return slide.shapes.add({
      geometry: radius ? "roundRect" : "rect",
      name,
      position,
      fill,
      line: { style: "solid", fill: line, width: line === "none" ? 0 : 1 },
      ...(radius ? { borderRadius: radius } : {}),
    });
  }

  function addRule(slide, left, top, width, color = C.ink, weight = 2) {
    slide.shapes.add({
      geometry: "line",
      position: { left, top, width, height: 0 },
      fill: "none",
      line: { style: "solid", fill: color, width: weight },
    });
  }

  function setNotes(slide, duration, teaching, sources = [], SRC = {}) {
    const urls = (sources || []).map((k) => SRC[k]).filter(Boolean);
    const sourceBlock = urls.length ? `\n\n[Sources]\n${urls.map((s) => `- ${s}`).join("\n")}\n[/Sources]` : "";
    slide.speakerNotes.textFrame.setText(`Timing: ${duration} minutes.\nTeaching notes: ${teaching}${sourceBlock}`);
    slide.speakerNotes.setVisible(true);
  }

  function addFooter(slide, weekLabel, no) {
    addRule(slide, G.margin, G.footerRuleY, G.contentW, C.ruleSoft, 1);
    addText(slide, `ARC 500  ·  ${weekLabel}`, { left: G.margin, top: G.footerTextY, width: 700, height: 20 }, { fontSize: T.eyebrow, color: C.muted, lineSpacing: LS.tight }, "footer");
    addText(slide, String(no).padStart(2, "0"), { left: G.stageW - G.margin - 72, top: G.footerTextY, width: 72, height: 20 }, { fontSize: T.eyebrow, color: C.muted, alignment: "right", lineSpacing: LS.tight }, "page");
  }

  /** Standard content-slide chrome: kicker, title, footer. Returns the slide. */
  function makeSlide(deck, weekLabel, title, kicker = "") {
    const slide = deck.slides.add();
    slide.background.fill = C.white;
    slideNo = deck.slides.items.length;
    if (kicker) {
      addText(slide, String(kicker).toUpperCase(), { left: G.margin, top: G.kickerY, width: 700, height: 20 }, { fontSize: T.eyebrow, bold: true, color: C.accent, lineSpacing: LS.tight }, "kicker");
    }
    addFitted(slide, title, { left: G.margin, top: G.titleY, width: G.contentW, height: G.titleH }, { fontSize: T.h1, color: C.ink, lineSpacing: LS.head }, "title");
    addFooter(slide, weekLabel, slideNo);
    return slide;
  }

  /**
   * Draw a head+body column, optically centred in the content band when short.
   * Returns the bottom y actually used, so callers can report band fill.
   */
  function column(slide, x, w, head, body, opts = {}) {
    const bandTop = opts.bandTop ?? G.contentTop;
    const bandH = opts.bandH ?? G.contentH;
    const bodySize = opts.bodySize ?? T.body;
    const headGap = 22;
    // head always renders bold (see the addFitted call below) -- measure it
    // as bold, or a head that truly needs 3 lines gets positioned as if it
    // only needed 2, and the body drawn right after it collides with line 3.
    const headH = head ? estimateHeight(head, w, T.h2, LS.head, false, true) : 0;
    const bodyH = body ? estimateHeight(body, w, bodySize, LS.body) : 0;
    const blockH = headH + (head && body ? headGap : 0) + bodyH;
    const top = opts.top ?? blockTop(blockH, bandTop, bandH, G.centerBias);
    let y = top;
    if (head) {
      addFitted(slide, head, { left: x, top: y, width: w, height: Math.max(36, headH + 6) }, { fontSize: T.h2, bold: true, color: C.ink, lineSpacing: LS.head }, `${opts.name || "col"}-head`);
      y += headH + headGap;
    }
    if (body) {
      addFitted(slide, body, { left: x, top: y, width: w, height: Math.max(30, Math.min(bodyH + 8, bandTop + bandH - y)) }, { fontSize: bodySize, color: C.muted, lineSpacing: LS.body }, `${opts.name || "col"}-body`);
      y += bodyH;
    }
    return y;
  }

  const ctx = { addText, addFitted, addPanel, addRule, setNotes, addFooter, makeSlide, column, get slideNo() { return slideNo; } };
  return ctx;
}

// ------------------------------------------------------------- layouts
/**
 * @param {object} [opts]
 * @param {(name: string) => string} [opts.resolveFigure] maps a spec's `figure`
 *   filename to an absolute path on disk (per-block `figures/` directory).
 */
export function makeLayouts(ctx, SRC, diag, opts = {}) {
  const { addText, addFitted, addPanel, addRule, setNotes, makeSlide, column } = ctx;
  const notes = (slide, s) => setNotes(slide, s.duration, s.teaching, s.sources, SRC);
  const fill = (s, used) => diag?.noteFill(ctx.slideNo, s.layout, used - G.contentTop, G.contentH);
  const resolveFigure = opts.resolveFigure ?? ((f) => f);

  return {
    title(deck, W, s) {
      const slide = deck.slides.add();
      slide.background.fill = C.charcoal;
      addText(slide, "<>  ARC 500", { left: G.margin, top: 48, width: 320, height: 30 }, { fontSize: T.h3, bold: true, color: C.white, lineSpacing: LS.tight }, "course-mark");
      addText(slide, "Programming with Python and Generative AI  ·  Scripting, Data Analysis, Visualization, Problem-Solving, and Optimization", { left: G.margin, top: 86, width: 1060, height: 26 }, { fontSize: T.eyebrow, color: "#9AA1AC", lineSpacing: LS.tight }, "course-full-title");
      addPanel(slide, { left: G.margin, top: 140, width: 14, height: 300 }, C.accent, "none", 0, "accent-bar");
      addText(slide, String(W).toUpperCase(), { left: G.margin + 44, top: 142, width: 760, height: 28 }, { fontSize: T.caption, bold: true, color: C.accentLight, lineSpacing: LS.tight }, "week-label");
      addFitted(slide, s.title, { left: G.margin + 44, top: 186, width: 1040, height: 200 }, { fontSize: T.display, bold: true, color: C.white, lineSpacing: LS.head }, "deck-title");
      addFitted(slide, s.subtitle, { left: G.margin + 44, top: 404, width: 960, height: 96 }, { fontSize: T.h2, color: "#D7D9DC", lineSpacing: LS.head }, "deck-subtitle");
      addRule(slide, G.margin + 44, 556, 260, C.white, 1);
      addText(slide, "JunHo Chun, PhD  ·  School of Architecture  ·  Syracuse University  ·  Fall 2026", { left: G.margin + 44, top: 580, width: 820, height: 28 }, { fontSize: T.caption, color: "#D7D9DC", lineSpacing: LS.tight }, "instructor");
      notes(slide, s);
    },

    statement(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Principle");
      const stH = estimateHeight(s.statement, G.contentW - 120, T.hero, LS.head, false, true);
      const supH = s.supporting ? estimateHeight(s.supporting, 980, T.h3, LS.body) : 0;
      const blockH = stH + (s.supporting ? 40 + 30 + supH : 0);
      let y = blockTop(blockH, G.contentTop, G.contentH, 0.3);
      addFitted(slide, s.statement, { left: G.margin, top: y, width: G.contentW - 120, height: stH + 8 }, { fontSize: T.hero, bold: true, color: C.ink, lineSpacing: LS.head }, "statement");
      y += stH + 30;
      addRule(slide, G.margin, y, 168, C.accent, 5);
      y += 34;
      if (s.supporting) {
        addFitted(slide, s.supporting, { left: G.margin, top: y, width: 980, height: supH + 8 }, { fontSize: T.h3, color: C.muted, lineSpacing: LS.body }, "supporting");
        y += supH;
      }
      fill(s, y);
      notes(slide, s);
    },

    outcomes(deck, W, s) {
      const slide = makeSlide(deck, W, s.title || "By the end, you should be able to…", "Learning outcomes");
      const cellW = G.colW - 76;
      const rowTops = [G.contentTop + 8, G.contentTop + 240];
      s.outcomes.forEach((o, i) => {
        const x = i % 2 === 0 ? G.margin : G.colRightX;
        const top = rowTops[Math.floor(i / 2)];
        addText(slide, String(i + 1), { left: x, top, width: 52, height: 48 }, { fontSize: T.h1, bold: true, color: C.accent, lineSpacing: LS.tight }, `outcome-number-${i}`);
        addFitted(slide, o.head, { left: x + 62, top: top + 2, width: cellW, height: 44 }, { fontSize: T.h3, bold: true, lineSpacing: LS.head }, `outcome-head-${i}`);
        addFitted(slide, o.body, { left: x + 62, top: top + 54, width: cellW + 14, height: 150 }, { fontSize: T.bodySm, color: C.muted, lineSpacing: LS.body }, `outcome-body-${i}`);
      });
      fill(s, rowTops[1] + 200);
      notes(slide, s);
    },

    agenda(deck, W, s) {
      const slide = makeSlide(deck, W, s.title || "Today’s learning sequence", "Road map");
      const n = s.items.length;
      const step = Math.min(96, Math.floor(G.contentH / n));
      const top = G.contentTop + Math.round((G.contentH - step * n) / 2);
      s.items.forEach((item, i) => {
        const y = top + i * step;
        addText(slide, String(i + 1).padStart(2, "0"), { left: G.margin, top: y + 6, width: 62, height: 34 }, { fontSize: T.caption, bold: true, color: C.accent, lineSpacing: LS.tight }, `agenda-no-${i}`);
        addRule(slide, G.margin + 74, y + 22, 78, i === 0 ? C.accent : C.ruleSoft, i === 0 ? 3 : 1);
        addFitted(slide, item, { left: G.margin + 186, top: y, width: G.contentW - 186, height: step - 12 }, { fontSize: T.h2, color: C.ink, lineSpacing: LS.head }, `agenda-item-${i}`);
      });
      fill(s, top + step * n);
      notes(slide, s);
    },

    ladder(deck, W, s) {
      const slide = makeSlide(deck, W, s.title || "Numerical challenge ladder", s.kicker || "Scaffold");
      const tiers = s.tiers || [];
      const rowGap = 14;
      const rowH = Math.floor((G.contentH - rowGap * 2 - 12) / 3);
      const labelW = 176;
      const answerW = 300;
      const taskW = G.contentW - labelW - answerW - 52;
      const levelColors = [C.green, C.accent, C.amber];
      tiers.forEach((tier, i) => {
        const y = G.contentTop + 4 + i * (rowH + rowGap);
        const fillColor = i === 1 ? C.panelBlue : C.panel2;
        addPanel(slide, { left: G.margin, top: y, width: G.contentW, height: rowH }, fillColor, C.ruleSoft, 8, `ladder-row-${i}`);
        addPanel(slide, { left: G.margin, top: y, width: 8, height: rowH }, levelColors[i] || C.accent, "none", 0, `ladder-accent-${i}`);
        addText(slide, String(tier.level || ["EASY", "MEDIUM", "HARD"][i]).toUpperCase(), { left: G.margin + 26, top: y + 18, width: labelW - 32, height: 24 }, { fontSize: T.eyebrow, bold: true, color: levelColors[i] || C.accent, lineSpacing: LS.tight }, `ladder-level-${i}`);
        addFitted(slide, tier.focus, { left: G.margin + 26, top: y + 50, width: labelW - 32, height: rowH - 62 }, { fontSize: T.caption, bold: true, color: C.ink, lineSpacing: LS.body }, `ladder-focus-${i}`);
        addFitted(slide, tier.task, { left: G.margin + labelW + 18, top: y + 18, width: taskW, height: rowH - 36 }, { fontSize: T.body, color: C.ink, lineSpacing: LS.body, verticalAlignment: "middle" }, `ladder-task-${i}`);
        addPanel(slide, { left: G.margin + labelW + taskW + 34, top: y + 18, width: 1, height: rowH - 36 }, C.rule, "none", 0, `ladder-divider-${i}`);
        addText(slide, "EXPECTED CHECK", { left: G.margin + labelW + taskW + 54, top: y + 18, width: answerW - 28, height: 20 }, { fontSize: T.eyebrow, bold: true, color: C.accentDeep, lineSpacing: LS.tight }, `ladder-check-label-${i}`);
        addFitted(slide, tier.answer, { left: G.margin + labelW + taskW + 54, top: y + 48, width: answerW - 28, height: rowH - 62 }, { typeface: tier.answerMono === false ? FONT.sans : FONT.mono, fontSize: T.bodySm, bold: true, color: C.ink, lineSpacing: LS.body }, `ladder-answer-${i}`, tier.answerMono !== false);
      });
      fill(s, G.contentBottom - 8);
      notes(slide, s);
    },

    process(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Method");
      const count = s.steps.length;
      const gap = count > 3 ? 24 : 38;
      const w = (G.contentW - gap * (count - 1)) / count;
      const panelTop = G.contentTop + 4;
      const panelH = G.contentH - 16;
      // Bodies in a 4-up row get the dense size; 2-3 up keeps full body size.
      const bodySize = count >= 4 ? T.bodySm : T.body;
      // A 4-up row is too narrow for h2 heads; drop one role, never a raw number.
      const headSize = count >= 4 ? T.h3 : T.h2;
      for (let i = 0; i < count - 1; i += 1) {
        const x = G.margin + w + i * (w + gap) + Math.round((gap - 16) / 2);
        slide.shapes.add({
          geometry: "chevron",
          name: `step-arrow-${i}`,
          position: { left: x, top: panelTop + panelH / 2 - 26, width: 16, height: 52 },
          fill: C.accentLight,
          line: { style: "solid", fill: C.accentLight, width: 0 },
        });
      }
      s.steps.forEach((step, i) => {
        const x = G.margin + i * (w + gap);
        addPanel(slide, { left: x, top: panelTop, width: w, height: panelH }, i === 0 ? C.panelBlue : C.panel2, i === 0 ? C.accent : C.ruleSoft, 10, `step-node-${i}`);
        const pad = 20;
        addText(slide, String(i + 1).padStart(2, "0"), { left: x + pad, top: panelTop + 20, width: 46, height: 30 }, { fontSize: T.caption, bold: true, color: C.accent, lineSpacing: LS.tight }, `step-number-${i}`);
        addFitted(slide, step.label, { left: x + pad + 52, top: panelTop + 22, width: w - pad * 2 - 52, height: 26 }, { fontSize: T.eyebrow, bold: true, color: C.accent, lineSpacing: LS.tight }, `step-label-${i}`);
        addRule(slide, x + pad, panelTop + 66, w - pad * 2, i === 0 ? C.accent : C.ink, i === 0 ? 3 : 2);
        const headH = estimateHeight(step.head, w - pad * 2, headSize, LS.head, false, true);
        addFitted(slide, step.head, { left: x + pad, top: panelTop + 86, width: w - pad * 2, height: Math.max(56, headH + 6) }, { fontSize: headSize, bold: true, lineSpacing: LS.head }, `step-head-${i}`);
        const bodyTop = panelTop + 86 + Math.max(56, headH + 6) + 16;
        addFitted(slide, step.body, { left: x + pad, top: bodyTop, width: w - pad * 2, height: panelTop + panelH - bodyTop - 18 }, { fontSize: bodySize, color: C.muted, lineSpacing: LS.body }, `step-body-${i}`);
      });
      fill(s, panelTop + panelH);
      notes(slide, s);
    },

    interface(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Spyder interface");
      const top = G.contentTop;
      const h = G.contentH - 8;
      addPanel(slide, { left: G.margin, top, width: G.contentW, height: h }, "#E8EAED", C.rule, 4, "app-frame");
      addPanel(slide, { left: G.margin, top, width: G.contentW, height: 38 }, C.charcoal, C.charcoal, 4, "app-toolbar");
      addText(slide, "SPYDER", { left: G.margin + 20, top: top + 9, width: 180, height: 22 }, { fontSize: T.eyebrow, bold: true, color: C.white, lineSpacing: LS.tight }, "app-name");
      const inner = G.margin + 18;
      addPanel(slide, { left: inner, top: top + 56, width: 660, height: 234 }, C.white, C.rule, 0, "editor-pane");
      addText(slide, "EDITOR", { left: inner + 18, top: top + 72, width: 200, height: 22 }, { fontSize: T.eyebrow, bold: true, color: C.accent, lineSpacing: LS.tight }, "editor-label");
      addFitted(slide, s.editorText, { left: inner + 18, top: top + 106, width: 616, height: 170 }, { typeface: FONT.mono, fontSize: T.mono, color: C.ink, lineSpacing: LS.mono }, "editor-text", true);
      addPanel(slide, { left: inner + 682, top: top + 56, width: 434, height: 150 }, C.white, C.rule, 0, "explorer-pane");
      addText(slide, "VARIABLE EXPLORER", { left: inner + 700, top: top + 72, width: 280, height: 22 }, { fontSize: T.eyebrow, bold: true, color: C.accent, lineSpacing: LS.tight }, "explorer-label");
      addFitted(slide, s.explorerText, { left: inner + 700, top: top + 106, width: 398, height: 88 }, { fontSize: T.bodySm, color: C.muted, lineSpacing: LS.body }, "explorer-text");
      addPanel(slide, { left: inner, top: top + 310, width: G.contentW - 36, height: h - 326 }, C.charcoal, C.charcoal, 0, "console-pane");
      addText(slide, "IPYTHON CONSOLE", { left: inner + 18, top: top + 324, width: 260, height: 20 }, { fontSize: T.eyebrow, bold: true, color: C.accentLight, lineSpacing: LS.tight }, "console-label");
      addFitted(slide, s.consoleText, { left: inner + 18, top: top + 354, width: G.contentW - 76, height: h - 380 }, { typeface: FONT.mono, fontSize: T.monoSm, color: C.white, lineSpacing: LS.mono }, "console-text", true);
      fill(s, top + h);
      notes(slide, s);
    },

    twoColumn(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Concept");
      // Both columns share one baseline: the taller block decides the top, so
      // the two heads always align even when their bodies differ in length.
      const measure = (c) =>
        estimateHeight(c.head, G.colW, T.h2, LS.head, false, true) + 22 + estimateHeight(c.body, G.colW, T.body, LS.body);
      const top = blockTop(Math.max(measure(s.left), measure(s.right)), G.contentTop, G.contentH, G.centerBias);
      const a = column(slide, G.margin, G.colW, s.left.head, s.left.body, { top, name: "left" });
      const b = column(slide, G.colRightX, G.colW, s.right.head, s.right.body, { top, name: "right" });
      fill(s, Math.max(a, b));
      notes(slide, s);
    },

    code(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Python syntax");
      const panelX = G.margin, panelW = 724;
      const panelTop = G.contentTop, panelH = G.contentH - 6;
      addPanel(slide, { left: panelX, top: panelTop, width: panelW, height: panelH }, C.charcoal, C.charcoal, 8, "code-panel");
      const pad = 26;
      const codeW = panelW - pad * 2;
      const codeLines = String(s.code || "").split("\n").length;
      const codeSize = exportSafeFontSize(s.codeSize || (codeLines >= 8 ? T.bodySm : T.mono));
      const outputSize = exportSafeFontSize(s.outputSize || T.monoSm);
      const outH = s.output ? Math.max(46, estimateHeight(s.output, codeW, outputSize, LS.mono, true) + 30) : 0;
      const codeH = panelH - pad * 2 - (s.output ? outH + 18 : 0);
      addFitted(slide, s.code, { left: panelX + pad, top: panelTop + pad, width: codeW, height: codeH }, { typeface: FONT.mono, fontSize: codeSize, color: C.white, lineSpacing: LS.mono }, "code", true);
      if (s.output) {
        const oy = panelTop + panelH - pad - outH;
        addRule(slide, panelX + pad, oy - 12, codeW, "#4E5258", 1);
        addText(slide, "OUTPUT", { left: panelX + pad, top: oy, width: 200, height: 18 }, { fontSize: T.eyebrow, bold: true, color: C.accentLight, lineSpacing: LS.tight }, "output-label");
        addFitted(slide, s.output, { left: panelX + pad, top: oy + 24, width: codeW, height: outH - 24 }, { typeface: FONT.mono, fontSize: outputSize, color: C.accentLight, lineSpacing: LS.mono }, "output", true);
      }
      const exX = panelX + panelW + 40, exW = G.stageW - G.margin - exX;
      column(slide, exX, exW, s.explainHead, s.explainBody, { name: "explain", bodySize: T.bodySm });
      fill(s, panelTop + panelH);
      notes(slide, s);
    },

    // NEW — a term gets its own slide: the word, a plain-language definition, a
    // concrete architectural example, and an optional confusion note. Replaces
    // burying vocabulary inside a generic two-column slide.
    definition(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Vocabulary");
      const leftW = 620;
      const hasNote = Boolean(s.note);
      const bandH = G.contentH - (hasNote ? 104 : 0);
      addText(slide, "TERM", { left: G.margin, top: G.contentTop, width: 200, height: 18 }, { fontSize: T.eyebrow, bold: true, color: C.accent, lineSpacing: LS.tight }, "term-label");
      addFitted(slide, s.term, { left: G.margin, top: G.contentTop + 26, width: leftW, height: 56 }, { typeface: s.termMono === false ? FONT.sans : FONT.mono, fontSize: T.h1, bold: true, color: C.ink, lineSpacing: LS.head }, "term");
      addRule(slide, G.margin, G.contentTop + 96, 120, C.accent, 4);
      const defH = estimateHeight(s.definition, leftW, T.body, LS.body);
      addFitted(slide, s.definition, { left: G.margin, top: G.contentTop + 122, width: leftW, height: Math.max(defH + 8, bandH - 132) }, { fontSize: T.body, color: C.ink, lineSpacing: LS.body }, "definition");
      const exX = G.margin + leftW + 48, exW = G.stageW - G.margin - exX;
      addPanel(slide, { left: exX - 22, top: G.contentTop, width: exW + 22, height: bandH - 8 }, C.panelBlue, C.ruleSoft, 8, "example-panel");
      addText(slide, s.exampleLabel ? String(s.exampleLabel).toUpperCase() : "IN PRACTICE", { left: exX, top: G.contentTop + 22, width: exW - 24, height: 18 }, { fontSize: T.eyebrow, bold: true, color: C.accentDeep, lineSpacing: LS.tight }, "example-label");
      const exHeadH = s.example.head ? estimateHeight(s.example.head, exW - 24, T.h3, LS.head, false, true) : 0;
      if (s.example.head) {
        addFitted(slide, s.example.head, { left: exX, top: G.contentTop + 50, width: exW - 24, height: exHeadH + 6 }, { typeface: s.exampleMono ? FONT.mono : FONT.sans, fontSize: T.h3, bold: true, color: C.ink, lineSpacing: LS.head }, "example-head");
      }
      addFitted(slide, s.example.body, { left: exX, top: G.contentTop + 50 + (s.example.head ? exHeadH + 18 : 0), width: exW - 24, height: bandH - 90 - (s.example.head ? exHeadH : 0) }, { fontSize: T.bodySm, color: C.muted, lineSpacing: LS.body }, "example-body");
      if (hasNote) {
        const ny = G.contentBottom - 84;
        addPanel(slide, { left: G.margin, top: ny, width: 6, height: 76 }, C.amber, "none", 0, "note-bar");
        addText(slide, s.noteLabel ? String(s.noteLabel).toUpperCase() : "COMMON CONFUSION", { left: G.margin + 22, top: ny + 2, width: 420, height: 18 }, { fontSize: T.eyebrow, bold: true, color: C.amber, lineSpacing: LS.tight }, "note-label");
        addFitted(slide, s.note, { left: G.margin + 22, top: ny + 24, width: G.contentW - 22, height: 74 }, { fontSize: T.bodySm, color: C.ink, lineSpacing: LS.body }, "note");
      }
      fill(s, G.contentBottom);
      notes(slide, s);
    },

    // NEW — one line of code, exploded. Labels are positioned by MONOSPACE
    // character index, so each bracket sits exactly under the substring it
    // names. Turns "read this line" from prose into an actual diagram.
    anatomy(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Anatomy");
      const codeSize = exportSafeFontSize(s.codeSize || 32);
      const cw = charWidth(codeSize, true);
      const codeLen = s.code.length;
      const codeW = codeLen * cw;
      const startX = Math.max(G.margin, Math.round((G.stageW - codeW) / 2));
      const codeY = G.contentTop + 26;
      addPanel(slide, { left: G.margin, top: G.contentTop - 8, width: G.contentW, height: 92 }, C.charcoal, C.charcoal, 8, "anatomy-code-panel");
      addText(slide, s.code, { left: startX, top: codeY, width: codeW + 40, height: 48 }, { typeface: FONT.mono, fontSize: codeSize, color: C.white, autoFit: "none", lineSpacing: LS.tight }, "anatomy-code");
      // Label placement is packed, not staggered by index. Parts are sorted
      // left-to-right and each one drops into the FIRST row where its label box
      // does not overlap a label already placed in that row. A fixed i % rows
      // stagger looked fine for evenly spaced parts and collided badly for
      // real code, where part widths vary (a 1-char operator next to a 9-char
      // name), so the number of rows is discovered here rather than declared.
      const bracketY = G.contentTop + 88;
      const CHIP = 26;
      // Clear the numbered chips that sit under the brackets before the first
      // label row starts, or row 0 lands on top of them.
      const labelsTop = bracketY + CHIP + 14;
      const GAPX = 16;
      const placed = [];
      const items = s.parts
        .map((p, i) => {
          const idx = p.at !== undefined ? p.at : s.code.indexOf(p.match);
          if (idx < 0) throw new Error(`anatomy: part "${p.match}" not found in code`);
          const spanW = Math.max(cw, (p.match ? p.match.length : p.len || 1) * cw);
          return { p, i, spanX: startX + idx * cw, spanW };
        })
        .sort((a, b) => a.spanX - b.spanX);

      for (const it of items) {
        const labelW = it.p.width || Math.max(180, Math.min(280, estimateLines(it.p.label, 240, T.h3, false, true) > 1 ? 260 : 210));
        const centre = it.spanX + it.spanW / 2;
        const lx = Math.min(G.stageW - G.margin - labelW, Math.max(G.margin, centre - labelW / 2));
        let row = 0;
        while (placed.some((q) => q.row === row && lx < q.lx + q.labelW + GAPX && q.lx < lx + labelW + GAPX)) row += 1;
        placed.push({ ...it, labelW, lx, row, centre });
      }

      // Parts are keyed by NUMBER, not by long leader lines. Leaders drawn from
      // a bracket down to a packed row inevitably cross the text of labels in
      // the rows between, and no routing rule fixes that reliably at this
      // density. A numbered chip under each bracket, repeated at the head of
      // its label, carries the same mapping and cannot collide with anything.
      placed.forEach((q, n) => (q.n = n + 1));
      const rowsUsed = Math.max(1, ...placed.map((q) => q.row + 1));
      // Row heights are measured, not divided evenly: an even split silently
      // starved the tallest label and let autoFit shrink it, which is exactly
      // the size drift this system exists to remove.
      const rowNeed = [];
      for (const q of placed) {
        // label always renders bold (see the addFitted call below) -- measure
        // it as bold, or a label that truly needs 2 lines gets positioned as
        // if it only needed 1, and the body drawn right after it collides
        // with line 2. Confirmed on real renders across three separate decks.
        const headH = Math.max(28, estimateHeight(q.p.label, q.labelW - CHIP - 10, T.h3, LS.head, false, true) + 4);
        const bodyH = q.p.body ? estimateHeight(q.p.body, q.labelW, T.caption, LS.body) + 6 : 0;
        q.headH = headH;
        q.bodyH = bodyH;
        rowNeed[q.row] = Math.max(rowNeed[q.row] || 0, headH + bodyH + 18);
      }
      // Row starts advance by each row's actual, unscaled need. A prior
      // version compressed the GAP between rows when total content exceeded
      // the available band but left each row's own box heights unscaled, so
      // a compressed next row could start before the previous row's real
      // text had finished rendering -- a confirmed chip-over-body collision
      // on real renders in three separate decks. Honest stacking can now run
      // past the content band in extreme cases; that is reported as a real,
      // visible overflow (fix: fewer/shorter parts) rather than silently
      // overlapping.
      const rowTop = [];
      let acc = labelsTop;
      for (let r = 0; r < rowsUsed; r += 1) {
        rowTop[r] = acc;
        acc += rowNeed[r];
      }
      if (acc > G.contentBottom + 2) diag?.noteOverflow(ctx.slideNo, "anatomy-rows", acc - labelsTop, G.contentBottom - labelsTop);
      for (const q of placed) {
        const top = rowTop[q.row];
        addRule(slide, q.spanX, bracketY, q.spanW, C.accent, 3);
        addPanel(slide, { left: q.centre - CHIP / 2, top: bracketY + 8, width: CHIP, height: CHIP }, C.accent, "none", 13, `part-chip-${q.i}`);
        addText(slide, String(q.n), { left: q.centre - CHIP / 2, top: bracketY + 13, width: CHIP, height: 18 }, { fontSize: T.eyebrow, bold: true, color: C.white, alignment: "center", lineSpacing: LS.tight }, `part-chipno-${q.i}`);
        addPanel(slide, { left: q.lx, top, width: CHIP - 4, height: CHIP - 4 }, C.accent, "none", 11, `part-lchip-${q.i}`);
        addText(slide, String(q.n), { left: q.lx, top: top + 4, width: CHIP - 4, height: 18 }, { fontSize: T.eyebrow, bold: true, color: C.white, alignment: "center", lineSpacing: LS.tight }, `part-lchipno-${q.i}`);
        addFitted(slide, q.p.label, { left: q.lx + CHIP + 6, top: top - 2, width: q.labelW - CHIP - 6, height: q.headH }, { fontSize: T.h3, bold: true, color: C.ink, lineSpacing: LS.head }, `part-head-${q.i}`);
        if (q.p.body) {
          addFitted(slide, q.p.body, { left: q.lx, top: top + q.headH + 8, width: q.labelW, height: q.bodyH }, { fontSize: T.caption, color: C.muted, lineSpacing: LS.body }, `part-body-${q.i}`);
        }
      }
      fill(s, G.contentBottom);
      notes(slide, s);
    },

    // NEW — commit before you run. Code with no output, a question, lettered
    // options, and the answer in a strip the instructor reveals last.
    predict(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Predict before you run");
      const answerH = 96;
      const bandH = G.contentH - answerH - 18;
      const panelW = 664;
      addPanel(slide, { left: G.margin, top: G.contentTop, width: panelW, height: bandH }, C.charcoal, C.charcoal, 8, "code-panel");
      addFitted(slide, s.code, { left: G.margin + 26, top: G.contentTop + 24, width: panelW - 52, height: bandH - 48 }, { typeface: FONT.mono, fontSize: T.mono, color: C.white, lineSpacing: LS.mono }, "code", true);
      const qx = G.margin + panelW + 40, qw = G.stageW - G.margin - qx;
      // The question box used to be hard-capped at 68pt (two lines' worth) with the
      // options nailed to a fixed offset below it. Any question longer than roughly 60
      // characters was therefore silently rescaled by autoFit — the exact type-size
      // drift this design system exists to prevent, and measurably visible in the deck
      // (a 147-character question rendered noticeably smaller than a 65-character one
      // on the same nominal role). Measure it instead and flow the options beneath.
      const qText = s.question || "What does this print?";
      const qH = Math.max(68, estimateHeight(qText, qw, T.h2, LS.head, false, true));
      addFitted(slide, qText, { left: qx, top: G.contentTop, width: qw, height: qH }, { fontSize: T.h2, bold: true, color: C.ink, lineSpacing: LS.head }, "question");
      const letters = ["A", "B", "C", "D", "E"];
      const QGAP = 12, OGAP = 6;
      const optTop = G.contentTop + qH + QGAP;
      const nOpts = s.options.length;
      // Give the options whatever the question left behind, never overrunning the band.
      // The previous version omitted the inter-option gaps from this division, so five
      // options silently ran past the band and into the answer panel; the text only
      // "fit" because it was spilling outside its own row.
      const optH = Math.min(58, Math.floor((bandH - qH - QGAP - OGAP * (nOpts - 1)) / nOpts));
      if (optH < 40) diag?.noteOverflow(ctx.slideNo, "predict-options", (40 - optH) * nOpts, 0);
      s.options.forEach((o, i) => {
        const y = optTop + i * (optH + OGAP);
        addPanel(slide, { left: qx, top: y, width: qw, height: optH }, C.panel2, C.ruleSoft, 6, `opt-${i}`);
        addText(slide, letters[i], { left: qx + 14, top: y + Math.round(optH / 2) - 12, width: 28, height: 24 }, { fontSize: T.h3, bold: true, color: C.accent, lineSpacing: LS.tight }, `opt-letter-${i}`);
        // Centre vertically inside the row rather than guessing a one-line offset, so a
        // two-line option sits correctly instead of riding high and clipping.
        addFitted(slide, String(o), { left: qx + 48, top: y + 4, width: qw - 62, height: optH - 6 }, { typeface: s.optionsMono === false ? FONT.sans : FONT.mono, fontSize: T.caption, color: C.ink, lineSpacing: LS.tight, verticalAlignment: "middle" }, `opt-text-${i}`);
      });
      const ay = G.contentBottom - answerH;
      addPanel(slide, { left: G.margin, top: ay, width: G.contentW, height: answerH }, C.panelBlue, C.accent, 8, "answer-panel");
      addText(slide, `ANSWER  ·  ${letters[s.answer]}`, { left: G.margin + 22, top: ay + 16, width: 320, height: 22 }, { fontSize: T.eyebrow, bold: true, color: C.accentDeep, lineSpacing: LS.tight }, "answer-label");
      // The why box left 14pt of the answer panel unused below it; reclaim that so a
      // slightly longer explanation renders at full size instead of being shrunk.
      addFitted(slide, s.why, { left: G.margin + 22, top: ay + 44, width: G.contentW - 44, height: answerH - 46 }, { fontSize: T.bodySm, color: C.ink, lineSpacing: LS.body }, "why");
      fill(s, G.contentBottom);
      notes(slide, s);
    },

    chart(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Visual evidence");
      slide.charts.add(s.chartType || "scatter", {
        position: { left: G.margin, top: G.contentTop, width: 736, height: G.contentH - 8 },
        title: s.chartTitle,
        titlePlacement: "aboveChart",
        titleTextStyle: { fontSize: T.caption, fill: C.ink, bold: true },
        categories: s.categories,
        series: s.series,
        hasLegend: s.hasLegend ?? true,
        legend: { position: "bottom", overlay: false, textStyle: { fontSize: T.eyebrow, fill: C.muted } },
        scatterOptions: { style: s.scatterStyle || "marker", varyColors: false },
        barOptions: s.barOptions,
        xAxis: { visible: true, title: { text: s.xTitle || "", textStyle: { fontSize: T.eyebrow, fill: C.muted } }, min: s.xMin, max: s.xMax, majorGridlines: { style: "solid", fill: "#E1E3E7", width: 1 }, textStyle: { fontSize: T.eyebrow, fill: C.muted } },
        yAxis: { visible: true, title: { text: s.yTitle || "", textStyle: { fontSize: T.eyebrow, fill: C.muted } }, min: s.yMin, max: s.yMax, majorGridlines: { style: "solid", fill: "#E1E3E7", width: 1 }, textStyle: { fontSize: T.eyebrow, fill: C.muted } },
        chartFill: C.white,
        chartLine: { style: "solid", fill: C.rule, width: 1 },
        plotAreaFill: C.white,
        plotAreaLine: { style: "solid", fill: C.rule, width: 1 },
      });
      const exX = G.margin + 736 + 40;
      column(slide, exX, G.stageW - G.margin - exX, s.explainHead, s.explainBody, { name: "chart-explain", bodySize: T.bodySm });
      fill(s, G.contentBottom);
      notes(slide, s);
    },

    // NEW — a real rendered figure (a matplotlib PNG produced by the same code the
    // students run, or an SVG concept diagram) beside an explanation. Text-only decks
    // asked students to imagine a plot the course could simply show them; every image
    // referenced here is generated by `figures/make_figures.py` in the same block, so a
    // slide can never drift from the code that produced it.
    figure(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Visual evidence");
      const wide = s.wide === true;
      const panelX = G.margin;
      const panelW = wide ? 900 : 724;
      const panelTop = G.contentTop;
      const capH = s.caption ? Math.max(24, estimateHeight(s.caption, panelW - 32, T.caption, LS.body) + 10) : 0;
      const panelH = G.contentH - 6 - capH;
      addPanel(slide, { left: panelX, top: panelTop, width: panelW, height: panelH }, C.white, C.rule, 8, "figure-panel");
      const pad = 14;
      const figureAlt = s.alt || s.title;
      slide.images.add({
        ...resolveFigure(s.figure),
        // `alt` is consumed by the in-memory inspector; `altText` is retained
        // for exporter compatibility. build.mjs also verifies/persists the
        // value in p:cNvPr/@descr because the current artifact exporter drops
        // it when serializing PowerPoint picture objects.
        alt: figureAlt,
        altText: figureAlt,
        position: { left: panelX + pad, top: panelTop + pad, width: panelW - pad * 2, height: panelH - pad * 2 },
        // contain, never cover: cropping a chart silently removes axis labels or data.
        fit: "contain",
      });
      if (s.caption) {
        addFitted(slide, s.caption, { left: panelX + 16, top: panelTop + panelH + 8, width: panelW - 32, height: capH }, { fontSize: T.caption, color: C.muted, lineSpacing: LS.body }, "figure-caption");
      }
      const exX = panelX + panelW + 40, exW = G.stageW - G.margin - exX;
      column(slide, exX, exW, s.explainHead, s.explainBody, { name: "figure-explain", bodySize: T.bodySm });
      fill(s, panelTop + panelH + capH);
      notes(slide, s);
    },

    table(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "Read the data");
      const width = s.callout ? 780 : G.contentW;
      const ratios = s.columnRatios?.length === s.columns.length ? s.columnRatios : s.columns.map(() => 1);
      const ratioTotal = ratios.reduce((a, b) => a + b, 0);
      const colWidths = ratios.map((v) => (width * v) / ratioTotal);
      const colLefts = colWidths.map((_, i) => G.margin + colWidths.slice(0, i).reduce((a, b) => a + b, 0));
      const n = s.rows.length + 1;
      const rowH = Math.min(56, Math.floor(G.contentH / n));
      // Cell size is derived from row count, not chosen per slide, so two tables
      // in the same deck never disagree about how big table text is.
      const baseCellSize = rowH >= 46 ? T.bodySm : T.caption;
      // A uniform row height silently shrank any cell whose text ran past one or two
      // lines — visible in the deck as a prose column rendering smaller than the short
      // label column beside it, on the same nominal role. Measure each row and give it
      // the height it actually needs, but only adopt that when the whole table still
      // fits the band; otherwise fall back to the original uniform rows so a dense
      // table degrades exactly as it used to rather than spilling off the slide.
      // Measure at the row-count-derived size first; if the table genuinely will not fit
      // the band that way, step the CELL SIZE down one notch (the same size a denser
      // table would have got anyway) and measure again, rather than falling back to
      // uniform rows that clip their own text.
      const measureAt = (size) => {
        const need = (text, w, bold) => estimateHeight(String(text), w - 24, size, LS.tight, false, bold) + 16;
        const hN = Math.max(rowH, ...s.columns.map((c, i) => need(c, colWidths[i], true)));
        const rN = s.rows.map((row) => Math.max(rowH, ...row.map((v, i) => need(v, colWidths[i], false))));
        return { headNeed: hN, rowNeeds: rN, total: hN + rN.reduce((a, b) => a + b, 0) };
      };
      let cellSize = baseCellSize;
      let m = measureAt(cellSize);
      if (m.total > G.contentH && cellSize !== T.caption) {
        cellSize = T.caption;
        m = measureAt(cellSize);
      }
      const headNeed = m.headNeed;
      const rowNeeds = m.rowNeeds;
      const measuredTotal = m.total;
      const flow = measuredTotal <= G.contentH;
      const headH = flow ? headNeed : rowH;
      const heights = flow ? rowNeeds : s.rows.map(() => rowH);
      const totalH = flow ? measuredTotal : rowH * n;
      const top = G.contentTop + Math.round((G.contentH - totalH) / 2);
      s.columns.forEach((c, i) => {
        addPanel(slide, { left: colLefts[i], top, width: colWidths[i], height: headH }, C.charcoal, C.white, 0);
        addFitted(slide, String(c), { left: colLefts[i] + 12, top: top + 8, width: colWidths[i] - 24, height: headH - 16 }, { fontSize: cellSize, bold: true, color: C.white, verticalAlignment: "middle", lineSpacing: LS.tight }, `header-${i}`);
      });
      s.rows.forEach((row, r) =>
        row.forEach((v, i) => {
          const y = top + headH + heights.slice(0, r).reduce((a, b) => a + b, 0);
          addPanel(slide, { left: colLefts[i], top: y, width: colWidths[i], height: heights[r] }, r % 2 ? C.panel2 : C.white, C.ruleSoft, 0);
          addFitted(slide, String(v), { left: colLefts[i] + 12, top: y + 8, width: colWidths[i] - 24, height: heights[r] - 16 }, { fontSize: cellSize, color: C.ink, verticalAlignment: "middle", lineSpacing: LS.tight }, `cell-${r}-${i}`);
        }),
      );
      if (s.callout) {
        const cx = G.margin + width + 40, cwid = G.stageW - G.margin - cx;
        addText(slide, s.calloutLabel ? String(s.calloutLabel).toUpperCase() : "ARCHITECTURAL LENS", { left: cx, top: G.contentTop + 6, width: cwid, height: 20 }, { fontSize: T.eyebrow, bold: true, color: C.accent, lineSpacing: LS.tight }, "callout-label");
        addFitted(slide, s.callout, { left: cx, top: G.contentTop + 40, width: cwid, height: G.contentH - 56 }, { fontSize: T.body, bold: true, color: C.ink, lineSpacing: LS.body }, "callout");
      }
      fill(s, top + totalH);
      notes(slide, s);
    },

    exercise(deck, W, s) {
      const slide = makeSlide(deck, W, s.title, s.kicker || "In-class check");
      const promptW = 420;
      addPanel(slide, { left: G.margin, top: G.contentTop, width: promptW, height: G.contentH - 8 }, C.accent, C.accent, 6, "exercise-accent");
      addFitted(slide, s.prompt, { left: G.margin + 28, top: G.contentTop + 30, width: promptW - 56, height: G.contentH - 68 }, { fontSize: T.h2, bold: true, color: C.white, verticalAlignment: "middle", lineSpacing: LS.head }, "exercise-prompt");
      const sx = G.margin + promptW + 44, sw = G.stageW - G.margin - sx;
      addText(slide, s.stepsLabel ? String(s.stepsLabel).toUpperCase() : "WORK THROUGH IT", { left: sx, top: G.contentTop + 4, width: sw, height: 20 }, { fontSize: T.eyebrow, bold: true, color: C.accent, lineSpacing: LS.tight }, "work-label");
      const n = s.steps.length;
      const stepTop = G.contentTop + 46;
      const stepH = Math.min(92, Math.floor((G.contentBottom - stepTop) / n));
      s.steps.forEach((st, i) => {
        const y = stepTop + i * stepH;
        addText(slide, `${i + 1}.`, { left: sx, top: y, width: 40, height: 32 }, { fontSize: T.h3, bold: true, color: C.accent, lineSpacing: LS.head }, `exercise-no-${i}`);
        addFitted(slide, st, { left: sx + 46, top: y, width: sw - 46, height: stepH - 10 }, { fontSize: T.body, color: C.ink, lineSpacing: LS.body }, `exercise-step-${i}`);
      });
      fill(s, G.contentBottom);
      notes(slide, s);
    },

    closing(deck, W, s) {
      const slide = deck.slides.add();
      slide.background.fill = C.charcoal;
      addText(slide, String(W).toUpperCase(), { left: G.margin, top: 48, width: 760, height: 24 }, { fontSize: T.caption, bold: true, color: C.accentLight, lineSpacing: LS.tight }, "close-week");
      addFitted(slide, s.title, { left: G.margin, top: 112, width: G.contentW, height: 112 }, { fontSize: T.hero, bold: true, color: C.white, lineSpacing: LS.head }, "close-title");
      addRule(slide, G.margin, 244, 168, C.accent, 5);
      const top = 284;
      const bottom = G.stageH - 40;
      const takeW = G.contentW - 84;
      // Row heights are measured per takeaway, not divided evenly -- an even
      // split let one long takeaway's wrapped third line collide with the
      // next takeaway's first line on a real render (confirmed on the
      // Weeks 9-12 revision pass: a 170-character takeaway needed 3 lines,
      // the fixed step budgeted 2, and its last line printed through the
      // next takeaway's text). Same fix pattern as anatomy()'s row packing.
      // Estimated against 85% of the real width, not the real width: measured
      // against an actual render, an 83-character takeaway at this font size
      // wrapped a line earlier than the shared ADVANCE.sans ratio (calibrated
      // against smaller table/body text) predicted, and the shortfall let
      // the next takeaway's chip start on top of this one's last line. A
      // narrower estimate-only width is a safety margin for this one large,
      // white, wide-column context; it does not touch the shared measure.mjs
      // constant other layouts already rely on being accurate, not padded.
      const rowNeed = s.takeaways.map((t) => Math.max(50, estimateHeight(t, takeW * 0.85, T.h2, LS.head) + 22));
      let y = top;
      s.takeaways.forEach((t, i) => {
        addText(slide, String(i + 1).padStart(2, "0"), { left: G.margin, top: y + 4, width: 58, height: 26 }, { fontSize: T.eyebrow, bold: true, color: C.accentLight, lineSpacing: LS.tight }, `take-no-${i}`);
        addFitted(slide, t, { left: G.margin + 84, top: y, width: takeW, height: rowNeed[i] - 10 }, { fontSize: T.h2, color: C.white, lineSpacing: LS.head }, `take-${i}`);
        y += rowNeed[i];
      });
      if (y - top > bottom - top + 2) diag?.noteOverflow(deck.slides.items.length, "closing-rows", y - top, bottom - top);
      notes(slide, s);
    },
  };
}
