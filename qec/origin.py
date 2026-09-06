def check_origin(Phi):
    """
    Origin drift check.
    Minimal rule:
        origin must remain a single-digit integer.
    Later this becomes a geometric emission-event invariant.
    """
    try:
        o = int(Phi.origin)
        return 0 <= o <= 9
    except ValueError:
        return False
