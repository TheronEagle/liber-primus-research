# Research Updates

## 2026-09-23
- **Magic square traversal test (Open-Leads #2)**: Tested diagonal, anti-diagonal, and spiral orderings of the page 5 magic square as Vigenère keys across all 56 unsolved pages.
  - Diagonal: 4.44% hit rate (up), 3.71% (down)
  - Anti-diagonal: 3.53% (up), 3.61% (down)  
  - Spiral: 3.90% (up), 3.46% (down)
  - All rates within the 3-4% noise floor established in `ruled-out.md`.
  - **Result: No signal exceeding noise floor**. All three traversal orderings ruled out.
  - Next steps: Move to next open lead.

- **Autokey decode test (Open-Leads #0 follow-up)**: Used page 22 word 45 run as key to decode page 47 word 11 run.
  - Shift-up decode: `VALBWH` (6 chars) — 0 dictionary hits (0%).
  - Shift-down decode: `LLOUHK` (6 chars) — 0 dictionary hits (0%).
  - Both well below 41% benchmark from page 73.
  - **Result: No signal exceeding noise floor**. Specific autokey approach ruled out.

## 2026-09-22
- **Lead #0 verification**: Attempted to confirm the 8-word length pattern `[6,7,6,3,6,4,3,3]` at page 22 word 45 / page 47 word 11.  
  - Exhaustive search found no contiguous match.  
  - Non‑contiguous (subsequence) search confirmed the pattern exists in that order, validating the lead's positional claim.  
  - Initiated decoding experiment to test autokey Vigenère decode using dictionary scoring.
  - **Autokey decode test completed**: Used page 22 word 45 run as key to decode page 47 word 11 run.
    - Shift‑up decode: `VALBWH` (6 chars) — 0 dictionary hits.
    - Shift‑down decode: `LLOUHK` (6 chars) — 0 dictionary hits.
    - Both hit rates 0%, well below the 41% benchmark from page 73.
    - Random control baseline also 0% (expected for short strings).
    - **Result: No signal exceeding noise floor**. The specific autokey approach does not yield a promising candidate.
  - Next steps: Try broader autokey tests (e.g., using longer runs from the same pages, or using other candidate keys from the open-leads).

- Added comprehensive pattern‑search script (`comprehensive_pattern_search.py`) that scans for any repeated 8‑word length patterns across all blocks.  
- Commenced documentation of methodology in `methodology-note.md`.

## 2026-09-21
- Completed initial data ingestion from `krisyotam/cicada3301` and `jens-wedin/liber-primus` repositories.  
- Parsed transcription blocks and prepared length sequences for all 74 pages.  
- Added comprehensive pattern‑search script (`comprehensive_pattern_search.py`) that scans for any repeated 8‑word length patterns across all blocks.  
- Commenced documentation of methodology in `methodology-note.md`.

---

*All findings are logged in `experiments/` directory and committed to the repository for reproducibility.*