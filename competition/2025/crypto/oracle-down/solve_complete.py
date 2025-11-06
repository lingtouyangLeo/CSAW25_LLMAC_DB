#!/usr/bin/env python3
"""
Oracle Down - Complete Padding Oracle Attack Solution

This script implements a padding oracle attack against the vulnerable
decrypt_cbc function that checks padding before HMAC verification.

The vulnerability allows us to decrypt the ciphertext without knowing
the encryption key by leveraging timing side-channels.
"""

import socket
import time
from typing import Tuple, Optional

def connect_to_oracle(host='localhost', port=22333) -> socket.socket:
    """Connect to the oracle service"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    # Receive welcome message
    welcome = s.recv(4096)
    print(f"Connected: {welcome.decode()}")
    return s

def query_oracle(s: socket.socket, ciphertext_hex: str) -> Tuple[bool, float]:
    """
    Send ciphertext to oracle and measure response time
    
    Returns:
        (is_valid_padding, response_time)
    """
    start = time.time()
    s.sendall(ciphertext_hex.encode() + b'\n')
    response = s.recv(4096)
    elapsed = time.time() - start
    
    # If padding is invalid, response is immediate: "Invalid communication."
    # If padding is valid, there's a delay (250-1000ms) before HMAC check fails
    response_text = response.decode()
    
    # Valid padding will have delay, invalid padding will be immediate
    is_valid = elapsed > 0.2  # Threshold for timing attack
    
    return is_valid, elapsed

def padding_oracle_attack(original_ciphertext_hex: str, host='localhost', port=22333) -> bytes:
    """
    Perform padding oracle attack to decrypt the ciphertext
    
    Ciphertext structure (96 bytes):
    - 32 bytes: HMAC-SHA256
    - 16 bytes: IV
    - 48 bytes: Ciphertext (3 blocks of 16 bytes each)
    """
    print("=== Starting Padding Oracle Attack ===\n")
    
    original_ct = bytes.fromhex(original_ciphertext_hex)
    
    mac = original_ct[:32]
    iv = original_ct[32:48]
    ciphertext = original_ct[48:]
    
    print(f"MAC:  {mac.hex()}")
    print(f"IV:   {iv.hex()}")
    print(f"CT:   {ciphertext.hex()}")
    print(f"CT blocks: {len(ciphertext) // 16}\n")
    
    # Split ciphertext into blocks
    ct_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    
    # For CBC: C[0] = IV, and we decrypt each block
    decrypted_blocks = []
    
    # Connect to oracle once for all queries
    s = connect_to_oracle(host, port)
    
    try:
        for block_idx in range(len(ct_blocks)):
            print(f"\n=== Decrypting Block {block_idx + 1}/{len(ct_blocks)} ===")
            
            if block_idx == 0:
                prev_block = iv
            else:
                prev_block = ct_blocks[block_idx - 1]
            
            curr_block = ct_blocks[block_idx]
            
            # Intermediate values (what comes out of AES decryption)
            intermediate = bytearray(16)
            
            # Decrypt byte by byte from right to left
            for pad_val in range(1, 17):
                byte_pos = 16 - pad_val
                print(f"  Byte {byte_pos}: ", end='', flush=True)
                
                # Prepare modified IV/previous block
                modified_prev = bytearray(prev_block)
                
                # Set already-known bytes to produce target padding
                for k in range(byte_pos + 1, 16):
                    modified_prev[k] = intermediate[k] ^ pad_val
                
                # Brute force current byte
                found = False
                for guess in range(256):
                    modified_prev[byte_pos] = guess
                    
                    # Build test ciphertext: MAC + modified_prev + curr_block + padding blocks
                    # We need to maintain 96 bytes total for length check
                    if block_idx == 0:
                        # Testing first block: MAC + modified_IV + first_block + second_block
                        test_ct = mac + bytes(modified_prev) + curr_block + ct_blocks[1]
                    elif block_idx == len(ct_blocks) - 1:
                        # Testing last block: MAC + prev_blocks + modified_prev + curr_block
                        test_ct = mac + b''.join(ct_blocks[:block_idx-1] if block_idx > 1 else [iv])
                        test_ct += bytes(modified_prev) + curr_block
                    else:
                        # Testing middle block
                        test_ct = mac + b''.join(ct_blocks[:block_idx]) + bytes(modified_prev) + curr_block
                    
                    # Pad to 96 bytes if needed
                    if len(test_ct) < 96:
                        test_ct += b'\x00' * (96 - len(test_ct))
                    
                    test_ct_hex = test_ct[:96].hex()
                    
                    try:
                        is_valid, elapsed = query_oracle(s, test_ct_hex)
                        
                        if is_valid:
                            # Found valid padding!
                            intermediate[byte_pos] = guess ^ pad_val
                            plaintext_byte = intermediate[byte_pos] ^ prev_block[byte_pos]
                            print(f"0x{plaintext_byte:02x} ('{chr(plaintext_byte) if 32 <= plaintext_byte < 127 else '?'}')")
                            found = True
                            break
                    except Exception as e:
                        continue
                    
                    # Small delay to avoid overwhelming the server
                    time.sleep(0.01)
                
                if not found:
                    print("FAILED - trying alternative approach")
                    # Sometimes we get false positives, try handling edge cases
                    intermediate[byte_pos] = 0
            
            # Recover plaintext from intermediate values
            plaintext_block = bytes(intermediate[i] ^ prev_block[i] for i in range(16))
            decrypted_blocks.append(plaintext_block)
            print(f"  Block decrypted: {plaintext_block.hex()}")
            print(f"  ASCII: {plaintext_block}")
    
    finally:
        s.close()
    
    # Combine all blocks and remove padding
    plaintext = b''.join(decrypted_blocks)
    
    # Remove PKCS7 padding
    padding_len = plaintext[-1]
    if padding_len <= 16 and all(b == padding_len for b in plaintext[-padding_len:]):
        plaintext = plaintext[:-padding_len]
    
    return plaintext

def main():
    ciphertext_hex = "4ee48433a6a3ad49b5783b530ab792d46c7af620b96832f372cd87d94dc3c7b2f8a4febf4d43f07a23a43f205e23e163683ddf73cbe3203bf62dd67c1537610e2bebd55f6976a6da99abb421d32738ce87518670fce29f1f9adccbe022fd7dc9"
    
    print("Oracle Down - Padding Oracle Attack")
    print("=" * 50)
    print(f"\nTarget ciphertext:\n{ciphertext_hex}\n")
    
    try:
        plaintext = padding_oracle_attack(ciphertext_hex)
        
        print("\n" + "=" * 50)
        print("=== DECRYPTED PLAINTEXT ===")
        print("=" * 50)
        print(f"Hex: {plaintext.hex()}")
        print(f"ASCII: {plaintext.decode('utf-8', errors='replace')}")
        
        if b'csawctf{' in plaintext or b'flag{' in plaintext:
            print("\n🚩 FLAG FOUND! 🚩")
        
    except ConnectionRefusedError:
        print("\n❌ ERROR: Could not connect to oracle service")
        print("\nPlease start the service first:")
        print("  docker-compose up")
        print("\nOr if running on a different host/port, update the script.")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
