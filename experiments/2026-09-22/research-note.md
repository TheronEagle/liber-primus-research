# Research Note: Pattern Search in Open-Leads Priority

## Current Status
- The reported 8-word-length pattern `[6,7,6,3,6,4,3,3]` from `open-leads.md` item 0 was not found at the expected positions:
  - Page 22 (block index 5) word 45 (1-indexed)
  - Page 47 (block index 30) word 11 (1-indexed)
- Page 22 contains 50 words total
- Page 47 contains 57 words total
- At word 45 of page 22 (0-index 44), the word length is 5
- At word 11 of page 47 (0-index 10), the word length is 3

## Analysis
This suggests either:
1. An indexing discrepancy in the block-to-page mapping
2. A misunderstanding of how word lengths are counted
3. The pattern might not be contiguous in the current data representation

## Next Steps
- Re-examine block structure and word extraction logic
- Verify against original page images if possible
- Consider alternative interpretations of the pattern (e.g., non-contiguous, different window size)

> **Research Discipline**: Always verify against primary sources before drawing conclusions.