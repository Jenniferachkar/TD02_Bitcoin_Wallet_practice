# scripts/bip32.py
import hmac, hashlib, struct

# secp256k1 curve order (n)
SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def master_key_from_seed(seed: bytes):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return I[:32], I[32:]

def _int_from_32(b: bytes) -> int:
    return int.from_bytes(b, "big")

def _bytes32(i: int) -> bytes:
    return i.to_bytes(32, "big")

def derive_child_key(parent_priv: bytes, parent_chaincode: bytes, index: int):
    if index < 0:
        raise ValueError("index must be non-negative")

    # For hardened derivation use 0x00 + parent_priv
    if index >= 0x80000000:
        data = b"\x00" + parent_priv + struct.pack(">L", index)
    else:
        # Non-hardened derivation needs parent public key.
        # We will not compute non-hardened pubkey here (left as optional).
        raise ValueError("Non-hardened derivation requested but parent public key not available in this function. Use hardened (index >= 0x80000000) or extend to compute pubkey.")

    I = hmac.new(parent_chaincode, data, hashlib.sha512).digest()
    IL, IR = I[:32], I[32:]

    parse_IL = _int_from_32(IL)
    k_par = _int_from_32(parent_priv)

    child_priv_int = (parse_IL + k_par) % SECP256K1_N
    child_priv = _bytes32(child_priv_int)
    child_chaincode = IR
    return child_priv, child_chaincode
