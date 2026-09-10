class SEFISyndrome:
    """
    Quantum syndrome container.
    """

    def __init__(self, error_positions):
        self.error_positions = error_positions

    def weight(self):
        return len(self.error_positions)

    def has_error(self):
        return self.weight() > 0


def detect(tx_bits, rx_bits):

    errors = []

    for i, (a, b) in enumerate(zip(tx_bits, rx_bits)):

        if a != b:
            errors.append(i)

    return SEFISyndrome(errors)