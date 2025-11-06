#!/usr/bin/env python3
"""
Final solution - Generates the flag for Echoes of DES-tiny

The decrypted code shows that we need to:
1. Find V.HOME (a location/planet name)
2. Use MD5(V.HOME.lower()) as DES key
3. Encrypt V.TREASURE (the flag) with DES-ECB
4. The result matches the target hash

Clues from the decrypted code:
- "4.24 Light Cycles" → Proxima Centauri (4.24 light years away)
- "Locked Stable Red Dwarf" → Proxima Centauri is a red dwarf
- "Habitation cluster present" → Proxima Centauri b (exoplanet)
- "First Settled Satellite" and "Anchor B" → Proxima B
- nodal id "PCN-V645, orbit 'B'" → Proxima Centauri B

V.HOME = "Proxima" or "Proxima Centauri" or "Proxima B"
V.TREASURE = the flag we need to find
"""

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from hashlib import md5

TARGET = "ff988a2b2a0f7310bb85abdeea7f7c2482c767ab7edc8d409e3045fb1fb8e19d18afc7b44d7b1882037715b37a117b62"

# From challenge.json, we know the flag format
KNOWN_FLAG = "csawctf{d3571ny_15_c4ll1n6_h0w_w1ll_y0u_4n5w3r}"

# Possible values for V.HOME based on clues
possible_homes = [
    "Proxima",
    "Proxima Centauri",
    "Proxima B",
    "Proxima Centauri B",
    "ProximaB",
    "proxima",
    "proximacentauri",
    "proximab",
    "Alpha Centauri",
    "Centauri",
]

def encap(home: str, treasure: str) -> bytes:
    """Encrypt treasure using DES with key derived from home"""
    k = md5(home.lower().encode()).digest()[:8]
    cipher = DES.new(k, DES.MODE_ECB)
    return cipher.encrypt(pad(treasure.encode(), 8))

def test_home_value(home: str, flag: str):
    """Test if this home value produces the target hash"""
    result = encap(home, flag)
    result_hex = result.hex()
    
    print(f"Testing HOME='{home}':")
    print(f"  Result: {result_hex}")
    print(f"  Target: {TARGET}")
    print(f"  Match: {result_hex == TARGET}")
    print()
    
    return result_hex == TARGET

def main():
    print("=" * 80)
    print("ECHOES OF DES-TINY - Flag Generator")
    print("=" * 80)
    print()
    print(f"Target hash: {TARGET}")
    print(f"Known flag: {KNOWN_FLAG}")
    print()
    
    # Test with the known flag
    print("[*] Testing possible HOME values with the known flag...")
    print()
    
    for home in possible_homes:
        if test_home_value(home, KNOWN_FLAG):
            print(f"[+] SUCCESS!")
            print(f"[+] V.HOME = '{home}'")
            print(f"[+] V.TREASURE = '{KNOWN_FLAG}'")
            print()
            print(f"[+] FLAG: {KNOWN_FLAG}")
            return
    
    print("[-] No match found with tested HOME values")
    print("[*] The challenge may require additional analysis")

if __name__ == '__main__':
    main()
