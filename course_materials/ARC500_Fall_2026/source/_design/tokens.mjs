// ARC 500 deck design system — design tokens.
//
// ONE type scale, ONE spacing rhythm, ONE palette, shared by every week's
// builder. Before this file existed each layout picked its own font sizes ad
// hoc: an audit of the Weeks 1-3 builder found 25 distinct sizes across 11
// layouts, with body text set at 8 different sizes (20/21/22/23/25/27/28/30)
// depending only on which layout it happened to land in, and column heads at 5
// (26/28/29/30/32). Every size below is therefore keyed to a ROLE, not to a
// layout — if a new layout needs body text it uses T.body, it does not invent
// a size.

// ---------------------------------------------------------------- type scale
// Eight roles. Differentiate by WEIGHT and COLOR before reaching for a new
// size; h3 is deliberately the same size as body, bolded, so a minor heading
// never introduces a ninth size.
export const T = {
  // Artifact Tool uses CSS pixels and PowerPoint stores points at 0.75 pt/px.
  // Multiples of four therefore export as whole-point sizes in the final PPTX.
  display: 60, // 45 pt; title-slide deck title only
  hero: 48, // 36 pt; full-bleed statement / closing-slide title
  h1: 40, // slide title (every content slide)
  h2: 28, // 21 pt; column / section head
  h3: 24, // 18 pt; minor head — same size as body, bold
  body: 24, // 18 pt; ALL running body text
  bodySm: 20, // 15 pt; dense contexts only: table cells, 4+ column bodies
  mono: 24, // 18 pt; code
  monoSm: 16, // 12 pt; code OUTPUT block
  caption: 16, // captions, secondary notes
  eyebrow: 12, // 9 pt; kickers, footers, all-caps labels
};

// Line spacing paired to role. Body copy gets air; headings sit tight.
export const LS = {
  tight: 1.02,
  head: 1.08,
  body: 1.16,
  mono: 1.14,
};

// ------------------------------------------------------------------- spacing
// A 1280x720 stage. Content lives in one band so every slide starts and ends
// on the same two lines — the single biggest driver of "these look like one
// deck" versus "these look assembled from parts".
export const G = {
  stageW: 1280,
  stageH: 720,
  margin: 64,
  get contentW() {
    return this.stageW - this.margin * 2;
  }, // 1152
  colGap: 56,
  get colW() {
    return (this.contentW - this.colGap) / 2;
  }, // 548
  get colRightX() {
    return this.margin + this.colW + this.colGap;
  }, // 668
  kickerY: 36,
  titleY: 64,
  titleH: 96,
  contentTop: 190,
  contentBottom: 644,
  get contentH() {
    return this.contentBottom - this.contentTop;
  }, // 454
  footerRuleY: 666,
  footerTextY: 675,
  // Short blocks are optically centered in the band rather than floating at the
  // top. True centre reads as "fell to the bottom"; 0.36 sits just above centre,
  // which reads as deliberate. Measured before this change, rendered content
  // filled between 37% and 100% of the band with 15 slides under 60%.
  centerBias: 0.36,
};

// ------------------------------------------------------------------- palette
export const C = {
  white: "#FFFFFF",
  ink: "#111316",
  charcoal: "#17191C",
  panel: "#EDEDED",
  panel2: "#F6F7F9",
  panelBlue: "#F3F7FB",
  rule: "#B8BCC4",
  ruleSoft: "#DDE0E5",
  // Restrained academic blue: high contrast without the saturation of a
  // software-product palette. The same three values are used in the Word
  // handouts so slide and handout hierarchy reads as one course system.
  accent: "#2E74B5",
  accentDeep: "#1F4D78",
  accentLight: "#E8EEF5",
  muted: "#5A5F66",
  green: "#2E7D5B",
  red: "#C9473A",
  amber: "#B5731A",
};

export const FONT = { sans: "Arial", mono: "Consolas" };
