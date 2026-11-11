# Run2: the 38 puzzles Not ready for misprint questions alone (2026-11-11)

Kind 4 of the manager's report of 2026-11-10. From `proofreview/run2/*/answer.json` in the run folder
(`C:/Users/adeja/Projects/blitz-work/runs/collegian`) by the report's own rule (`scripts/an6.py`): the answer is
Not ready and every flag is on a clue and says "misprint". Checked against the ledger on
`claude/collegian-run2-run` (`fixes/decisions.jsonl`): each one's latest AI review is Not ready, of
2026-11-11; and against `triage/run2/triage.json`: each passes the ship check. 38 puzzles, 46 flags.
No model was called to make this list. The ids alone, comma-separated, for `--pids`:
`manager/2026-11-11-misprint-rereview.txt`.

| puzzle | flags | clues asked about | crops in its input | note |
|---|---|---|---|---|
| collegian1977-01-06-L001 | 1 | A71 | 8 |  |
| collegian1977-09-19-L001 | 4 | A18, A55, A69, D42 | 9 |  |
| collegian1977-12-07-L001 | 1 | D38 | 4 |  |
| collegian1977-12-14-L001 | 1 | A41 | 3 |  |
| collegian1977-12-15-L001 | 1 | A26 | 9 |  |
| collegian1977-12-19-L001 | 1 | D41 | 11 |  |
| collegian1977-12-20-L001 | 1 | A23 | 6 |  |
| collegian1978-01-10-L001 | 1 | D29 | 5 | no crop for the clue: stays a flag under the rule |
| collegian1978-01-20-L003 | 1 | A15 | 0 | no crop for the clue: stays a flag under the rule |
| collegian1978-09-01-L001 | 1 | A15 | 4 |  |
| collegian1978-09-15-L001 | 1 | A49 | 5 |  |
| collegian1978-09-19-L001 | 1 | D11 | 8 |  |
| collegian1978-10-24-L001 | 1 | D4 | 12 |  |
| collegian1978-10-26-L001 | 1 | A40 | 6 |  |
| collegian1979-01-11-L001 | 1 | A31 | 3 |  |
| collegian1979-01-15-L001 | 1 | A51 | 5 |  |
| collegian1979-01-29-L001 | 1 | A36 | 6 |  |
| collegian1979-02-13-L001 | 1 | D27 | 1 |  |
| collegian1979-04-16-L001 | 1 | A26 | 2 |  |
| collegian1979-04-17-L003 | 1 | D33 | 9 | no crop for the clue: stays a flag under the rule |
| collegian1979-04-20-L001 | 2 | A43, D18 | 12 |  |
| collegian1979-11-29-L001 | 2 | A24, A44 | 11 |  |
| collegian1980-04-11-L003 | 1 | D26 | 15 |  |
| collegian1980-06-30-L003 | 1 | D45 | 7 |  |
| collegian1980-07-07-L003 | 2 | A62, D47 | 14 |  |
| collegian1980-07-14-L003 | 1 | D44 | 13 |  |
| collegian1980-07-21-L003 | 1 | A10 | 1 |  |
| collegian1980-09-25-L003 | 1 | D33 | 17 |  |
| collegian1980-10-06-L003 | 2 | A42, D12 | 3 |  |
| collegian1980-11-06-L003 | 1 | A46 | 7 |  |
| collegian1981-01-29-L003 | 1 | D37 | 4 | words missing from the printed clue: stays a flag under the rule |
| collegian1981-02-12-L003 | 2 | A62, D53 | 12 |  |
| collegian1981-02-20-L003 | 1 | D8 | 3 |  |
| collegian1981-03-25-L003 | 1 | D36 | 6 | the clue printed is another clue's idea: stays a flag under the rule |
| collegian1981-03-31-L003 | 1 | A37 | 12 |  |
| collegian1981-04-27-L003 | 1 | A5 | 1 | no crop for the clue: stays a flag under the rule |
| collegian1981-04-29-L003 | 1 | D48 | 2 | no crop for the clue: stays a flag under the rule |
| collegian1981-05-15-L003 | 1 | A63 | 3 |  |

## The second review, once xword-ocr `claude/unruffled-ritchie-9382c7` is merged

The reviewer's fixed instructions then correct a plain printer's typo (an edit, with what was printed
recorded) and can say Ready. Not run: it spends model tokens, so it is the owner's call.

From an xword-ocr checkout at the merged main, with this branch merged into the collegian checkout the
run writes to (`C:/Users/adeja/Projects/collegian-run2-run`), so `editorial.md` and the ids file are there:

```
uv run xword-ocr proof-review build --out C:/Users/adeja/Projects/blitz-work/runs/collegian --run run2 --fixes C:/Users/adeja/Projects/collegian-run2-run/fixes/fixes.toml --pids "$(cat C:/Users/adeja/Projects/collegian-run2-run/manager/2026-11-11-misprint-rereview.txt)"
```

That replaces the 38 input folders (their old answers go; the ledger keeps them) and `INSTRUCTIONS.md`,
and keeps the other rows of `index.json`. Then the `xword-proof` agent on Opus, 8 groups of 5 folders (the
last of 3), and:

```
uv run xword-ocr proof-review record --out C:/Users/adeja/Projects/blitz-work/runs/collegian --run run2 --fixes C:/Users/adeja/Projects/collegian-run2-run/fixes/fixes.toml
uv run xword-ocr proof-review attach --out C:/Users/adeja/Projects/blitz-work/runs/collegian --run run2 --fixes C:/Users/adeja/Projects/collegian-run2-run/fixes/fixes.toml
```

Cost at run2's measured rate (20k tokens a puzzle): 38 x 20k = **about 0.76 M tokens** on Opus, plus about
85k for one supervising agent: about 0.85 M in all.

What to expect: 7 of the 38 stay Not ready by the rule itself (5 have no crop for the clue, 2 are not plain
typos; marked above). The other 31 have only typos the crop shows cleanly, though the reviewer may still
call a few close ("Serious tumors" for EDEMAS, "Midwest region" for PALESTINE).
