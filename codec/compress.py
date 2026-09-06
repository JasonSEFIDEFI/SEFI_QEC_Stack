def to_binary(n):
    """
    Convert integer string to 4-bit binary.
    """
    try:
        return format(int(n), "04b")
    except ValueError:
        return "0000"


def compress(Phi):
    """
    Compress Phi into a pipe-delimited SEFI-QEC bitstring.
    """
    fields = [
        to_binary(Phi.origin),
        to_binary(Phi.authorship),
        to_binary(Phi.sovereignty),
        to_binary(Phi.warp),
        to_binary(Phi.metric),
    ]
    return "|".join(fields)


def decompress(bitstring):
    """
    Decompress pipe-delimited bitstring back into fields.
    """
    if "|" not in bitstring:
        parts = [bitstring[i:i+4] for i in range(0, len(bitstring), 4)]
    else:
        parts = bitstring.split("|")

    def parse(part, fallback="0"):
        try:
            value = int(part, 2)
        except (ValueError, TypeError):
            return fallback

        if value > 9:
            return fallback
        return str(value)

    if len(parts) < 5:
        parts = parts + ["0000"] * (5 - len(parts))
    elif len(parts) > 5:
        parts = parts[:5]

    return {
        "origin": parse(parts[0]),
        "authorship": parse(parts[1]),
        "sovereignty": parse(parts[2]),
        "warp": parse(parts[3]),
        "metric": parse(parts[4]),
    }
