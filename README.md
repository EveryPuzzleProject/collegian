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

- `puzzles.tsv`: one row per issue in the archive for the run (920 issues): `found` (a puzzle on `page`),
  `absent` (a person looked: no puzzle that day) or, in a working copy, `unsure` (under review), and the archive link.
  The archive's page numbers (`seq`) count spreads in scan order, not the printed page numbers.
- `exceptions.tsv`: oddities. 1978-01-20 reprints a missed grid on the front page, with an apology and no clues;
  nine issues from 1981-06-10 carry the help-wanted ad; 1976-03-22 is a puzzle titled "Nazism" whose grid is
  swastika-shaped (flagged for care when it is imported).

## Coverage and status (2026-11-05)

- The archive has no issues from 1975-12-20 to 1976-03-10, so the first puzzle in it (1976-03-11) is probably
  not Shenk's first; the true start falls somewhere in that gap and can't be pinned down from this archive.
  Puzzles from the missing issues are not included.
- All 920 issues in the archive for the run are settled by a person: 873 with a puzzle page, 47 without one.
- Diagramless puzzles, if any, are not yet separated out: the OCR can't detect them.
- Next: fetch the puzzle images, collect the answers (printed in the next day's classifieds), then read the
  puzzles into [xd](https://github.com/century-arcade/xd) format.

`puzzles.tsv` and `exceptions.tsv` are generated from the project's working records by
`tools/collegian/scan.py publish` in [blitz](https://github.com/EveryPuzzleProject/blitz); edit those, not these.
