# Public research ledger

## 2026-10-23 — first standard-QM benchmark implementation

Purpose: create reproducible synthetic quantum reference data and a
syndrome-only reference decoder comparison. No SEFI advantage or new physics
was tested or established. No hardware jobs were submitted.

Inspected bases:

* SEFI_QEC_Stack `7be66ac5d3e487196121dec136c3136ee5246963`.
* SEFI-PY `847a071351ed2b1c54e240fd9a520a1cce238178`.

The Stack's existing recovery compares transmitted/received identity bits;
its circuit syndrome is a placeholder. Its phase-flip routine returns bits
unchanged. Those paths remain intact and are excluded from physical reference
results. SEFI-PY defines QuantumState twice and has an order-dependent circular
import; the new example initializes field_sovereignty first. No existing
source or history was replaced. New standalone benchmark files use their own
MIT license; the parent research license remains unchanged.

### Actual validation

Environment: Windows, Python 3.14.7, NumPy 2.5.4, pytest 9.1.1, PCG64.
Commands below are written relative to the repository unless otherwise noted.

| Check | Actual local result |
| --- | --- |
| `python -m pytest benchmark_pipeline/tests -q` with writable workspace basetemp | 37 passed; final run 92.25 seconds |
| `python -m pytest tests -q` with repository root on PYTHONPATH | 25 existing Stack tests passed in 2.18 seconds |
| Editable package install, including console entry point | Built and installed sefi-quantum-benchmark 0.1.0 |
| `sefi-benchmark --help` | Successful |
| SEFI-PY `python integrations/quantum_benchmark_example.py` | Actual QuantumState normalized and round-trip passed |
| `python benchmark_pipeline/examples/reproduce.py <new-output>` | All four QEC runs and all five noisy-state export kinds completed |

The 37 tests include exhaustive explicit-statevector checks of every matched
error pattern for each code, independent density/Choi checks and analytic
limits. Five noisy-state export kinds are Haar, mixed, Bell, GHZ and discrete
random circuit, each with amplitude damping and optional labeled descriptors.
CI is configured on Python 3.10, 3.12 and 3.14; its remote status is recorded
separately rather than inferred from these local results.

### Measured reference results

Run: seed 42; 10,000 training trials and 10,000 test trials per code; p=0.1;
ideal one-round syndrome; independent matched Pauli errors. Minimum-weight and
training-only lookup gave identical counts in this run.

| Code | Identity logical failures | Minimum-weight / lookup failures | Minimum-weight rate (Wilson 95%) | Exact matched-model rate |
| --- | --- | --- | --- | --- |
| bit3 | 1018/10000 | 274/10000 | 2.74% (2.438–3.079%) | 2.8% |
| phase3 | 1018/10000 | 274/10000 | 2.74% (2.438–3.079%) | 2.8% |
| bit5 | 1000/10000 | 88/10000 | 0.88% (0.715–1.083%) | 0.856% |
| phase5 | 1000/10000 | 88/10000 | 0.88% (0.715–1.083%) | 0.856% |

All minimum-weight and lookup residuals returned to the code space. Identity
had 2691 codespace failures for n=3 and 4102 for n=5. Logical failure means
decoded root Pauli failure, not state infidelity. Paired bit/phase runs use
the same streams and mathematically equivalent matched error distributions,
so identical counts are expected; these are not independent replications.

[example-results.json](example-results.json) records raw counts, intervals,
input SHA-256 hashes, software versions and actual local scoring times.
Reproduce with `examples/reproduce.py`; timing values will differ. The
published seed makes these demos reproducible and **not blind evaluations**.
Do not reuse them as secret test data. Full generated outputs remain available
locally and can be regenerated; no evaluator secrets for an active challenge
are committed.

### Failed attempts and corrections

* First test run: 28 passed, 9 fixture setup errors because the sandbox could
  not create pytest's default temporary directories. Moving basetemp into the
  writable workspace produced 37 passes. These were environment errors, not
  suppressed test failures.
* First legacy suite invocation from the outer workspace: 7 collection errors
  due to missing repository import paths. With the correct repository root
  on PYTHONPATH, all 25 existing tests passed.
* Direct SEFI-PY core.quantum import initially failed on the existing circular
  import. Initializing core.field_sovereignty first fixed the example without
  changing or mocking legacy classes; actual adapter execution passed.
* Initial editable-install attempts failed on temporary-directory permissions
  and a missing local setuptools build backend. Installation with an explicit
  workspace temporary directory and isolated build dependencies succeeded.

### Interpretation and next questions

The reference rates agree with the known repetition-code model within
sampling uncertainty. This validates the narrow implementation, not a theory
of quantum geometry. Minimum-weight is optimal for this matched independent
noise at p<0.5. No SEFI decoder is implemented or compared. Future correlated
noise, circuit faults, general-Pauli codes and isolated decoder execution
require additional implementation and independent tests before claims.

For a practical research workflow, see [PUT_TO_WORK.md](PUT_TO_WORK.md).

### Public CI verification

The published implementation commit is
`aaad1aa1adfe358f468cfd7c371fb1f29259fcf5`. All three Linux CI jobs (Python
3.10, 3.12 and 3.14) completed successfully, including tests, installation and
CLI examples: [GitHub Actions run](https://github.com/JasonSEFIDEFI/SEFI_QEC_Stack/actions/runs/40046229740).
The companion SEFI-PY implementation commit
`c907b24ab91293bd542807b975e07f81b3be7cef` also passed its actual-class adapter
CI: [integration run](https://github.com/JasonSEFIDEFI/SEFI-PY/actions/runs/40046235231).
This section is a documentation-only follow-up; those outcomes refer to the
exact implementation commits above. Both updates were published on
`feat/quantum-benchmark-v1`; default branches were not changed or merged.
