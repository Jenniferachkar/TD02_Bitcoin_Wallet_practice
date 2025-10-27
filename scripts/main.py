from bip39 import generate_entropy, entropy_to_mnemonic
from bip32 import master_key_from_seed, derive_child_key
import hashlib, binascii, os

def derive_from_mnemonic(mnemonic):
    seed = hashlib.pbkdf2_hmac("sha512", " ".join(mnemonic).encode(), b"mnemonic", 2048)
    master_priv, chaincode = master_key_from_seed(seed)
    print("\n=== STEP 3: MASTER KEYS (BIP-32) ===")
    print("Master Private Key:", binascii.hexlify(master_priv).decode())
    print("Chain Code:", binascii.hexlify(chaincode).decode())
    return master_priv, chaincode

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(script_dir, "bip39_english.txt")

    with open(wordlist_path, "r") as f:
        wordlist = [w.strip() for w in f.readlines()]

    print("=== BITCOIN WALLET TOOL ===")
    print("1. Generate new wallet")
    print("2. Import existing mnemonic")
    print("3. Derive child key at index N (hardened recommended)")
    print("4. Derive child key at index N, level M (repeat derivation M times)")
    choice = input("Choose option (1-4): ").strip()

    master_priv = None
    chaincode = None

    if choice == "1":
        entropy = generate_entropy()
        print("\n=== STEP 1: RANDOM ENTROPY ===")
        print("Entropy (hex):", entropy.hex())
        mnemonic = entropy_to_mnemonic(entropy, wordlist)
        print("\n=== STEP 2: MNEMONIC ===")
        print("Mnemonic:", " ".join(mnemonic))
        master_priv, chaincode = derive_from_mnemonic(mnemonic)

    elif choice == "2":
        mnemonic_input = input("\nEnter your 12 mnemonic words separated by spaces:\n> ").strip().split()
        master_priv, chaincode = derive_from_mnemonic(mnemonic_input)

    elif choice == "3":
        mnemonic_input = input("\nEnter your 12 mnemonic words (or press Enter to paste later):\n> ").strip()
        if mnemonic_input:
            mnemonic_input = mnemonic_input.split()
            master_priv, chaincode = derive_from_mnemonic(mnemonic_input)
        else:
            print("You must provide a mnemonic now (or use option 1/2 first).")
            return

        idx = int(input("Enter index (use >= 0x80000000 for hardened; hex OK with 0x...): ").strip(), 0)
        child_priv, child_chain = derive_child_key(master_priv, chaincode, idx)
        print("\n=== CHILD KEY ===")
        print("Index:", idx)
        print("Child Private Key:", binascii.hexlify(child_priv).decode())
        print("Child Chain Code:", binascii.hexlify(child_chain).decode())

    elif choice == "4":
        mnemonic_input = input("\nEnter your 12 mnemonic words (or press Enter to paste later):\n> ").strip()
        if mnemonic_input:
            mnemonic_input = mnemonic_input.split()
            master_priv, chaincode = derive_from_mnemonic(mnemonic_input)
        else:
            print("You must provide a mnemonic now (or use option 1/2 first).")
            return

        idx = int(input("Enter index (use >= 0x80000000 for hardened): ").strip(), 0)
        levels = int(input("Enter number of derivation levels M (e.g., 3): ").strip())
        cur_priv, cur_chain = master_priv, chaincode
        for level in range(levels):
            cur_priv, cur_chain = derive_child_key(cur_priv, cur_chain, idx)
            print(f"Level {level+1} done.")
        print("\n=== RESULT AFTER {} LEVELS ===".format(levels))
        print("Final Private Key:", binascii.hexlify(cur_priv).decode())
        print("Final Chain Code:", binascii.hexlify(cur_chain).decode())

    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
