# The Daily Collegian: editorial notes

How the Collegian prints its crosswords and how we transcribe them. The text step and the AI
proof reviewer read this file after their own instructions (xword-ocr `textstep.instructions`,
`proofreview.instructions`: `editorial.md` beside `fixes/`); reviewers can check a
transcription against it. The publication's rules that code applies (no title from December
1977, the standing byline, the keys never printed) are in `fixes/fixes.toml`, not here.

Each note: what the paper does, how we transcribe it, and where it was settled.

**Draft, 2026-11-11:** the wording of the first note is the project's rule as blitz
`publications/REVIEW.md` has it (the editorial rule of 2026-11-06, blitz PR 74), not a new rule
for this paper. To be confirmed by the project manager before it is merged.

- **Printer's typos in clues.** The Collegian's clues were set quickly and carry many plain
  typos; run2's AI review asked about one on 38 puzzles and nothing else (manager's report
  2026-11-10, kind 4: "Wahs out", "Explosive mountian"). The rule is the project's: the text is
  the puzzle as the publisher meant it, not a facsimile of the page (the corpus's rule,
  EDITORIAL.md: obvious mistakes are corrected to what was meant; nothing the publisher did on
  purpose is changed). A plain printer's typo is corrected: a wrong, extra or missing letter set
  cleanly in type becomes the word that was meant. When the scan shows the misspelling cleanly,
  say so in the note ("D1 is printed 'cockail'; corrected to cocktail"), so the record shows the
  slip was the printer's, not the OCR's.
- **What the publisher did on purpose stays.** Puzzles have gimmicks (missing or extra letters,
  pun spellings, several letters in one square, dialect), so an odd spelling may be the point:
  check whether the answer grid only works with it, and keep it. When you can't tell a typo from
  wordplay, keep it as printed, say it's a close call, and a person decides.
- **Only correct what you can see in the scan.** A doubtful word with no crop to check is a
  question for a person, not a correction.
