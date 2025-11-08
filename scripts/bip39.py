from __future__ import annotations

import os
import hashlib
import unicodedata
from pathlib import Path
from typing import List, Tuple

# ---- Wordlist ---------------------------------------------------------------

_WORDLIST_FILE = Path(__file__).with_name("bip39_english.txt")


def load_wordlist() -> List[str]:
    """Load the English BIP-39 wordlist (2048 words)."""
    with open(_WORDLIST_FILE, "r", encoding="utf-8") as f:
        words = [w.strip() for w in f.readlines()]
    if len(words) != 2048:
        raise ValueError("Wordlist must contain exactly 2048 words.")
    return words


# ---- Entropy & checksum -----------------------------------------------------

def generate_entropy(bits: int = 128) -> bytes:
    """
    Generate secure random entropy of size 128/192/256 bits.
    """
    if bits not in (128, 192, 256):
        raise ValueError("Entropy must be 128, 192, or 256 bits.")
    return os.urandom(bits // 8)


def _sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _bits_from_bytes(b: bytes) -> str:
    return bin(int.from_bytes(b, "big"))[2:].zfill(len(b) * 8)


def _bytes_from_bits(bitstr: str) -> bytes:
    # length must be a multiple of 8
    if len(bitstr) % 8 != 0:
        raise ValueError("bit string length must be a multiple of 8")
    return int(bitstr, 2).to_bytes(len(bitstr) // 8, "big")


def _checksum_bits(entropy: bytes) -> str:
    """
    CS length = ENT/32 bits (BIP-39).
    """
    ent_len = len(entropy) * 8
    cs_len = ent_len // 32
    h = _sha256(entropy)
    return _bits_from_bytes(h)[:cs_len]


def split_into_11bit_groups(bitstr: str) -> List[int]:
    """
    Split a bit string into 11-bit integers (BIP-39 index groups).
    """
    if len(bitstr) % 11 != 0:
        raise ValueError("Total bit length must be a multiple of 11")
    return [int(bitstr[i : i + 11], 2) for i in range(0, len(bitstr), 11)]


# ---- Encode entropy -> mnemonic ---------------------------------------------

def entropy_to_mnemonic(entropy: bytes, wordlist: List[str] | None = None) -> str:
    """
    ENT + CS -> groups of 11 -> words.
    """
    if wordlist is None:
        wordlist = load_wordlist()

    ent_bits = _bits_from_bytes(entropy)
    cs_bits = _checksum_bits(entropy)
    full = ent_bits + cs_bits  # ENT || CS

    indices = split_into_11bit_groups(full)
    words = [wordlist[i] for i in indices]
    return " ".join(words)


# ---- Decode mnemonic -> entropy (with checksum validation) ------------------

def _normalize_str(s: str) -> str:
    # BIP-39 specifies NFKD normalization
    return unicodedata.normalize("NFKD", s)


def mnemonic_to_entropy(mnemonic: str, wordlist: List[str] | None = None) -> bytes:
    """
    Convert mnemonic -> entropy. Validates checksum. Raises ValueError if invalid.
    """
    if wordlist is None:
        wordlist = load_wordlist()

    words = _normalize_str(mnemonic).strip().split()
    if len(words) not in (12, 15, 18, 21, 24):
        raise ValueError("Mnemonic must have 12, 15, 18, 21, or 24 words.")

    # map words -> indices
    try:
        indices = [wordlist.index(w) for w in words]
    except ValueError as e:
        raise ValueError(f"Word not in BIP-39 list: {e}") from None

    # join indices to bit string
    bits = "".join(bin(i)[2:].zfill(11) for i in indices)

    # split into ENT + CS
    total_len = len(bits)
    ent_len = (total_len * 32) // 33  # because total = ENT + ENT/32 = ENT * 33/32
    cs_len = total_len - ent_len

    ent_bits = bits[:ent_len]
    cs_bits = bits[ent_len:]

    entropy = _bytes_from_bits(ent_bits)
    if _checksum_bits(entropy) != cs_bits:
        raise ValueError("Invalid mnemonic checksum.")
    return entropy


# ---- Mnemonic -> seed -------------------------------------------------------

def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:
    """
    PBKDF2-HMAC-SHA512 with 2048 iterations, salt = 'mnemonic' + passphrase (NFKD).
    Returns 64-byte seed.
    """
    m = _normalize_str(mnemonic)
    salt = "mnemonic" + _normalize_str(passphrase)
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), salt.encode("utf-8"), 2048)


# ---- Convenience helpers for CLI output -------------------------------------

def print_entropy_views(entropy: bytes) -> None:
    """
    Print the entropy in hex / bytes length / binary.
    """
    print("Entropy (hex):", entropy.hex())
    print("Entropy (bytes):", len(entropy))
    print("Entropy (bin):", _bits_from_bytes(entropy))


def print_11bit_groups(entropy: bytes) -> None:
    ent_bits = _bits_from_bytes(entropy)
    cs_bits = _checksum_bits(entropy)
    full = ent_bits + cs_bits
    groups = split_into_11bit_groups(full)
    print("Checksum bits:", cs_bits)
    print("Total bits (ENT+CS):", len(full))
    print("11-bit groups (indices):", groups)


# ---- Demo ----------------------------------------

def _demo() -> None:
    """
    Minimal interactive flow (kept here so main.py can import the pure functions).
    Covers the TD points:
      - generate secure integer (entropy)
      - show hex/bytes/bin and 11-bit groups
      - map to words (mnemonic)
      - allow import/validation of a mnemonic
      - derive seed (to verify on iancoleman.io/bip39)
    """
    wl = load_wordlist()

    print("=== BIP-39 DEMO ===")
    choice = input("1) Generate mnemonic  2) Import mnemonic  -> ").strip()

    if choice == "1":
        bits = input("Entropy size [128/192/256]: ").strip() or "128"
        entropy = generate_entropy(int(bits))
        print_entropy_views(entropy)
        print_11bit_groups(entropy)
        mnemonic = entropy_to_mnemonic(entropy, wl)
        print("\nMnemonic:\n", mnemonic)
    elif choice == "2":
        mnemonic = input("Enter mnemonic phrase:\n").strip()
        entropy = mnemonic_to_entropy(mnemonic, wl)
        print("\nMnemonic is VALID.")
        print_entropy_views(entropy)
        print_11bit_groups(entropy)
    else:
        print("Invalid choice.")
        return

    passphrase = input("\nOptional passphrase (press Enter for none): ").strip()
    seed = mnemonic_to_seed(mnemonic, passphrase)
    print("\nSeed (hex):", seed.hex())
    print("\nVerify on https://iancoleman.io/bip39/ (mnemonic + passphrase).")


if __name__ == "__main__":
    _demo()
