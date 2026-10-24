import numpy as np
from .validation import valid_density, valid_channel

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)


def kraus(name, p):
    if not np.isfinite(p) or not 0 <= p <= 1:
        raise ValueError("probability must be finite in [0, 1]")
    if name in ("bit_flip", "phase_flip"):
        return [np.sqrt(1-p)*I, np.sqrt(p)*(X if name == "bit_flip" else Z)]
    if name == "depolarizing":
        # p is probability of a uniformly sampled nonidentity Pauli.
        return [np.sqrt(1-p)*I] + [np.sqrt(p/3)*a for a in (X, Y, Z)]
    if name == "amplitude_damping":
        return [np.diag([1, np.sqrt(1-p)]), np.array([[0, np.sqrt(p)], [0, 0]])]
    raise ValueError("unknown channel")


def expand(op, n, target):
    if not isinstance(target, int) or not 0 <= target < n:
        raise ValueError("invalid target")
    result = np.array([[1]], complex)
    for q in range(n):
        result = np.kron(result, op if q == target else I)
    return result


def apply_channel(rho, operators, target=0):
    rho = np.asarray(rho, complex)
    if not valid_density(rho) or not valid_channel(operators):
        raise ValueError("invalid density matrix or CPTP channel")
    n = rho.shape[0].bit_length()-1
    if 2**n != rho.shape[0] or n < 1 or any(np.asarray(k).shape != (2, 2) for k in operators):
        raise ValueError("expected qubit state and single-qubit channel")
    full = [expand(k, n, target) for k in operators]
    return sum(k @ rho @ k.conj().T for k in full)
