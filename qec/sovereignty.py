from quantum.sovereignty_surface import within_surface


def check_sovereignty(Phi):
    """
    SEFI sovereignty check.

    Sovereignty is maintained when the
    worldline remains inside the allowed
    sovereignty surface.
    """

    return within_surface(Phi)