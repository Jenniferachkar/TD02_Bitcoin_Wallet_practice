from bip39 import generate_entropy, entropy_to_mnemonic, mnemonic_to_seed
from bip32 import generate_master_key, private_to_public, derive_child_key
from colorama import Fore, Style, init
init(autoreset=True)

def main():
    print(Fore.CYAN + "=== BITCOIN WALLET TOOL ===")
    print("1. Generate new wallet")
    print("2. Import existing mnemonic")
    choice = input("Choose option (1 or 2): ")

    if choice == "1":
        entropy = generate_entropy()
        mnemonic = entropy_to_mnemonic(entropy)
        print(Fore.GREEN + "\nMnemonic:\n" + mnemonic)
    else:
        mnemonic = input("Enter mnemonic phrase:\n")

    seed = mnemonic_to_seed(mnemonic)
    master_priv, master_chain = generate_master_key(seed)
    master_pub = private_to_public(master_priv)

    print(Fore.YELLOW + "\n--- MASTER KEYS ---")
    print("Master Private Key:", master_priv.hex())
    print("Master Chain Code:", master_chain.hex())
    print("Master Public Key:", master_pub.hex())

    # Derive one child for demonstration
    child_priv, child_chain = derive_child_key(master_priv, master_chain, 0)
    print(Fore.MAGENTA + "\n--- CHILD KEY (m/0) ---")
    print("Child Private Key:", child_priv.hex())
    print("Child Chain Code:", child_chain.hex())

if __name__ == "__main__":
    main()
