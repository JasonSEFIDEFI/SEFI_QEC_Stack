from transport.curvature import apply_curvature

def propagate(Phi, steps=1):
    """
    Worldline propagation with curvature.
    """
    Phi_curved = apply_curvature(Phi, curvature=steps)
    return Phi_curved
