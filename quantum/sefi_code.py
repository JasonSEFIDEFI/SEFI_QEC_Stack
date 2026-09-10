from quantum.encoder import SEFIEncoder
from quantum.decoder import SEFIDecoder
from quantum.syndrome_extractor import SyndromeExtractor


class SEFICode:

    def __init__(self):

        self.encoder = SEFIEncoder()
        self.decoder = SEFIDecoder()
        self.syndrome = SyndromeExtractor()

    def encode(self, phi):

        return self.encoder.encode(phi)

    def decode(self, bits):

        return self.decoder.decode(bits)

    def syndrome_extract(
        self,
        tx,
        rx
    ):

        return self.syndrome.extract(tx, rx)