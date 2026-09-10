import math
from core.identity_types import Phi


def sovereignty_distance(phi: Phi) -> float:
    """
    Euclidean distance of the GWFM worldline position
    from the origin in geometric space.
    """
    return math.sqrt(phi.x**2 + phi.y**2 + phi.z**2)


def within_surface(phi: Phi, radius: float = 100.0) -> bool:
    """
    Sovereignty surface check.

    Sovereignty is maintained when the worldline remains
    inside the allowed sovereignty radius.
    """
    return sovereignty_distance(phi) <= radius
