#!/usr/bin/env node
// Aggregate a variant's results.jsonl into metrics.md and a Clef-shaped
// scores.jsonl. Every number here recomputes from the rows; nothing is typed in.
//
//   node scripts/summarize.mjs [variant] [flow]   (defaults: baseline, orrery-precision)
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const variant = process.argv[2] ?? 'baseline';
const flow = process.argv[3] ?? 'orrery-precision';
const vdir = join(HERE, '..', '.claude', 'hillclimb', flow, variant);
const rows = readFileSync(join(vdir, 'results.jsonl'), 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l));
const errors = existsSync(join(vdir, 'errors.jsonl')) ? readFileSync(join(vdir, 'errors.jsonl'), 'utf8').split('\n').filter(Boolean).length : 0;
const ok = rows.filter(r => r.status === 'ok');

// Per-case mean over reps, then over cases (the builder's way).
const byCase = new Map();
for (const r of ok) { if (!byCase.has(r.prompt_id)) byCase.set(r.prompt_id, []); byCase.get(r.prompt_id).push(r); }
const cases = [...byCase.entries()].map(([id, rs]) => ({
  id, label: rs[0].meta.label, p: decimalMean(rs.map(r => r.grade.p_true)), correct: mean(rs.map(r => r.grade.correct)),
  brier: mean(rs.map(r => r.grade.brier)), bare: mean(rs.map(r => r.grade.verdict_correct)),
  spread: rs.length > 1 ? Math.max(...rs.map(r => r.grade.p_true)) - Math.min(...rs.map(r => r.grade.p_true)) : null,
  reps: rs.length, any: rs.some(r => r.grade.correct === 1) ? 1 : 0, all: rs.every(r => r.grade.correct === 1) ? 1 : 0,
  maj: rs.filter(r => r.grade.correct === 1).length * 2 > rs.length ? 1 : 0,
}));
const pos = cases.filter(c => c.label === 1), neg = cases.filter(c => c.label === 0);
function mean(a) { return a.length ? a.reduce((s, x) => s + x, 0) / a.length : NaN; }
// p_true arrives as short decimals; a plain float sum can leave two equal means a
// last-bit apart, turning a true AUROC tie into a strict comparison. Rounding the
// mean to 1e-9 keeps equal decimal means equal (float error is far below that).
function decimalMean(a) { return Math.round(mean(a) * 1e9) / 1e9; }
function wilson(k, n) { if (!n) return [NaN, NaN]; const z = 1.96, p = k / n, d = 1 + z * z / n, c = p + z * z / (2 * n), h = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return [(c - h) / d, (c + h) / d]; }
function auroc(P, N) { if (!P.length || !N.length) return NaN; let s = 0; for (const a of P) for (const b of N) s += a.p > b.p ? 1 : a.p === b.p ? 0.5 : 0; return s / (P.length * N.length); }
const pct = x => Number.isNaN(x) ? 'n/a' : (100 * x).toFixed(1) + '%';
const ci = (k, n) => { const [lo, hi] = wilson(k, n); return Number.isNaN(lo) ? '' : ` (95% CI ${pct(lo)}–${pct(hi)})`; };

const recallK = pos.reduce((s, c) => s + c.correct, 0), specK = neg.reduce((s, c) => s + c.correct, 0);
const cost = ok.reduce((s, r) => s + (r.reported_cost_usd ?? 0), 0);
let md = `# ${variant}: Orrery finding-precision eval\n\n`;
md += `${cases.length} cases scored (${pos.length} kept, ${neg.length} refuted), ${ok.length} rep rows, ${errors} failed attempt(s) in errors.jsonl (not in the means).\n\n`;
md += `| metric | value |\n|---|---|\n`;
md += `| recall (kept scored real at p≥0.5) | ${pct(recallK / pos.length)}${ci(recallK, pos.length)} |\n`;
md += `| specificity (refuted scored not-real at p≥0.5) | ${pct(specK / neg.length)}${ci(specK, neg.length)} |\n`;
md += `| AUROC of p_true (kept vs refuted) | ${Number.isNaN(auroc(pos, neg)) ? 'n/a' : auroc(pos, neg).toFixed(3)} |\n`;
md += `| Brier (lower is better) | ${mean(cases.map(c => c.brier)).toFixed(3)} |\n`;
md += `| bare verdict agreement (true=1, partial=0.5, false=0) | ${pct(mean(cases.map(c => c.bare)))} |\n`;
md += `| mean p_true on kept / on refuted | ${mean(pos.map(c => c.p)).toFixed(2)} / ${mean(neg.map(c => c.p)).toFixed(2)} |\n`;
const spreads = cases.map(c => c.spread).filter(x => x != null);
if (spreads.length) md += `| rep-to-rep spread of p_true (mean, max) | ${mean(spreads).toFixed(2)}, ${Math.max(...spreads).toFixed(2)} |\n`;
// Capability = right on at least one rep; reliability = right on every rep. Only
// cases with k>1 reps enter, so a partly finished run reports on what it has.
// Majority = right on more than half the reps (a tie counts as wrong). A split case
// is right on some reps but not all; "outvoted" counts the split cases where the
// right verdict was found but a majority vote would discard it.
const multi = cases.filter(c => c.reps > 1);
if (multi.length) {
  const ks = [...new Set(multi.map(c => c.reps))].sort((a, b) => a - b).join('/');
  for (const [name, set] of [['all', multi], ['kept', multi.filter(c => c.label === 1)], ['refuted', multi.filter(c => c.label === 0)]]) {
    if (!set.length) continue;
    const anyK = set.reduce((s, c) => s + c.any, 0), allK = set.reduce((s, c) => s + c.all, 0);
    md += `| ${name}: correct on ≥1 of k=${ks} reps / on every rep (${set.length} cases) | ${pct(anyK / set.length)}${ci(anyK, set.length)} / ${pct(allK / set.length)}${ci(allK, set.length)} |\n`;
    const majK = set.reduce((s, c) => s + c.maj, 0);
    const splitK = set.filter(c => c.any && !c.all).length, outvotedK = set.filter(c => c.any && !c.maj).length;
    md += `| ${name}: correct by majority of reps / split cases / split cases outvoted | ${pct(majK / set.length)}${ci(majK, set.length)} / ${splitK} / ${outvotedK} |\n`;
  }
}
md += `| mean latency / tool calls / cost per rep | ${mean(ok.map(r => r.latency_s)).toFixed(0)} s / ${mean(ok.map(r => r.tool_calls)).toFixed(1)} / $${cost ? (cost / ok.length).toFixed(3) : 'not measured'} |\n`;
md += `| total reported cost | ${cost ? '$' + cost.toFixed(2) : 'not measured'} |\n\n`;
md += `## Refuted cases (specificity, one line each)\n\n| case | p_true | correct |\n|---|---|---|\n`;
for (const c of neg) md += `| ${c.id} | ${c.p.toFixed(2)} | ${c.correct} |\n`;
md += `\n## Kept cases scored below 0.5\n\n`;
const missed = pos.filter(c => c.p < 0.5);
md += missed.length ? `| case | p_true |\n|---|---|\n` + missed.map(c => `| ${c.id} | ${c.p.toFixed(2)} |`).join('\n') + '\n' : 'none\n';
writeFileSync(join(vdir, 'metrics.md'), md);

// Clef / Jev SystemOne shape: one noul question per case, probability per option.
const lines = ok.map(r => JSON.stringify({
  case_id: r.prompt_id, rep: r.rep, label: r.meta.label, model: r.model, variant,
  state: r.prompt, questions: [{ name: 'finding_is_real', type: 'noul', p: { true: r.grade.p_true, false: +(1 - r.grade.p_true).toFixed(4) } }],
  bare_verdict: r.explanation?.correct?.match(/verifies=(\w+)/)?.[1] ?? null,
}));
writeFileSync(join(vdir, 'scores.jsonl'), lines.join('\n') + '\n');
console.log(md.split('\n').slice(0, 14).join('\n'));
console.log(`-> ${join(vdir, 'metrics.md')}, scores.jsonl (${lines.length} lines)`);
