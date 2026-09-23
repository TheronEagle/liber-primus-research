# Research Updates

## 2026-09-24 (final session)
- **Final analysis of Open-Leads #0 (deep analysis at corrected positions):**
  - **Pattern 1** (blocks 19 & 44): Word-lengths match perfectly (8-word run), but Gematria VALUES differ. They share 3 n=6-grams and 2 n=7-grams at the SAME relative positions - strong structural correlation but different ciphertext.
    - Autokey/running-key tests: no signal (gibberish output).
    - Shared n-grams as Vigenère keys: no signal.
  - **Pattern 2** (block 40): **Unique global occurrence** of `[5,4,7,3,6,3,7,4]` - only happens ONCE in the entire corpus!
    - Self-decrypt with all 39 offsets: max hit rate 3.51% (2/57) - exactly noise floor.
    - **Result: No signal exceeding noise floor**.
  - **Conclusion for lead #0**: Structural word-length correlation is real but doesn't yield a usable key. All reasonable cryptographic interpretations exhausted without signal above noise. **LEAD #0 RULED OUT.**

- **Magic Square Diagonal/Spiral Traversal Test (Open-Leads #2 - remaining):** Tested all 6 traversals (diagonal main/anti, spiral cw/ccw, zigzag rows/cols) of the page 5 magic square as Vigenère keys.
  - Best: diagonal_main 4.44% (up)
  - All results 3.4% - 4.4%, noise floor.
  - **Result: No signal exceeding noise floor**. All diagonal/spiral/zigzag traversals ruled out.

- **Unique Pattern Systematic Test (block 40):** Tested unique pattern as Vigenère key (all rotations), autokey, running key, reversed.
  - Best: 4.66% (reversed, offset 21) - noise floor.
  - **Result: No signal.**

- **Rail Fence Transposition Test (Open-Leads #6 - remaining):** Tested 2-10 rails.
  - Best: 2 rails at 4.55% - noise floor. **Ruled out.**

- **Reversed Key Text Test (Open-Leads #6 - remaining):** 4 texts × 2 directions.
  - Best: Blake forward 4.41% - noise floor. **Ruled out.**

- **Illustration Steganalysis (Open-Leads #5):** Pages 8-14, 32, 55 analyzed.
  - All show smoothly decaying NN histograms - natural stippling. **Ruled out.**

- **Baseline raw transliteration:** 6.41% hit rate (higher than Vigenère noise floor but far below 41% benchmark).

- **Live community state check (Open-Leads #7):** No new breakthroughs. Wiki, Wikipedia, Nox Populi all confirm 56 unsolved pages.

## Summary: ALL LEADS TESTED AND RULED OUT

| Lead | Status | Best Hit Rate | Benchmark |
|------|--------|---------------|-----------|
| #0 Word-length pattern | RULED OUT | 3.5% | 41% |
| #1 Continuous stream | RULED OUT | 3.75% | 41% |
| #2 Magic square (all traversals) | RULED OUT | 4.44% | 41% |
| #3 Word-length analysis | RULED OUT | 3.5% | 41% |
| #4 Numbers as direction | RULED OUT | 6.55% | 41% |
| #5 Illustration steganalysis | RULED OUT | N/A | N/A |
| #6 Non-substitution ciphers (all variants) | RULED OUT | 4.70% | 41% |
| #7 Community state | CHECKED | - | - |

**ALL LEADS EXHAUSTED.** No signal above noise floor found in any test. The Liber Primus unsolved pages remain unsolved, consistent with the global community state.

The repository now contains a complete, transparent, and reproducible record of all tests conducted. All code, data, and results are committed and pushed to GitHub.