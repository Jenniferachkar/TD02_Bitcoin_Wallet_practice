import os, argparse, hashlib

def generate_entropy(bits=128):
    return os.urandom(bits // 8)

def entropy_to_binary(entropy: bytes):
    return ''.join(f'{b:08b}' for b in entropy)

def load_wordlist(path="bip39_english.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [w.strip() for w in f.readlines()]

def main():
    parser = argparse.ArgumentParser(description="TD02 – BIP39 & BIP32 interactive CLI")
    parser.add_argument("--bits", type=int, default=128, help="Entropy length (128–256)")
    args = parser.parse_args()

    # STEP 1: entropy
    entropy = generate_entropy(args.bits)
    print("\n=== STEP 1: RANDOM ENTROPY ===")
    print("Entropy (bytes):", entropy)
    print("Entropy (hex):", entropy.hex())

    # STEP 2: binary
    binary = entropy_to_binary(entropy)
    print("Entropy (binary):", binary)

    # STEP 3: split into 11-bit chunks
    chunks = [binary[i:i+11] for i in range(0, len(binary), 11)]
    print("\n=== STEP 2: 11-bit CHUNKS ===")
    for i, c in enumerate(chunks):
        print(f"Chunk {i:02d}: {c}  ({int(c, 2)})")

    # STEP 4: convert to mnemonic words
    words = load_wordlist()
    mnemonic_words = [words[int(c, 2)] for c in chunks if len(c) == 11]
    mnemonic = ' '.join(mnemonic_words)
    print("\n=== STEP 3: MNEMONIC REPRESENTATION ===")
    print(mnemonic)

if __name__ == "__main__":
    main()
