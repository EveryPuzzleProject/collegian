# Collegian batch manager: what a fresh session needs

The Daily Collegian (Penn State), Mike Shenk's crosswords, 1976-03-11 to 1981-05-15. Batch
`collegian-1976-81`, 797 puzzles. A manager is a new session each week: read this, the charter (blitz
`design/operating-model.md`, "Batch manager"), and the latest report in this folder. Reports are
`manager/YYYY-MM-DD.md`, in the charter's four parts.

## What the manager may and may not do

Owns: this repo, `collegian-scans`, the run folder, the batch. Must not: change `xword-ocr` or `blitz`
code, type puzzle content, merge, publish to the live site or its bucket, send anything to gxd, change a
rule the owner set, spend past the token line. Each of those is a request to the project manager, in the
report. A kind of pipeline failure is described with evidence (milestone, puzzle count, three ids) for
the dev lane.

## Where things are

| what | where |
|---|---|
| this repo (public index, fix file, ledger, records) | `C:\Users\adeja\Projects\collegian`; `fixes/fixes.toml` (publication rules, `[ocr] key_entries`), `fixes/decisions.jsonl` (the ledger), `fixes/no-key-printed.tsv` (generated), `pipeline/` |
| scans and harvest records (private) | `C:\Users\adeja\Projects\collegian-scans` |
| run folder (outside every repo) | `C:\Users\adeja\Projects\blitz-work\runs\collegian` (`EPP_RUNS=C:/Users/adeja/Projects/blitz-work/runs`); `HANDOVER.md` there has every stage's exact command |
| the run's scripts | `scripts/` in the run folder: `01_reread.py`, `02_packets.py`, `03_reuse.py`, `common.py` (fixed paths), `review_plan.py` (review groups), `an*.py` (the report's tallies) |
| run1's outputs (read only) | `C:\Users\adeja\Projects\blitz-work\collegian-run1-backup`; also `s3://epp-blitz/runs/collegian/run1/` |
| page image cache and stage artifacts | `C:\Users\adeja\Projects\xword-ocr\.cache\ia` (always pass `--cache` in full) |
| gxd answers | `C:\Users\adeja\Projects\xd\gxd.sqlite` |
| harvest tools, /boxes and /answers views | blitz `tools/collegian/` |
| lessons and measurements | blitz `design/collegian-lessons.md`; xword-ocr `docs/collegian-run2.md` |
| memory | `~/.claude/projects/C--Users-adeja-Projects-blitz/memory/` (`collegian-shenk-harvest.md`, `collegian-run2-prep.md`, `operating-model.md`) |

## The run registry

`pipeline/triage/runs.json` says which run is current (what the review site shows) and what each is.

| run | state | code | where |
|---|---|---|---|
| run1 | current: live on the review site | 2026-11-06 | `blitz-work/collegian-run1-backup` |
| run2 | run 2026-11-10, not published | xword-ocr 422eace, collegian 522febd, blitz 62a6072 | `blitz-work/runs/collegian` (`textstep/run2`, `proof/run2`, `triage/run2`, `proofreview/run2`) |

Run2's worktrees, on merged main of each repo, all on a branch named `claude/collegian-run2-run`:
`xword-ocr/.claude/worktrees/collegian-run2-run` (run every `uv run xword-ocr` from here),
`C:\Users\adeja\Projects\collegian-run2-run` (this repo: the fix path the session records are keyed to;
keep one fix path for a whole run), `blitz/.claude/worktrees/collegian-run2-run`. Remove them only after
this repo's branch is merged.

## Standing terms (owner, 2026-11-10)

- An AI reviewer's Ready with a passing ship check counts as the one Ready needed to ship. This repo has
  no `fixes/ship-rule.json` yet, so pass `--ai-ready both` to `blitz ship` until the owner approves one.
- Fixes apply forward; nothing is back-filled. The scan is the proof.
- The batch page asks people for held-on-a-question first.
- The untitled rule starts 1977-12-01. The 75 no-key-printed puzzles stay held until the owner decides
  whether they ship unsolved.
- Text step and AI proof review run on Opus. Pause and ask at about 7 M model tokens for a run.
- Nothing published, shipped or merged without the owner.

## Things learned running run2

- `uv` is not on the tool shell's PATH: `C:\Users\adeja\miniforge3\Scripts\uv.exe`.
- Always give `--fixes` and `--cache` in full; a command that doesn't find the fix file runs without the
  publication's rules, silently.
- Measured rates: text step 15k tokens a puzzle, AI proof review 20k a puzzle (100k a group of 5).
- Launch model agents through one small supervising agent per wave (it launches the batches and reports
  one line each with token counts), so the manager session isn't woken per batch. At most 20 agents run
  at once in a session: keep a wave to 15 batches and run waves one after another.
- Agents can write `answer.json` into the run folder; none was refused.
- Never print `textstep-status` unfiltered: it lists every puzzle.
- `blitz ship ... --record` writes only `pipeline/ship/<batch>.json` (status, nothing shipped);
  `--no-site` reads the ledger alone.
- A Not ready in the ledger stands across runs (run1's AI review still holds 151 puzzles in run2's
  record); see the 2026-11-10 report, kind 2.

## Next week, from the 2026-11-10 report

1. The owner's three decisions (ship the 69 and publish run2; the 271-puzzle review; no-key-printed).
2. If the misprint rule is confirmed, add `fixes/editorial.md` and review again only the 38 puzzles held
   on a misprint question.
3. When a dev-lane fix lands for a kind, re-run from the stage it invalidates and make the record again.
4. The crop boxes for autumn 1977 and December 1977-1978 need a person on /boxes, then `scan.py pages`.
