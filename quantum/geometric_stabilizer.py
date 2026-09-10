from quantum.geometry_syndrome import geometry_syndrome
from quantum.sovereignty_surface import within_surface


class GeometricStabilizer:
    """
    Geometric SEFI stabilizer.
    """

    def evaluate(self, phi):

        return {
            "inside_surface": within_surface(phi),
            "geometry_syndrome": geometry_syndrome(phi),
        }

    def valid(self, phi):

        syndrome = geometry_syndrome(phi)

        return (
            within_surface(phi)
            and len(syndrome) == 0
        )