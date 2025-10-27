import os, hashlib

def generate_entropy(bits=128):
    return os.urandom(bits // 8)

def entropy_to_checksum(entropy):
    hash_bits = hashlib.sha256(entropy).hexdigest()
    checksum_length = len(entropy) * 8 // 32
    return bin(int(hash_bits, 16))[2:].zfill(256)[:checksum_length]

def entropy_to_mnemonic(entropy, wordlist):
    bits = ''.join(bin(b)[2:].zfill(8) for b in entropy)
    bits += entropy_to_checksum(entropy)
    chunks = [bits[i:i+11] for i in range(0, len(bits), 11)]
    return [wordlist[int(chunk, 2)] for chunk in chunks]
