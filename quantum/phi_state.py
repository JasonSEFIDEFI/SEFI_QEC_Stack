from codec.sefi_codec import encode


def phi_to_bitlist(phi):
    """
    Convert Phi to a 20-bit quantum-ready register.
    """

    encoded = encode(phi)

    encoded = encoded.replace("|", "")

    return [int(bit) for bit in encoded]