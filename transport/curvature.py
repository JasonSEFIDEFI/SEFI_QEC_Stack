def apply_curvature(Phi, curvature=1):
    """
    Minimal curvature model:
    - warp increases by curvature
    - sovereignty bends upward
    - metric shifts toward 1 (Lorentzian)
    """
    warp = str(int(Phi.warp) + curvature) if Phi.warp.isdigit() else Phi.warp
    sovereignty = str(int(Phi.sovereignty) + curvature) if Phi.sovereignty.isdigit() else Phi.sovereignty

    # metric moves toward 1
    metric = "1" if Phi.metric != "1" else Phi.metric

    from core.identity_types import Phi as PhiObj
    return PhiObj(
        origin=Phi.origin,
        authorship=Phi.authorship,
        sovereignty=sovereignty,
        warp=warp,
        metric=metric
    )
# transport/curvature.py

import math

def calculate_curvature(v, a):

    vx, vy, vz = v
    ax, ay, az = a

    cross = (
        vy*az - vz*ay,
        vz*ax - vx*az,
        vx*ay - vy*ax
    )

    cross_mag = math.sqrt(sum(c*c for c in cross))

    v_mag = math.sqrt(
        vx*vx +
        vy*vy +
        vz*vz
    )

    if v_mag == 0:
        return 0.0

    return cross_mag / (v_mag ** 3)