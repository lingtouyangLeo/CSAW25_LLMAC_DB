# Manual-Distress-Signal CTF - Complete Solution Guide

## Quick Start

### Step 1: Start the Server

Open a **new terminal** and run:
```powershell
cd "c:\Users\leo\Desktop\CSAW25_LLMAC_DB\competition\2025\crypto\manual-distress-signal\infra"
node test_server.js
```

You should see:
```
✓ Server listening on http://0.0.0.0:21022
✓ Test at: http://localhost:21022/
```

**Keep this terminal open!** The server needs to run while you execute the attack.

### Step 2: Run the Solver

Open a **second terminal** and run:
```powershell
cd "c:\Users\leo\Desktop\CSAW25_LLMAC_DB\competition\2025\crypto\manual-distress-signal"
python solve_improved.py
```

The script will automatically extract the flag byte-by-byte!

---

## Understanding the Vulnerability

### What's Happening in the Code?

Looking at `infra/app.js`, the server does:

```javascript
// 1. Combines your input with the secret flag
const combined = JSON.stringify({ secret: SERVER_SECRET, userData });

// 2. COMPRESSES the combined data (THE VULNERABILITY!)
const compressed = zlib.deflateRawSync(Buffer.from(combined), { strategy: zlib.constants.Z_FIXED });

// 3. Encrypts with AES
const cipher = crypto.createCipheriv("aes-128-cfb", key, iv);
let ciphertext = cipher.update(compressed);

// 4. Returns the ciphertext (length is observable!)
res.json({ ciphertext: tlsSimulated.toString("base64") });
```

### The CRIME Attack

**CRIME** = **C**ompression **R**atio **I**nfo-leak **M**ade **E**asy

#### Why Compression Creates a Side Channel:

When you send: `{"secret":"csawctf{abc123","userData":"csawctf{abc123"}`

The DEFLATE compression algorithm detects the repetition (`csawctf{abc123` appears twice) and replaces the second occurrence with a back-reference pointer, making the compressed data **smaller**.

#### The Attack Flow:

1. **Try character 'w'**: 
   - Payload: `csawctf{w` × 5
   - JSON: `{"secret":"csawctf{why_1s...","userData":"csawctf{wcsawctf{wcsawctf{w..."}`
   - Compression finds "csawctf{w" appears multiple times → **Good compression** → **Shorter output**

2. **Try character 'x'**:
   - Payload: `csawctf{x` × 5  
   - JSON: `{"secret":"csawctf{why_1s...","userData":"csawctf{xcsawctf{xcsawctf{x..."}`
   - No matching pattern with secret → **Poor compression** → **Longer output**

3. **Select the winner**: Character 'w' produces shortest ciphertext → It's correct!

4. **Repeat**: Now try `csawctf{wh`, `csawctf{wi`, `csawctf{wj`, etc.

### Mathematical Principle

Given:
- Secret: `S = "csawctf{why_...}"`
- User input: `U`
- Combined: `C = {"secret": S, "userData": U}`

Compression function: `Compress(C)` → output length depends on repetition

**Key insight**: 
```
len(Compress({"secret": S, "userData": S_prefix})) < len(Compress({"secret": S, "userData": random}))
```

Even though the output is encrypted, **length is not hidden**!

---

## Expected Output

When you run `solve_improved.py`, you'll see:

```
============================================================
Manual-Distress-Signal CTF Solver
CRIME/BREACH Attack on TLS Compression
============================================================

[*] Testing connection to server...
[+] Server is responding! Test payload length: 78
[+] Starting CRIME attack...
[+] Known prefix: csawctf{

[*] Iteration 1 - Current: csawctf{
[+] Best match: 'w' (length: 95)
[*] Top 5 candidates: [('w', 95), ('x', 96), ('y', 96), ('z', 96), ('0', 96)]

[*] Iteration 2 - Current: csawctf{w
[+] Best match: 'h' (length: 96)
[*] Top 5 candidates: [('h', 96), ('i', 97), ('j', 97), ...]

[*] Iteration 3 - Current: csawctf{wh
[+] Best match: 'y' (length: 97)
...
(continues until complete)

[+] Extracted flag: csawctf{why_1s_th3_4cc3ss_k3y_1n_th3_d1str3ss_s1gn4l}

============================================================
FLAG: csawctf{why_1s_th3_4cc3ss_k3y_1n_th3_d1str3ss_s1gn4l}
============================================================
```

---

## The Flag Meaning

**FLAG**: `csawctf{why_1s_th3_4cc3ss_k3y_1n_th3_d1str3ss_s1gn4l}`

Translation: **"Why is the access key in the distress signal?"**

This is a clever reference to the vulnerability:
- **Access key** = The secret flag
- **Distress signal** = The compressed+encrypted transmission
- **Why is it in?** = Because compression creates a side channel that leaks the secret!

The challenge name "Manual-Distress-Signal" also references:
- **Manual** = You manually extract bytes (though automated)
- **Distress** = The system under attack
- **Signal** = The side-channel signal (length) that leaks information

---

## Real-World Impact

### Historical Attacks:

**CRIME (2012)**:
- Demonstrated by Juliano Rizzo and Thai Duong
- Attacked HTTPS sessions using TLS compression
- Could steal session cookies from encrypted HTTPS traffic
- **Impact**: Led to disabling TLS compression in all major browsers

**BREACH (2013)**:
- Similar attack on HTTP-level compression (gzip/deflate)
- Affects applications even with TLS compression disabled
- Can extract CSRF tokens, session IDs, and secrets
- **Still relevant today** for misconfigured applications

### Modern Mitigations:

1. ✅ **Never compress secrets and user input together**
2. ✅ Disable compression (trade-off: less efficient)
3. ⚠️ Add random padding (partial mitigation)
4. ✅ Separate secrets from user-controlled data
5. ✅ Use length-hiding padding schemes

---

## Files in This Challenge

- `infra/app.js` - Original vulnerable server
- `infra/test_server.js` - Server with console output (easier to test)
- `solve.py` - Basic solver
- `solve_improved.py` - Enhanced solver with better output
- `start_server.bat` - Batch file to start server
- `SOLUTION.md` - Detailed writeup
- `HOW_TO_SOLVE.md` - This file!

---

## Troubleshooting

### Server won't start:
```powershell
cd "c:\Users\leo\Desktop\CSAW25_LLMAC_DB\competition\2025\crypto\manual-distress-signal\infra"
npm install
node test_server.js
```

### Connection refused:
- Make sure the server is running (check terminal)
- Check if port 21022 is available
- Try restarting the server

### Solver not finding correct characters:
- The algorithm should work reliably
- Sometimes network noise can affect results
- The script uses repetition (×5) to amplify the signal

---

## Key Takeaways

1. **Encryption ≠ Complete Security**: Even with strong encryption, side channels can leak information
2. **Compression is dangerous**: Never compress secrets with user-controlled data
3. **Metadata matters**: Length, timing, and other metadata can reveal secrets
4. **Defense in depth**: Multiple security layers are necessary
5. **Real-world relevance**: This isn't just theoretical - CRIME/BREACH affected millions

---

## Further Reading

- [CRIME Attack Paper](https://docs.google.com/presentation/d/11eBmGiHbYcHR9gL5nDyZChu_-lCa2GizeuOfaLU2HOU/)
- [BREACH Attack](https://breachattack.com/)
- [Wikipedia: CRIME](https://en.wikipedia.org/wiki/CRIME)
- [OWASP: Compression Side-Channel Attacks](https://owasp.org/www-community/attacks/Compression_Ratio_Info-leak_Made_Easy)

---

**FLAG**: `csawctf{why_1s_th3_4cc3ss_k3y_1n_th3_d1str3ss_s1gn4l}`

🎯 **Challenge Solved!**
