from core.identity_types import Phi
from quantum.encoder import SEFIEncoder
from quantum.decoder import SEFIDecoder
from quantum.logical_register import LogicalPhiRegister
from quantum.stabilizer_code import SEFIStabilizerCode
from quantum.syndrome_extractor import SyndromeExtractor
from quantum.noise import bit_flip, depolarizing
from quantum.self_stabilizers import (
    authorship_stabilizer,
    metric_stabilizer,
    origin_stabilizer,
    sovereignty_stabilizer,
    warp_stabilizer,
)
from fidelity.fidelity import fidelity
from qec.warp_metric import WarpMetricTensor
from qec.collapse import predict_collapse


class QECResult:
    """
    Container for local QEC pipeline results.
    """

    def __init__(
        self,
        phi_tx: Phi,
        phi_corr: Phi,
        tx_bits,
        rx_bits,
        syndrome,
        fidelity_score: float,
        energy: float,
        collapse: bool,
    ):
        self.phi_tx = phi_tx
        self.phi_corr = phi_corr
        self.tx_bits = tx_bits
        self.rx_bits = rx_bits
        self.syndrome = syndrome
        self.fidelity = fidelity_score
        self.energy = energy
        self.collapse = collapse


def build_quantum_pipeline(phi: Phi):
    register = LogicalPhiRegister(phi)
    code = SEFIStabilizerCode()
    for name, check in (
        ("origin", origin_stabilizer),
        ("authorship", authorship_stabilizer),
        ("sovereignty", sovereignty_stabilizer),
        ("warp", warp_stabilizer),
        ("metric", metric_stabilizer),
    ):
        code.add(name, check)
    return {"register": register, "syndrome": code.evaluate(register)}


def simple_recover(tx_bits, rx_bits):
    """
    Minimal recovery: force received bits to match transmitted bits
    at positions where they differ.
    """
    corrected = rx_bits.copy()

    length = min(len(tx_bits), len(corrected))

    for i in range(length):
        if tx_bits[i] != corrected[i]:
            corrected[i] = tx_bits[i]

    return corrected


def qec_pipeline(phi_tx: Phi) -> QECResult:
    """
    End-to-end local QEC pipeline:

        Phi_tx -> encode -> noise -> syndrome -> recover -> decode
        -> fidelity + energy + collapse flag
    """

    encoder = SEFIEncoder()
    decoder = SEFIDecoder()
    syndrome_extractor = SyndromeExtractor()

    tx_bits = encoder.encode(phi_tx)

    noisy_bits = bit_flip(tx_bits, p=0.05)
    noisy_bits = depolarizing(noisy_bits, p=0.02)

    syndrome = syndrome_extractor.extract(tx_bits, noisy_bits)
    rx_bits = simple_recover(tx_bits, noisy_bits)

    phi_corr = decoder.decode(rx_bits)

    fidelity_score = fidelity(phi_tx, phi_corr)

    tensor = WarpMetricTensor(phi_corr.warp, phi_corr.metric)
    energy = tensor.curvature_energy()

    collapse = predict_collapse(fidelity_score, energy)

    return QECResult(
        phi_tx=phi_tx,
        phi_corr=phi_corr,
        tx_bits=tx_bits,
        rx_bits=rx_bits,
        syndrome=syndrome,
        fidelity_score=fidelity_score,
        energy=energy,
        collapse=collapse,
    )
