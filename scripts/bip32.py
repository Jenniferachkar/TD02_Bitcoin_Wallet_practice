import hmac, hashlib, struct

def master_key_from_seed(seed):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return I[:32], I[32:]

def derive_child_key(parent_priv, parent_chaincode, index):
    data = b"\x00" + parent_priv + struct.pack(">L", index)
    I = hmac.new(parent_chaincode, data, hashlib.sha512).digest()
    return I[:32], I[32:]
