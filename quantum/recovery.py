def recover(tx_bits, rx_bits):
    """
    Perfect recovery for simulation.

    Later replaced by:
        stabilizer syndromes
        logical recovery circuits
        Azure execution results
    """

    corrected = rx_bits.copy()

    for i in range(len(tx_bits)):

        if tx_bits[i] != corrected[i]:
            corrected[i] = tx_bits[i]

    return corrected