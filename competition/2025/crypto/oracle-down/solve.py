#!/usr/bin/env python3
"""
Oracle Down - Padding Oracle Attack Solution

The vulnerability:
- decrypt_cbc checks padding BEFORE verifying HMAC
- If padding is wrong, it raises exception immediately
- If padding is correct, it delays with obfuscate_hmac() then checks HMAC
- We can use timing to determine correct padding

However, since we don't have network access to the oracle service,
we need to analyze the structure and potentially brute-force or use
known-plaintext attacks.

Structure:
- 32 bytes: HMAC
- 16 bytes: IV
- 48 bytes: Ciphertext (3 blocks)
Total: 96 bytes (192 hex chars)
"""

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad
import time

def padding_oracle_attack_local(ciphertext_hex):
    """
    Since we have the source code, we can try to understand the encryption
    and potentially reverse-engineer it or use other attacks.
    """
    ciphertext = bytes.fromhex(ciphertext_hex)
    
    print(f"Total ciphertext length: {len(ciphertext)} bytes ({len(ciphertext_hex)} hex chars)")
    print(f"Expected: 96 bytes (32 HMAC + 16 IV + 48 CT)")
    
    mac = ciphertext[:32]
    iv = ciphertext[32:48]
    ct = ciphertext[48:]
    
    print(f"\nMAC: {mac.hex()}")
    print(f"IV:  {iv.hex()}")
    print(f"CT:  {ct.hex()}")
    print(f"CT blocks: {len(ct) // 16}")
    
    return mac, iv, ct

def cbc_decrypt_with_iv_manipulation(iv, ct_block, key):
    """
    CBC decryption: plaintext = IV XOR AES_decrypt(ciphertext_block)
    We can manipulate IV to control the plaintext
    """
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_block = cipher.decrypt(ct_block)
    plaintext = bytes(a ^ b for a, b in zip(iv, decrypted_block))
    return plaintext, decrypted_block

def brute_force_key_space():
    """
    If we need to brute force, we can try common patterns
    But this is likely not the intended solution
    """
    pass

def analyze_padding_oracle():
    """
    Main analysis function
    """
    ciphertext_hex = "4ee48433a6a3ad49b5783b530ab792d46c7af620b96832f372cd87d94dc3c7b2f8a4febf4d43f07a23a43f205e23e163683ddf73cbe3203bf62dd67c1537610e2bebd55f6976a6da99abb421d32738ce87518670fce29f1f9adccbe022fd7dc9"
    
    mac, iv, ct = padding_oracle_attack_local(ciphertext_hex)
    
    print("\n=== Padding Oracle Attack Analysis ===")
    print("\nThe vulnerability allows us to:")
    print("1. Modify the ciphertext byte by byte")
    print("2. Use timing to detect valid padding")
    print("3. Recover plaintext without the key")
    
    print("\n=== Attack Strategy ===")
    print("Since we don't have network access to the oracle,")
    print("we need to either:")
    print("1. Start the Docker service and connect to it")
    print("2. Analyze the encryption scheme for weaknesses")
    print("3. Use known-plaintext attacks if we know the format")
    
    # The flag format is likely: csawctf{...}
    print("\n=== Known Plaintext ===")
    print("Flag format: csawctf{...}")
    print("This gives us known plaintext to work with!")
    
    return mac, iv, ct

def padding_oracle_decrypt_block(oracle_func, ct_blocks, block_idx):
    """
    Decrypt a single block using padding oracle attack
    
    For CBC mode:
    P[i] = D(C[i]) XOR C[i-1]
    
    Where C[0] is the IV
    """
    if block_idx == 0:
        prev_block = bytearray(16)  # Will be the IV
    else:
        prev_block = bytearray(ct_blocks[block_idx - 1])
    
    curr_block = ct_blocks[block_idx]
    decrypted = bytearray(16)
    
    # Decrypt byte by byte from right to left
    for pad_val in range(1, 17):
        print(f"  Decrypting byte {16 - pad_val + 1}/16 (padding value: {pad_val})")
        
        # Prepare the modified previous block
        modified = bytearray(prev_block)
        
        # Set already-known bytes to produce the target padding
        for k in range(1, pad_val):
            modified[16 - k] = prev_block[16 - k] ^ decrypted[16 - k] ^ pad_val
        
        # Brute force the current byte
        found = False
        for guess in range(256):
            modified[16 - pad_val] = guess
            
            # Test with oracle
            if oracle_func(bytes(modified) + curr_block):
                # Valid padding found
                decrypted[16 - pad_val] = guess ^ prev_block[16 - pad_val] ^ pad_val
                found = True
                print(f"    Found: {decrypted[16 - pad_val]:02x}")
                break
        
        if not found:
            print(f"    ERROR: Could not find valid byte!")
            return None
    
    return bytes(decrypted)

if __name__ == "__main__":
    print("=== Oracle Down CTF Challenge ===\n")
    analyze_padding_oracle()
    
    print("\n=== Next Steps ===")
    print("To complete this attack, we need to:")
    print("1. Start the Docker service: docker-compose up")
    print("2. Connect to the oracle service")
    print("3. Send crafted ciphertexts and measure response times")
    print("4. Use timing differences to decrypt the message")
    
    print("\nAlternatively, if we can access the oracle programmatically,")
    print("we can automate the padding oracle attack.")
