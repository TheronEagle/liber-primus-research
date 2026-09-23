#!/usr/bin/env python3
"""
Debug columnar transposition with a simple test case - CORRECTED.
"""

import sys
sys.path.insert(0, 'skill/cicada-3301-solver/scripts')
from gematria_toolkit import RUNE_TO_VAL, VAL_TO_LATIN, ALPHABET_SIZE

def get_column_order(keyword):
    """
    Get the column reading order for keyed columnar transposition.
    Returns list of column indices in the order they should be read.
    The order is determined by alphabetical order of keyword letters.
    """
    # Number columns by alphabetical order of keyword letters
    # Ties broken by original position
    key_pairs = [(ch, i) for i, ch in enumerate(keyword)]
    key_pairs.sort(key=lambda x: (x[0], x[1]))
    col_order = [pair[1] for pair in key_pairs]
    return col_order

def columnar_encrypt(plaintext, keyword):
    """Encrypt plaintext using columnar transposition with keyword."""
    num_cols = len(keyword)
    n = len(plaintext)
    num_rows = (n + num_cols - 1) // num_cols
    
    # Fill grid row by row
    grid = []
    for i in range(0, n, num_cols):
        row = plaintext[i:i+num_cols]
        # Pad last row if needed
        if len(row) < num_cols:
            row = row + [None] * (num_cols - len(row))
        grid.append(row)
    
    # Read columns in keyword order
    col_order = get_column_order(keyword)
    ciphertext = []
    for col_idx in col_order:
        for row in range(len(grid)):
            val = grid[row][col_idx]
            if val is not None:
                ciphertext.append(val)
    return ciphertext

def columnar_decrypt(ciphertext, keyword):
    """Decrypt ciphertext using columnar transposition with keyword."""
    num_cols = len(keyword)
    n = len(ciphertext)
    num_rows = (n + num_cols - 1) // num_cols
    num_full_cols = n % num_cols
    if num_full_cols == 0:
        num_full_cols = num_cols
    
    col_order = get_column_order(keyword)
    
    # Calculate column heights
    col_heights = [num_rows if i < num_full_cols else num_rows - 1 for i in range(num_cols)]
    
    # Fill grid column by column in keyword order
    grid = [[None] * num_cols for _ in range(num_rows)]
    idx = 0
    for col_idx in col_order:
        height = col_heights[col_idx]
        for row in range(height):
            grid[row][col_idx] = ciphertext[idx]
            idx += 1
    
    # Read out row by row
    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            val = grid[row][col]
            if val is not None:
                result.append(val)
    return result

# Test
print("=== Test 1: Simple case ===")
plaintext = list(range(20))
keyword = "HELLO"
print(f"Plaintext: {plaintext}")
print(f"Keyword: {keyword} (length {len(keyword)})")

ciphertext = columnar_encrypt(plaintext, keyword)
print(f"Ciphertext: {ciphertext} (length {len(ciphertext)})")

decrypted = columnar_decrypt(ciphertext, keyword)
print(f"Decrypted: {decrypted}")
print(f"Match: {decrypted == plaintext}")

print("\n=== Test 2: Different keyword ===")
keyword2 = "KEY"
plaintext2 = list(range(15))
print(f"Plaintext: {plaintext2}")
print(f"Keyword: {keyword2} (length {len(keyword2)})")

ciphertext2 = columnar_encrypt(plaintext2, keyword2)
print(f"Ciphertext: {ciphertext2}")

decrypted2 = columnar_decrypt(ciphertext2, keyword2)
print(f"Decrypted: {decrypted2}")
print(f"Match: {decrypted2 == plaintext2}")

print("\n=== Test 3: Non-square ===")
keyword3 = "CRYPTO"
plaintext3 = list(range(30))
print(f"Plaintext: {plaintext3}")
print(f"Keyword: {keyword3} (length {len(keyword3)})")

ciphertext3 = columnar_encrypt(plaintext3, keyword3)
print(f"Ciphertext: {ciphertext3}")

decrypted3 = columnar_decrypt(ciphertext3, keyword3)
print(f"Decrypted: {decrypted3}")
print(f"Match: {decrypted3 == plaintext3}")