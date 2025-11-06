#!/usr/bin/env python3
"""
Enhanced solve script for Echoes of DES-tiny
"""

from Crypto.Cipher import DES
import hashlib
import itertools

# The target hash
TARGET_HASH = "ff988a2b2a0f7310bb85abdeea7f7c2482c767ab7edc8d409e3045fb1fb8e19d18afc7b44d7b1882037715b37a117b62"

def try_password(ciphertext, password, verbose=False):
    """Try decrypting with various key derivation methods"""
    try:
        # Method 1: Direct password (padded to 8 bytes)
        if len(password) <= 8:
            key = password.ljust(8, '\x00').encode() if isinstance(password, str) else password.ljust(8, b'\x00')
        else:
            key = password[:8].encode() if isinstance(password, str) else password[:8]
        
        cipher = DES.new(key, DES.MODE_ECB)
        # Handle non-multiple of 8
        ct_len = (len(ciphertext) // 8) * 8
        plaintext = cipher.decrypt(ciphertext[:ct_len])
        
        if verbose:
            print(f"  Method 1 (direct pad): {plaintext[:50]}")
        
        # Check for valid Python
        if (plaintext.startswith(b'#!') or plaintext.startswith(b'import') or 
            plaintext.startswith(b'from') or b'csawctf' in plaintext.lower()[:200] or
            b'def ' in plaintext[:200] or b'print(' in plaintext[:200]):
            return plaintext, f"{password} (direct)"
        
        # Method 2: MD5 hash of password
        key = hashlib.md5(password.encode() if isinstance(password, str) else password).digest()[:8]
        cipher = DES.new(key, DES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext[:ct_len])
        
        if verbose:
            print(f"  Method 2 (MD5): {plaintext[:50]}")
        
        if (plaintext.startswith(b'#!') or plaintext.startswith(b'import') or 
            plaintext.startswith(b'from') or b'csawctf' in plaintext.lower()[:200] or
            b'def ' in plaintext[:200] or b'print(' in plaintext[:200]):
            return plaintext, f"{password} (MD5)"
        
        # Method 3: SHA256 hash of password
        key = hashlib.sha256(password.encode() if isinstance(password, str) else password).digest()[:8]
        cipher = DES.new(key, DES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext[:ct_len])
        
        if verbose:
            print(f"  Method 3 (SHA256): {plaintext[:50]}")
        
        if (plaintext.startswith(b'#!') or plaintext.startswith(b'import') or 
            plaintext.startswith(b'from') or b'csawctf' in plaintext.lower()[:200] or
            b'def ' in plaintext[:200] or b'print(' in plaintext[:200]):
            return plaintext, f"{password} (SHA256)"
            
    except Exception as e:
        if verbose:
            print(f"  Error: {e}")
    
    return None, None

def generate_wordlist():
    """Generate targeted wordlist based on hints"""
    base_words = [
        # Jack Dorsey related
        'twttr', 'twitter', 'dorsey', 'jack', 'jackdorsey', 'odeo', 'square', 
        'bluesky', '@jack',
        # Crypto/Bitcoin (Dorsey is a Bitcoin advocate)
        'bitcoin', 'btc', 'satoshi', 'crypto',
        # Challenge hints
        'cookbook', 'electronic', 'anarchist', 'des', 'destiny', 'probe', 
        'space', 'alien', 'archive',
        # DES/Crypto references
        'desbook', 'cryptonomicon', 'cypherpunk',
        # Common passwords
        'password', 'admin', 'test', 'user',
    ]
    
    # Generate variations
    words = []
    for w in base_words:
        words.append(w)
        words.append(w.upper())
        words.append(w.capitalize())
        words.append(w + '123')
        words.append('123' + w)
        words.append(w + '!')
        words.append(w + '1')
    
    # Add some combinations
    combos = [
        'jack_dorsey',
        'jack-dorsey', 
        'electronic_cookbook',
        'electronic-cookbook',
        'anarchist_cookbook',
        'anarchist-cookbook',
        'des-tiny',
        'destinydes',
    ]
    words.extend(combos)
    
    return list(set(words))  # Remove duplicates

def main():
    print("[*] Echoes of DES-tiny - Enhanced Solver")
    print(f"[*] Target: {TARGET_HASH}\n")
    
    # Load ciphertext
    with open('dist/scrambled', 'rb') as f:
        ciphertext = f.read()
    
    print(f"[*] Ciphertext: {len(ciphertext)} bytes")
    print(f"[*] First 32 bytes (hex): {ciphertext[:32].hex()}")
    print()
    
    # Generate wordlist
    wordlist = generate_wordlist()
    print(f"[*] Generated {len(wordlist)} password candidates")
    print(f"[*] Sample passwords: {wordlist[:10]}")
    print()
    
    # Try each password
    print("[*] Attempting decryption...")
    for i, password in enumerate(wordlist):
        if i % 50 == 0 and i > 0:
            print(f"[*] Tried {i} passwords...")
        
        plaintext, method = try_password(ciphertext, password, verbose=False)
        if plaintext:
            print(f"\n[+] SUCCESS! Password: {method}")
            print(f"[+] Decrypted content preview:")
            print(plaintext[:500].decode('utf-8', errors='ignore'))
            print("\n...")
            
            # Save full decrypted content
            with open('decrypted_code.py', 'wb') as f:
                f.write(plaintext)
            print(f"\n[+] Full content saved to decrypted_code.py")
            
            return plaintext
    
    print("\n[-] Password not found in wordlist")
    print("[!] You may need to provide a larger wordlist like rockyou.txt")
    return None

if __name__ == '__main__':
    result = main()
