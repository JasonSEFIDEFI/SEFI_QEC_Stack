"""Small dense statevector circuits; qubit zero is the most significant bit."""
import numpy as np
from .states import dimension
from .channels import I, X, Y, Z, H, expand


def random_circuit(n, depth, rng):
    """Seeded discrete gate ensemble, not Haar-random unitaries."""
    dimension(n)
    if type(depth) is not int or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    operations = []
    for _ in range(depth):
        names = ["H", "S", "X", "Y", "Z"] + (["CNOT"] if n > 1 else [])
        name = str(rng.choice(names))
        targets = rng.choice(n, size=2 if name == "CNOT" else 1, replace=False)
        operations.append((name, *(int(t) for t in targets)))
    return operations


def run_circuit(n, operations, initial=None):
    d = dimension(n)
    v = np.zeros(d, complex) if initial is None else np.array(initial, complex, copy=True)
    if initial is None:
        v[0] = 1
    if v.shape != (d,) or not np.isfinite(v).all() or not np.isclose(np.vdot(v, v), 1):
        raise ValueError("invalid initial state")
    gates = {"I": I, "X": X, "Y": Y, "Z": Z, "H": H, "S": np.diag([1, 1j])}
    for operation in operations:
        name, *targets = operation
        if name == "CNOT":
            if len(targets) != 2 or len(set(targets)) != 2 or any(type(t) is not int or not 0 <= t < n for t in targets):
                raise ValueError("CNOT needs distinct valid control and target")
            c, t = targets
            permutation = np.arange(d)
            for i in range(d):
                if i & (1 << (n-1-c)):
                    permutation[i] ^= 1 << (n-1-t)
            v = v[permutation]
        elif name in gates and len(targets) == 1:
            v = expand(gates[name], n, targets[0]) @ v
        else:
            raise ValueError("unsupported gate or arity")
    return v


def measure(v, shots, rng):
    v = np.asarray(v)
    if v.ndim != 1 or not np.isfinite(v).all() or not np.isclose(np.vdot(v, v), 1) or type(shots) is not int or shots < 0:
        raise ValueError("invalid state or shot count")
    return rng.multinomial(shots, np.abs(v)**2)
