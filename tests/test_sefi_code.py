from core.identity_types import Phi

from quantum.sefi_code import SEFICode


def test_sefi_code_roundtrip():

    phi = Phi(
        "1",
        "2",
        "3",
        "4",
        "5"
    )

    code = SEFICode()

    encoded = code.encode(phi)

    decoded = code.decode(encoded)

    assert decoded.origin == "1"
    assert decoded.authorship == "2"
    assert decoded.sovereignty == "3"
    assert decoded.warp == "4"
    assert decoded.metric == "5"


def test_syndrome_detection():

    code = SEFICode()

    tx = [0] * 20
    rx = tx.copy()

    rx[7] = 1

    syndrome = code.syndrome_extract(
        tx,
        rx
    )

    assert syndrome == [7]