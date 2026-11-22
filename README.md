# Calibrating auditors of code-review claims

Code, cases, run data and paper source for "Calibrating Auditors of Code-Review Claims, and Auditing Their Labels" (Benjamin Meadows, 2026). Paper: [Zenodo DOI to be added].

Claude Opus 5.5, Fable 5.1, Sonnet 5.5 and Haiku 5.5 (in one harness), DeepSeek Flash (in the same harness, behind a proxy) and SWE-2 High (in the Devin CLI) re-checked 144 labelled claims about four public repositories and reported a probability that each claim is a real finding. This repository holds every completed run row, the cases with their label sources, the scripts that compute every number in the paper, and the paper's LaTeX source.

## Reproduce the paper's numbers

Requirements: Python 3 (checked on 3.13 and 3.15), standard library only, and git. The full analysis took 20 minutes on one core of a 2013 Xeon.

```
make reproduce
```

`make reproduce` runs `scripts/analyze-p1.py` over the run rows in `runs/`, which writes `runs/analysis/analysis.json`. It then runs `scripts/paper-numbers.py`, which regenerates `paper/numbers.tex` and `paper/tables/*.tex`. Last, it runs `git diff` on those files. If the command exits 0, every number and table the paper prints was recomputed from the raw rows and matches the committed copy.

To build the PDF, install [tectonic](https://tectonic-typesetting.github.io/) and run `make paper`.

## Layout

| Path | Contents |
|---|---|
| `runs/` | One directory per paper run (see the next table), each with `results.jsonl` (completed attempts), `errors.jsonl` (failed attempts), `scores.jsonl`, `run.json` and `metrics.md`. `cases-paper-144.json` is the case set. `budgets.json` records the turn and time limits of each run. |
| `panel/` | The blind three-model label panel (`v1` Gemini 4 Argon, `v2` Kimi K3, `v3-grok` Grok 4.7) and its agreement summary. |
| `sources/` | Label sources: `council-cases.json` (33 claims refuted in earlier review rounds, with the refutation), `mutated-cases.json` (53 constructed false claims, each with the file and line that make it false), `mutated-sample-20.json` (the planned ruling sample) and `mutant-ruling.json` (the one mutant the maintainer ruled, then dropped). |
| `first-pass/` | The first-pass case set of Section 3. |
| `review/p1-results/` | Rows of the two text-only probes of Section 8.4. |
| `harness/`, `run-eval.mjs` | The agent definition the lanes ran and the runner. Both are byte-identical to the versions that produced the runs. |
| `scripts/` | Analysis, number generation, run provenance, panel agreement and row export. |
| `paper/` | LaTeX source, the generated `numbers.tex` and `tables/`, the analysis plan with its change log, and the materiality rule for count errors. |

| Run | Lane | Cases |
|---|---|---|
| `baseline` | Opus 5.5 | 130 non-Squint cases, three runs each |
| `v3` | Opus 5.5 | 14 Squint cases, three runs each |
| `v1` | SWE-2 High | 144, three runs each |
| `v2` | DeepSeek Flash | 144, three runs each |
| `v4` | Sonnet 5.5 | 144, three runs each |
| `v5` | Haiku 5.5 | 144, three runs each |
| `v6` | Fable 5.1 | 144, one run each |
| `v7` | Fable 5.1, second run | 60 drawn cases |
| `v8` | Haiku 5.5, files inline, no tools | 144, three runs each |
| `v10` | Haiku 5.5, files inline, no tools | 14-case smoke run |

The Sonnet 5.5 inline lane was planned as `v9` and was not run.

## Re-running a lane

Re-running a lane needs the providers' accounts and is not needed to reproduce the numbers. `run-eval.mjs` documents its options in its header. The runner refuses to run unattended when the harness differs from the approved version (Section 2 of the paper). Model behaviour changes over time, so a re-run produces new rows, not the published ones.

## What is not included

- Raw response streams and session transcripts. The rows in `results.jsonl` keep each verdict, probability, explanation, tool-call count, latency and reported cost.
- Repository checkouts. Each case names its repository and commit, so the files can be fetched from GitHub.
- The fresh audit round that was dropped before it was ruled (Section 4 of the paper).
- The outside-model review rounds on the analysis and drafts.

Home-directory paths in the copied rows are written as `~/`, and the scripts read `runs/` and `panel/` where the original layout used a hidden directory. `make reproduce` shows that these edits leave every published number unchanged.

## License

Code: MIT (`LICENSE`). Paper text, cases and run data: CC BY 4.0.
