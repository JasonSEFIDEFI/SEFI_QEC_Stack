import itertools
import numpy as np
import pytest
from sefi_benchmark import haar, mixed, bell, ghz, density, kraus, apply_channel, run_circuit
from sefi_benchmark.channels import X, Z, H, expand
from sefi_benchmark.circuits import measure, random_circuit
from sefi_benchmark.validation import valid_density, valid_channel
from sefi_benchmark.qec import DecoderInput, decode, syndrome


@pytest.mark.parametrize("n", [1, 2, 3, 5])
def test_states(n):
    rng = np.random.default_rng(19)
    for _ in range(12):
        pure = haar(n, rng)
        assert valid_density(density(pure))
        assert abs(np.trace(density(pure) @ density(pure))-1) < 1e-10
        assert valid_density(mixed(n, rng))
        assert valid_density(mixed(n, rng, rank=1))
    assert valid_density(density(ghz(n)))


def test_haar_moments_and_seed():
    assert np.array_equal(haar(3, np.random.default_rng(12)), haar(3, np.random.default_rng(12)))
    rng = np.random.default_rng(7)
    population = np.array([abs(haar(2, rng)[0])**2 for _ in range(10000)])
    assert abs(population.mean() - 1/4) < .01
    assert abs(np.mean(population**2) - 2/(4*5)) < .01


@pytest.mark.parametrize("name", ["bit_flip", "phase_flip", "depolarizing", "amplitude_damping"])
@pytest.mark.parametrize("p", [0., .17, 1.])
def test_cptp(name, p):
    ks = kraus(name, p)
    assert valid_channel(ks)
    # Independent Kraus completeness, in addition to the Choi partial trace.
    assert np.allclose(sum(k.conj().T @ k for k in ks), np.eye(2))
    rho = density(bell())
    for q in (0, 1):
        assert valid_density(apply_channel(rho, ks, q))


def test_channel_analytic_limits():
    one = np.diag([0., 1.])
    assert np.allclose(apply_channel(one, kraus("amplitude_damping", .3)), np.diag([.3, .7]))
    assert np.allclose(apply_channel(one, kraus("bit_flip", 1)), np.diag([1, 0]))
    plus = np.ones((2, 2)) / 2
    assert np.allclose(apply_channel(plus, kraus("phase_flip", .5)), np.eye(2)/2)
    assert np.allclose(apply_channel(one, kraus("depolarizing", .75)), np.eye(2)/2)
    assert not valid_density(np.diag([1.1, -.1]))
    assert not valid_density(np.array([[1, 1], [0, 0]]))
    assert not valid_channel([2*np.eye(2)])
    assert not valid_channel([])
    with pytest.raises(ValueError):
        apply_channel(one, [2*np.eye(2)])


def test_circuits():
    assert np.allclose(run_circuit(2, [("H", 0), ("CNOT", 0, 1)]), bell())
    assert np.allclose(run_circuit(3, [("H", 0), ("CNOT", 0, 1), ("CNOT", 0, 2)]), ghz(3))
    v = haar(3, np.random.default_rng(5))
    assert np.allclose(run_circuit(3, [("CNOT", 2, 0), ("CNOT", 2, 0)], v), v)
    a = measure(bell(), 100, np.random.default_rng(1))
    assert a.sum() == 100 and a[1] == a[2] == 0
    a = random_circuit(3, 40, np.random.default_rng(17))
    assert a == random_circuit(3, 40, np.random.default_rng(17))
    assert valid_density(density(run_circuit(3, a)))


@pytest.mark.parametrize("code", ["bit3", "phase3", "bit5", "phase5"])
def test_exhaustive_qec_against_statevector(code):
    n = int(code[-1]); phase = code.startswith("phase")
    # Independent physical preparation, Pauli faults, stabilizer expectation,
    # recovery and inverse circuit for every possible matched error pattern.
    psi = haar(1, np.random.default_rng(51))
    initial = np.kron(psi, np.eye(1, 2**(n-1), 0).ravel())
    encoding = [("CNOT", 0, q) for q in range(1, n)]
    basis = [("H", q) for q in range(n)] if phase else []
    encoded = run_circuit(n, encoding+basis, initial)
    fault = Z if phase else X
    check = X if phase else Z
    for error in itertools.product((0, 1), repeat=n):
        noisy = encoded.copy()
        for q, bit in enumerate(error):
            if bit:
                noisy = expand(fault, n, q) @ noisy
        measured = []
        for q in range(n-1):
            stabilizer = expand(check, n, q) @ expand(check, n, q+1)
            expectation = np.vdot(noisy, stabilizer @ noisy).real
            assert abs(abs(expectation)-1) < 1e-10
            measured.append(int(expectation < 0))
        assert tuple(measured) == syndrome(error)
        correction = decode(DecoderInput(code, tuple(measured)))
        corrected = noisy.copy()
        for q, bit in enumerate(correction):
            if bit:
                corrected = expand(fault, n, q) @ corrected
        decoded = run_circuit(n, basis+list(reversed(encoding)), corrected)
        # Trace out ancillas without relying on residual parity calculations.
        matrix = decoded.reshape(2, -1)
        rho = matrix @ matrix.conj().T
        expected = psi if sum(error) <= n//2 else X @ psi
        assert np.allclose(rho, density(expected))


@pytest.mark.parametrize("bad", [-1, np.nan, 1.1])
def test_invalid_probability(bad):
    with pytest.raises(ValueError):
        kraus("bit_flip", bad)
