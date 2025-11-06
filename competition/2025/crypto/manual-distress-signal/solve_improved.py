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
    
    max_iterations = 100  # Safety limit
    iteration = 0
    
    while not known.endswith("}") and iteration < max_iterations:
        iteration += 1
        print(f"\n[*] Iteration {iteration} - Current: {known}")
        
        # Try each possible character
        lengths = {}
        
        for char in charset:
            # Craft payload that will compress well if char is correct
            candidate = known + char
            
            # Create payload with repetition to amplify compression effect
            # The key insight: when candidate matches the secret, compression is better
            payload = candidate * 5  # Increased repetition for better signal
            
            length = get_ciphertext_length(payload)
            if length:
                lengths[char] = length
                #print(f"  {char}: {length}", end="\r")
        
        if not lengths:
            print("\n[-] Failed to get any responses")
            break
        
        # The character with shortest ciphertext is most likely correct
        sorted_chars = sorted(lengths.items(), key=lambda x: x[1])
        best_char = sorted_chars[0][0]
        best_length = sorted_chars[0][1]
        
        print(f"[+] Best match: '{best_char}' (length: {best_length})")
        
        # Show top 5 candidates for debugging
        print(f"[*] Top 5 candidates: {sorted_chars[:5]}")
        
        known += best_char
        
        # If we hit closing brace, we're done
        if best_char == "}":
            break
    
    print(f"\n[+] Extracted flag: {known}")
    return known

if __name__ == "__main__":
    print("="*60)
    print("Manual-Distress-Signal CTF Solver")
    print("CRIME/BREACH Attack on TLS Compression")
    print("="*60)
    
    # First, test the connection
    print("\n[*] Testing connection to server...")
    test_length = get_ciphertext_length("test")
    if test_length:
        print(f"[+] Server is responding! Test payload length: {test_length}")
    else:
        print("[-] Cannot connect to server. Make sure it's running!")
        print("[*] Start the server with: node infra/test_server.js")
        exit(1)
    
    flag = extract_flag()
    print(f"\n{'='*60}")
    print(f"FLAG: {flag}")
    print(f"{'='*60}")
