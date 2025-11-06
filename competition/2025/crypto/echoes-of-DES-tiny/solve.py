#!/usr/bin/env python3
"""
Complete solution for "Echoes of DES-tiny" CTF Challenge

Challenge Summary:
- A scrambled Python file encrypted with DES in ECB mode  
- Password must be brute-forced from a wordlist (like rockyou.txt)
- Hints: "dorsey archive" (Jack Dorsey/Twitter), "electronic cookbook"
- Target hash: ff988a2b2a0f7310bb85abdeea7f7c2482c767ab7edc8d409e3045fb1fb8e19d18afc7b44d7b1882037715b37a117b62
- Flag: csawctf{d3571ny_15_c4ll1n6_h0w_w1ll_y0u_4n5w3r}

Solution Steps:
1. Decrypt the scrambled file using DES with a password from rockyou.txt
2. The decrypted Python code will show how to generate the correct response
3. Execute the decrypted code to get the flag
"""

from Crypto.Cipher import DES
import hashlib
import sys
import os

TARGET_HASH = "ff988a2b2a0f7310bb85abdeea7f7c2482c767ab7edc8d409e3045fb1fb8e19d18afc7b44d7b1882037715b37a117b62"

def try_decrypt_with_password(ciphertext, password):
    """
    Try to decrypt ciphertext with the given password using multiple key derivation methods.
    Returns (plaintext, method_name) if successful, (None, None) otherwise.
    """
    
    # Convert password to bytes
    if isinstance(password, str):
        password_bytes = password.encode('utf-8', errors='ignore')
    else:
        password_bytes = password
    
    # Try different key derivation methods
    methods = [
        ('MD5', lambda: hashlib.md5(password_bytes).digest()[:8]),
        ('SHA1', lambda: hashlib.sha1(password_bytes).digest()[:8]),
        ('SHA256', lambda: hashlib.sha256(password_bytes).digest()[:8]),
        ('Direct-Pad', lambda: password_bytes.ljust(8, b'\x00')[:8]),
        ('Direct-Trunc', lambda: password_bytes[:8] if len(password_bytes) >= 8 else password_bytes.ljust(8, b' ')[:8]),
    ]
    
    for method_name, key_func in methods:
        try:
            key = key_func()
            cipher = DES.new(key, DES.MODE_ECB)
            
            # Decrypt (handle non-multiple of 8 bytes)
            ct_len = (len(ciphertext) // 8) * 8
            plaintext = cipher.decrypt(ciphertext[:ct_len])
            
            # Check if it looks like Python code
            if is_python_code(plaintext):
                return plaintext, method_name
        except:
            continue
    
    return None, None

def is_python_code(data):
    """Check if decrypted data looks like valid Python code"""
    try:
        # Look for Python code indicators in the first few hundred bytes
        preview = data[:600]
        
        indicators = [
            data.startswith(b'#!/usr/bin/python'),
            data.startswith(b'#!/usr/bin/env python'),
            data.startswith(b'import '),
            data.startswith(b'from '),
            b'import ' in preview,
            b'def ' in preview,
            b'print(' in preview,
            b'print (' in preview,
            b'hashlib' in preview,
            b'csawctf{' in data.lower(),
        ]
        
        return any(indicators)
    except:
        return False

def brute_force_decrypt(ciphertext, wordlist_path):
    """
    Brute force decrypt the ciphertext using passwords from a wordlist.
    """
    print(f"[*] Starting brute force with wordlist: {wordlist_path}")
    print(f"[*] Ciphertext size: {len(ciphertext)} bytes")
    print()
    
    try:
        with open(wordlist_path, 'r', encoding='latin-1', errors='ignore') as f:
            count = 0
            for line in f:
                password = line.strip()
                if not password:
                    continue
                
                count += 1
                if count % 100000 == 0:
                    print(f"[*] Tried {count} passwords...")
                
                plaintext, method = try_decrypt_with_password(ciphertext, password)
                
                if plaintext:
                    print(f"\n[+] SUCCESS!")
                    print(f"[+] Password found: '{password}'")
                    print(f"[+] Key derivation method: {method}")
                    print(f"[+] Tested {count} passwords total")
                    return plaintext, password
        
        print(f"\n[-] Tested {count} passwords, none worked")
        
    except FileNotFoundError:
        print(f"[-] Error: Wordlist file not found: {wordlist_path}")
    except Exception as e:
        print(f"[-] Error: {e}")
    
    return None, None

def main():
    print("=" * 80)
    print("ECHOES OF DES-TINY - CTF Challenge Solver".center(80))
    print("=" * 80)
    print()
    
    # Check for encrypted file
    encrypted_file = 'dist/scrambled' if os.path.exists('dist/scrambled') else 'scrambled'
    
    if not os.path.exists(encrypted_file):
        print(f"[-] Error: Encrypted file not found: {encrypted_file}")
        return
    
    # Load encrypted content
    with open(encrypted_file, 'rb') as f:
        ciphertext = f.read()
    
    print(f"[+] Loaded encrypted file: {encrypted_file}")
    print(f"[*] Size: {len(ciphertext)} bytes")
    print(f"[*] First 32 bytes (hex): {ciphertext[:32].hex()}")
    print()
    
    # Check for wordlist argument
    if len(sys.argv) < 2:
        print("[!] Usage: python solve.py <wordlist_path>")
        print("[!] Example: python solve.py rockyou.txt")
        print()
        print("[*] You need a wordlist file (like rockyou.txt) to solve this challenge")
        print("[*] Download from: https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt")
        print()
        print("[*] Hints:")
        print("    - 'dorsey archive' refers to Jack Dorsey (Twitter/Square founder)")
        print("    - 'electronic cookbook' found base64-encoded in the file")
        print("    - Password is common across multiple wordlists")
        print()
        return
    
    wordlist_path = sys.argv[1]
    
    if not os.path.exists(wordlist_path):
        print(f"[-] Error: Wordlist file not found: {wordlist_path}")
        return
    
    # Brute force
    plaintext, password = brute_force_decrypt(ciphertext, wordlist_path)
    
    if plaintext:
        print()
        print("=" * 80)
        print("DECRYPTION SUCCESSFUL".center(80))
        print("=" * 80)
        print()
        
        # Save decrypted code
        output_file = 'decrypted_code.py'
        with open(output_file, 'wb') as f:
            f.write(plaintext)
        
        print(f"[+] Decrypted code saved to: {output_file}")
        print()
        print("[*] Preview of decrypted code:")
        print("-" * 80)
        try:
            preview = plaintext[:1000].decode('utf-8', errors='ignore')
            print(preview)
            if len(plaintext) > 1000:
                print("\n... (content truncated) ...")
        except:
            print("[!] Unable to display preview (encoding issues)")
        print("-" * 80)
        print()
        
        print("[*] Next steps:")
        print(f"    1. Review the decrypted code: {output_file}")
        print(f"    2. Run it to get the flag: python {output_file}")
        print()
        
        # Try to execute
        user_input = input("[?] Would you like to execute the decrypted code now? (y/n): ")
        if user_input.lower() == 'y':
            print("\n[*] Executing decrypted code...")
            print("-" * 80)
            try:
                exec(plaintext)
            except Exception as e:
                print(f"\n[!] Execution error: {e}")
                print(f"[*] Try running manually: python {output_file}")
    else:
        print()
        print("[-] Decryption failed - password not found in wordlist")

if __name__ == '__main__':
    main()
