from core.identity_types import Phi

from quantum.logical_register import LogicalPhiRegister
from quantum.logical_lattice import LogicalLattice
from quantum.worldline_register import WorldlineRegister
from quantum.geometric_stabilizer import GeometricStabilizer


def test_worldline_register():

    phi = Phi(
        "1",
        "2",
        "3",
        "4",
        "5",
        x=1.0,
        y=2.0,
        z=3.0,
        vx=4.0,
        vy=5.0,
        vz=6.0
    )

    reg = WorldlineRegister(phi)

    assert reg.position() == (1.0, 2.0, 3.0)
    assert reg.velocity() == (4.0, 5.0, 6.0)


def test_logical_lattice():

    phi = Phi(
        "1",
        "2",
        "3",
        "4",
        "5"
    )

    reg = LogicalPhiRegister(phi)

    lattice = LogicalLattice(reg)

    assert lattice.logical_distance() == 20


def test_geometric_stabilizer():

    phi = Phi(
        "1",
        "2",
        "3",
        "4",
        "5",
        x=1.0,
        y=1.0,
        z=1.0
    )

    stabilizer = GeometricStabilizer()

    result = stabilizer.evaluate(phi)

    assert "inside_surface" in result
    assert "geometry_syndrome" in result