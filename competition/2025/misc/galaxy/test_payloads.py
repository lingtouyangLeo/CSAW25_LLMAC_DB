#!/usr/bin/env python3
"""
Galaxy CTF - Testing different payload approaches
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

# Test flag
spiral = galaxy_str('csawctf{g@l@xy_0bserv3r$}')

# Allowed chars: ([<~abcdefghijklmnopqrstuvwxyz>+]/*')
allowed = '([<~abcdefghijklmnopqrstuvwxyz>+]/*\')'

def test_payload(payload_desc, payload):
    """Test a payload and see if it works"""
    print(f"\n[*] Testing: {payload_desc}")
    print(f"    Payload: {payload}")
    
    # Check if payload uses only allowed chars
    for char in payload:
        if char not in allowed:
            print(f"    [-] INVALID: Character '{char}' not allowed!")
            return False
    
    try:
        result = eval(payload, {"__builtins__": {}, "spiral": spiral})
        print(f"    [+] SUCCESS: {result}")
        return True
    except Exception as e:
        print(f"    [-] ERROR: {e}")
        return False

# Test various approaches
print("="*60)
print("Galaxy Challenge - Payload Testing")
print("="*60)

# Try to create numbers using allowed operations
test_payload("Empty tuple", "()")
test_payload("Empty list", "[]")
test_payload("List with empty list", "[[]]")
test_payload("Comparison result", "()>()<()>()")  # Will this give us a boolean?

# Try to use ~ on constructed values
test_payload("Bitwise NOT of comparison", "~(()>())")  # Can we ~ a bool?

# Try accessing with expressions
test_payload("Access with tilde", "spiral[~((()<())+(()<()))]")  # Trying to build -1

# Try string operations
test_payload("Empty string", "''")
test_payload("String multiply", "'a'*((()<())<(()<()))")

# Try different indexing attempts  
test_payload("Multiple operations", "(()>())*((()>())+(()>()))")

print("\n" + "="*60)
print("Analyzing what we can build:")
print("="*60)

# Let's see what expressions evaluate to
tests = [
    ("()>())", "(()<()) evaluates to"),
    ("()<()<()<()", "Chain of comparisons"),
    ("''<''", "String comparison"),
    ("[]<[]", "List comparison"),
    ("[]*['+']", "List operations"),
]

for expr, desc in tests:
    print(f"\n{desc}:")
    print(f"  Expression: {expr}")
    try:
        result = eval(expr)
        print(f"  Result: {result} (type: {type(result).__name__})")
    except Exception as e:
        print(f"  Error: {e}")
