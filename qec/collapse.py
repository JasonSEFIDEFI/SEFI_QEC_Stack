def predict_collapse(fidelity_score: float, energy: float, threshold: float = 0.5) -> bool:
    """
    Predict collapse:
    collapse if fidelity < threshold and energy is high.
    """
    return fidelity_score < threshold and energy > 10.0
