import argparse
import json
import time
from pathlib import Path
import numpy as np
from .datasets import export_qec, read_inputs, write_json, environment
from .qec import decode, score, train_lookup, analytic_failure, code_size
from .states import haar, mixed, bell, ghz, density
from .features import geometric_descriptors
from .channels import kraus, apply_channel
from .circuits import random_circuit, run_circuit


def benchmark(root):
    root = Path(root)
    train = read_inputs(root/"decoder/train.jsonl")
    test = read_inputs(root/"decoder/test.jsonl")
    labels = json.loads((root/"decoder/train_labels.json").read_text())
    truth = json.loads((root/"evaluator/test_truth.json").read_text())
    fitted = train_lookup(train, labels)
    results = {}
    for name, decoder in (("identity", lambda o: decode(o, "identity")),
                          ("minimum_weight", decode), ("train_lookup", fitted)):
        start = time.perf_counter()
        results[name] = score(test, truth, decoder)
        results[name]["seconds"] = time.perf_counter()-start
    manifest = json.loads((root/"decoder/manifest.json").read_text())
    results["analytic_minimum_weight"] = analytic_failure(code_size(manifest["code"]), manifest["p"])
    results["analytic_identity"] = manifest["p"]
    results["environment"] = environment()
    write_json(root/"evaluator/benchmark.json", results)
    return results


def main():
    parser = argparse.ArgumentParser(description="Standard QM generators; ideal syndrome-only repetition benchmarks")
    sub = parser.add_subparsers(dest="command", required=True)
    q = sub.add_parser("qec")
    q.add_argument("output"); q.add_argument("--seed", type=int, default=42)
    q.add_argument("--shots", type=int, default=1000); q.add_argument("--p", type=float, default=.1)
    q.add_argument("--code", choices=["bit3", "bit5", "phase3", "phase5"], default="bit3")
    b = sub.add_parser("benchmark"); b.add_argument("dataset")
    s = sub.add_parser("states"); s.add_argument("output")
    s.add_argument("--seed", type=int, default=42); s.add_argument("--qubits", type=int, default=2)
    s.add_argument("--count", type=int, default=10)
    s.add_argument("--kind", choices=["haar", "mixed", "bell", "ghz", "circuit"], default="haar")
    s.add_argument("--depth", type=int, default=12)
    s.add_argument("--sefi-features", action="store_true")
    s.add_argument("--noise", choices=["bit_flip", "phase_flip", "depolarizing", "amplitude_damping"])
    s.add_argument("--p", type=float, default=.1)
    args = parser.parse_args()
    if args.command == "qec":
        print(export_qec(args.output, args.seed, args.shots, args.p, args.code))
    elif args.command == "benchmark":
        print(json.dumps(benchmark(args.dataset), indent=2))
    else:
        if args.count < 1 or (args.kind == "bell" and args.qubits != 2):
            parser.error("count must be positive; Bell requires two qubits")
        rng = np.random.Generator(np.random.PCG64(args.seed))
        states = []
        circuits = []
        for _ in range(args.count):
            operations = random_circuit(args.qubits, args.depth, rng) if args.kind == "circuit" else None
            circuits.append(operations)
            state = {"haar": lambda: density(haar(args.qubits, rng)),
                     "mixed": lambda: mixed(args.qubits, rng),
                     "bell": lambda: density(bell()), "ghz": lambda: density(ghz(args.qubits)),
                     "circuit": lambda: density(run_circuit(args.qubits, operations))}[args.kind]()
            if args.noise:
                for target in range(args.qubits):
                    state = apply_channel(state, kraus(args.noise, args.p), target)
            states.append(state)
        root = Path(args.output); root.mkdir(parents=True, exist_ok=False)
        np.savez_compressed(root/"states.npz", density=np.array(states))
        write_json(root/"manifest.json", {**environment(), "seed": args.seed, "kind": args.kind,
                   "count": args.count, "qubits": args.qubits,
                   "noise": args.noise, "p": args.p if args.noise else None,
                   "circuits": circuits if args.kind == "circuit" else None,
                   "mixed_measure": "Ginibre induced, rank=dimension", "features":
                   [geometric_descriptors(r) for r in states] if args.sefi_features else None})


if __name__ == "__main__":
    main()
