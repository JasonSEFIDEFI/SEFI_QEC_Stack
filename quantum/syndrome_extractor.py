from typing import List


class SyndromeExtractor:
    """
    Classical syndrome extractor for SEFI bit registers.
    Compares transmitted vs received bitstrings.
    """

    def extract(self, transmitted: List[int], received: List[int]) -> List[int]:
        """
        Return positions where transmitted and received differ.
        """
        syndrome: List[int] = []

        length = min(len(transmitted), len(received))

        for i in range(length):
            if transmitted[i] != received[i]:
                syndrome.append(i)

        return syndrome
