# Research Methodology Note – Pattern Verification in Open-Leads Item 0

**Date:** 2026-09-22  
**Author:** AI Research Agent (Corey Mitchell)  
**Goal:** Verify the highest‑priority lead from `open-leads.md` item 0:  
> “8‑word‑length run `[6,7,6,3,6,4,3,3]` matching exactly at page 22 word 45 and page 47 word 11.”

---

## 1. Data Source Overview
- **Primary transcription file:** `data/liber-primus-jens/download/rtkd_liber_primus_transcription.txt`
- **Structure:** The file stores 74 blocks separated by a line containing only `%`.  
  Each block corresponds to a transcribed page of the Liber Primus.  
  According to `page-catalog.md`, approximate mappings are:
  - **Block 5 → page 22**  
  - **Block 30 → page 47**  
  (Caveat: the catalogue notes an off‑by‑one uncertainty.)

---

## 2. Extraction Logic
1. **Block Splitting** – Split on “%” line endings and strip whitespace.  
2. **Word Tokenisation** – Within each block, remove “/” and newline characters, then split on “-”.  
3. **Length Computation** – For each token (rune‑group), count the number of runes using the Gematria Primus mapping (`RUNE_TO_VAL`).  
4. **Word‑Length Sequence** – Produce a list of length‑values for the page.

The process was implemented in `comprehensive_pattern_search.py` and executed successfully; it produced the raw length sequences for all blocks.

---

## 3. Target Search
- **Pattern of interest:** `[6, 7, 6, 3, 6, 4, 3, 3]` (8‑word contiguous run).  
- **Method:** Slid an 8‑word window across each page’s length list and recorded every start index where the slice matched the target pattern.  
- **Result:** **No matches** were found at the expected start positions:
  - Page 22 (block 5) start index 44 (word 45) → no match.  
  - Page 47 (block 30) start index 10 (word 11) → no match.  
- The search also scanned for *any* occurrence of the pattern in any block; **zero occurrences** were detected across the entire corpus.

---

## 4. Observations & Potential Issues
| Observation | Interpretation |
|-------------|----------------|
| The word‑index numbers (45, 11) map to length‑5 and length‑3 tokens respectively in the current extraction. | The target pattern (`[6,7,6,3,6,4,3,3]`) does **not** align with those lengths, suggesting either a **mis‑indexing** (perhaps the leads use 1‑based page numbers that do not line up with our block‑to‑page mapping) or that **different delimiters/tokenisation rules** were used in the original source. |
| No global occurrence of the pattern was found anywhere in the 74 blocks. | Either the pattern is exceedingly rare (statistically unlikely to appear) or the **interpretation of “word length”** might differ (e.g., counting runes instead of runes per token). |
| The block‑to‑page mapping is not 100 % verified. | A systematic cross‑check against the PDF images (or the `page-catalog.md` index) could reveal an **off‑by‑one** error, which would move the expected tokens to a different block. |

---

## 5. Next‑Step Recommendations
1. **Verify Block‑to‑Page Mapping**  
   - Manually compare the `%` delimiter positions in the transcription file against the **PDF images** of pages 22 and 47 (if available) to confirm that block 5 truly corresponds to page 22 and block 30 to page 47.  
   - If an offset error is discovered, adjust the indices accordingly and re‑run the pattern search.

2. **Re‑examine Tokenisation Rules**  
   - Ensure that the tokenisation step (splitting on “-”, stripping “/”, handling newlines) exactly mirrors the original transcription.  
   - Look for edge cases where consecutive delimiters might produce empty tokens that could shift subsequent indices.

3. **Consider Non‑Contiguous Matching**  
   - Investigate whether the “run” might be **non‑contiguous** (e.g., a pattern of lengths that appears when skipping certain tokens). This would broaden the search space and could surface the lead in a different arrangement.

4. **Document Findings Systematically**  
   - Continue to log each investigative step in a dedicated markdown file (as done with `methodology-note.md`).  
   - Include snippets of the raw length lists and surrounding tokens for transparency and reproducibility.

5. **Commit Incremental Results**  
   - After each methodological refinement (e.g., corrected mapping, re‑tokenisation), commit the updated scripts and notes to the repository (`liber-primus-research`). This maintains a clear audit trail for future reviewers.

---

## 6. Status Summary
- **Pattern verification:** *unsuccessful* – no occurrence of `[6,7,6,3,6,4,3,3]` found at the expected positions.  
- **Current artifacts:**  
  - `comprehensive_pattern_search.py` – full‑scale search implementation.  
  - `methodology-note.md` – documented approach and observations.  
- **Next focus:** *mapping verification* and *tokenisation audit*.

> **Discipline Reminder:** Every positive claim must be backed by verifiable evidence (e.g., a concrete match of the pattern). Until such evidence is obtained, all leads remain *candidate* items and should be treated as tentative hypotheses.

--- 

*End of note.*  
