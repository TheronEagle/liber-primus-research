# Open Leads — Untried or Partially-Explored Directions

**Status legend:** 🔴 tested, ruled out (see ruled-out.md) · 🟡 partially tested,
inconclusive · 🟢 untested, genuinely open

## 🟢 0. HIGHEST PRIORITY — the page 22 / page 47 word-length match

A round-2 session found something worth prioritizing over everything else in this
file: an 8-word-length run (`[6,7,6,3,6,4,3,3]`) that matches EXACTLY between word
45 of page 22 and word 11 of page 47. Full details and the significance estimate
are in `ruled-out.md`'s "Round 2 tests" section. This is the single most specific,
concrete, checkable lead currently in this file — everything else here is a
category of technique to try; this is an actual coordinate pointing at two
specific pages.

**Concrete next steps, in order of cheapness:**
1. Extract the exact rune sequences at page 22 word 45 (8 words) and page 47 word
   11 (8 words). Compare their Gematria VALUES directly (not just lengths) —
   if they're also identical or near-identical in values, that's a much stronger
   signal than the length match alone and might mean these two spans are the
   SAME plaintext phrase, which would let you solve for a page-specific key at
   that location by assuming a probable-word crib (e.g. if it's a repeated
   ritual phrase like "AS ABOVE SO BELOW" or similar cadence, an 8-word phrase
   is a workable crib length).
2. If the values differ, try an autokey/running-key test: use page 22's runes
   (or their values) as the decryption key for page 47's corresponding region,
   and vice versa, both directions.
2. Check whether this pattern recurs elsewhere at shorter lengths (6-7 words) —
   the Kasiski-on-lengths test already found some 6-length and shorter repeats
   worth a second look (see raw output logged when this was run; re-run
   `kasiski_on_seq` — not yet added to the toolkit script, only run ad hoc — on
   the word-length sequence with n=6,7 and cross-reference all matches, not just
   the longest one).
3. `word_length_kasiski()` and `extend_match()` are now in
   `scripts/gematria_toolkit.py` (added and verified working). Running
   `word_length_kasiski(global_lens, ngram_lengths=(8,))` surfaced a SECOND
   8-word-length match not caught in the first ad hoc pass: pattern
   `[5,4,7,3,6,3,7,4]` shared between **page 43 and page 58**. Two independent
   8-length matches existing in the same corpus somewhat raises the odds that at
   least one is structurally real rather than coincidental (though it also means
   there are more candidate windows, which cuts the other way statistically —
   worth a more careful significance calculation than the back-of-envelope one
   in ruled-out.md if this becomes the focus of a session). Check n=6 and n=7 too
   — shorter matches will be far more numerous and mostly noise, but worth a scan.

---

Ranked roughly by plausibility/interest, not certainty. None of these are verified
to work — they're documented as "worth trying before inventing something new,"
not "known to be promising." Update the status of each as they get tried.

## 🔴 1. Cross-page continuous key/stream (not reset per page)

**Status: TESTED, RULED OUT** (round 2). The totient-of-primes stream run
continuously across the full 56-page concatenation, plus at several offsets,
scored within noise band every time. See `ruled-out.md`. Not worth re-testing
unless a genuinely different continuous stream is proposed.

## 🔴 2. Page 5's magic square as a key source

**Status: TESTED, RULED OUT** (round 2), for row-major and column-major
flattening. See `ruled-out.md` for exact numbers. **Still untested:** diagonal or
spiral-order flattening of the same square — the square's symmetry means
row-major and column-major are similar to each other, but a diagonal/spiral
traversal would be a genuinely different sequence and hasn't been tried.

## 🟡 3. Word-length pattern analysis (not letter-content)

**Status: TESTED, RESULT PROMISING BUT INCONCLUSIVE** (round 2) — this is what
surfaced the page 22 / page 47 match at the top of this file. See item 0 above and
`ruled-out.md`'s Round 2 section for full detail and next steps. Don't re-run the
basic version of this test; instead follow the specific next-step checklist in
item 0.

## 🔴 4. "Their numbers are the direction" (2016 verified Cicada message)

**Status: TESTED, RULED OUT** (round 4). A confirmed, authenticated 2016 Cicada
communication states: "Liber Primus is the way, its words are the map, their
meaning is the road, and their numbers are the direction." The community broadly
interprets "words are the map" / "meaning is the road" as already-understood (the
book's philosophical content guides the reader). "Numbers are the direction" has
never been turned into a working decryption step. Tested interpretations:
- Gematria VALUES of solved page as directions/steps (turtle graphics/walk on grid): noise
- Page NUMBERS as pointers/offsets into other solved plaintexts: noise
- Continuous totient stream across pages: 3.75% (noise)
- Totient stream as word-order permutation: 6.55% (noise)
- Page-numbered totient offsets: 4.08% (noise)
- Solved page 73 values as key: 3.71% (noise)
- Prime sequence mod 29: 3.82% (noise)
**Result: No signal exceeding noise floor**. All tested interpretations ruled out.

## 🔴 5. Illustration steganalysis on pages other than 74

**Status: TESTED, RULED OUT** (round 3). Pages 8-14, 32, and 55 have been checked
with connected-component + nearest-neighbor spacing analysis. All show smoothly
decaying NN distance histograms consistent with natural/stochastic point
processes — no sharp peaks at fixed spacings that would indicate Braille-style or
binary-grid encoding. **Result: no hidden structure found.** Consistent with page
74's negative result. Not worth re-testing unless a genuinely different image
analysis technique is proposed.

## 🔴 6. Non-substitution cipher families

**Status: TESTED, RULED OUT** (rounds 2-5).
- **Simple columnar transposition** (grid widths 2-30, no column reordering): best result 0.048 hit rate at width 14, only marginally above noise. See `ruled-out.md`.
- **Keyed columnar transposition** (columns permuted by keyword): **TESTED, RULED OUT** (round 4). Tested 35 Cicada vocabulary keywords. Best: "TOTIENT" → "TOIEN" (5 cols): 4.70% hit rate. All results 3.35% - 4.70%, consistent with noise floor.
- **Rail fence (zigzag) transposition**: **TESTED, RULED OUT** (round 5). Tested 2-10 rails across all 56 unsolved pages. Best: 2 rails at 4.55% hit rate. All results 3.1% - 4.6%, consistent with noise floor.
- **Book cipher / running key** from external text (KJV Bible, Crowley's Liber AL, Mabinogion, Blake's Marriage of Heaven and Hell): **TESTED, RULED OUT** (rounds 2-5). Whole text, every offset, both forward and reversed signs. See `ruled-out.md` and round 4/5 tests. Best result: Blake forward 4.41%. All results 2.9% - 4.4%, consistent with noise floor.

---

## 7. Live community state

**Status: CHECKED (2026-09-24).** The r/a3301 subreddit and cicadasolvers.com
community are still active. The Uncovering Cicada Wiki (uncovering-cicada.fandom.com)
was accessible as of 2026-09-24 and contains current summary of solve status (56
unsolved pages listed). The Nox Populi YouTube/Discord community (run by 2013
winner) continues to facilitate solving efforts. Wikipedia confirms the third
puzzle (Liber Primus) remains unsolved as of 2026; last verified PGP-signed
Cicada message was April 2017. **No new public breakthroughs or hypotheses
observed since last check.** The open-leads.md and ruled-out.md in this repo
reflect the current known state of research.

---

---

**When you rule something out:** move it to `ruled-out.md` with full methodology
and results, so the next session doesn't re-derive it. When you find something
promising but inconclusive, add it here with what's known so far. When you get a
verified solve, write it up fully in `solved-pages.md`.