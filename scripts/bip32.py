from __future__ import annotations
import hmac
import hashlib
import struct
import ecdsa

# ---------- HMAC-SHA512 ------------------------------------------------------

def _hmac_sha512(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha512).digest()

# ---------- Master key generation -------------------------------------------

def generate_master_key(seed: bytes) -> tuple[bytes, bytes]:
    """
    Generate master private key and chain code from a seed.
    Returns (master_private_key, master_chain_code).
    """
    I = _hmac_sha512(b"Bitcoin seed", seed)
    master_priv, master_chain = I[:32], I[32:]
    return master_priv, master_chain

# ---------- Private → public -------------------------------------------------

def private_to_public(privkey: bytes) -> bytes:
    """
    Return compressed public key corresponding to a 32-byte private key.
    """
    sk = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    prefix = b"\x02" if vk.pubkey.point.y() % 2 == 0 else b"\x03"
    x = vk.pubkey.point.x()
    return prefix + x.to_bytes(32, "big")

# ---------- Child key derivation --------------------------------------------

def derive_child_key(parent_priv: bytes, parent_chain: bytes, index: int) -> tuple[bytes, bytes]:
    """
    Derive a child private key and chain code from the parent at the given index.
    Hardened if index >= 0x80000000.
    """
    hardened = index >= 0x80000000
    if hardened:
        data = b"\x00" + parent_priv + struct.pack(">L", index)
    else:
        pub = private_to_public(parent_priv)
        data = pub + struct.pack(">L", index)

    I = _hmac_sha512(parent_chain, data)
    child_priv_int = (int.from_bytes(I[:32], "big") + int.from_bytes(parent_priv, "big")) % ecdsa.SECP256k1.order
    child_priv = child_priv_int.to_bytes(32, "big")
    child_chain = I[32:]
    return child_priv, child_chain

# ---------- Recursive derivation ---------------------------------

def derive_path(master_priv: bytes, master_chain: bytes, path: str) -> tuple[bytes, bytes]:
    """
    Derive key along a path such as m/0/1/2' .
    Hardened indices use ' at the end.
    """
    segments = path.split("/")[1:]  # drop leading 'm'
    key, chain = master_priv, master_chain
    for seg in segments:
        hardened = seg.endswith("'")
        index = int(seg[:-1]) if hardened else int(seg)
        if hardened:
            index += 0x80000000
        key, chain = derive_child_key(key, chain, index)
    return key, chain

# ---------- CLI demonstration -----------------------------------------------

def _demo():
    import binascii
    from bip39 import mnemonic_to_seed

    print("=== BIP-32 DEMO ===")
    mnemonic = input("Enter BIP-39 mnemonic:\n").strip()
    passphrase = input("Optional passphrase (press Enter for none): ").strip()
    seed = mnemonic_to_seed(mnemonic, passphrase)

    master_priv, master_chain = generate_master_key(seed)
    master_pub = private_to_public(master_priv)

    print("\nMaster Private Key:", master_priv.hex())
    print("Master Chain Code :", master_chain.hex())
    print("Master Public Key :", master_pub.hex())

    child_priv, child_chain = derive_child_key(master_priv, master_chain, 0)
    print("\nChild (m/0) Private Key:", child_priv.hex())
    print("Child (m/0) Chain Code :", child_chain.hex())

    path = input("\nEnter derivation path (e.g. m/0/1 or m/44'/0'/0'):\n").strip()
    if path:
        priv, chain = derive_path(master_priv, master_chain, path)
        print(f"\nDerived key for {path}:")
        print("Private:", priv.hex())
        print("Chain  :", chain.hex())

if __name__ == "__main__":
    _demo()
