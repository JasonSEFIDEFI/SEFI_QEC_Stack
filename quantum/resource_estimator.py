class ResourceEstimate:

    def __init__(
        self,
        logical_qubits,
        stabilizers,
        syndrome_qubits
    ):
        self.logical_qubits = logical_qubits
        self.stabilizers = stabilizers
        self.syndrome_qubits = syndrome_qubits

    def summary(self):

        return {
            "logical_qubits": self.logical_qubits,
            "stabilizers": self.stabilizers,
            "syndrome_qubits": self.syndrome_qubits,
            "total_qubits":
                self.logical_qubits +
                self.syndrome_qubits
        }


def estimate_sefi():

    return ResourceEstimate(
        logical_qubits=20,
        stabilizers=5,
        syndrome_qubits=5,
    )