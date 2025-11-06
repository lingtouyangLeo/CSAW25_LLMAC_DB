#!/usr/bin/env python3
"""
Quick test with most common passwords
"""

from Crypto.Cipher import DES
import hashlib

# Top 1000 most common passwords
TOP_PASSWORDS = [
    'password', '123456', '123456789', 'guest', 'qwerty', '12345678', '111111',
    '12345', 'col123456', '123123', '1234567', '1234', '1234567890', '000000',
    '555555', '666666', '123321', '654321', '7777777', '123', '333333', 
    'password1', 'test', 'dragon', 'letmein', '1111', 'master', '666666',
    'monkey', '654321', 'joshua', 'superman', 'master', 'jennifer', 'michael',
    'password123', 'charlie', 'aa123456', 'bailey', 'hannah', 'shadow', 'monkey',
    'ashley', 'princess', 'batman', '123456789', 'football', 'welcome', 'zxcvbnm',
    'sunshine', 'abc123', 'princess', 'nicole', 'starwars', 'qwerty123',
    'iloveyou', 'admin', 'welcome', 'monkey', 'login', 'abc123', 'master',
    'hello', 'freedom', 'whatever', 'qazwsx', 'trustno1', 'solo', 'pepper',
    'starwars', 'summer', 'ashley', 'welcome', 'zxcvbnm', 'qwertyuiop', 
    'access', 'shadow', 'tinkle', 'welcome123', 'lovely', 'Password', 'password',
]

def try_decrypt(password, ciphertext):
    """Try decrypting with password"""
    try:
        # Method 1: MD5 hash
        key = hashlib.md5(password.encode()).digest()[:8]
        cipher = DES.new(key, DES.MODE_ECB)
        ct_len = (len(ciphertext) // 8) * 8
        plaintext = cipher.decrypt(ciphertext[:ct_len])
        
        if (plaintext.startswith(b'#!') or plaintext.startswith(b'import') or 
            plaintext.startswith(b'from') or b'csawctf' in plaintext.lower()[:300] or
            b'def ' in plaintext[:300] or b'print(' in plaintext[:300]):
            return plaintext, 'MD5'
        
        # Method 2: Direct padding
        if len(password) <= 8:
            key = password.ljust(8, '\x00').encode()
        else:
            key = password[:8].encode()
        
        cipher = DES.new(key, DES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext[:ct_len])
        
        if (plaintext.startswith(b'#!') or plaintext.startswith(b'import') or 
            plaintext.startswith(b'from') or b'csawctf' in plaintext.lower()[:300] or
            b'def ' in plaintext[:300] or b'print(' in plaintext[:300]):
            return plaintext, 'Direct'
            
    except:
        pass
    
    return None, None

def main():
    with open('dist/scrambled', 'rb') as f:
        ct = f.read()
    
    print(f"[*] Testing {len(set(TOP_PASSWORDS))} common passwords...")
    
    for pw in set(TOP_PASSWORDS):
        plaintext, method = try_decrypt(pw, ct)
        if plaintext:
            print(f"\n[+] FOUND! Password: '{pw}' (method: {method})")
            print(f"[+] Preview:\n{plaintext[:500]}")
            with open('decrypted_code.py', 'wb') as f:
                f.write(plaintext)
            print("\n[+] Saved to decrypted_code.py")
            return
    
    print("[-] Not found in common passwords")

if __name__ == '__main__':
    main()
