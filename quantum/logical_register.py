from quantum.phi_state import phi_to_bitlist


class LogicalPhiRegister:

    def __init__(self, phi):

        self.phi = phi
        self.bits = phi_to_bitlist(phi)

    @property
    def size(self):

        return len(self.bits)

    def get(self, index):

        return self.bits[index]

    def set(self, index, value):

        self.bits[index] = int(value)

    def snapshot(self):

        return self.bits.copy()
