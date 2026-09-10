from core.identity_types import Phi
from quantum.qec_pipeline import build_quantum_pipeline


def test_quantum_pipeline():

    phi = Phi(
        "1",
        "2",
        "3",
        "4",
        "5"
    )

    result = build_quantum_pipeline(phi)

    assert "register" in result
    assert "syndrome" in result

    assert len(result["syndrome"]) == 5