"""Standard QM benchmark tools. No new physics is asserted."""
__version__ = "0.1.0"
from .states import haar, mixed, bell, ghz, density
from .channels import kraus, apply_channel
from .circuits import run_circuit
