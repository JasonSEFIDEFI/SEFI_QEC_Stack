"""Optional SEFI-inspired descriptors; no physical dynamics or decoder truth."""
import numpy as np
from .validation import valid_density


def geometric_descriptors(rho):
    """Conventional purity and spectrum entropy, labeled as geometric inspiration.

    Only for state-analysis datasets. Never attached to QEC decoder observations.
    """
    if not valid_density(rho):
        raise ValueError("invalid density matrix")
    eigenvalues = np.linalg.eigvalsh(rho)
    positive = eigenvalues[eigenvalues > 0]
    return {"namespace": "sefi_inspired_descriptive_only", "purity": float(np.trace(rho @ rho).real),
            "entropy_bits": float(-np.sum(positive*np.log2(positive))), "new_physics": False}
