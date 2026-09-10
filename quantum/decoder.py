from core.identity_types import Phi


class SEFIDecoder:

    def decode(self, bits):

        if len(bits) != 20:
            raise ValueError(
                "SEFI register must contain 20 bits."
            )

        def decode_field(chunk):

            value = int(
                "".join(str(x) for x in chunk),
                2
            )

            if value > 9:
                value = 0

            return str(value)

        return Phi(
            origin=decode_field(bits[0:4]),
            authorship=decode_field(bits[4:8]),
            sovereignty=decode_field(bits[8:12]),
            warp=decode_field(bits[12:16]),
            metric=decode_field(bits[16:20]),
        )