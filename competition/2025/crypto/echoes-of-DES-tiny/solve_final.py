#!/usr/bin/env python3
"""
Final comprehensive solve script for Echoes of DES-tiny

This script will:
1. Try to brute-force the DES key with comprehensive wordlists
2. Once decrypted, execute the code to get the flag
3. Generate the response that matches the target hash
"""

from Crypto.Cipher import DES
import hashlib
import sys
import os

TARGET_HASH = "ff988a2b2a0f7310bb85abdeea7f7c2482c767ab7edc8d409e3045fb1fb8e19d18afc7b44d7b1882037715b37a117b62"

def try_decrypt(password, ciphertext, verbose=False):
    """Try multiple decryption methods"""
    methods = []
    
    # Method 1: MD5 hash of password
    try:
        key = hashlib.md5(password.encode() if isinstance(password, str) else password).digest()[:8]
        methods.append(('MD5', key))
    except:
        pass
    
    # Method 2: SHA256 hash
    try:
        key = hashlib.sha256(password.encode() if isinstance(password, str) else password).digest()[:8]
        methods.append(('SHA256', key))
    except:
        pass
    
    # Method 3: Direct password (padded/truncated to 8 bytes)
    try:
        if isinstance(password, str):
            pw_bytes = password.encode()
        else:
            pw_bytes = password
        
        if len(pw_bytes) < 8:
            key = pw_bytes + b'\x00' * (8 - len(pw_bytes))
        elif len(pw_bytes) > 8:
            key = pw_bytes[:8]
        else:
            key = pw_bytes
        methods.append(('Direct', key))
    except:
        pass
    
    # Try each method
    for method_name, key in methods:
        try:
            cipher = DES.new(key, DES.MODE_ECB)
            ct_len = (len(ciphertext) // 8) * 8
            plaintext = cipher.decrypt(ciphertext[:ct_len])
            
            # Check for Python code indicators
            indicators = [
                plaintext.startswith(b'#!/'),
                plaintext.startswith(b'import '),
                plaintext.startswith(b'from '),
                b'csawctf{' in plaintext.lower(),
                b'def ' in plaintext[:500],
                b'print(' in plaintext[:500],
                b'hashlib' in plaintext[:500],
            ]
            
            if any(indicators):
                if verbose:
                    print(f"[DEBUG] Match with method {method_name}")
                return plaintext, f"{password} ({method_name})"
                
        except Exception as e:
            if verbose:
                print(f"[DEBUG] Error with {method_name}: {e}")
    
    return None, None

def generate_comprehensive_wordlist():
    """Generate comprehensive wordlist based on all hints"""
    
    base_words = [
        # Direct hints
        'twitter', 'twttr', 'dorsey', 'jack', 'jackdorsey', '@jack',
        'cookbook', 'electronic', 'anarchist', 'des', 'destiny', 'probe',
        'space', 'alien', 'archive',
        
        # Jack Dorsey companies/projects
        'odeo', 'square', 'bluesky', 'block',
        
        # Crypto/Bitcoin (Dorsey connection)
        'bitcoin', 'btc', 'satoshi', 'crypto', 'cypherpunk',
        
        # DES related
        'deskey', 'despass', 'tinydes', 'tiny', 'tripledes', '3des',
        'destinydes', 'desbook',
        
        # Electronic cookbook references
        'anarchistcookbook', 'electroniccookbook', 'cryptonomicon',
        'jollyroger', 'cookbook',
        
        # Common CTF passwords
        'flag', 'csawctf', 'csaw', 'ctf', 'challenge',
        
        # Common passwords
        'password', 'admin', 'test', 'user', 'guest', 'root',
        '123456', '12345678', 'qwerty', 'abc123',
    ]
    
    # Generate variations
    wordlist = set()
    for word in base_words:
        wordlist.add(word)
        wordlist.add(word.upper())
        wordlist.add(word.capitalize())
        wordlist.add(word.lower())
        
        # With numbers
        for i in range(10):
            wordlist.add(word + str(i))
            wordlist.add(str(i) + word)
        
        wordlist.add(word + '123')
        wordlist.add('123' + word)
        wordlist.add(word + '!')
        wordlist.add(word + '@')
        wordlist.add(word + '#')
    
    # Combinations
    combos = [
        'jack_dorsey', 'jack-dorsey', 'jackdorsey',
        'electronic_cookbook', 'electronic-cookbook',
        'anarchist_cookbook', 'anarchist-cookbook',
        'des-tiny', 'des_tiny', 'destiny',
        'twttr123', 'twitter123',
    ]
    wordlist.update(combos)
    
    return sorted(list(wordlist))

def main():
    print("=" * 70)
    print("ECHOES OF DES-TINY - COMPREHENSIVE SOLVER")
    print("=" * 70)
    print(f"\n[*] Target hash: {TARGET_HASH}")
    
    # Load ciphertext
    scrambled_path = 'dist/scrambled' if os.path.exists('dist/scrambled') else 'scrambled'
    if not os.path.exists(scrambled_path):
        print(f"[-] Cannot find {scrambled_path}")
        return
    
    with open(scrambled_path, 'rb') as f:
        ciphertext = f.read()
    
    print(f"[*] Loaded ciphertext: {len(ciphertext)} bytes")
    print(f"[*] First 32 bytes (hex): {ciphertext[:32].hex()}")
    
    # Generate wordlist
    wordlist = generate_comprehensive_wordlist()
    print(f"\n[*] Generated {len(wordlist)} password candidates")
    print(f"[*] Sample: {wordlist[:15]}")
    
    # If external wordlist provided, use it
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        print(f"\n[*] Loading external wordlist: {sys.argv[1]}")
        try:
            with open(sys.argv[1], 'r', encoding='latin-1', errors='ignore') as f:
                external = [line.strip() for line in f if line.strip()]
            wordlist = external + wordlist
            print(f"[*] Total passwords to try: {len(wordlist)}")
        except Exception as e:
            print(f"[-] Error loading wordlist: {e}")
    
    # Brute force
    print("\n[*] Starting brute force attack...\n")
    
    for i, password in enumerate(wordlist):
        if i % 1000 == 0 and i > 0:
            print(f"[*] Progress: {i}/{len(wordlist)} passwords tested...")
        
        plaintext, method = try_decrypt(password, ciphertext)
        
        if plaintext:
            print(f"\n{'='*70}")
            print(f"[+] SUCCESS! Password found: {method}")
            print(f"{'='*70}\n")
            
            # Save decrypted code
            output_file = 'decrypted_code.py'
            with open(output_file, 'wb') as f:
                f.write(plaintext)
            
            print(f"[+] Decrypted code saved to: {output_file}")
            print(f"\n[*] Preview of decrypted content:")
            print("-" * 70)
            preview = plaintext[:800].decode('utf-8', errors='ignore')
            print(preview)
            if len(plaintext) > 800:
                print("\n... (truncated) ...")
            print("-" * 70)
            
            # Try to execute to get the flag
            print(f"\n[*] Attempting to execute decrypted code...")
            try:
                exec(plaintext, {'__name__': '__main__'})
            except Exception as e:
                print(f"[!] Execution error: {e}")
                print(f"[*] You may need to run the decrypted code manually")
            
            return True
    
    print(f"\n[-] Password not found after trying {len(wordlist)} candidates")
    print(f"[!] Try providing rockyou.txt as an argument:")
    print(f"    python solve_final.py /path/to/rockyou.txt")
    
    return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
