#!/usr/bin/env python3
"""
Galaxy CTF - Working Solution

Key discoveries:
1. ~(()>()) = ~False = -1  (bitwise NOT of False gives -1)
2. We can use + to add more Falses to get other negative numbers
3. We can build expressions like: spiral[~(()>()+()>())] to get different indices

Strategy:
- ()>() evaluates to False (which is 0 in arithmetic context)
- ~False = -1
- ~(False+False) = ~0 = -1
- ~(False+False+...+False) = -1 (since multiple Falses still sum to 0)

Wait, that won't help us get different indices...

Let me think: We need to construct different negative numbers.
- ~0 = -1
- ~1 = -2
- ~2 = -3
- etc.

How to build 0, 1, 2, 3, ...?
- ()>() = False = 0 (in arithmetic)
- But we need True = 1

Can we get True?
- ()<() = False
- ()>() = False  
- []==[] should be True, but we can't use ==
- What about: ()<[]? or []>()? These might be True or False...

Let me test!
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
allowed = '([<~abcdefghijklmnopqrstuvwxyz>+]/*\')'

# Test comparisons to find True values
print("Testing comparisons to find True:")
tests = {
    "()>()": ()>(),
    "()<()": ()<(),
    "[]>[]": []>[],
    "[]<[]": []<[],
    "()>[]": ()>[],
    "()<[]": ()<[],
    "[]>()": []>(),
    "[]<()": []<(),
    "''<''": ''<'',
}

for expr, val in tests.items():
    print(f"  {expr:12} = {val:5} (int: {int(val) if isinstance(val, bool) else '?'})")

print("\nTesting arithmetic with booleans:")
print(f"  False + False = {False + False}")
print(f"  False + True = {False + True}")
print(f"  True + True = {True + True}")
print(f"  ~0 = {~0}")
print(f"  ~1 = {~1}")
print(f"  ~2 = {~2}")

print("\nCan we build different numbers?")
# If we have a True value, we can build: 0, 1, 2, 3, ...
# Let's say []<() = True (hypothetically)
if []<():
    print("  []<() is True!")
    print(f"  ()>() = {()>()}")  # False = 0
    print(f"  []<() = {[]<()}")  # True = 1
    print(f"  []<()+[]<() = {[]<()+[]<()}")  # True + True = 2
    print(f"  []<()+[]<()+[]<() = {[]<()+[]<()+[]<()}")  # 3
    
    print("\n  Now building negative indices:")
    for i in range(5):
        if i == 0:
            expr = "()>()"
            idx = ~int(eval(expr))
        else:
            expr = "+".join(["[]<()"] * i)
            idx = ~int(eval(expr))
        print(f"    ~({expr}) = {idx}")

if ()<[]:
    print("\n  ()<[] is True!")
    base = "()<[]"
    for i in range(5):
        if i == 0:
            expr = "()>()"
            idx = ~int(eval(expr))
        else:
            expr = "+".join([base] * i)
            idx = ~int(eval(expr))
        print(f"    ~({expr}) = {idx}")
