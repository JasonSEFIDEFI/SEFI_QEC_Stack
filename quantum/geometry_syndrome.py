def geometry_syndrome(phi):

    syndrome = []

    if not (0 <= float(phi.x) <= 100):
        syndrome.append("X_DRIFT")

    if not (0 <= float(phi.y) <= 100):
        syndrome.append("Y_DRIFT")

    if not (0 <= float(phi.z) <= 100):
        syndrome.append("Z_DRIFT")

    return syndrome