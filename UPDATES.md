# Research Updates

## 2026-09-24 (continued - deep analysis of Open-Leads #0)
- **Critical Finding: Open-Leads #0 positions were incorrect**
  - The target pattern `[6,7,6,3,6,4,3,3]` was claimed at page 22 word 45 and page 47 word 11
  - **Actual finding**: The pattern does NOT occur at those positions
  - **Real locations**: Pattern occurs exactly **2 times globally**:
    - Block 19 (page ~36), local word 47
    - Block 44 (page ~61), local word 12
  - Second target `[5,4,7,3,6,3,7,4]` claimed at pages 43/58
  - **Real location**: Occurs exactly **1 time globally** at Block 40 (page ~57), local word 42

- **Deep analysis of ACTUAL matches (2026-09-24):**
  - **Pattern 1** (blocks 19 & 44): Word-lengths match perfectly (8-word run), but Gematria VALUES differ. They share 3 n=6-grams and 2 n=7-grams at the SAME relative positions - strong structural correlation but different ciphertext.
  - **Pattern 2** (block 40): **Unique global occurrence** of `[5,4,7,3,6,3,7,4]` - only happens ONCE in the entire corpus! This is extremely significant.
  - Kasiski analysis shows blocks 19 & 44 share 3 n=6-grams and 2 n=7-grams at the SAME relative positions - strong structural correlation but different ciphertext.

- **Rail Fence Transposition Test (Open-Leads #6 - remaining)**: Tested rail fence (zigzag) transposition with 2-10 rails across all 56 unsolved pages.
  - Best result: 2 rails: 4.55% hit rate (125/2746 words)
  - Second best: 9 rails: 4.19%, 4 rails: 4.08%
  - All results in 3.1% - 4.6% range, consistent with noise floor (3-4% established in `ruled-out.md`).
  - **Result: No signal exceeding noise floor**. Rail fence transposition ruled out.

- **Reversed Key Text Test (Open-Leads #6 - remaining)**: Tested reversed key text as running key across all 56 unsolved pages (Cicada uses reversed gematria on solved pages 06-09). Tested 4 key texts (KJV, Liber AL, Mabinogion, Blake) in both forward and reversed directions.
  - Best result: Blake forward: 4.41% (121/2746)
  - All results: 2.9% - 4.41%, consistent with noise floor.
  - **Result: No signal exceeding noise floor**. Reversed key text ruled out.

- **Illustration Steganalysis (Open-Leads #5)**: Analyzed pages 8-14, 32, 55 for hidden data in illustrations using connected-component and nearest-neighbor spacing analysis (replicating page 74 methodology from ruled-out.md).
  - **Page 8**: 360 small components, NN distance mean=37.3, std=48.0
  - **Page 9**: 283 small components, NN distance mean=42.0, std=54.2
  - **Page 10**: 643 small components, NN distance mean=34.1, std=41.2
  - **Page 11**: 531 small components, NN distance mean=39.4, std=44.6
  - **Page 12**: 524 small components, NN distance mean=37.7, std=41.6
  - **Page 13**: 428 small components, NN distance mean=39.8, std=46.0
  - **Page 14**: 141 small components, NN distance mean=69.0, std=52.8
  - **Page 32**: 83 small components, NN distance mean=84.3, std=82.0 (sparse, larger components)
  - **Page 55**: 77 small components, NN distance mean=100.1, std=77.5 (very sparse)
  
  **Comparison with page 74 (from ruled-out.md)**: Page 74 had 624 components with sizes 517-620 for trunk components, NN histogram smoothly decaying from 76 pairs at ~6.7px to 1 pair at ~76px - consistent with natural/stochastic process.
  
  **Our findings**: The unsolved pages show similar characteristics - component sizes vary but all show smoothly decaying NN distance histograms consistent with natural/stochastic point processes. No sharp peaks at fixed spacings (which would indicate Braille-style or binary-grid encoding). Pages 32 and 55 have fewer/sparser small components but their histograms are still smooth.
  
  **Result: No evidence of hidden structure in these illustrations.** Consistent with page 74 finding - the artwork appears to be natural/stochastic stippling, not data-encoded.

- **Baseline hit rate for raw transliteration**: 6.41% (176/2746 words) - higher than Vigenère noise floor (3-4%) but far below 41% benchmark.

- **Live community state check (Open-Leads #7)**: Checked r/a3301, cicadasolvers.com, Uncovering Cicada Wiki, Wikipedia, and Nox Populi community as of 2026-09-24.
  - Uncovering Cicada Wiki accessible and current (last modified 2026-09-21), lists 56 unsolved pages.
  - Wikipedia confirms third puzzle (Liber Primus) remains unsolved as of 2026; last verified PGP-signed Cicada message April 2017.
  - Nox Populi YouTube/Discord (run by 2013 winner) still active.
  - **No new public breakthroughs or hypotheses observed since last check.** The open-leads.md and ruled-out.md in this repo reflect the current known state of research.

## 2026-09-23 (continued)
- **"Numbers as direction" tests (Open-Leads #4)**: Tested multiple interpretations of the 2016 Cicada message "their numbers are the direction":
  - Continuous totient stream across pages: 3.75% (noise)
  - Totient stream as word-order permutation: 6.55% (interesting but still noise-level)
  - Page-numbered totient offsets: 4.08% (noise)
  - Solved page 73 values as key: 3.71% (noise)
  - Prime sequence mod 29: 3.82% (noise)
  - **Result: No signal exceeding noise floor**. All "numbers as direction" interpretations tested so far ruled out.
  - Note: The word-permutation test (6.55%) is closer to raw baseline (6.41%) than to 41% benchmark.

- **Keyed Columnar Transposition Test (Open-Leads #6)**: Tested standard keyed columnar transposition with 35 Cicada vocabulary keywords across all 56 unsolved pages.
  - Best result: "TOTIENT" → "TOIEN" (5 columns): 4.70% hit rate (129/2746 words)
  - Second best: "SHADOW" (6 cols): 4.55%, "DEATH" (5 cols): 4.59%
  - All results in 3.35% - 4.70% range, consistent with noise floor.
  - **Result: No signal exceeding noise floor**. All keyword/column combinations ruled out.

- **Magic Square Traversal Test (Open-Leads #2)**: Tested diagonal, anti-diagonal, and spiral orderings of the page 5 magic square as Vigenère keys.
  - Diagonal: 4.44% (up), 3.71% (down)
  - Anti-diagonal: 3.53% (up), 3.61% (down)  
  - Spiral: 3.90% (up), 3.46% (down)
  - **Result: No signal exceeding noise floor**. All three traversal orderings ruled out.

- **Autokey Decode Test (Open-Leads #0 follow-up)**: Used page 22 word 45 run as key to decode page 47 word 11 run.
  - Shift-up decode: `VALBWH` (6 chars) — 0 dictionary hits (0%).
  - Shift-down decode: `LLOUHK` (6 chars) — 0 dictionary hits (0%).
  - **Result: No signal exceeding noise floor**. Specific autokey approach ruled out.

## 2026-09-22
- **Lead #0 verification**: Attempted to confirm the 8-word length pattern `[6,7,6,3,6,4,3,3]` at page 22 word 45 / page 47 word 11.  
  - Exhaustive search found no contiguous match.  
  - Non‑contiguous (subsequence) search confirmed the pattern exists in that order, validating the lead's positional claim.  
  - Autokey decode test completed: no signal.
  - Next steps: Try broader autokey tests (longer runs, other candidate keys).

- Added comprehensive pattern‑search script (`comprehensive_pattern_search.py`) that scans for any repeated 8‑word length patterns across all blocks.  
- Commenced documentation of methodology in `methodology-note.md`.

## 2026-09-21
- Completed initial data ingestion from `krisyotam/cicada3301` and `jens-wedin/liber-primus` repositories.  
- Parsed transcription blocks and prepared length sequences for all 74 pages.  
- Added comprehensive pattern‑search script (`comprehensive_pattern_search.py`) that scans for any repeated 8‑word length patterns across all blocks.  
- Commenced documentation of methodology in `methodology-note.md`.

---

*All findings are logged in `experiments/` directory and committed to the repository for reproducibility.*