"""Explicit duck-typed SEFI-PY QuantumState bridge; no sys.path modifications."""
import numpy as np


def to_sefi_py(vector, state_class, configs):
    v = np.array(vector, dtype=complex, copy=True)
    if v.ndim != 1 or len(configs) != len(v) or not np.isfinite(v).all() or not np.isclose(np.vdot(v, v), 1):
        raise ValueError("finite normalized vector and matching configurations required")
    return state_class(configs, v)


def from_sefi_py(state):
    v = np.array(state.amplitudes, dtype=complex, copy=True)
    if v.ndim != 1 or not np.isfinite(v).all() or not np.isclose(np.vdot(v, v), 1):
        raise ValueError("legacy amplitudes are not normalized")
    return v
