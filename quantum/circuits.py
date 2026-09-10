from quantum.phi_state import phi_to_bitlist
from quantum.registers import SEFI_REGISTER_SIZE


class SEFICircuit:
    """
    Quantum-ready representation of a SEFI identity state.

    This is intentionally backend-neutral so it can later target:
        - Azure Quantum
        - Qiskit
        - Q#
        - Resource Estimator
    """

    def __init__(self, bits):
        if len(bits) != SEFI_REGISTER_SIZE:
            raise ValueError(
                f"Expected {SEFI_REGISTER_SIZE} bits, got {len(bits)}"
            )

        self.bits = bits

    def syndrome(self):
        """
        Placeholder syndrome extraction.

        Returns positions of logical 1s.
        """

        return [i for i, bit in enumerate(self.bits) if bit == 1]

    def parity(self):
        """
        Simple parity check.
        """

        return sum(self.bits) % 2

    def register_view(self):
        """
        Human-readable register layout.
        """

        return {
            "origin": self.bits[0:4],
            "authorship": self.bits[4:8],
            "sovereignty": self.bits[8:12],
            "warp": self.bits[12:16],
            "metric": self.bits[16:20],
        }


def build_circuit(phi):
    """
    Build a SEFI logical circuit representation from Phi.
    """

    bits = phi_to_bitlist(phi)

    return SEFICircuit(bits)