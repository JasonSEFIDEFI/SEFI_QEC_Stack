# SEFI QEC Stack — Research Software

**Status: experimental software prototype; not validated quantum error correction.**

This repository contains Python software exploring identity-state encoding, rule-based correction, simulated channel disturbances, and proposed geometric diagnostics associated with SEFI/GWFM. The terminology is part of a research model, not proof of a new physical quantum-error-correction mechanism.

## What exists in this repository

- [`stack.py`](stack.py) — `sefi_qec_pipeline(observables, channel_model)`, which orchestrates identity construction, propagation, encoding, a supplied channel, decoding, rule-based correction, and diagnostics.
- [`core/identity_types.py`](core/identity_types.py) — `Phi` identity-state data object.
- [`codec/sefi_codec.py`](codec/sefi_codec.py) — encoding and decoding wrappers.
- [`qec/stabilizer.py`](qec/stabilizer.py) — rule-based identity checks and corrections; not a demonstrated physical stabilizer code.
- [`fidelity/fidelity.py`](fidelity/fidelity.py) — a **heuristic identity-match score**, despite its historical function name. It is **not quantum-state fidelity** and does not establish a physical fidelity bound.
- [`quantum/circuits.py`](quantum/circuits.py) — a 20-bit representation and parity calculation; its `syndrome()` implementation is explicitly a placeholder, not stabilizer syndrome measurement.
- [`tests/test_stack.py`](tests/test_stack.py) — source-level software tests for the pipeline and selected behaviors.

**Correction to earlier documentation:** the main orchestrator is `stack.py` at repository root, **not** `qec_stack/stack.py`. There is no verified `QECStack().run()` API here.

## Reproduce and inspect

From the repository root in a suitable Python environment:

```bash
python -m pytest tests/test_stack.py
python stack.py
```

These are commands to run, **not a claim that this documentation audit executed them**. Review the test results, environment, and dependencies before reporting success. The direct pipeline entry point is `sefi_qec_pipeline(observables, channel_model)`.

## Optional Azure integration

The repository contains [`quantum/azure_job.py`](quantum/azure_job.py) with an Azure Quantum submission wrapper and an optional `azure-quantum` dependency declared in [`pyproject.toml`](pyproject.toml). This is an integration path, **not evidence of a successful cloud job or a hardware QEC demonstration**. Actual target compatibility, credentials, backend execution, and results must be checked independently.

## Scientific and engineering limits

- The software's identity-field corrections are not equivalent to quantum stabilizer measurements or fault-tolerant logical correction.
- The historical fidelity function returns a rule-based score, not a physical overlap or measured logical fidelity.
- A 20-bit register representation is not, by itself, a quantum error-correcting code.
- No logical-error-rate advantage, threshold, latency guarantee, or experimental SEFI mechanism is established here.
- Before making performance claims, specify a physical noise model, reference code and decoder, matched baselines, reproducible seeds, uncertainty, and test hardware.

The SEFI/GWFM/DEFI interpretations remain hypotheses unless independently derived and tested. Preserve mathematical definitions, simulation outputs, and physical evidence as separate categories.

**Author:** Jason Duran Dutton. Research and software development in progress.
