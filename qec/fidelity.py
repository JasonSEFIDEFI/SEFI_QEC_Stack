from core.identity_types import Phi


def fidelity(Phi_original: Phi, Phi_corrected: Phi) -> float:
    """
    Fidelity scoring:
    1.0 = perfect match
    0.9 = metric corrected
    0.85 = origin corrected
    0.8 = authorship corrected
    0.7 = sovereignty corrected
    0.5 = warp corrected
    0.0 = failure
    """

    if Phi_original.__dict__ == Phi_corrected.__dict__:
        return 1.0

    if Phi_original.metric == Phi_corrected.metric:
        return 0.9

    if Phi_original.origin == Phi_corrected.origin:
        return 0.85

    if Phi_original.authorship == Phi_corrected.authorship:
        return 0.8

    if Phi_original.sovereignty == Phi_corrected.sovereignty:
        return 0.7

    if Phi_original.warp == Phi_corrected.warp:
        return 0.5

    return 0.0
