from bip39 import generate_entropy, entropy_to_mnemonic
from bip32 import master_key_from_seed
import hashlib, binascii

def main():
    with open("bip39_english.txt") as f:
        wordlist = [w.strip() for w in f.readlines()]

    entropy = generate_entropy()
    print("\n=== STEP 1: RANDOM ENTROPY ===")
    print("Entropy (bytes):", entropy)
    print("Entropy (hex):", entropy.hex())

    mnemonic = entropy_to_mnemonic(entropy, wordlist)
    print("\n=== STEP 2: MNEMONIC ===")
    print("Mnemonic:", " ".join(mnemonic))

    seed = hashlib.pbkdf2_hmac("sha512", " ".join(mnemonic).encode(), b"mnemonic", 2048)
    master_priv, chaincode = master_key_from_seed(seed)
    print("\n=== STEP 3: MASTER KEYS (BIP-32) ===")
    print("Master Private Key:", binascii.hexlify(master_priv).decode())
    print("Chain Code:", binascii.hexlify(chaincode).decode())

if __name__ == "__main__":
    main()
