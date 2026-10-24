"""Ideal one-round repetition stabilizers under matched independent Pauli noise.

bit3/bit5 correct X only; phase3/phase5 correct Z only. These are not
arbitrary-Pauli correcting codes. No measurement faults are simulated.
"""
from dataclasses import dataclass
import numpy as np


def code_size(code):
    if code not in ("bit3", "bit5", "phase3", "phase5"):
        raise ValueError("unknown repetition code")
    return int(code[-1])


def syndrome(error):
    return tuple(int(a)^int(b) for a, b in zip(error[:-1], error[1:]))


@dataclass(frozen=True)
class DecoderInput:
    code: str
    syndrome: tuple

    def __post_init__(self):
        n = code_size(self.code)
        if type(self.syndrome) is not tuple or len(self.syndrome) != n-1 or any(type(x) is not int or x not in (0, 1) for x in self.syndrome):
            raise ValueError("invalid syndrome")


def decode(observation, strategy="minimum_weight"):
    n = code_size(observation.code)
    if strategy == "identity":
        return (0,) * n
    if strategy != "minimum_weight":
        raise ValueError("unknown decoder")
    candidate = [0]
    for bit in observation.syndrome:
        candidate.append(candidate[-1] ^ bit)
    if sum(candidate) > n // 2:
        candidate = [1-x for x in candidate]
    return tuple(candidate)


def train_lookup(observations, errors):
    """Fit correction table ONLY from training labels; unseen syndromes use MW."""
    from collections import Counter, defaultdict
    observations, errors = list(observations), list(errors)
    if len(observations) != len(errors):
        raise ValueError("training lengths differ")
    counts = defaultdict(Counter)
    for obs, error in zip(observations, errors):
        e = tuple(error)
        if len(e) != code_size(obs.code) or any(x not in (0, 1) for x in e) or syndrome(e) != obs.syndrome:
            raise ValueError("invalid training label")
        counts[(obs.code, obs.syndrome)][e] += 1
    table = {key: sorted(c, key=lambda e: (-c[e], e))[0] for key, c in counts.items()}
    return lambda obs: table.get((obs.code, obs.syndrome), decode(obs))


def score(observations, truth, decoder):
    """Trusted evaluator: decoder receives only frozen DecoderInput objects.

    logical_failure is residual on root qubit after inverse encoding and
    tracing ancillary qubits. codespace_failure detects residual syndrome.
    """
    observations, truth = list(observations), list(truth)
    if not observations or len(observations) != len(truth):
        raise ValueError("nonempty equal length evaluation data required")
    failures = outside = 0
    for obs, error in zip(observations, truth):
        correction = tuple(decoder(obs))
        n = code_size(obs.code)
        if len(correction) != n or any(x not in (0, 1) for x in correction):
            raise ValueError("decoder returned invalid correction")
        if len(error) != n or any(x not in (0, 1) for x in error) or syndrome(error) != obs.syndrome:
            raise ValueError("invalid evaluation truth")
        residual = tuple(int(a)^int(b) for a, b in zip(error, correction))
        failures += residual[0]
        outside += any(syndrome(residual))
    count = len(observations)
    rate = failures / count
    # Wilson 95% interval, including valid endpoints for 0/n and n/n.
    z = 1.959963984540054
    center = (rate + z*z/(2*count)) / (1+z*z/count)
    half = z*np.sqrt(rate*(1-rate)/count + z*z/(4*count*count))/(1+z*z/count)
    return {"shots": count, "logical_failures": failures, "logical_error_rate": rate,
            "wilson95": [max(0., center-half), min(1., center+half)],
            "codespace_failures": int(outside)}


def analytic_failure(n, p):
    from math import comb
    return sum(comb(n, k)*p**k*(1-p)**(n-k) for k in range(n//2+1, n+1))
