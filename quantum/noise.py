import random
from typing import List


def bit_flip(bits: List[int], p: float = 0.05) -> List[int]:
    """
    X error channel: flips bits with probability p.
    """
    out = bits.copy()

    for i in range(len(out)):
        if random.random() < p:
            out[i] ^= 1

    return out


def phase_flip(bits: List[int], p: float = 0.05) -> List[int]:
    """
    Placeholder Z channel.

    Recorded as metadata until full state-vector
    simulation exists. Currently returns bits unchanged.
    """
    return bits.copy()


def depolarizing(bits: List[int], p: float = 0.05) -> List[int]:
    """
    Simple depolarizing channel: randomizes bits with probability p.
    """
    out = bits.copy()

    for i in range(len(out)):
        if random.random() < p:
            out[i] = random.choice([0, 1])

    return out
