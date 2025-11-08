import os, hashlib, binascii
from pathlib import Path

WORDLIST_PATH = Path(__file__).parent / "wordlist.txt"

def load_wordlist():
    with open(WORDLIST_PATH, "r", encoding="utf-8") as f:
        return [w.strip() for w in f.readlines()]

def generate_entropy(bits=128):
    return os.urandom(bits // 8)

def entropy_to_mnemonic(entropy):
    wordlist = load_wordlist()
    checksum = hashlib.sha256(entropy).hexdigest()
    checksum_bits = bin(int(checksum, 16))[2:].zfill(256)[:len(entropy) * 8 // 32]
    entropy_bits = bin(int.from_bytes(entropy, "big"))[2:].zfill(len(entropy) * 8)
    bits = entropy_bits + checksum_bits

    words = [wordlist[int(bits[i:i+11], 2)] for i in range(0, len(bits), 11)]
    return " ".join(words)

def mnemonic_to_seed(mnemonic, passphrase=""):
    salt = "mnemonic" + passphrase
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode("utf-8"), salt.encode("utf-8"), 2048)
