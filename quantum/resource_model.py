class SEFIResourceModel:

    def __init__(
        self,
        logical_qubits=20,
        stabilizers=5,
        syndrome_qubits=5
    ):

        self.logical_qubits = logical_qubits
        self.stabilizers = stabilizers
        self.syndrome_qubits = syndrome_qubits

    @property
    def total_qubits(self):

        return (
            self.logical_qubits +
            self.syndrome_qubits
        )

    def report(self):

        return {
            "logical_qubits": self.logical_qubits,
            "stabilizers": self.stabilizers,
            "syndrome_qubits": self.syndrome_qubits,
            "total_qubits": self.total_qubits,
        }