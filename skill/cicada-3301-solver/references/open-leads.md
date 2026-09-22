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

## 4. "Their numbers are the direction" (2016 verified Cicada message)

**Status: not operationalized.** A confirmed, authenticated 2016 Cicada
communication states: "Liber Primus is the way, its words are the map, their
meaning is the road, and their numbers are the direction." The community broadly
interprets "words are the map" / "meaning is the road" as already-understood (the
book's philosophical content guides the reader). "Numbers are the direction" has
never been turned into a working decryption step. Possible untried interpretations:
- The Gematria VALUES (not letters) of a solved page, read as a sequence of
  directions/steps (like turtle graphics or a walk on a grid) — possibly meant to
  trace a path on the magic squares, or to index into some external
  document/coordinate system.
- The page NUMBERS themselves (17, 20, 23, 25, 32...) as pointers/offsets into
  something else — e.g., using page numbers as indices into other solved
  plaintexts (an interpage key-derivation scheme).
This is speculative — flagged as interesting but nobody has built and tested a
concrete hypothesis from it yet.

## 5. Illustration steganalysis on pages other than 74

**Status: only page 74's illustration has been checked** (connected-component +
nearest-neighbor spacing analysis; see ruled-out.md — came back negative). Several
other pages (mentioned in community notes as pages 8-14, 32, 55 having
dendrite/root-style illustrations) have NOT been checked with the same pixel
analysis. Since page 74's illustration is on an already-solved page and still came
back clean, it's plausible the artwork genuinely carries no hidden data anywhere —
but this hasn't been confirmed for the pages that matter (the unsolved ones).

## 🟡 6. Non-substitution cipher families

**Status: partially tested (round 2).** Simple columnar transposition (grid
widths 2-30, no column reordering) was tried on direct transliteration: best
result 0.048 hit rate at width 14, only marginally above the 0.034-0.040 noise
band and likely a multiple-comparisons artifact (29 widths tested). See
`ruled-out.md`. **Still untested:**
- Keyed columnar transposition (columns permuted according to a keyword, the more
  common real-world variant of this cipher — plain fixed-width transposition was
  the weak/naive version of this test).
- Rail fence and other transposition variants.
- A book cipher / running key drawn from external text (e.g. using the KJV Bible,
  a specific philosophical text referenced by Cicada's ideology, or another Cicada
  document as the literal key stream rather than a short repeated word).

## 7. Live community state

**Status: needs a fresh check, not a one-time answer.** The r/a3301 and
cicadasolvers.com communities are still active and occasionally test new
hypotheses; their current state changes over time in a way no static file can
capture. Any future session with web search should do a fresh, current search
(not rely on this file) before assuming the state described in `solved-pages.md`
and `ruled-out.md` is still fully up to date — cite the search date when updating
this skill.

---

**When you rule something out:** move it to `ruled-out.md` with full methodology
and results, so the next session doesn't re-derive it. When you find something
promising but inconclusive, add it here with what's known so far. When you get a
verified solve, write it up fully in `solved-pages.md`.
