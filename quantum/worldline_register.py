class WorldlineRegister:
    """
    Quantum-side representation
    of GWFM worldline information.
    """

    def __init__(self, phi):

        self.x = phi.x
        self.y = phi.y
        self.z = phi.z

        self.vx = phi.vx
        self.vy = phi.vy
        self.vz = phi.vz

    def position(self):

        return (
            self.x,
            self.y,
            self.z,
        )

    def velocity(self):

        return (
            self.vx,
            self.vy,
            self.vz,
        )

    def state(self):

        return {
            "position": self.position(),
            "velocity": self.velocity(),
        }