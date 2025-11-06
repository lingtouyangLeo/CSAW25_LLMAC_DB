#!/usr/bin/env python3
"""
CRIME/BREACH Attack Solution for Manual-Distress-Signal CTF

This exploits the compression side-channel in the TLS-like implementation.
When user input shares common prefixes with the secret, compression is more
efficient, resulting in shorter ciphertext.
"""

import requests
import base64
import string
from collections import defaultdict

# Target server (local or remote)
# For local testing: http://localhost:21022/send
# For remote: http://crypto.chal.csaw.io/send
URL = "http://localhost:21022/send"

def get_ciphertext_length(payload):
    """Send payload and get the ciphertext length."""
    try:
        response = requests.post(URL, json={"data": payload}, timeout=5)
        data = response.json()
        if "ciphertext" in data:
            ciphertext = base64.b64decode(data["ciphertext"])
            return len(ciphertext)
    except Exception as e:
        print(f"Error: {e}")
    return None

def extract_flag():
    """Extract the flag byte by byte using compression oracle."""
    
    # Known flag format
    known = "csawctf{"
    charset = string.ascii_lowercase + string.digits + "_}"
    
    print(f"[+] Starting CRIME attack...")
    print(f"[+] Known prefix: {known}")
    
    while not known.endswith("}"):
        print(f"\n[*] Current: {known}")
        
        # Try each possible character
        lengths = {}
        
        for char in charset:
            # Craft payload that will compress well if char is correct
            # We include the known prefix + candidate char multiple times
            # to maximize compression advantage
            candidate = known + char
            
            # Create payload with repetition to amplify compression effect
            payload = candidate * 3
            
            length = get_ciphertext_length(payload)
            if length:
                lengths[char] = length
                print(f"  {char}: {length}", end="\r")
        
        if not lengths:
            print("\n[-] Failed to get any responses")
            break
        
        # The character with shortest ciphertext is most likely correct
        best_char = min(lengths.keys(), key=lambda k: lengths[k])
        
        print(f"\n[+] Best match: {best_char} (length: {lengths[best_char]})")
        
        # Show top 3 candidates for debugging
        sorted_chars = sorted(lengths.items(), key=lambda x: x[1])
        print(f"[*] Top 3: {sorted_chars[:3]}")
        
        known += best_char
        
        # If we hit closing brace, we're done
        if best_char == "}":
            break
    
    print(f"\n[+] Extracted flag: {known}")
    return known

if __name__ == "__main__":
    # Note: For local testing, change URL to http://localhost:80/send
    # For competition: http://crypto.chal.csaw.io/send
    
    print("="*60)
    print("Manual-Distress-Signal CTF Solver")
    print("CRIME/BREACH Attack on TLS Compression")
    print("="*60)
    
    flag = extract_flag()
    print(f"\n{'='*60}")
    print(f"FLAG: {flag}")
    print(f"{'='*60}")
