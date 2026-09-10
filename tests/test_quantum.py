from core.identity_types import Phi
from quantum.circuits import build_circuit


def test_build_quantum_circuit():

    phi = Phi(
        "1",
        "2",
        "3",
        "4",
        "5"
    )

    circuit = build_circuit(phi)

    assert len(circuit.bits) == 20


def test_register_view():

    phi = Phi(
        "1",
        "2",
        "3",
        "4",
        "5"
    )

    circuit = build_circuit(phi)

    registers = circuit.register_view()

    assert set(registers.keys()) == {
        "origin",
        "authorship",
        "sovereignty",
        "warp",
        "metric"
    }


def test_parity():

    phi = Phi(
        "1",
        "2",
        "3",
        "4",
        "5"
    )

    circuit = build_circuit(phi)

    assert circuit.parity() in (0, 1)