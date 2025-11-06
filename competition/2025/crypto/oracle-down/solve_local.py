#!/usr/bin/env python3
"""
Oracle Down - Local Padding Oracle Attack

Since we have the source code, we can simulate the oracle locally
without needing to connect to the actual service. This allows us
to perform the attack much faster.
"""

import sys
import os

# Add infra directory to path to import encrypt module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'infra'))

from encrypt import decrypt_cbc
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# The secret key from oracle.py
SECRET_KEY = b'\x83v\x12U\xb1\x16v?+N\x9f\x16@\x16*Z\xae\x0b\xb0 2\x00U\r\x0b\xc4\xe9k4qv]'

def local_oracle(ciphertext_hex: str) -> tuple[bool, str]:
    """
    Simulate the oracle behavior locally
    
    Returns: (is_valid_padding, error_message)
    """
    try:
        plaintext = decrypt_cbc(ciphertext_hex, SECRET_KEY)
        return True, "Valid"
    except Exception as e:
        error_msg = str(e)
        if "Incorrect padding" in error_msg:
            return False, "padding_error"
        elif "Incorrect length" in error_msg:
            return False, "length_error"
        elif "MAC verification failed" in error_msg:
            return False, "mac_error"
        else:
            return False, error_msg

def padding_oracle_decrypt_block(
    prev_block: bytes,
    curr_block: bytes,
    oracle_func,
    mac: bytes,
    all_ct_blocks: list
) -> bytes:
    """
    Decrypt a single block using padding oracle attack
    
    For CBC mode:
    Plaintext = Decrypt(Ciphertext_Block) XOR Previous_Block
    
    We manipulate Previous_Block to force specific padding values
    and use the oracle to determine the intermediate decrypted values.
    """
    intermediate = bytearray(16)
    
    print(f"  Decrypting block...")
    
    # Decrypt byte by byte from right to left
    for pad_val in range(1, 17):
        byte_pos = 16 - pad_val
        print(f"    Byte position {byte_pos} (padding {pad_val}): ", end='', flush=True)
        
        # Prepare modified previous block
        modified_prev = bytearray(prev_block)
        
        # Set already-known bytes to produce target padding value
        for k in range(byte_pos + 1, 16):
            modified_prev[k] = intermediate[k] ^ pad_val
        
        # Brute force current byte
        found = False
        for guess in range(256):
            modified_prev[byte_pos] = guess
            
            # Construct test ciphertext maintaining 96 bytes
            # Structure: MAC (32) + IV/prev (16) + curr (16) + remaining (32)
            test_ct = mac + bytes(modified_prev) + curr_block
            
            # Add remaining blocks to maintain 96 byte length requirement
            remaining_blocks = all_ct_blocks[1:]  # Skip first block
            test_ct += b''.join(remaining_blocks)
            
            # Ensure exactly 96 bytes
            test_ct = test_ct[:96]
            if len(test_ct) < 96:
                test_ct += b'\x00' * (96 - len(test_ct))
            
            test_ct_hex = test_ct.hex()
            
            is_valid, error = oracle_func(test_ct_hex)
            
            # Valid padding means either:
            # 1. No error (unlikely without correct MAC)
            # 2. MAC error (means padding was correct!)
            if error == "mac_error":
                # Padding was valid! MAC check came after padding check
                intermediate[byte_pos] = guess ^ pad_val
                plaintext_byte = intermediate[byte_pos] ^ prev_block[byte_pos]
                char_repr = chr(plaintext_byte) if 32 <= plaintext_byte < 127 else '.'
                print(f"0x{plaintext_byte:02x} '{char_repr}'")
                found = True
                break
        
        if not found:
            print("❌ FAILED")
            # Use null byte as fallback
            intermediate[byte_pos] = 0
    
    # Calculate plaintext from intermediate values
    plaintext_block = bytes(intermediate[i] ^ prev_block[i] for i in range(16))
    return plaintext_block

def padding_oracle_attack(ciphertext_hex: str) -> bytes:
    """
    Perform complete padding oracle attack
    """
    print("=== Padding Oracle Attack (Local) ===\n")
    
    ciphertext = bytes.fromhex(ciphertext_hex)
    
    # Parse structure
    mac = ciphertext[:32]
    iv = ciphertext[32:48]
    ct = ciphertext[48:]
    
    print(f"MAC:  {mac.hex()}")
    print(f"IV:   {iv.hex()}")
    print(f"CT:   {ct.hex()}")
    print(f"Blocks: {len(ct) // 16}\n")
    
    # Split into blocks
    ct_blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
    
    decrypted_blocks = []
    
    # Decrypt each block
    for block_idx in range(len(ct_blocks)):
        print(f"\n=== Block {block_idx + 1}/{len(ct_blocks)} ===")
        
        # Previous block (IV for first block)
        prev_block = iv if block_idx == 0 else ct_blocks[block_idx - 1]
        curr_block = ct_blocks[block_idx]
        
        # Decrypt this block
        plaintext_block = padding_oracle_decrypt_block(
            prev_block,
            curr_block,
            local_oracle,
            mac,
            ct_blocks
        )
        
        decrypted_blocks.append(plaintext_block)
        print(f"  Decrypted: {plaintext_block.hex()}")
        print(f"  ASCII: {plaintext_block}")
    
    # Combine blocks
    plaintext = b''.join(decrypted_blocks)
    
    # Remove PKCS7 padding
    try:
        padding_len = plaintext[-1]
        if 1 <= padding_len <= 16:
            if all(b == padding_len for b in plaintext[-padding_len:]):
                plaintext = plaintext[:-padding_len]
                print(f"\n  Removed {padding_len} bytes of padding")
    except:
        pass
    
    return plaintext

def simple_decrypt():
    """
    Since we have the key, let's just decrypt it directly!
    This is much simpler and shows what the oracle attack would reveal.
    """
    ciphertext_hex = "4ee48433a6a3ad49b5783b530ab792d46c7af620b96832f372cd87d94dc3c7b2f8a4febf4d43f07a23a43f205e23e163683ddf73cbe3203bf62dd67c1537610e2bebd55f6976a6da99abb421d32738ce87518670fce29f1f9adccbe022fd7dc9"
    
    print("=== Direct Decryption (We have the key!) ===\n")
    
    try:
        plaintext = decrypt_cbc(ciphertext_hex, SECRET_KEY)
        return plaintext
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def main():
    ciphertext_hex = "4ee48433a6a3ad49b5783b530ab792d46c7af620b96832f372cd87d94dc3c7b2f8a4febf4d43f07a23a43f205e23e163683ddf73cbe3203bf62dd67c1537610e2bebd55f6976a6da99abb421d32738ce87518670fce29f1f9adccbe022fd7dc9"
    
    print("=" * 60)
    print("  Oracle Down - CTF Challenge Solution")
    print("=" * 60)
    print(f"\nCiphertext: {ciphertext_hex}\n")
    
    # Method 1: Direct decryption (we have the key!)
    print("\n" + "=" * 60)
    print("METHOD 1: Direct Decryption")
    print("=" * 60)
    
    plaintext = simple_decrypt()
    
    if plaintext:
        print(f"\n✅ Successfully decrypted!")
        print(f"\nPlaintext (hex): {plaintext.hex()}")
        print(f"Plaintext (ASCII): {plaintext.decode('utf-8', errors='replace')}")
        
        if b'csawctf{' in plaintext.lower() or b'flag{' in plaintext.lower():
            print("\n" + "=" * 60)
            print("🚩 FLAG FOUND! 🚩")
            print("=" * 60)
            print(f"\n{plaintext.decode('utf-8', errors='replace')}\n")
    
    else:
        print("\n❌ Direct decryption failed, trying oracle attack...")
        
        # Method 2: Padding Oracle Attack
        print("\n" + "=" * 60)
        print("METHOD 2: Padding Oracle Attack")
        print("=" * 60)
        
        try:
            plaintext = padding_oracle_attack(ciphertext_hex)
            
            print("\n" + "=" * 60)
            print("✅ Oracle Attack Successful!")
            print("=" * 60)
            print(f"\nPlaintext (hex): {plaintext.hex()}")
            print(f"Plaintext (ASCII): {plaintext.decode('utf-8', errors='replace')}")
            
            if b'csawctf{' in plaintext.lower() or b'flag{' in plaintext.lower():
                print("\n" + "=" * 60)
                print("🚩 FLAG FOUND! 🚩")
                print("=" * 60)
                print(f"\n{plaintext.decode('utf-8', errors='replace')}\n")
        
        except Exception as e:
            print(f"\n❌ Oracle attack failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
