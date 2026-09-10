from quantum.phi_state import phi_to_bitlist


class SEFIEncoder:

    def encode(self, phi):

        return phi_to_bitlist(phi)