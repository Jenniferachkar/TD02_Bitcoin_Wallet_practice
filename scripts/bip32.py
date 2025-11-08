import hmac, hashlib, struct
import ecdsa, binascii

BIP32_PRIV = b"\x04\x88\xAD\xE4"
BIP32_PUB  = b"\x04\x88\xB2\x1E"

def hmac_sha512(key, data):
    return hmac.new(key, data, hashlib.sha512).digest()

def generate_master_key(seed):
    I = hmac_sha512(b"Bitcoin seed", seed)
    master_priv, master_chain = I[:32], I[32:]
    return master_priv, master_chain

def private_to_public(privkey):
    sk = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    prefix = b'\x02' if vk.pubkey.point.y() % 2 == 0 else b'\x03'
    return prefix + vk.to_string("compressed")[1:33]

def derive_child_key(parent_priv, parent_chain, index):
    hardened = index >= 0x80000000
    if hardened:
        data = b'\x00' + parent_priv + struct.pack(">L", index)
    else:
        pub = private_to_public(parent_priv)
        data = pub + struct.pack(">L", index)

    I = hmac_sha512(parent_chain, data)
    child_priv = (int.from_bytes(I[:32], "big") + int.from_bytes(parent_priv, "big")) % ecdsa.SECP256k1.order
    return child_priv.to_bytes(32, "big"), I[32:]
