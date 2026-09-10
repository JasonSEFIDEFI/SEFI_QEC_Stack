def propagate(Phi, dt=1.0):
    """
    GWFM worldline propagation.
    """

    Phi.x += Phi.vx * dt
    Phi.y += Phi.vy * dt
    Phi.z += Phi.vz * dt

    return Phi
