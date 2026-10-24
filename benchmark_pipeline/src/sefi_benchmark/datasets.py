"""Versioned exports with explicit public decoder / trusted evaluator boundary."""
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
from . import __version__
from .qec import code_size, syndrome, DecoderInput


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+"\n", encoding="utf-8")


def read_inputs(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()]
    for row in rows:
        if set(row) != {"id", "code", "syndrome"}:
            raise ValueError("decoder file contains unexpected fields")
    return [DecoderInput(r["code"], tuple(r["syndrome"])) for r in rows]


def environment():
    return {"package": __version__, "numpy": np.__version__, "python": platform.python_version(),
            "rng": "PCG64", "schema": "sefi-benchmark/1", "endianness": "qubit 0 is MSB"}


def export_qec(root, seed=42, shots=1000, p=0.1, code="bit3"):
    n = code_size(code)
    if type(seed) is not int or seed < 0 or type(shots) is not int or shots < 1 or not np.isfinite(p) or not 0 <= p <= 1:
        raise ValueError("invalid seed, shots, or probability")
    root = Path(root)
    root.mkdir(parents=True, exist_ok=False)  # Never overwrite a previous run.
    public, private = root/"decoder", root/"evaluator"
    public.mkdir(); private.mkdir()
    streams = np.random.SeedSequence(seed).spawn(2)
    hashes = {}
    for split, stream in zip(("train", "test"), streams):
        rng = np.random.Generator(np.random.PCG64(stream))
        errors = (rng.random((shots, n)) < p).astype(int)
        observations = [{"id": f"{split}-{i}", "code": code, "syndrome": syndrome(e)} for i, e in enumerate(errors)]
        path = public/f"{split}.jsonl"
        path.write_text("".join(json.dumps(r, sort_keys=True)+"\n" for r in observations), encoding="utf-8")
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        write_json(private/f"{split}_truth.json", errors.tolist())
        if split == "train":
            write_json(public/"train_labels.json", errors.tolist())
    write_json(public/"manifest.json", {**environment(), "code": code, "shots_per_split": shots,
               "model": "ideal syndrome, independent matched Pauli errors", "p": p,
               "input_sha256": hashes, "split_policy": "separate SeedSequence child streams"})
    write_json(private/"provenance.json", {**environment(), "seed": seed,
               "spawn_keys": {"train": [0], "test": [1]},
               "warning": "Seed and test truth are oracle information. Never mount this folder for a decoder."})
    return root
