#!/usr/bin/env python3
"""
Galaxy CTF - Find True value

We need to find an expression that gives us True (which equals 1 in arithmetic)
Allowed chars: ([<~abcdefghijklmnopqrstuvwxyz>+]/*')
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

print("Testing expressions that might give True:")
tests = [
    ("()>()", ()>()),  # False
    ("()<()", ()<()),  # False  
    ("[]>[]", []>[]),  # False
    ("[]<[]", []<[]),  # False
    ("''<''", ''<''),  # False
    ("[]+[]", []+[]),  # Empty list
    ("[]+[]+[]", []+[]+[]),  # Empty list
    ("[[]]>[]", [[]]>[]),  # True! Non-empty list > empty list
    ("[]<[[]]", []<[[]]),  # True! Empty list < non-empty list
    ("'a'>''", 'a'>''),  # True! Non-empty string > empty string
    ("''<'a'", ''<'a'),  # True! Empty string < non-empty string
]

for expr, val in tests:
    try:
        print(f"  {expr:20} = {str(val):10} (type: {type(val).__name__:4}) ", end="")
        if isinstance(val, bool):
            print(f"int: {int(val)}")
        else:
            print()
    except Exception as e:
        print(f" ERROR: {e}")

print("\nNow let's try to build numbers using [[]]>[]:")
# [[]]>[] should be True = 1
if [[]]>[]:
    print("  [[]]>[] = True = 1")
    
    # Build numbers 0, 1, 2, 3, ...
    for i in range(10):
        if i == 0:
            num_expr = "()>()"  # False = 0
            num = int(()>())
        else:
            # Add i copies of True
            num_expr = "+".join(["[[]]>[]"] * i)
            num = int(eval(num_expr))
        
        neg_idx = ~num
        print(f"    i={i}: ~({num}) = {neg_idx}")
        
        # Try to access spiral with this index
        try:
            idx_expr = f"~({num_expr})"
            char = eval(f"spiral[{idx_expr}]", {"spiral": spiral})
            print(f"        spiral[{idx_expr}] = '{char}'")
        except Exception as e:
            print(f"        ERROR: {e}")

print("\nBut wait - can we use 'a' in allowed chars?")
allowed_chars = "([<~abcdefghijklmnopqrstuvwxyz>+]/*')"
test_str = "'a'"
print(f"  'a' uses only allowed chars: {all(c in allowed_chars for c in test_str)}")

# Actually, we have all lowercase letters available!
# So we can use any single letter string comparisons

print("\nUsing single letter comparisons:")
# 'a'<'b' is True
# 'b'<'a' is False
if 'a'<'b':
    print("  'a'<'b' = True = 1")
    
    for i in range(10):
        if i == 0:
            num_expr = "()>()"
            num = 0
        else:
            num_expr = "+".join(["'a'<'b'"] * i)
            num = i
        
        neg_idx = ~num
        idx_expr = f"~({num_expr})"
        
        try:
            char = eval(f"spiral[{idx_expr}]", {"spiral": spiral})
            print(f"    {i}: spiral[{idx_expr}] = '{char}'")
        except Exception as e:
            print(f"    {i}: ERROR: {e}")

print("\nLet's extract the whole flag:")
flag = ""
for i in range(30):  # Assume flag is less than 30 chars
    if i == 0:
        num_expr = "()>()"
    else:
        num_expr = "+".join(["'a'<'b'"] * i)
    
    idx_expr = f"~({num_expr})"
    
    try:
        char = eval(f"spiral[{idx_expr}]", {"spiral": spiral})
        flag += char
    except Exception as e:
        break

print(f"\nReconstructed flag (reversed): {flag}")
print(f"Actual flag: {flag[::-1]}")
