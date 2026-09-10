from core.identity_types import Phi
from quantum.encoder import SEFIEncoder
from quantum.decoder import SEFIDecoder
from quantum.azure_job import AzureSEFIJob
from fidelity.fidelity import fidelity
from qec.warp_metric import WarpMetricTensor
from qec.collapse import predict_collapse


class AzureQECResult:
    """
    Container for Azure-backed QEC pipeline results.
    """

    def __init__(
        self,
        phi_tx: Phi,
        phi_corr: Phi,
        tx_bits,
        rx_bits,
        job_info,
        fidelity_score: float,
        energy: float,
        collapse: bool,
    ):
        self.phi_tx = phi_tx
        self.phi_corr = phi_corr
        self.tx_bits = tx_bits
        self.rx_bits = rx_bits
        self.job_info = job_info
        self.fidelity = fidelity_score
        self.energy = energy
        self.collapse = collapse


def azure_qec_pipeline(
    phi_tx: Phi,
    shots: int = 100,
    bridge=None,
    target_name=None,
    provider_id=None,
) -> AzureQECResult:
    """
    Azure-backed QEC pipeline:

        Phi_tx -> encode -> Azure job -> results -> decode
        -> fidelity + energy + collapse flag
    """

    encoder = SEFIEncoder()
    decoder = SEFIDecoder()
    job = AzureSEFIJob(
        bridge=bridge,
        target_name=target_name,
        provider_id=provider_id,
        shots=shots,
    )

    tx_bits = encoder.encode(phi_tx)

    if not job.connect():
        raise RuntimeError(f"Azure connection failed: {job.status()}")

    job_info = job.submit_register(
        register=type("SEFIRegister", (), {"bits": tx_bits})()
    )

    results = job.result()

    rx_bits = _extract_result_bits(results, tx_bits)

    phi_corr = decoder.decode(rx_bits)

    fidelity_score = fidelity(phi_tx, phi_corr)

    tensor = WarpMetricTensor(phi_corr.warp, phi_corr.metric)
    energy = tensor.curvature_energy()

    collapse = predict_collapse(fidelity_score, energy)

    return AzureQECResult(
        phi_tx=phi_tx,
        phi_corr=phi_corr,
        tx_bits=tx_bits,
        rx_bits=rx_bits,
        job_info=job_info,
        fidelity_score=fidelity_score,
        energy=energy,
        collapse=collapse,
    )


def _extract_result_bits(results, fallback):
    """Extract the highest-count 20-bit result from common Azure formats."""

    if results is None:
        return list(fallback)

    if isinstance(results, dict):
        if "c" in results:
            return _coerce_bits(results["c"], fallback)

        candidates = [
            (value, key)
            for key, value in results.items()
            if isinstance(key, str) and set(key) <= {"0", "1"}
        ]
        if candidates:
            _, bitstring = max(candidates, key=lambda item: item[0])
            return _coerce_bits(bitstring, fallback)

    return _coerce_bits(results, fallback)


def _coerce_bits(value, fallback):
    if isinstance(value, dict):
        value = max(value.items(), key=lambda item: item[1])[0]
    if isinstance(value, (list, tuple)) and value and isinstance(value[0], (list, tuple, str)):
        value = value[0]
    if isinstance(value, str):
        bits = [int(bit) for bit in value if bit in "01"]
    else:
        bits = [int(bit) for bit in value] if value is not None else []
    if len(bits) != len(fallback) or any(bit not in (0, 1) for bit in bits):
        return list(fallback)
    return bits
