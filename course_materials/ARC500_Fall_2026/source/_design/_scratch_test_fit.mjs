import { estimateHeight, estimateLines } from './measure.mjs';
const codeW = 672;
const candidates = {
  v1: `from scipy.optimize import linprog
c = [-60, -25]
A_ub = [[1, 1], [400, 150]]
b_ub = [200, 50000]
bounds = [(0, 120), (0, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub,
              bounds=bounds, method='highs')
print(res.x)
print(res.fun)
print(res.success)`,
  v2: `from scipy.optimize import linprog

# maximize 60x1+25x2 -> minimize the negative
c = [-60, -25]
A_ub = [[1, 1], [400, 150]]   # area, budget
b_ub = [200, 50000]
bounds = [(0, 120), (0, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub,
              bounds=bounds, method='highs')
print(res.x)
print(res.fun)
print(res.success)`,
  v3: `from scipy.optimize import linprog
# c, A_ub, b_ub, bounds from cell [1] above
res = linprog(c, A_ub=A_ub, b_ub=b_ub,
              bounds=bounds, method='highs')
print(res.x)
print(res.fun)
print(res.success)`,
};
for (const [k,v] of Object.entries(candidates)) {
  console.log(k, 'lines', estimateLines(v, codeW, 22, true), 'height', estimateHeight(v, codeW, 22, 1.14, true).toFixed(1));
}
