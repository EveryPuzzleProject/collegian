# The Daily Collegian: editorial notes

How the Collegian prints its crosswords and how we transcribe them. The text step and the AI
proof reviewer read this file after their own instructions (xword-ocr `textstep.instructions`,
`proofreview.instructions`: `editorial.md` beside `fixes/`); reviewers can check a
transcription against it. The publication's rules that code applies (no title from December
1977, the standing byline, the keys never printed) are in `fixes/fixes.toml`, not here.

Each note: what the paper does, how we transcribe it, and where it was settled.

**Draft, 2026-11-11:** the first note is the owner's rule of 2026-11-11 as the AI proof
reviewer's instructions have it (xword-ocr `proofreview.INSTRUCTIONS`, `docs/ship-gate.md`), not
a new rule for this paper; what counts as a plain typo and what stays is in the wording of blitz
`publications/REVIEW.md`. To be confirmed by the project manager before it is merged.

- **Printer's typos in clues and headers.** The Collegian's clues were set quickly and carry many plain
  typos; run2's AI review asked about one on 38 puzzles and nothing else (manager's report
  2026-11-10, kind 4: "Wahs out", "Explosive mountian"). Two kinds of change are kept apart.
  A reading fix, where the scan or the OCR was bad, makes our text match the print: it is
  welcome and automatic. A correction of a good scan where the original has a mistake is always
  recorded and never edited into our text: the xd here stays as printed, and the correction is
  proposed in review (the word as printed, the word meant, the crop as evidence) and applied at
  the gxd export, as gxd's editorial (the corpus's rule, EDITORIAL.md: obvious mistakes are
  corrected to what was meant; nothing the publisher did on purpose is changed).
- **What is a plain typo.** A wrong, extra or missing letter set cleanly in type, where only
  one word can have been meant ("cockail" for cocktail).
- **What the publisher did on purpose stays.** Puzzles have gimmicks (missing or extra letters,
  pun spellings, several letters in one square, dialect), so an odd spelling may be the point:
  check whether the answer grid only works with it. When you can't tell a typo from wordplay,
  propose nothing, say it's a close call, and a person decides.
- **Only propose what you can see in the scan.** A doubtful word with no crop to check is a
  question for a person.
- **A letter the answer key misprints** is different: it is corrected in review, and recorded as
  a correction of the print, not a reading fix (the square, the letter the key printed, the
  letter it was corrected to, the key's crop as evidence), so the xd carries a note of it. The
  keys are small and, from 1979, typewritten (E reads as B, F as P: `fixes/fixes.toml`,
  `key_entries`), so a letter the crossings contradict is far more often a misreading than a
  misprint: only a letter the crop shows plainly, with both crossing clues against it, is one.
