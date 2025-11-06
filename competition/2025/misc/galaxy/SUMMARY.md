# Galaxy Challenge - Summary

## Challenge Summary

**Galaxy** is a Python jail challenge where you must extract a flag from a restricted Python environment with:
- Custom class blocking positive indexing
- Random substitution cipher on input
- Severely limited character set
- No builtin functions available

## Solution Summary

Extract the flag using **negative indexing** by constructing negative integers from allowed primitives:

1. `~0 = -1` (bitwise NOT of 0 gives -1)
2. Build 0 from: `()>()` (False = 0)
3. Build 1 from: `('a'<'b')` (True = 1)
4. Build larger numbers by adding True values
5. Extract each character: `spiral[~(expression)]`
6. Reverse the result

## Files Created

### Solution Files
- **`solution.py`** - Automated solver (local and remote)
- **`manual_solver.py`** - Helper for manual solving
- **`extract_flag.py`** - Demonstration of extraction technique

### Analysis Files
- **`test_payloads.py`** - Testing different payload approaches
- **`find_true.py`** - Finding ways to construct boolean values
- **`test_comparisons.py`** - Testing comparison operators

### Documentation
- **`SOLUTION.md`** - Complete technical writeup
- **`README.md`** - Quick reference guide

## Flag

```
csawctf{g@l@xy_0bserv3r$}
```

## Key Techniques Learned

1. **Bitwise NOT for negative numbers:** `~n = -(n+1)`
2. **Boolean arithmetic:** True=1, False=0 in calculations
3. **Character-by-character extraction** when direct access is blocked
4. **Building primitives** from limited character sets
5. **Substitution cipher handling** - server decrypts automatically

## Quick Reference

### Example Payloads
```python
spiral[~(()>())]                                    # -1: Last char
spiral[~(('a'<'b'))]                                # -2
spiral[~(('a'<'b')+('a'<'b'))]                      # -3
spiral[~(('a'<'b')+('a'<'b')+('a'<'b'))]            # -4
```

### Allowed Characters
```
( ) [ ] < > ~ a-z + ] / * '
```

### Testing Locally
```bash
python solution.py
```

Output: `csawctf{g@l@xy_0bserv3r$}`

## Challenge Rating

**Difficulty:** Medium  
**Category:** Misc (Python Jail)  
**Skills Required:**
- Python operator knowledge
- Understanding of type coercion
- Creative problem-solving
- Bitwise operations

## Notes

The challenge is clever because:
1. It blocks the obvious approach (positive indexing)
2. It removes the colon (can't use slicing syntax)
3. It uses a cipher (adds complexity)
4. But it leaves just enough primitives to solve it!

The solution requires understanding that:
- Negative indexing still works
- We can build any negative number using `~` and arithmetic
- Booleans can be used as integers
