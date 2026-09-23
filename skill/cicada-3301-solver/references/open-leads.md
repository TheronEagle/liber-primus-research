# Open Leads — Untried or Partially-Explored Directions

**Status legend:** 🔴 tested, ruled out (see ruled-out.md) · 🟡 partially tested,
inconclusive · 🟢 untested, genuinely open

## 🟢 0. HIGHEST PRIORITY — the word-length match at ACTUAL positions

**IMPORTANT CORRECTION (2026-09-24)**: The original open-leads.md claimed the pattern `[6,7,6,3,6,4,3,3]` matched at page 22 word 45 and page 47 word 11. **This was incorrect.** Deep analysis shows:
- The pattern `[6,7,6,3,6,4,3,3]` does NOT occur at those positions.
- The pattern occurs exactly **2 times globally**:
  - Block 19 (page ~36), local word 47
  - Block 44 (page ~61), local word 12
- The second pattern `[5,4,7,3,6,3,7,4]` was claimed at pages 43/58.
- **Actual finding**: Occurs exactly **1 time globally** at Block 40 (page ~57), local word 42.

**Revised next steps for this lead:**
1. Extract the exact rune sequences at the **ACTUAL** matching positions (block 19 word 47 and block 44 word 12).
2. Compare their Gematria VALUES directly (not just lengths) — if they're also identical or near-identical in values, that's a much stronger signal.
3. If the values differ, try an autokey/running-key test: use one page's runes (or their values) as the decryption key for the other page's corresponding region, and vice versa, both directions.
4. Check whether this pattern recurs elsewhere at shorter lengths (6-7 words) — the Kasiski-on-lengths test already found some 6-length and shorter repeats worth a second look (see `scripts/gematria_toolkit.py` for `word_length_kasiski()` and `extend_match()`).
5. Check n=6 and n=7 too — shorter matches will be far more numerous and mostly noise, but worth a scan.

**Status update (2026-09-24)**: 
- Values differ between the two blocks (verified).
- Autokey/running-key tests on both blocks: no signal (gibberish output).
- Shared n-grams as keys: no signal.
- **Pattern 2 (block 40)**: Unique global occurrence. Self-decrypt with all offsets: max hit rate 3.51% (2/57) - exactly noise floor. No signal.

**Status: TESTED, RESULT NEGATIVE.** The structural word-length correlation is real but doesn't yield a usable key. All reasonable cryptographic interpretations of the length correlation have been exhausted without signal above noise.

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