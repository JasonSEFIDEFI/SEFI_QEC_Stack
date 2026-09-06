def check_consistency(Phi_original, Phi_corr):
    """
    Reconstruction consistency:
    counts how many invariants match.
    """
    matches = 0
    for field in ["origin", "authorship", "sovereignty", "warp", "metric"]:
        if getattr(Phi_original, field) == getattr(Phi_corr, field):
            matches += 1
    return matches
