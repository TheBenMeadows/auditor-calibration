#!/usr/bin/env node
// Render cases.json as cases.md for the inputs review. One table, then one
// section per case with the claim in a fenced block. Generated, never edited.
import { readFileSync, writeFileSync } from 'node:fs';

const data = JSON.parse(readFileSync(new URL('../cases.json', import.meta.url), 'utf8'));
const cases = data.cases;
const pos = cases.filter(c => c.label === 1).length;
const neg = cases.length - pos;
const fence = '`'.repeat(Math.max(3, ...cases.map(c => (c.claim.match(/`+/g) ?? []).reduce((m, s) => Math.max(m, s.length), 0) + 1)));

let md = `# Orrery finding-precision eval: inputs for review\n\n`;
md += `${cases.length} cases: ${pos} kept findings (label 1), ${neg} refuted claims (label 0). `;
md += `Each case is the claim as a worker raised it, stripped of evidence and verdict. The auditor gets the claim, the commit and the paths; it is told the live site has changed and to verify against the commit through GitHub.\n\n`;
md += `Audited commits: 0819 = \`${data.refs['0819'].sha}\`, 0927 = \`${data.refs['0927'].sha}\`.\n\n`;
md += `| id | tags | label | where |\n|---|---|---|---|\n`;
for (const c of cases) md += `| ${c.id} | ${c.tags.join(', ')} | ${c.label} | ${c.where.map(w => '`' + w + '`').join(', ')} |\n`;
md += `\n`;
for (const c of cases) {
  md += `## ${c.id}\n\nlabel ${c.label} (${c.label ? 'kept' : 'refuted'}), ${c.tags.join(', ')}; where: ${c.where.map(w => '`' + w + '`').join(', ')}\n\n${fence}\n${c.claim}\n${fence}\n\n`;
}
writeFileSync(new URL('../cases.md', import.meta.url), md);
console.log(`${cases.length} cases (${pos} kept, ${neg} refuted) -> cases.md`);
