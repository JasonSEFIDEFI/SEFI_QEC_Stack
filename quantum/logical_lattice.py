from quantum.logical_register import LogicalPhiRegister


class LogicalLattice:
    """
    Logical qubit lattice for SEFI/GWFM states.
    """

    def __init__(self, register: LogicalPhiRegister):
        self.register = register

    def logical_distance(self):

        return len(self.register.bits)

    def weight(self):

        return sum(self.register.bits)

    def density(self):

        if len(self.register.bits) == 0:
            return 0.0

        return self.weight() / len(self.register.bits)

    def snapshot(self):

        return {
            "distance": self.logical_distance(),
            "weight": self.weight(),
            "density": self.density(),
        }