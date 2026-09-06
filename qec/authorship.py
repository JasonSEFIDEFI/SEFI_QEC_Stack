def check_authorship(Phi):
    """
    Authorship consistency check.
    Minimal rule:
        authorship must remain a single-digit integer.
    Later this becomes a geometric stress-energy signature.
    """
    try:
        a = int(Phi.authorship)
        return 0 <= a <= 9
    except ValueError:
        return False
