import { estimateHeight, estimateLines } from './measure.mjs';
const qw = 1152 - 44; // G.contentW - 44
const whys = {
  A: "res.x = [80, 120], -res.fun = 7800.0 (cell [1], next) - beats (120,0)'s $7,200, since it spends the full budget AND area.",
  B: "area_used = 200.0 and budget_used = 50000.0 - both bind exactly (cells [2]-[3], next); the structural cap has slack.",
  C: "linprog always minimizes - c_ai=[60,25] silently asks for the true minimum, [0,0], with res_ai.success still True.",
  D: "res_new.x = [40,160], -res_new.fun = 6400.0 (cell [7], next) - solar's higher cost shifts the mix toward green roof.",
  E: "res_w.x = [100,50] (cell [8], next): area and budget both bind; the triple-pane cap (80 m2) has slack at 50 m2 used.",
};
for (const [k,v] of Object.entries(whys)) {
  console.log(k, 'len', v.length, 'lines', estimateLines(v, qw, 19, false), 'height', estimateHeight(v, qw, 19, 1.16, false).toFixed(1), '(budget 38)');
}
