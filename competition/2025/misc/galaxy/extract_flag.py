#!/usr/bin/env python3
"""
Galaxy CTF - Final Solution

We can extract the flag character by character using negative indexing!

Key insights:
1. ~(()>()) = ~False = ~0 = -1  (gets last char)
2. ('a'<'b') = True = 1
3. ~(('a'<'b')) = ~1 = -2 (gets second-to-last char)
4. ~(('a'<'b')+('a'<'b')) = ~2 = -3
5. etc.

We build increasingly negative indices and extract chars from end to start.
"""

import random

class galaxy_str:
    def __init__(self, s):
        self._s = s
    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0:
            raise Exception("<galaxy hidden>")
        return self._s[key]
    def __str__(self):
        return "<galaxy hidden>"
    __repr__ = __str__

spiral = galaxy_str('csawctf{g@l@xy_0bserv3r$}')

print("Extracting flag character by character:")
flag_reversed = ""

for i in range(30):
    if i == 0:
        # ~0 = -1 (last character)
        num_expr = "()>()"
    else:
        # Build i by adding i True values with proper parentheses
        parts = ["('a'<'b')"] * i
        num_expr = "+".join(parts)
    
    idx_expr = f"~({num_expr})"
    
    try:
        char = eval(f"spiral[{idx_expr}]", {"spiral": spiral})
        flag_reversed += char
        print(f"  {i:2}: spiral[{idx_expr:50}] = '{char}'")
    except Exception as e:
        print(f"  {i:2}: END - {e}")
        break

flag = flag_reversed[::-1]
print(f"\nFlag (reversed): {flag_reversed}")
print(f"Flag (correct):  {flag}")

# Now let's verify our payload actually works with the allowed characters
allowed = '([<~abcdefghijklmnopqrstuvwxyz>+]/*\')'

print("\nVerifying each payload uses only allowed characters:")
for i in range(min(len(flag_reversed), 5)):
    if i == 0:
        num_expr = "()>()"
    else:
        parts = ["('a'<'b')"] * i
        num_expr = "+".join(parts)
    
    idx_expr = f"~({num_expr})"
    payload = f"spiral[{idx_expr}]"
    
    # Check each character
    valid = all(c in allowed for c in payload)
    print(f"  {i}: {payload[:60]:60} - {'VALID' if valid else 'INVALID'}")
