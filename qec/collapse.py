def predict_collapse(fidelity_score, energy, threshold=0.5):
    """
    Predict collapse:
    collapse if fidelity < threshold and energy is high.
    """
    return fidelity_score < threshold and energy > 10
