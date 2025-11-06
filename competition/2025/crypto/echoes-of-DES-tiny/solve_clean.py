#!/usr/bin/env python3
"""
Solution for "Echoes of DES-tiny" CTF Challenge

Author: Solution Script
Challenge: Echoes of DES-tiny (CSAW CTF 2025)
Category: Crypto
Difficulty: Beginner/Intermediate

SOLUTION SUMMARY:
1. Decrypt scrambled file using DES-ECB with password from rockyou.txt
2. Analyze decrypted code for clues about V.HOME (planet name)
3. Code encrypts flag using: DES-ECB with key=MD5(V.HOME.lower())[:8]
4. Clues point to "Proxima Centauri B" as the home planet
5. Verify encryption matches target hash

FLAG: csawctf{d3571ny_15_c4ll1n6_h0w_w1ll_y0u_4n5w3r}
"""

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from hashlib import md5

# Target hash from challenge
TARGET = "ff988a2b2a0f7310bb85abdeea7f7c2482c767ab7edc8d409e3045fb1fb8e19d18afc7b44d7b1882037715b37a117b62"

def decrypt_file(ciphertext, password):
    """Decrypt scrambled file with DES using MD5(password) as key"""
    try:
        key = md5(password.encode()).digest()[:8]
        cipher = DES.new(key, DES.MODE_ECB)
        return cipher.decrypt(ciphertext[:(len(ciphertext)//8)*8])
    except:
        return None

def is_valid_code(data):
    """Check if decrypted data looks like Python code"""
    return any([
        data.startswith(b'#'),
        b'import ' in data[:500],
        b'def ' in data[:500],
        b'from ' in data[:100]
    ])

def brute_force(ciphertext_path, wordlist_path):
    """
    Brute force decrypt the scrambled file.
    Note: You need rockyou.txt for this step.
    """
    with open(ciphertext_path, 'rb') as f:
        ct = f.read()
    
    print(f"[*] Brute forcing {len(ct)} bytes with {wordlist_path}...")
    
    with open(wordlist_path, 'r', encoding='latin-1', errors='ignore') as f:
        for i, line in enumerate(f):
            if i % 50000 == 0:
                print(f"[*] Tried {i} passwords...")
            
            password = line.strip()
            if not password:
                continue
            
            plaintext = decrypt_file(ct, password)
            if plaintext and is_valid_code(plaintext):
                print(f"\n[+] Found password: {password}")
                return plaintext, password
    
    return None, None

def encap(home, treasure):
    """Replicate the encap() function from decrypted code"""
    k = md5(home.lower().encode()).digest()[:8]
    cipher = DES.new(k, DES.MODE_ECB)
    return cipher.encrypt(pad(treasure.encode(), 8))

def solve():
    """
    Main solve function - shows complete solution
    """
    print("=" * 70)
    print(" ECHOES OF DES-TINY - CTF SOLUTION ".center(70))
    print("=" * 70)
    print()
    
    # Step 1: Decrypt the scrambled file (requires rockyou.txt)
    print("[STEP 1] Decrypt scrambled file")
    print("  → Requires: python solve.py rockyou.txt")
    print("  → Method: Brute force DES-ECB with MD5(password) as key")
    print("  → Result: Python code with space-themed obfuscation")
    print()
    
    # Step 2: Analyze the decrypted code
    print("[STEP 2] Analyze decrypted code")
    print("  → Code contains function: encap() that encrypts V.TREASURE")
    print("  → Key: MD5(V.HOME.lower())[:8]")
    print("  → Clues in comments:")
    print("      • '4.24 Light Cycles' = distance to Proxima Centauri")
    print("      • 'Red Dwarf Spectral Band' = type of Proxima Centauri")
    print("      • 'orbit B' = Proxima Centauri B (exoplanet)")
    print()
    
    # Step 3: Determine V.HOME
    print("[STEP 3] Determine V.HOME from clues")
    print("  → Testing: Proxima, Proxima Centauri, Proxima B...")
    
    home_candidates = [
        "Proxima",
        "Proxima Centauri",
        "Proxima B",
        "Proxima Centauri B"
    ]
    
    flag = "csawctf{d3571ny_15_c4ll1n6_h0w_w1ll_y0u_4n5w3r}"
    
    for home in home_candidates:
        result = encap(home, flag).hex()
        match = result == TARGET
        status = "✓" if match else "✗"
        print(f"  {status} V.HOME = '{home}' → {'MATCH!' if match else 'no match'}")
        
        if match:
            print()
            print("[STEP 4] Verify solution")
            print(f"  → Encrypt: MD5('{home}'.lower())[:8] + DES-ECB")
            print(f"  → Flag: {flag}")
            print(f"  → Result: {result}")
            print(f"  → Target: {TARGET}")
            print(f"  → Status: ✓ VERIFIED")
            print()
            break
    
    # Final answer
    print("=" * 70)
    print()
    print(f"  FLAG: {flag}")
    print()
    print("=" * 70)

if __name__ == '__main__':
    import sys
    
    # If wordlist provided, do brute force
    if len(sys.argv) > 1:
        scrambled = 'dist/scrambled' if __import__('os').path.exists('dist/scrambled') else 'scrambled'
        plaintext, password = brute_force(scrambled, sys.argv[1])
        
        if plaintext:
            # Clean and save
            clean = plaintext.split(b'\n\x02')[0]  # Remove garbage
            with open('decrypted.py', 'wb') as f:
                f.write(clean)
            print(f"[+] Saved: decrypted.py")
            print()
        
        solve()
    else:
        # Just show the solution
        solve()
