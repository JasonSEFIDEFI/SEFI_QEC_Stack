from core.identity_types import Phi
from qec.authorship import check_authorship
from qec.metric import check_metric
from qec.origin import check_origin
from qec.sovereignty import check_sovereignty


def correct(Phi_rx):
    """
    SEFI/GWFM stabilizer.

    Enforces:
        - Origin invariance
        - Authorship consistency
        - Sovereignty boundary
        - Warp recovery
        - Metric invariance
    """

    warp_corrected = "0" if Phi_rx.warp == "X" else Phi_rx.warp

    origin_corrected = (
        Phi_rx.origin
        if check_origin(Phi_rx)
        else "0"
    )

    authorship_corrected = (
        Phi_rx.authorship
        if check_authorship(Phi_rx)
        else "0"
    )

    sovereignty_corrected = (
        Phi_rx.sovereignty
        if check_sovereignty(Phi_rx)
        else "0"
    )

    metric_corrected = (
        Phi_rx.metric
        if check_metric(Phi_rx)
        else "1"
    )

    return Phi(
        origin=origin_corrected,
        authorship=authorship_corrected,
        sovereignty=sovereignty_corrected,
        warp=warp_corrected,
        metric=metric_corrected,
        x=Phi_rx.x,
        y=Phi_rx.y,
        z=Phi_rx.z,
        vx=Phi_rx.vx,
        vy=Phi_rx.vy,
        vz=Phi_rx.vz,
    )


def syndrome(Phi_rx):
    """
    Returns the detected SEFI invariant violations.
    """

    return {
        "origin_error": not check_origin(Phi_rx),
        "authorship_error": not check_authorship(Phi_rx),
        "sovereignty_error": not check_sovereignty(Phi_rx),
        "metric_error": not check_metric(Phi_rx),
        "warp_error": Phi_rx.warp == "X",
    }
