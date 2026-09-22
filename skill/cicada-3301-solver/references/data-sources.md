# Data Sources

Page images, rune transcriptions, and word lists are too large to bundle directly
in this skill. Fetch them fresh each session (network access permitting) rather
than relying on stale local copies, since community archives do get corrected.

## Primary archive: krisyotam/cicada3301 (GitHub)

```
git clone --depth 1 https://github.com/krisyotam/cicada3301.git
```

Key paths inside it:
- `liber-primus/pages/NN.jpg` — all 75 page images, sequential numbering (00-74)
- `liber-primus/GEMATRIA-PRIMUS.md` — the cipher table (also reproduced in this
  skill's `references/gematria-primus.md`)
- `liber-primus/runes-text.txt` — rune-level transcription of LP2 pages, `%`
  delimited by page (57 blocks; block index i corresponds to sequential page
  `17+i`... EXCEPT double-check this against the index file each time, off-by-one
  errors are easy here — cross-reference with `liber-primus__index.txt` below)
- `liber-primus/decoded/DECODED-PAGES.md` — community summary of solve status per
  page (useful overview, but cross-check specific claims — this file has been
  observed to be occasionally imprecise about edge cases, e.g. it doesn't clearly
  flag pages 73/74 as solved even though they are — verify against the index file)
- `tools/solvers/iddqd/liber-primus__index/liber-primus__index.txt` — the
  authoritative page index: sequential/internal numbering crosswalk + short title
  for each page/section. **This is the most reliable single file for "is this page
  solved and what's it called."**
- `tools/solvers/iddqd/liber-primus__transcription--master/` — an alternate,
  differently-segmented full transcription (organized by content section rather
  than strictly by page — useful for cross-verification but doesn't map 1:1 to
  page numbers, use the index file to align them)
- `tools/solvers/iddqd/ttf/BabelStoneRunicBeorhtnoth.ttf` — a Unicode Futhorc font,
  useful for rendering reference glyphs to visually cross-check OCR/transcription
  of a page image, though note it's a generic Futhorc font and NOT pixel-identical
  to the book's stylized display font — use it for topological comparison
  (stroke count/direction), not exact template matching.
- `liber-primus/analysis/HINTS-NEVER-USED.md` — pre-2014 puzzle-stage hints; mostly
  already incorporated into known solves, but worth a skim for anything overlooked.

## English word list for dictionary scoring

```
curl -sL "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt" -o words_alpha.txt
```
~370,000 words, one per line. Filter to length ≥3 to avoid noisy 1-2 letter matches
inflating scores. This is what `scripts/gematria_toolkit.py`'s `dict_score()` expects.

## Live community resources (check current state, don't assume this skill is current)

- cicadasolvers.com — active community wiki/quickstart guide to puzzle status
- r/a3301 (Reddit) — active discussion, sometimes has the most current hypotheses
- uncovering-cicada.fandom.com — detailed wiki (was returning errors on fetch as of
  this skill's last update — may need a different access method or may be
  temporarily down; try again)

## User-uploaded PDF (if applicable to this session)

If the user has uploaded a PDF/scan of the physical Liber Primus book, note that
printed/scanned compilations sometimes interleave blank pages, cover art, or
duplicate content differently than the sequential `00.jpg`-`74.jpg` archive
numbering. Always verify a specific uploaded page against the archive via visual
comparison (render both at the same resolution, compare directly) before assuming
page N of the PDF equals page N of the archive — confirmed to differ by exactly
one index at least once (PDF page 75 = archive `74.jpg`, i.e. PDF is 1-indexed
where the archive is 0-indexed, when this was checked).
