from core.identity_types import Phi
from qec.authorship import check_authorship
from qec.metric import check_metric
from qec.origin import check_origin
from qec.sovreignty import check_sovereignty


def correct(Phi_rx):
    """
    Stabilizer:
    1. Correct warp corruption
    2. Enforce sovereignty boundary
    3. Enforce authorship consistency
    """

    warp_corrected = "0" if Phi_rx.warp == "X" else Phi_rx.warp

    if not check_sovereignty(Phi_rx):
        sovereignty_corrected = "0"
    else:
        sovereignty_corrected = Phi_rx.sovereignty

    if not check_authorship(Phi_rx):
        authorship_corrected = "0"
    else:
        authorship_corrected = Phi_rx.authorship

    if not check_origin(Phi_rx):
        origin_corrected = "0"
    else:
        origin_corrected = Phi_rx.origin

    if not check_metric(Phi_rx):
        metric_corrected = "1"
    else:
        metric_corrected = Phi_rx.metric

    return Phi(
        origin=origin_corrected,
        authorship=authorship_corrected,
        sovereignty=sovereignty_corrected,
        warp=warp_corrected,
        metric=metric_corrected,
    )
