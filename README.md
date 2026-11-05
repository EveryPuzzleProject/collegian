# collegian

An index of Mike Shenk's crosswords in The Daily Collegian (Penn State), March 1976 – June 1981:
for each issue in the Penn State Libraries archive, which page the crossword is on, with a link to it.
Part of the [Every Puzzle Project](https://github.com/EveryPuzzleProject).

Shenk, who later edited the Wall Street Journal crossword, was a Penn State student when the Collegian
started running his daily puzzle (the first with his byline is 1976-03-12). In June 1981 the paper ran an
ad in the puzzle's place: he had taken a job with GAMES magazine and the paper was "looking for two or
three bright, witty persons to take his place".

Source: [The Daily Collegian, 1940–2010](https://panewsarchive.psu.edu/lccn/sn85054904/) in the Pennsylvania
Newspaper Archive (open, with page images and OCR text). This repo holds an index only, no images.

## Files

- `puzzles.tsv`: one row per issue in the archive for the run (920 issues): `found` (a puzzle on `page`) or
  `absent` (a person looked: no puzzle that day), whether a person or the OCR located it, and the archive link.
  The archive's page numbers (`seq`) count spreads in scan order, not the printed page numbers.
- `exceptions.tsv`: oddities. 1978-01-20 reprints a missed grid on the front page, with an apology and no clues;
  nine issues from 1981-06-10 carry the help-wanted ad.

## Status (2026-11-05)

- All 920 issues are settled: 873 with a puzzle page, 47 without one.
- 412 of the `found` rows were located by OCR text alone and not yet checked by eye; 461 were confirmed by a person.
- Diagramless puzzles, if any, are not yet separated out: the OCR can't detect them.
- Next: fetch the puzzle images, collect the answers (printed in the next day's classifieds), then read the
  puzzles into [xd](https://github.com/century-arcade/xd) format.

`puzzles.tsv` and `exceptions.tsv` are generated from the project's working records by
`tools/collegian/scan.py publish` in [blitz](https://github.com/EveryPuzzleProject/blitz); edit those, not these.
