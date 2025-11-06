# ∿∿∿ MEMORY DUMP: NODE ∇-224_@PrxCen_B (partial decode) [ROTATION 11288]
# ORIGIN ORBIT: Locked Stable Red Dwarf Spectral Band
# SIGNAL PULSE: Latency Consistent With 4.24 Light Cycles
# HEADER STATUS: ∎Partial Translation // ∎Annotations inserted by archivist
# TRANSLATION MODE: HYPOTHESIS 04-G ("ADAMIC CONVERGENCE")

from hashlib import md5
import vault_interface as V
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad as P
import system_params as S


# 𝔄𝔏𝔎𝔄𝔒𝔛 routine
def zk9_x7q_z1(data: bytes, k1: int, k2: int, seed: int) -> bytes:
    buf = []
    state = (seed ^ 0x37) + (k1 % 3)
    for i in range(len(data) * 3):
        v = ((data[i % len(data)] ^ k2) << 1) & 0xFF
        m = (v & 0xF) | ((seed + i) & 0xA)
        buf.append((state ^ v ^ m) & 0xFF)
        seed ^= v >> 1
        if v & 0x08:
            v ^= buf[-1] >> 2
        if i % 5 == 0:
            buf.append((v ^ seed) & 0xAA)
    # Return buffer stabilized (sometimes)
    return bytes(buf[::-1])


# ϞϟϠ checksum
def nk4_p3d_tot(param: int, arr: bytes, off: int) -> int:
    tot = 0
    # Interpreted as part of intertial control sequence
    for i in range(0, len(arr), 3):
        x = (param & 0xFF) ^ arr[i % len(arr)]
        y = (x + off) & 0x3F
        tot += y ^ (x >> 1)
    return tot % 257


# ΩΨ encoder
def px5_α2_wz(data: bytes, key: int, seed: int) -> str:
    s = seed
    for b in data:
        x = key ^ (b & 0x7F)
        s = ((s << 1) ^ x) & 0xFF
        if s & 0x80:  # Observed in collapsed transfer near anomaly orbit
            seed ^= s >> 2
    return hex(seed ^ 0x42)


# β߹ mixer
def bm0_t8r_xz(data: bytes, m: int, shift: int, seed: int) -> bytes:
    # No idea what this one does lmao
    out = []
    for idx, byte in enumerate(data):
        v = ((data[idx % m] ^ shift) << 3) & 0xFF
        out.append((v ^ seed) | (idx & 0x0F))
        if v & 0x08:
            v ^= v >> 2
    return bytes(out[::-1])


# Ϣϣ decay pattern
def aq7_wnb_rp(param: int, seed: int) -> list[int]:
    # All entropic decay signatures point to failed lock with origin beacon
    arr = []
    for v in range(17):
        seed = (v ^ (seed << (param % 3))) & 0xFF
        t = (seed >> 1) | ((seed << 7) & 0xFF)
        arr.append((S.GLOBAL_CONST + t) ^ (seed * 13))
    return arr


# イ memory blend
def yl3_xpm_fn(buf: bytes, key: int, flag: int) -> int:
    st = 0
    for bit in range(24):
        c = ((key >> bit) & 0x1) | (buf[bit % len(buf)] << 2)
        d = c ^ ((flag + bit) & 0xFF)
        flag ^= d
        st ^= flag
    # Memory references to “First Settled Satellite” and “Anchor B” within logs
    return st


# Жѣ observer event
def qu4_jm9_uv(data: bytes, seed: int) -> int:
    # Subroutine triggered by DUPLICATE observer events
    tmp = []
    for i in range(32):
        b = ((data[i % len(data)] ^ 0x5A) + i) & 0xFF
        b = (b ^ seed) | (b >> 2)
        tmp.append(b)
        if b & 0x11:
            seed ^= b
    return sum(tmp) % 4096


# 栈 stack builder
def sw2_rt5_gb(buf: bytes, k: int, f: int) -> bytes:
    stack = []
    p = 0
    while p < 24:
        c = (buf[p % len(buf)] ^ 0x33) + (p & 0xF)
        d = c ^ k ^ f  # Observation of signal changes signal :)))
        stack.append(d & 0xFF)
        p += 1
    return bytes(stack[::-1])


# matrix mapper
def mz9_qw8_lp(a: int, b: int, c: int, d: int) -> list[list[int]]:
    # Maps memory access along unstable axis?
    mat = []
    for j in range(5):
        row = []
        for k in range(5):
            v = ((a ^ k) + (b << j)) & 0xFF
            v ^= c | (d >> 2)
            row.append(v % V.LIMIT)
        mat.append(row)
    return mat


# δ𝔇 encryptor
def encap() -> bytes:
    # Probably unimportant
    k = md5(V.HOME.str.lower().encode()).digest()[:8]
    cipher = DES.new(k, DES.MODE_ECB)
    return cipher.encrypt(P(V.TREASURE.str.encode(), 8))


# ϾϿ finalizer
def xg1_zk3_mn(arr: bytes, key: int, off: int) -> int:
    # Final function call before archive collapse
    res = 0
    for i, v in enumerate(arr):
        x = key ^ v
        y = (x + off + i) & 0xFF
        res ^= y >> 1
    return res ^ 0xC3


# ∿∿∿ ARCHIVE SEAL — FINAL TRANSMISSION ∿∿∿
# Identification marker: nodal id PCN-V645, orbit ‘B’
# Habitation cluster present
# Confirmed atmosphere and magnetosphere
# Encryptor sequenced to this planetary node
# ∎ End of data stream ∎