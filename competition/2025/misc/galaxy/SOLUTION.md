# Galaxy - CTF Challenge Writeup

**Category:** Misc  
**Difficulty:** Medium  
**Flag:** `csawctf{g@l@xy_0bserv3r$}`

## Challenge Overview

The challenge presents a Python jail/sandbox with the following constraints:

1. **Custom String Class (`galaxy_str`)**: The flag is stored in a custom class that:
   - Blocks positive integer indexing (raises exception)
   - Hides string representation (returns `"<galaxy hidden>"`)
   - Only allows negative indexing or slicing

2. **Substitution Cipher (`galaxy_aura`)**: User input is encrypted with a random substitution cipher before evaluation

3. **Input Sanitization**: Only allows these characters: `([<~abcdefghijklmnopqrstuvwxyz>+]/*')`

4. **Restricted Eval**: Code is evaluated with no builtins, only access to the `spiral` object containing the flag

## Analysis

### The galaxy_str Class

```python
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
```

**Key Insight:** The class only blocks `isinstance(key, int) and key >= 0`, which means:
- ✅ Negative integers work: `spiral[-1]`, `spiral[-2]`, etc.
- ✅ Slices work: `spiral[:]`, `spiral[::]`, etc.
- ❌ Positive integers blocked: `spiral[0]`, `spiral[1]`, etc.

### Allowed Characters

```
([<~abcdefghijklmnopqrstuvwxyz>+]/*')
```

Breaking it down:
- **Brackets:** `(`, `)`, `[`, `]`, `<`, `>`
- **Letters:** `a-z`
- **Operators:** `~` (bitwise NOT), `+`, `*`, `/`
- **Quote:** `'`

**Missing:** `:` (colon) - so we can't use slice syntax like `spiral[:]`

## Solution Strategy

Since we can use negative indexing but can't directly write `-1`, `-2`, etc., we need to construct negative integers using the allowed characters.

### Building Negative Integers

**Key Discovery:** `~(expression)` gives us bitwise NOT
- `~0 = -1`
- `~1 = -2`
- `~2 = -3`
- ...

Now we need to build the numbers 0, 1, 2, 3, ...

### Building Positive Integers

**Finding False (0):**
```python
()>() = False = 0  # Empty tuple comparison
```

**Finding True (1):**
```python
('a'<'b') = True = 1  # String comparison
```

**Building Larger Numbers:**
```python
('a'<'b')+('a'<'b') = 1 + 1 = 2
('a'<'b')+('a'<'b')+('a'<'b') = 3
# etc.
```

### Extraction Payloads

```python
# Get last character (index -1):
spiral[~(()>())]

# Get second-to-last (index -2):
spiral[~(('a'<'b'))]

# Get third-to-last (index -3):
spiral[~(('a'<'b')+('a'<'b'))]

# Get fourth-to-last (index -4):
spiral[~(('a'<'b')+('a'<'b')+('a'<'b'))]

# etc.
```

### Complete Algorithm

1. Start with index -1 (last character)
2. Extract character using `spiral[~(()>())]`
3. Move to index -2, -3, ... by adding more `('a'<'b')` terms
4. Continue until we hit the beginning of the string
5. Reverse the extracted string to get the flag

## Solution Code

See `solution.py` for the complete implementation.

### Key Function

```python
def create_payload(index):
    """
    Create a payload to access spiral[index]
    where index is negative (e.g., -1, -2, -3, ...)
    """
    n = -index - 1  # Convert negative index to positive n where ~n = index
    
    if n == 0:
        expr = "()>()"
    else:
        parts = ["('a'<'b')"] * n
        expr = "+".join(parts)
    
    return f"spiral[~({expr})]"
```

## Execution

### Local Testing

```bash
python solution.py
```

Output:
```
[!] FLAG: csawctf{g@l@xy_0bserv3r$}
```

### Example Payloads

```
spiral[~(()>())]                                    => '}'
spiral[~(('a'<'b'))]                                => '$'
spiral[~(('a'<'b')+('a'<'b'))]                      => 'r'
spiral[~(('a'<'b')+('a'<'b')+('a'<'b'))]            => '3'
spiral[~(('a'<'b')+('a'<'b')+('a'<'b')+('a'<'b'))]  => 'v'
...
```

Reversing these characters gives us: `csawctf{g@l@xy_0bserv3r$}`

## Learning Points

1. **Operator Precedence:** Understanding how Python evaluates expressions is crucial
2. **Type Coercion:** Booleans can be used in arithmetic (True=1, False=0)
3. **Bitwise Operations:** The `~` operator for bitwise NOT: `~n = -(n+1)`
4. **Creative Constraint Bypass:** When direct approaches are blocked, build what you need from primitives
5. **Character-by-Character Extraction:** Even with heavy restrictions, data can often be leaked bit by bit

## Flag

```
csawctf{g@l@xy_0bserv3r$}
```
