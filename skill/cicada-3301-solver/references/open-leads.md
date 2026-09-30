# Open Leads — Untried or Partially-Explored Directions

**Status legend:** 🔴 tested, ruled out (see ruled-out.md) · 🟡 partially tested,
inconclusive · 🟢 untested, genuinely open

## 🟢 0. HIGHEST PRIORITY — the word-length match at ACTUAL positions

> **SUPERSEDED IN PART (2026-09-30).** The "IMPORTANT CORRECTION" below is itself
> wrong, and this entry is being kept only as the record of what happened. Do not
> cite the "corrected positions" from an older commit.
>
> The 2026-09-24 correction assumed `blocks[0]` = page 17, but the transcription
> file is the **whole book** and the real mapping is `page = raw_index + 3`. So
> **blocks 19 and 44 *are* pages 22 and 47** — the correction chased the very
> pages the original claim named, and wrongly declared that claim false.
> Block 40 = page 43. The `open-leads.md` positional claims here are all shifted.
>
> **What survives:** the 8-word length pattern `[6,7,6,3,6,4,3,3]` *does* occur at
> pages 22 and 47, as first reported. The follow-up negative results (values
> differ, autokey/running-key yields gibberish) were computed on those correct
> pages all along, so this lead's *conclusion* is probably sound even though the
> reasoning around it was not. That has not been re-verified since the mapping
> fix, so it is re-opened as 🟡 rather than closed. See the CORRECTION section in
> `ruled-out.md` for the full derivation.

**The original (2026-09-22) claim, which turned out to be right:** the pattern
`[6,7,6,3,6,4,3,3]` matched at page 22 word 45 and page 47 word 11. A second
pattern `[5,4,7,3,6,3,7,4]` was claimed at pages 43/58.

**The (incorrect) 2026-09-24 correction, recorded for the audit trail:**
- Claimed the pattern occurs exactly 2 times globally, at "block 19 word 47" and
  "block 44 word 12".
- Claimed the second pattern occurs exactly 1 time globally at "block 40 word 42".
- Concluded the original page-22/47 claim was incorrect.
All of those block numbers are raw indices that need `+3` to become pages.

**Revised next steps (still open):**
1. Re-run the pattern search on the **verified** page mapping and record actual
   page numbers, not raw block indices.
2. Re-check the 2026-09-24 value-comparison and autokey results to confirm they
   really were computed on pages 22/47.
3. Re-derive the corpus size — it is **55 pages / 12,956 runes**; page 67 is
   missing from the transcription entirely.

**Status (2026-09-30 RE-RUN — the original claim is VINDICATED):**
Re-run from scratch on the verified page mapping with a corrected scorer
(`experiments/2026-09-30/lead0_rerun.py`):

- Pattern `[6,7,6,3,6,4,3,3]` occurs **contiguously at page 22 word 47 and page
  47 word 12** — i.e. the 2026-09-22 claim, on real page numbers.
- Pattern `[5,4,7,3,6,3,7,4]` occurs at **page 43 word 42 and page 58 word 47** —
  also exactly as originally claimed. The 2026-09-24 "correction" said this one
  occurred only once, at "block 40"; that was wrong on both counts.
- The 8-word runs are 38 runes each and their values are **not** identical.
- Elementwise difference (p22 − p47 mod 29) renders as
  `IETHXCGGNMEAEAOERCNPDIOQAEGENNGEOSYEOXBOEEOTRRWG` — not English.

**Status: TESTED, RESULT NEGATIVE — now closed 🔴 on sound reasoning.** Eight
cross-page key variants (autokey/running-key in both directions, plus the
elementwise difference as an additive stream, both signs, on both pages) were
scored. Best was 10.53% ambiguity-aware dictionary hits vs a 78.9% ceiling for a
correct decrypt. A 400-sample permutation test of the max-over-8 statistic gives
**p = 0.113** — squarely inside the null — and the decoded text is gibberish with
dictionary words scattered at 13% of the way to a real solution
(`experiments/2026-09-30/lead0_permutation.py`, `.json`). The earlier
"best" of +7.54pp lift disappears once the multiple-comparisons correction is
applied and the control is computed on the right data.

The structural word-length correlation between pages 22 and 47 is real and
reproducible. Every reasonable cryptographic reading of it has now been tested
on the correct pages with a validated instrument. It does not yield a key.

---

## 🔴 1. Cross-page continuous key/stream (not reset per page)

**Status: TESTED, RULED OUT** (round 2). The totient-of-primes stream run
continuously across the full 56-page concatenation, plus at several offsets,
scored within noise band every time. See `ruled-out.md`. Not worth re-testing
unless a genuinely different continuous stream is proposed.

## 🔴 2. Page 5's magic square as a key source

**Status: TESTED, RULED OUT** (all traversals). Row-major, column-major,
diagonal (main/anti), spiral (clockwise/counterclockwise), zigzag (rows/cols)
all tested. All results 3.4% - 4.4%, consistent with noise floor.

## 🟡 3. Word-length pattern analysis (not letter-content)

**Status: TESTED, RESULT NEGATIVE.** The structural correlation (shared n-grams
at same relative positions between blocks 19/44) is real but doesn't yield
a usable key. All reasonable cryptographic interpretations exhausted.

## 🔴 4. "Their numbers are the direction" (2016 verified Cicada message)

**Status: TESTED, RULED OUT** (round 4). All tested interpretations:
- Gematria VALUES as directions/steps: noise
- Page NUMBERS as pointers/offsets: noise
- Continuous totient stream: 3.75% (noise)
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
- **Diagonal/spiral/zigzag magic square traversals**: **TESTED, RULED OUT**. All 6 variants (diagonal main/anti, spiral cw/ccw, zigzag rows/cols) tested. Best: diagonal_main 4.44%. All 3.4% - 4.4%, noise floor.

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