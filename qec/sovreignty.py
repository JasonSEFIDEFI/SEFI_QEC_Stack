def check_sovereignty(Phi):
    """
    Sovereignty boundary check.
    A photon is sovereign if its sovereignty field is within allowed bounds.
    For now: sovereignty must be an integer between 0 and 9.
    """
    try:
        s = int(Phi.sovereignty)
        return 0 <= s <= 9
    except ValueError:
        return False
