"""Complex Gaussian Haar vectors and Hilbert-Schmidt induced mixed states."""
import numpy as np


def dimension(n):
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or not 1 <= n <= 10:
        raise ValueError("qubit count must be an integer in [1, 10]")
    return 2 ** int(n)


def haar(n, rng):
    d = dimension(n)
    v = rng.normal(size=d) + 1j * rng.normal(size=d)
    return v / np.linalg.norm(v)


def density(v):
    v = np.asarray(v, dtype=complex)
    if v.ndim != 1 or not np.isfinite(v).all() or not np.isclose(np.vdot(v, v), 1):
        raise ValueError("expected normalized finite statevector")
    return np.outer(v, v.conj())


def mixed(n, rng, rank=None):
    d = dimension(n)
    rank = d if rank is None else rank
    if isinstance(rank, bool) or not isinstance(rank, (int, np.integer)) or not 1 <= rank <= d:
        raise ValueError("rank must be an integer in [1, dimension]")
    a = rng.normal(size=(d, rank)) + 1j * rng.normal(size=(d, rank))
    rho = a @ a.conj().T
    return rho / np.trace(rho)


def ghz(n):
    v = np.zeros(dimension(n), complex)
    v[0] = v[-1] = 1 / np.sqrt(2)
    return v


def bell():
    return ghz(2)
