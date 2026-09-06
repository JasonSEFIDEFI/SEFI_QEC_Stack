class WarpMetricTensor:
    """
    Minimal SEFI warp-metric tensor.
    Encodes coupling between warp and metric.
    """
    def __init__(self, warp, metric):
        self.warp = int(warp) if str(warp).isdigit() else 0
        self.metric = int(metric) if str(metric).isdigit() else 1

    def curvature_energy(self):
        """
        Simple energy: E = warp^2 * metric
        """
        return self.warp ** 2 * self.metric
