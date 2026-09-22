# Gematria Primus — Cipher Table

The Gematria Primus is the cipher/alphabet system Cicada 3301 introduced in the 2013
puzzle. It maps 29 Anglo-Saxon Futhorc runes to the first 29 prime numbers, and to
Latin letter(s). It underlies essentially all Liber Primus text.

| Index | Prime | Rune | Unicode | Latin | Name    |
|-------|-------|------|---------|-------|---------|
| 0     | 2     | ᚠ    | U+16A0  | F     | Feoh    |
| 1     | 3     | ᚢ    | U+16A2  | U/V   | Ur      |
| 2     | 5     | ᚦ    | U+16A6  | TH    | Thorn   |
| 3     | 7     | ᚩ    | U+16A9  | O     | Os      |
| 4     | 11    | ᚱ    | U+16B1  | R     | Rad     |
| 5     | 13    | ᚳ    | U+16B3  | C/K   | Cen     |
| 6     | 17    | ᚷ    | U+16B7  | G     | Gyfu    |
| 7     | 19    | ᚹ    | U+16B9  | W     | Wynn    |
| 8     | 23    | ᚻ    | U+16BB  | H     | Haegl   |
| 9     | 29    | ᚾ    | U+16BE  | N     | Nyd     |
| 10    | 31    | ᛁ    | U+16C1  | I/J   | Is      |
| 11    | 37    | ᛄ    | U+16C4  | IO/IA | Ior     |
| 12    | 41    | ᛇ    | U+16C7  | EO    | Eolhx   |
| 13    | 43    | ᛈ    | U+16C8  | P     | Peorth  |
| 14    | 47    | ᛉ    | U+16C9  | X     | Eolh    |
| 15    | 53    | ᛋ    | U+16CB  | S/Z   | Sigel   |
| 16    | 59    | ᛏ    | U+16CF  | T     | Tir     |
| 17    | 61    | ᛒ    | U+16D2  | B     | Beorc   |
| 18    | 67    | ᛖ    | U+16D6  | E     | Eh      |
| 19    | 71    | ᛗ    | U+16D7  | M     | Mann    |
| 20    | 73    | ᛚ    | U+16DA  | L     | Lagu    |
| 21    | 79    | ᛝ    | U+16DD  | NG/ING| Ing     |
| 22    | 83    | ᛟ    | U+16DF  | OE    | Ethel   |
| 23    | 89    | ᛞ    | U+16DE  | D     | Daeg    |
| 24    | 97    | ᚪ    | U+16AA  | A     | Ac      |
| 25    | 101   | ᚫ    | U+16AB  | AE    | Aesc    |
| 26    | 103   | ᚣ    | U+16A3  | Y     | Yr      |
| 27    | 107   | ᛡ    | U+16E1  | EA    | Ear     |
| 28    | 109   | ᛠ    | U+16E0  | Q(rare)| Cweorth|

Word separator: `•` (U+2022, bullet). In the community's plain-text transcriptions
this is often rendered as `-` (word break) or `/` (line-continuation) or `.` (sentence
end) — check the specific transcription source's conventions in
`data-sources.md` before parsing.

## Two versions exist

- **Gematria Primus 2013**: the original, published as a chart image in the 2013
  puzzle. This is the table above.
- **Gematria Primus 2014**: a reversed (Atbash-style) variant reconstructed by the
  community from solved pages — used to solve page 01 ("A Warning"). To compute it,
  reverse the rune order against the same prime/letter sequence (rune at index i
  in 2013 maps according to the rune at index 28-i in 2014). Always double check
  against a known-solved page before trusting a from-scratch reconstruction.

## Ambiguous letter mappings — important gotcha

Several runes map to MORE than one possible Latin rendering (C/K, S/Z, IO/IA, and
sometimes U/V). When brute-forcing or scoring candidate decryptions, you often need
to try multiple spellings of the resulting "word" against a dictionary, or normalize
both the candidate and the dictionary (e.g., treat C and K as interchangeable) before
scoring. Getting this wrong silently lowers your dictionary hit rate and can make a
real hit look like noise. `scripts/gematria_toolkit.py` handles this via
`normalize_ambiguous()` — use it rather than a plain string equality dictionary check.

## Known content clues from solved pages (thematically important)

These aren't cipher mechanics, but they're explicit statements from the book itself
that may be operative hints, not just flavor text:

- "The primes are sacred." (page 5)
- "The totient function is sacred." (page 5) — this literally led to solving page 73
  ("An End") via a stream of φ(nth prime) = (nth prime − 1), mod 29. See
  `solved-pages.md`.
- "All things should be encrypted." (page 5)
- Verified 2016 Cicada message (outside the book): "Liber Primus is the way, its
  words are the map, their meaning is the road, and their numbers are the direction."
  Nobody has turned "their numbers are the direction" into a working decryption step
  yet — flagged as an open lead, see `open-leads.md`.
