# SEFI Quantum Benchmark Pipeline

An independently implemented, MIT-licensed Python package for standard quantum
mechanics software tests. No new physics or SEFI advantage is claimed. The
parent repository retains its existing research license and code unchanged.

## Install and run

From the SEFI_QEC_Stack repository root:

```sh
python -m pip install -e './benchmark_pipeline[test]'
python -m pytest benchmark_pipeline/tests -q
sefi-benchmark states runs/haar --kind haar --seed 42 --qubits 2 --count 20
sefi-benchmark states runs/noisy --kind ghz --qubits 3 --noise amplitude_damping --p 0.1
sefi-benchmark qec runs/bit3 --code bit3 --seed 42 --shots 10000 --p 0.1
sefi-benchmark benchmark runs/bit3
```

Every generation command requires a new output directory; previous runs are
never overwritten. `python -m sefi_benchmark.cli` also works. Python 3.10+
and NumPy are required. The dense simulator is for small systems (prefer <=5
qubits); its explicit allocation limit is 10 qubits, not a scalability claim.
These are seeded pseudorandom numerical samples, not hardware-generated
random qubits. `--kind circuit --depth 12` exports seeded discrete random
circuits and their resulting states; this gate ensemble is not Haar-uniform.

## API and conventions

```python
import numpy as np
from sefi_benchmark import haar, mixed, density, kraus, apply_channel, run_circuit
from sefi_benchmark.validation import valid_density, valid_channel
from sefi_benchmark.qec import DecoderInput, decode

rng = np.random.Generator(np.random.PCG64(42))
rho = density(haar(2, rng))
noisy = apply_channel(rho, kraus('amplitude_damping', 0.1), target=0)
assert valid_density(noisy)
bell = run_circuit(2, [('H', 0), ('CNOT', 0, 1)])
correction = decode(DecoderInput('bit3', (1, 0)))
```

Qubit zero is the most significant tensor factor. Haar vectors use independent
complex Gaussian amplitudes followed by normalization. Mixed states are
normalized complex Ginibre `A A†`; the default is the Hilbert-Schmidt induced
ensemble with square A, not a uniform spectrum. Optional rank is an upper
bound on mathematical rank, almost surely attained. Bell is Phi+; GHZ is
`(|0...0> + |1...1>)/sqrt(2)`. Circuit gates: I, X, Y, Z, H, S, CNOT. Seeded
computational-basis shot sampling is available as `circuits.measure`.

Noise channels use Kraus operators: bit flip, phase flip, depolarizing and
amplitude damping. **Depolarizing p means total probability of a nonidentity
Pauli**, each X/Y/Z with p/3; p=3/4 is fully depolarizing. State exports apply
the selected single-qubit channel independently to all qubits. NPZ contains
complex density matrices and loads with `allow_pickle=False`; JSON records
schema, generator, noise, versions, RNG, seed and optional descriptors.

## QEC model and metrics

`bit3`, `bit5` encode alpha|0>+beta|1> into alpha|0...0>+beta|1...1>.
Stabilizers are adjacent Zi Zi+1, noise is independent X. `phase3`, `phase5`
apply H to every encoded qubit, use adjacent Xi Xi+1 checks and independent Z
noise. Syndrome bit 1 denotes stabilizer eigenvalue -1. Measurements are ideal,
one round only. No arbitrary-Pauli protection, circuit-level fault tolerance,
surface-code threshold or hardware result is claimed. Density-matrix CPTP
experiments are separate from these sampled matched-Pauli QEC experiments.

The benchmark reports root-qubit logical Pauli failure after inverse encoding
and ancilla discard; it is not input-state infidelity or logical measurement
sampling. For phase codes the physical Z becomes decoded X. A separate count
reports failures to return to the code subspace. This distinction matters for
identity recovery. Minimum-weight correction has exact logical failure
`sum(comb(n,k)*p**k*(1-p)**(n-k), k>n//2)`. Identity recovery has root error p.
The third baseline learns most-frequent full error per syndrome using only
training labels, with deterministic tie breaking and minimum-weight fallback.
Wilson 95% intervals describe binomial sampling uncertainty, not model error.
Timings include Python scoring overhead and are local observations, not
hardware-comparable decoder latency measurements.

## Leakage boundary and splits

Exports have two folders:

* `decoder/`: train/test JSONL with only ID, code and syndrome; training labels;
  public model metadata and input hashes. `read_inputs` rejects extra fields.
* `evaluator/`: test truth, original seeds, spawn keys, training truth copy and
  benchmark reports. This directory is **trusted evaluator material**.

Each split uses a distinct child of SeedSequence, then explicit PCG64. Splits
are independent random trials; repeated syndromes and identical small error
patterns are expected and are not evidence of leakage. Fit preprocessing and
learned decoders on training data only. Decoder callbacks receive immutable
`DecoderInput(code, syndrome)` objects with no IDs, seeds, amplitudes, injected
errors, transmitted data or test labels. Optional geometric descriptors never
enter those objects. Retraining or selecting models against test results
invalidates a held-out evaluation.

**This Python API is not a security sandbox.** An untrusted decoder must run
in a separate process/container with only decoder files mounted, no evaluator
filesystem, no seed and no evaluator object memory. Publishing seeds or test
truth enables reconstruction: published seeded runs are reproducibility demos,
not blind challenges. Keep evaluator exports private for real held-out tests
and release them only after evaluation is closed. Changing the seed is needed
for a fresh challenge; hashing or renaming it is not sufficient protection.

Same seed/configuration/version yields the same numeric data. Pin Python/NumPy
for byte comparisons; compressed NPZ bytes and timing fields are not promised
to match across platforms. JSONL observations and truth are tested for exact
repeatability in the recorded environment.

## SEFI integration and optional geometry

`quantum.benchmark` provides the opt-in Stack bridge. In SEFI-PY,
`integrations/quantum_benchmark.py` provides a seeded QuantumState constructor
and dataset wrapper after this package is installed. No legacy dynamics are
used to generate standard QM reference data. `adapters.to_sefi_py` accepts the
actual caller's class and configurations; `from_sefi_py` checks normalization
and copies amplitudes rather than silently repairing an invalid state.

`--sefi-features` attaches optional **SEFI-inspired descriptive only** purity
and von Neumann entropy to state datasets. Both are conventional quantities;
they supply no new law or claimed QEC advantage. They are deliberately absent
from QEC decoder files. Existing identity-based recovery and placeholder
syndromes are not used as physical reference decoders.

## Validation and research record

Tests include Hermiticity/trace/positive-semidefiniteness, Haar moments,
Kraus completeness plus independent Choi positivity and partial-trace checks,
analytic channel limits, circuit Bell/GHZ checks, exhaustive statevector QEC
checks for every matched error pattern, analytic failure-rate comparisons,
repeatability, split separation and decoder field restrictions. See
[RESEARCH_LEDGER.md](RESEARCH_LEDGER.md) for actual local outcomes and caveats.
CI is configured separately; local passing tests do not establish a CI pass.

Standard reference material:

* [IBM channel representations](https://quantum.cloud.ibm.com/learning/en/courses/general-formulation-of-quantum-information/quantum-channels/representations-of-channels)
* [IBM repetition codes](https://quantum.cloud.ibm.com/docs/en/tutorials/repetition-codes)
* [IBM error correction II](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/error-correction-ii)
