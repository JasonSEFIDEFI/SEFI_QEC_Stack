from dataclasses import dataclass


@dataclass
class GeometricState:
	"""Basic GWFM geometric state."""

	x: float
	y: float
	z: float
	vx: float
	vy: float
	vz: float