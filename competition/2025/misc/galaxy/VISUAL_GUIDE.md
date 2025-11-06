# Galaxy Challenge - Visual Solution Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    GALAXY CTF CHALLENGE                         │
│                  Python Jail + Cipher Combo                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  THE OBSTACLE: galaxy_str class                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  class galaxy_str:                                              │
│      def __getitem__(self, key):                                │
│          if isinstance(key, int) and key >= 0:                  │
│              raise Exception("<galaxy hidden>")  ← BLOCKS THIS  │
│          return self._s[key]                                    │
│                                                                 │
│  ❌ spiral[0]   → Exception                                     │
│  ❌ spiral[1]   → Exception                                     │
│  ✅ spiral[-1]  → Works! (last character)                       │
│  ✅ spiral[-2]  → Works! (second-to-last)                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  THE PROBLEM: Limited Characters                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Allowed: ([<~abcdefghijklmnopqrstuvwxyz>+]/*')                 │
│                                                                 │
│  ❌ Can't use: - (minus sign)                                   │
│  ❌ Can't use: : (colon for slicing)                            │
│  ❌ Can't use: _ (underscore)                                   │
│  ❌ Can't use: digits 0-9                                       │
│                                                                 │
│  So we CAN'T write: spiral[-1] directly!                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  THE SOLUTION: Build Negative Numbers with ~                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Bitwise NOT (~) operator:                                      │
│                                                                 │
│     ~0 = -1                                                     │
│     ~1 = -2                                                     │
│     ~2 = -3                                                     │
│     ~3 = -4                                                     │
│     ...                                                         │
│                                                                 │
│  So if we can build 0, 1, 2, 3, ... we can get -1, -2, -3...!  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  BUILDING BLOCKS: Creating Numbers                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Creating 0 (False):                                            │
│     ()>() = False = 0                                           │
│                                                                 │
│  Creating 1 (True):                                             │
│     ('a'<'b') = True = 1                                        │
│                                                                 │
│  Creating 2:                                                    │
│     ('a'<'b') + ('a'<'b') = 1 + 1 = 2                           │
│                                                                 │
│  Creating 3:                                                    │
│     ('a'<'b') + ('a'<'b') + ('a'<'b') = 3                       │
│                                                                 │
│  And so on...                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  EXTRACTION: Getting Each Character                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Flag: csawctf{g@l@xy_0bserv3r$}                                │
│                                                                 │
│  Position:  c s a w c t f { g @ l @ x y _ 0 b s e r v 3 r $ }  │
│  Index:     0 1 2 3 4 5 6 7 8 9 ...                            24│
│  Negative: -25-24-23-22 ...                           -3 -2 -1  │
│                                                                 │
│  Extract from END to START:                                     │
│                                                                 │
│  spiral[~(()>())]                  = spiral[~0] = spiral[-1] = }│
│  spiral[~(('a'<'b'))]              = spiral[~1] = spiral[-2] = $│
│  spiral[~(('a'<'b')+('a'<'b'))]    = spiral[~2] = spiral[-3] = r│
│  ...                                                            │
│                                                                 │
│  Collected: }$r3vresb0_yx@l@g{ftcwasc                           │
│  Reversed:  csawctf{g@l@xy_0bserv3r$}  ← FLAG!                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  PAYLOAD PATTERN                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  To get character at position -(n+1):                           │
│                                                                 │
│     ┌───────────────────────────────────────────┐              │
│     │  spiral[~( <n True values added> )]       │              │
│     └───────────────────────────────────────────┘              │
│                                                                 │
│  Where each True value is: ('a'<'b')                            │
│  And they're connected with: +                                  │
│                                                                 │
│  Example for n=5 (to get index -6):                             │
│                                                                 │
│     spiral[~(('a'<'b')+('a'<'b')+('a'<'b')+('a'<'b')+('a'<'b'))]│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  IMPORTANT NOTES                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. The substitution cipher is handled by the server            │
│     - Server encrypts its mapping                               │
│     - Server decrypts your input before eval                    │
│     - Just send plaintext payloads!                             │
│                                                                 │
│  2. All characters in the payload MUST be from allowed set      │
│     - No numbers, no underscores, no colons                     │
│                                                                 │
│  3. Extract from end to beginning, then reverse                 │
│     - We can only build non-negative n                          │
│     - So we can only get -1, -2, -3, ... (backward)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
