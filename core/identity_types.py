class Phi:
    """
    Geometric identity object for SEFI-QEC.
    Represents the five SEFI invariants.
    """
    def __init__(self, origin, authorship, sovereignty, warp, metric):
        self.origin = origin
        self.authorship = authorship
        self.sovereignty = sovereignty
        self.warp = warp
        self.metric = metric

    def __repr__(self):
        return f"Phi(origin={self.origin}, authorship={self.authorship}, sovereignty={self.sovereignty}, warp={self.warp}, metric={self.metric})"
