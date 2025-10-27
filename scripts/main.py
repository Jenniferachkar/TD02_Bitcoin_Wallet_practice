from bip39 import generate_entropy, entropy_to_mnemonic
from bip32 import master_key_from_seed
import hashlib, binascii, os

def derive_from_mnemonic(mnemonic, wordlist):
    seed = hashlib.pbkdf2_hmac("sha512", " ".join(mnemonic).encode(), b"mnemonic", 2048)
    master_priv, chaincode = master_key_from_seed(seed)
    print("\n=== STEP 3: MASTER KEYS (BIP-32) ===")
    print("Master Private Key:", binascii.hexlify(master_priv).decode())
    print("Chain Code:", binascii.hexlify(chaincode).decode())

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(script_dir, "bip39_english.txt")

    with open(wordlist_path, "r") as f:
        wordlist = [w.strip() for w in f.readlines()]

    print("=== BITCOIN WALLET TOOL ===")
    print("1. Generate new wallet")
    print("2. Import existing mnemonic")
    choice = input("Choose option (1 or 2): ")

    if choice == "1":
        entropy = generate_entropy()
        print("\n=== STEP 1: RANDOM ENTROPY ===")
        print("Entropy (hex):", entropy.hex())

        mnemonic = entropy_to_mnemonic(entropy, wordlist)
        print("\n=== STEP 2: MNEMONIC ===")
        print("Mnemonic:", " ".join(mnemonic))
        derive_from_mnemonic(mnemonic, wordlist)

    elif choice == "2":
        mnemonic_input = input("\nEnter your 12 mnemonic words separated by spaces:\n> ").strip().split()
        derive_from_mnemonic(mnemonic_input, wordlist)

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
