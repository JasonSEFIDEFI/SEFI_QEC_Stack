def encode(Phi):
    return compress(Phi)

from core.identity_types import Phi

def decode(bitstring):
    parts = decompress(bitstring)
    from core.identity_types import Phi
    return Phi(
        origin=parts["origin"],
        authorship=parts["authorship"],
        sovereignty=parts["sovereignty"],
        warp=parts["warp"],
        metric=parts["metric"]
    )

from codec.compress import compress, decompress
