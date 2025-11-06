# Galaxy - CSAW CTF 2025

A Python jail challenge involving a custom string class, substitution cipher, and restricted evaluation.

## Quick Summary

**Challenge Type:** Python Jail / Sandbox Escape  
**Key Concept:** Negative indexing bypass  
**Flag:** `csawctf{g@l@xy_0bserv3r$}`

## Files

- `main.py` - The challenge code (also in `dist/` and `infra/`)
- `solution.py` - Complete working solution with local and remote solving
- `SOLUTION.md` - Detailed writeup explaining the approach
- `extract_flag.py` - Demonstration of flag extraction technique
- `test_payloads.py` - Testing various payload approaches
- `find_true.py` - Finding ways to construct True/False values

## Quick Solve

```bash
python solution.py
```

## The Challenge

You're given access to a Python eval() with:
- Only allowed characters: `([<~abcdefghijklmnopqrstuvwxyz>+]/*')`
- Input goes through a random substitution cipher
- Only the `spiral` object (containing flag) is accessible
- The object blocks positive indexing but allows negative indexing

## The Solution

Use negative indexing to extract the flag character by character:

```python
spiral[~(()>())]                    # Gets last char: '}'
spiral[~(('a'<'b'))]                # Gets -2 index: '$'
spiral[~(('a'<'b')+('a'<'b'))]      # Gets -3 index: 'r'
# ... continue extracting and reverse the result
```

**Key Insights:**
- `~0 = -1`, `~1 = -2`, `~2 = -3`, etc. (bitwise NOT)
- `()>() = False = 0`
- `('a'<'b') = True = 1`
- Add True values to build larger numbers

## Running the Challenge

### Local Testing
```bash
# Just run the solution
python solution.py

# Or test the challenge server locally
python dist/main.py
```

### Docker (if infrastructure is set up)
```bash
docker-compose up
# Then connect to localhost:21009
```

## See Also

- `SOLUTION.md` - Full technical writeup
- `challenge.json` - Challenge metadata
