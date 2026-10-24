"""Physical checks independent of generator normalization and channel construction."""
import numpy as np


def valid_density(rho, atol=1e-10):
    a = np.asarray(rho)
    return bool(a.ndim == 2 and a.shape[0] == a.shape[1] and a.shape[0] > 0
                and np.isfinite(a).all() and np.allclose(a, a.conj().T, atol=atol, rtol=0)
                and abs(np.trace(a) - 1) <= atol
                and np.linalg.eigvalsh(a).min() >= -atol)


def choi(operators):
    # Column vectorization; input tensor output ordering.
    vectors = [np.asarray(k).reshape(-1, order="F") for k in operators]
    return sum(np.outer(v, v.conj()) for v in vectors)


def valid_channel(operators, atol=1e-10):
    if not operators:
        return False
    ks = [np.asarray(k) for k in operators]
    d = ks[0].shape[0] if ks[0].ndim == 2 else 0
    if not d or any(k.shape != (d, d) or not np.isfinite(k).all() for k in ks):
        return False
    c = choi(ks)
    trace_output = np.trace(c.reshape(d, d, d, d), axis1=1, axis2=3)
    return bool(np.linalg.eigvalsh(c).min() >= -atol and
                np.allclose(trace_output, np.eye(d), atol=atol, rtol=0))
