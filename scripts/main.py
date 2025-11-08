# main.py
# Bitcoin Wallet Tool — combines BIP-39 (mnemonic) and BIP-32 (key derivation)
# Author: Jennifer El Achkar

from bip39 import (
    generate_entropy,
    entropy_to_mnemonic,
    mnemonic_to_seed,
    mnemonic_to_entropy,
    load_wordlist,
)
from bip32 import (
    generate_master_key,
    private_to_public,
    derive_child_key,
    derive_path,
)
from colorama import Fore, Style, init

init(autoreset=True)


def generate_new_wallet():
    """Generate a new wallet with random entropy."""
    bits = int(input("Enter entropy size (128 / 192 / 256): ") or "128")
    entropy = generate_entropy(bits)
    mnemonic = entropy_to_mnemonic(entropy)
    seed = mnemonic_to_seed(mnemonic)

    print(Fore.CYAN + "\n=== NEW WALLET GENERATED ===")
    print(Fore.YELLOW + "\nMnemonic:\n" + Style.RESET_ALL + mnemonic)
    print("\nSeed (hex):", seed.hex())

    master_priv, master_chain = generate_master_key(seed)
    master_pub = private_to_public(master_priv)

    print(Fore.MAGENTA + "\n--- MASTER KEYS ---")
    print("Master Private Key:", master_priv.hex())
    print("Master Chain Code :", master_chain.hex())
    print("Master Public Key :", master_pub.hex())

    # Derive first child (m/0)
    child_priv, child_chain = derive_child_key(master_priv, master_chain, 0)
    print(Fore.GREEN + "\n--- CHILD KEY (m/0) ---")
    print("Child Private Key :", child_priv.hex())
    print("Child Chain Code  :", child_chain.hex())

    # Save to file
    save = input("\nSave wallet info to file? (y/n): ").lower()
    if save == "y":
        with open("wallet_backup.txt", "w") as f:
            f.write("Mnemonic:\n" + mnemonic + "\n\n")
            f.write("Seed (hex): " + seed.hex() + "\n")
            f.write("Master Private Key: " + master_priv.hex() + "\n")
            f.write("Master Chain Code: " + master_chain.hex() + "\n")
            f.write("Master Public Key: " + master_pub.hex() + "\n")
        print(Fore.GREEN + "\nWallet information saved to wallet_backup.txt")


def import_wallet():
    """Import an existing mnemonic and derive keys."""
    wl = load_wordlist()
    mnemonic = input("Enter your mnemonic phrase:\n").strip()

    # Validate and convert
    try:
        entropy = mnemonic_to_entropy(mnemonic, wl)
        print(Fore.GREEN + "\nMnemonic is valid.")
    except ValueError as e:
        print(Fore.RED + f"\nInvalid mnemonic: {e}")
        return

    passphrase = input("Optional passphrase (press Enter for none): ").strip()
    seed = mnemonic_to_seed(mnemonic, passphrase)

    master_priv, master_chain = generate_master_key(seed)
    master_pub = private_to_public(master_priv)

    print(Fore.MAGENTA + "\n--- MASTER KEYS ---")
    print("Master Private Key:", master_priv.hex())
    print("Master Chain Code :", master_chain.hex())
    print("Master Public Key :", master_pub.hex())

    # Derive specific paths
    while True:
        path = input(
            Fore.CYAN + "\nEnter derivation path (e.g. m/0, m/0/1, m/44'/0'/0') or 'q' to quit:\n"
        ).strip()
        if path.lower() == "q":
            break
        try:
            priv, chain = derive_path(master_priv, master_chain, path)
            print(Fore.YELLOW + f"\nDerived key for {path}:")
            print("Private Key:", priv.hex())
            print("Chain Code :", chain.hex())
        except Exception as e:
            print(Fore.RED + f"Error deriving path {path}: {e}")


def main():
    print(Fore.CYAN + "=== BITCOIN WALLET TOOL ===")
    print("1. Generate new wallet")
    print("2. Import existing mnemonic")
    print("3. Exit")

    choice = input("\nChoose option (1, 2, or 3): ").strip()

    if choice == "1":
        generate_new_wallet()
    elif choice == "2":
        import_wallet()
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
