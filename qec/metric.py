def check_metric(Phi):
    """
    Metric invariance check.
    Minimal rule:
        metric must be one of: 0, 1, 5
    Later this becomes Lorentzian signature invariance.
    """
    return Phi.metric in ["0", "1", "5"]
