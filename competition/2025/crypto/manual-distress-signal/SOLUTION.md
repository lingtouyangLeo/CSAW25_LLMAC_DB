# Manual-Distress-Signal CTF Solution

## Challenge Overview

**Category**: Crypto  
**Flag**: `csawctf{why_1s_th3_4cc3ss_k3y_1n_th3_d1str3ss_s1gn4l}`

## Vulnerability: CRIME/BREACH Attack

This challenge implements a vulnerable TLS-like protocol that combines:
1. User-controlled input
2. Server secret (the flag)
3. **Compression** before encryption
4. Observable ciphertext length

This is a textbook example of the **CRIME** (Compression Ratio Info-leak Made Easy) attack.

## How the Vulnerability Works

### Server-Side Process (from `app.js`):

```javascript
const combined = JSON.stringify({ secret: SERVER_SECRET, userData });
const compressed = zlib.deflateRawSync(Buffer.from(combined), { strategy: zlib.constants.Z_FIXED });
const cipher = crypto.createCipheriv("aes-128-cfb", key, iv);
let ciphertext = cipher.update(compressed);
```

The server:
1. Creates JSON: `{"secret":"csawctf{...}","userData":"<user_input>"}`
2. **Compresses** it with DEFLATE
3. Encrypts with AES (random key each time)
4. Returns the ciphertext

### The Side Channel:

**Compression algorithms (like DEFLATE) replace repeated sequences with references.**

When your input matches part of the secret:
- **Good Match**: `{"secret":"csawctf{abc","userData":"csawctf{abc"}` 
  - Compression finds repetition → Smaller output
  
- **Bad Match**: `{"secret":"csawctf{abc","userData":"csawctf{xyz"}`
  - No repetition → Larger output

**Even though the output is encrypted, the LENGTH reveals information!**

## Attack Strategy

### Byte-by-Byte Extraction:

1. **Start with known prefix**: `csawctf{` (standard CTF flag format)

2. **For each unknown position**:
   - Try all possible characters (a-z, 0-9, _, })
   - Send payload with candidate: `csawctf{a`, `csawctf{b`, etc.
   - Measure ciphertext length
   
3. **Select the character** that produces the **shortest ciphertext**
   - This indicates best compression
   - Best compression means most repetition
   - Most repetition means correct match!

4. **Repeat** until you hit the closing `}`

### Why Repetition in Payload?

The solution script uses `payload = candidate * 3` because:
- More occurrences of the correct prefix amplify the compression advantage
- Makes the length difference more noticeable
- Reduces false positives

## Solution Script

Run:
```bash
python solve.py
```

The script will:
1. Try each character position
2. Send requests with different candidates
3. Measure response lengths
4. Select the character with best compression
5. Build the flag character by character

## Historical Context

### Real-World Impact:

- **CRIME (2012)**: Demonstrated against HTTPS/TLS compression
  - Led to disabling TLS compression in browsers
  
- **BREACH (2013)**: Similar attack on HTTP compression
  - Affects gzip/deflate on HTTP responses

- **Modern Relevance**: While TLS compression is disabled, HTTP-level compression is still used, making BREACH-style attacks possible in certain scenarios

### Mitigations:

1. **Don't compress secrets and user input together** ✓
2. Disable compression (breaks efficiency)
3. Add random padding (mitigates but doesn't eliminate)
4. Use encrypt-then-compress (wrong order in this challenge)
5. Separate secrets from user-controlled data

## Why This Challenge Name?

"Manual-Distress-Signal" is a clever reference to:
- **Manual**: You need to manually extract bytes (or automate it)
- **Distress**: The vulnerability (compression) is under distress/attack
- **Signal**: The side-channel signal (length) leaks information

And the flag itself: `why_1s_th3_4cc3ss_k3y_1n_th3_d1str3ss_s1gn4l`  
**"Why is the access key in the distress signal?"** - Because compression creates a side channel!

## Key Takeaways

1. **Never compress secrets with user-controlled data**
2. **Encryption doesn't hide everything** - metadata like length can leak information
3. **Side channels are subtle** - even "secure" encryption can be broken by observing peripheral information
4. **Defense in depth** - multiple layers needed, not just encryption

## References

- CRIME: https://en.wikipedia.org/wiki/CRIME
- BREACH: https://breachattack.com/
- Original CRIME paper: https://docs.google.com/presentation/d/11eBmGiHbYcHR9gL5nDyZChu_-lCa2GizeuOfaLU2HOU/
