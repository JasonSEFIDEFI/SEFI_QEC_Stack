"""Public seeded demos, not blind evaluations. Output must be a new directory."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from sefi_benchmark.datasets import export_qec, write_json, environment
from sefi_benchmark.cli import benchmark


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    root = Path(args.output).resolve()
    root.mkdir(parents=True, exist_ok=False)
    summary = {"environment": environment(), "purpose": "public reproducibility demo, not blind", "runs": {}}
    for code in ("bit3", "bit5", "phase3", "phase5"):
        dataset = export_qec(root/code, seed=42, shots=10000, p=.1, code=code)
        summary["runs"][code] = benchmark(dataset)
        summary["runs"][code]["test_input_sha256"] = hashlib.sha256((dataset/"decoder/test.jsonl").read_bytes()).hexdigest()
    for kind in ("haar", "mixed", "bell", "ghz", "circuit"):
        subprocess.run([sys.executable, "-m", "sefi_benchmark.cli", "states", str(root/kind),
                        "--kind", kind, "--count", "5", "--noise", "amplitude_damping",
                        "--p", ".1", "--sefi-features"], check=True)
    write_json(root/"summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
