def no_noise(bitstring):
    return bitstring

def flip_warp(bitstring):
    """
    Simulates a simple channel error by flipping the warp field.
    """
    parts = bitstring.split("|")
    parts[3] = "X"  # warp corruption
    return "|".join(parts)
def break_sovereignty(bitstring):
    """
    Corrupt the sovereignty field.
    """
    parts = bitstring.split("|")
    parts[2] = "99"  # sovereignty out of bounds
    return "|".join(parts)
def corrupt_authorship(bitstring):
    """
    Corrupt the authorship field.
    """
    parts = bitstring.split("|")
    parts[1] = "99"  # invalid authorship
    return "|".join(parts)
def corrupt_origin(bitstring):
    """
    Corrupt the origin field.
    """
    parts = bitstring.split("|")
    parts[0] = "99"
    return "|".join(parts)
def corrupt_metric(bitstring):
    """
    Corrupt the metric field.
    """
    parts = bitstring.split("|")
    parts[4] = "X"
    return "|".join(parts)
