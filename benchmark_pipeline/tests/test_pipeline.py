import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import pytest
from sefi_benchmark.datasets import export_qec, read_inputs
from sefi_benchmark.qec import decode, score, DecoderInput, train_lookup, analytic_failure
from sefi_benchmark.cli import benchmark
from sefi_benchmark.adapters import to_sefi_py, from_sefi_py
from sefi_benchmark.features import geometric_descriptors


def test_reproducible_split_and_boundary(tmp_path):
    a = export_qec(tmp_path/"a", seed=112, shots=300)
    b = export_qec(tmp_path/"b", seed=112, shots=300)
    for path in a.rglob("*"):
        if path.is_file():
            assert path.read_bytes() == (b/path.relative_to(a)).read_bytes()
    train = json.loads((a/"evaluator/train_truth.json").read_text())
    test = json.loads((a/"evaluator/test_truth.json").read_text())
    assert train != test
    public = "".join(p.read_text() for p in (a/"decoder").glob("*"))
    assert '"seed"' not in public and '"test_truth"' not in public
    observations = read_inputs(a/"decoder/test.jsonl")
    def spy(obs):
        assert set(vars(obs)) == {"code", "syndrome"}
        return decode(obs)
    result = score(observations, test, spy)
    assert result["codespace_failures"] == 0
    with pytest.raises(FileExistsError):
        export_qec(a)
    leaked = tmp_path/"leaked.jsonl"
    leaked.write_text('{"id":"test-0","code":"bit3","syndrome":[0,0],"seed":112}\n')
    with pytest.raises(ValueError):
        read_inputs(leaked)


@pytest.mark.parametrize("code", ["bit3", "bit5", "phase3", "phase5"])
def test_benchmark_analytic(tmp_path, code):
    root = export_qec(tmp_path/code, seed=901, shots=20000, p=.1, code=code)
    result = benchmark(root)
    empirical = result["minimum_weight"]["logical_error_rate"]
    expected = analytic_failure(int(code[-1]), .1)
    assert abs(empirical - expected) < 5*np.sqrt(expected*(1-expected)/20000)
    assert result["minimum_weight"]["codespace_failures"] == 0
    assert result["identity"]["logical_error_rate"] > empirical


def test_train_only_lookup():
    obs = DecoderInput("bit3", (1, 0))
    trained = train_lookup([obs]*3, [(1, 0, 0)]*3)
    assert trained(obs) == (1, 0, 0)
    assert trained(DecoderInput("bit3", (0, 1))) == (0, 0, 1)
    with pytest.raises(ValueError):
        train_lookup([obs], [])
    with pytest.raises(ValueError):
        score([obs], [(1, 0, 0)], lambda o: [0])


def test_adapter_and_features():
    class Legacy:
        def __init__(self, configs, amplitudes):
            self.configs, self.amplitudes = configs, amplitudes
    v = np.array([1, 1j])/np.sqrt(2)
    state = to_sefi_py(v, Legacy, ["a", "b"])
    assert np.array_equal(v, from_sefi_py(state))
    state.amplitudes[0] = 0
    assert v[0] != 0
    with pytest.raises(ValueError):
        from_sefi_py(state)
    features = geometric_descriptors(np.eye(2)/2)
    assert features["purity"] == .5 and features["entropy_bits"] == 1


def test_cli(tmp_path):
    for kind in ("haar", "mixed", "bell", "ghz", "circuit"):
        subprocess.run([sys.executable, "-m", "sefi_benchmark.cli", "states", str(tmp_path/kind),
                        "--kind", kind, "--count", "2", "--sefi-features", "--noise", "amplitude_damping"], check=True, capture_output=True)
        with np.load(tmp_path/kind/"states.npz", allow_pickle=False) as data:
            assert data["density"].shape == (2, 4, 4)


@pytest.mark.parametrize("code,p,shots", [("unknown", .1, 5), ("bit3", -1, 5), ("bit3", .1, 0)])
def test_bad_dataset_arguments(tmp_path, code, p, shots):
    with pytest.raises(ValueError):
        export_qec(tmp_path/"bad", code=code, p=p, shots=shots)
