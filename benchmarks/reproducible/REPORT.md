# Reproducible SEFI/QEC experiment report — October 23, 2026

## Finding

A conditional computational advantage was confirmed for spatial regularization over independent per-qubit calibration. It is also achieved by conventional graph regularization. No SEFI-specific advantage over a matched conventional method was established in this study.

On 200 fresh calibration datasets, seven-qubit repetition decoding with ten known-probe calibration samples per qubit had average exact logical error **0.0445%** for independent estimates and **0.0349%** for graph smoothing: **21.66% relative reduction**. The paired absolute error-rate difference was -9.64193675e-05, with a seed-bootstrap 95% interval [-0.00012828883269388423, -6.882113843727838e-05]. Conventional graph regularization tied the geometric implementation using an independently computed eigendecomposition.

The counterexample matters: alternating noise increased error from **0.0901%** to **0.2170%** under the same smoothing. This is a conditional prior benefit, not a universal decoder gain. Confirmation used fresh random seeds, not a separate team or independently written complete simulator. Its condition was selected after exploration; it is not an externally preregistered study.

## Implemented facts from inspected source

- SEFI_QEC_Stack source commit: `7be66ac5d3e487196121dec136c3136ee5246963`.
- SEFI-PY source commit: `847a071351ed2b1c54e240fd9a520a1cce238178`.
- The QEC stack encodes five decimal fields into twenty classical bits. `simple_recover(tx_bits, rx_bits)` copies the transmitted truth into the received message. `SyndromeExtractor.extract` also compares transmitted and received messages. These are oracle demonstrations, not syndrome-only physical QEC. `phase_flip` returns its input unchanged. The bit randomizer called depolarizing is a classical channel, not a full Pauli state simulation.
- SEFI-PY Evolution implements `point - d_N*N - d_B*B`; its interpretation as normal projection assumes an orthonormal frame and supplied displacements. The new circle experiment estimates the nearest circle point from the noisy observation and known manifold, without passing the true generating angle to a decoder.
- SEFI-PY's existing pilot-assisted bosonic estimator is a conventional Gaussian posterior mean. Sixteen probe modes share payload displacement; their resource cost is part of the assumption.
- The spherical source implements an uncalibrated dimensionless two-field fixed-charge model at Q=100000, lambda=12. This is a model calculation, not a particle measurement.
- AST import inventories and source SHA-256 hashes are saved in `source_audit.json`. Existing SEFI-PY core requirements declare pytest while tested modules also import NumPy. The stack has no mandatory runtime dependencies declared and an optional Azure dependency; no Azure jobs were submitted. New experiment dependency versions are pinned separately.

## Mathematical derivations, not empirical claims

For a repetition code, adjacent parity syndrome is s_i=e_i XOR e_(i+1). Its two compatible errors are e and its bitwise complement. Choosing the more probable compatible error minimizes expected logical 0/1 loss when the noise prior is known. No reparameterization of the same information can beat that exact Bayes decision under that prior and loss. For odd distance n and iid bit error p, logical X failure is sum_(k>(n/2)) binomial(n,k) p^k (1-p)^(n-k); exhaustive enumeration tests match this expression.

For independent heterogeneous noise, log odds w_i=log((1-p_i)/p_i) turn maximum likelihood into weighted geometric distance. This gives the calibrated geometric decoder and the conventional likelihood decoder the same decision. Correlated noise requires the joint probability; the benchmark explicitly uses its full enumerated distribution.

The graph estimator minimizes ||z-y||^2 + lambda ||D z||^2 in fitted log-odds coordinates. Its unique solution is (I+lambda D^T D)^(-1)y because the Hessian is positive definite. This is conventional graph regularization. The penalty lambda=2 was fixed before evaluation, not optimized on the reported test outcomes.

For orthonormal normal columns A, correction y-A A^T(y-q) removes the measured normal component. With a known unit circle and frame at the observation's nearest point, the repository formula equals conventional nearest-circle projection. It cannot identify an unknown tangential displacement from one observation. Nonorthogonal frames instead require the Gram matrix A^T A; this is an assumption boundary, not a demonstrated failure under the formula's intended orthonormal conditions.

Projected Euler preserves oscillator radius but rotates by atan(dt) per step rather than dt. Energy preservation therefore does not imply correct phase; accumulated phase error is order dt^2. RK4 and midpoint supply convergence references.

## Hypotheses and controls

1. Arbitrary geometric weights might improve decoding: tested with a fixed spatial metric and temporal surface-code weight factors 0.5 and 2. These choices are exploratory engineering hypotheses, not uniquely derived SEFI predictions.
2. Smooth geometry could reduce calibration variance: tested against pooled, independent Jeffreys, and conventional graph-regularized estimates, followed by fresh-seed confirmation and an alternating-field negative control.
3. Normal projection could improve noisy trajectory recovery: tested against the identical conventional projection, wrong manifold radius, inaccurate frames, tangent noise, radial noise, Gaussian and heavy-tailed noise.
4. Stable energy could imply accurate integration: checked against exact oscillator motion and time-step refinement.
5. Existing spherical critical points might survive discretization and boundary changes: re-solved on four grids and evaluated finite-grid Hessian sectors l=0 through 4. This is not a nonlinear or continuum stability theorem.

## Runs actually completed

| Family | Completed work | Scope |
|---|---|---|
| Repetition QEC | 45 noise/distance conditions, 180 decoder cells; 2,700,000 sampled error patterns and 10,800,000 decoder evaluations | Distances 3,5,7; iid, heterogeneous, and adjacent-pair mixture; exact enumeration plus three paired seeds |
| Finite calibration | 7,200 method/seed/deployment records across 36 conditions | 50 seeds per condition; budgets 10,50,500; smooth/alternating noise; matched, reversed, burst deployments |
| Confirmation | 1,600 method/seed records across two conditions | 200 fresh calibration datasets per condition; exact held-out risk; paired bootstrap |
| Surface memory | 36 noisy stabilizer circuits, 180 decoder cells; 1,080,000 circuit shots | Distances 3,5,7; X/Z memories; three circuit noise levels; uniform and measurement-heavy noise; five decoder choices |
| Geometric recovery | 96 method/noise cells; 480,000 generated noisy points, 2,880,000 estimates | Four noise families, four scales, six methods; same observations for every method |
| Numerical convergence | 20 deterministic runs | Five time steps, Euler, projected Euler, midpoint, RK4; exact harmonic-oscillator reference |
| Bosonic reproduction | 560,000 held-out payload trials plus 280,000 calibration injections | Existing seven-noise-level protocol with 20 seeds; physical channel and cutoff checks |
| Spherical reproduction | Four fresh relaxations plus 60 finite-grid curvature blocks | h=0.8,0.4,0.2 at L=60; h=0.2 at L=80; five angular sectors, three blocks each |

These are evaluated sample counts, not a claim that every sample across every condition is statistically independent. Common random numbers deliberately pair methods and sometimes conditions.

## Observed outcomes

- In the known-prior repetition benchmarks, calibrated geometry and conventional likelihood have the same exact logical risk in all 45 conditions. The arbitrary metric can hurt. Exact rates are provided alongside sampling intervals, so zero observed failures are not represented as proof of zero risk.
- Surface-code example (distance 5, X memory, p=.003 uniform circuit noise, five rounds): ordinary matched MWPM had 102/30000 failures; conventional correlated matching had 76/30000. All other conditions and geometric results are retained, not only this illustrative comparison. No geometry-specific improvement was found from the two fixed temporal weightings.
- At isotropic Gaussian coordinate noise sigma=.1, circle-projection MSE was 0.010049282, versus 0.029973967 without correction. The repository normal correction and conventional nearest-circle estimator agree to floating-point precision. This demonstrates the value of a known constraint, not a uniquely SEFI mechanism.
- A deliberately nonorthogonal frame produced a normal residual of 0.579986 for the unadjusted formula, versus 1.78e-16 with a Gram solve. The original orthonormal-frame condition must be respected.
- Bosonic primary sigma=.2 reproduction: unconditional entanglement fidelity was 0.887923216 for ML and 0.952117975 for both geometry and conventional posterior. Paired improvement over ML was 0.064194759, 95% seed-bootstrap interval [0.063584543,0.064762980]. Matching the prior removes the apparent geometry-specific gain. Physical-channel completeness error was below 1e-15; small negative Choi eigenvalues were roundoff-scale. Distribution-shift controls, leakage, timing, and oscillator cutoff checks are retained.
- All four fresh spherical relaxations reached residual below 1e-7. Energy/charge at h=.4 and .2, L=60 was 1.377361076 and 1.377366536; expanding L to 80 changed the latter by about 4.06e-12. These lie below the model's free-field mass sqrt(2), a conditional energetic comparison. Near-zero symmetry directions and positive sampled curvatures do not prove global, nonlinear, or all-mode stability.

## Validation, uncertainty, and performance

The six separately executed test suites all passed: [{"suite": "qec", "exit_code": 0, "tail": ["30 passed in 2.18s"]}, {"suite": "core", "exit_code": 0, "tail": ["33 passed in 4.87s"]}, {"suite": "evolution", "exit_code": 0, "tail": ["46 passed in 56.71s"]}, {"suite": "bosonic", "exit_code": 0, "tail": ["19 passed in 3.85s"]}, {"suite": "spherical", "exit_code": 0, "tail": ["3 passed in 9.68s"]}, {"suite": "geometry", "exit_code": 0, "tail": ["3 passed in 5.13s"]}]. Surface noiseless-memory and identity-weight reconstruction smoke checks also passed before its sweep. Primary QEC and geometric raw arrays were regenerated and compared exactly: [{"suite": "qec", "arrays_compared": 180, "identical": true}, {"suite": "geometry", "arrays_compared": 96, "identical": true}].

Logical failure intervals are 95% Wilson binomial intervals. Paired shot-level differences include their standard errors. Calibration intervals bootstrap independent calibration seeds; exact evaluation removes test-shot uncertainty but not uncertainty from calibration/model selection. Geometric MSE tables provide paired standard errors and per-seed values; heavy-tail uncertainty may converge slowly. Exploratory tables have no familywise significance guarantee; the explicitly separated confirmation uses fresh seeds. Model uncertainty and hardware mismatch are not included in these intervals.

Every sweep records wall-clock costs; surface data separately record sampling, all-decoder setup, decode throughput, and detector/qubit counts. The existing bosonic timing protocol rotates method order over 51 repeats. New timings are local machine observations affected by concurrent workloads, batching, setup, and library versions, not claims of asymptotic or hardware speedup. Python peak memory and energy consumption were not measured. Simulator qubit indexing/counts are not a hardware resource estimate.

## Reproduction

Use Python 3.14.7 for the captured environment. Install `requirements-core.lock.txt` in the QEC benchmark for the NumPy reference runs; use the separate `requirements-surface.lock.txt` environment for surface runs. SEFI-PY experiments use `research/2026-10-23/requirements.lock.txt`. The original package declarations were inspected before installing optional simulator dependencies. Keep the two environments separate because their captured NumPy/Matplotlib versions differ.

From SEFI_QEC_Stack root:
```
python benchmarks/reproducible/run.py
python benchmarks/reproducible/calibration.py
python benchmarks/reproducible/calibration.py --confirm
python benchmarks/reproducible/surface.py
python -m pytest -q -p no:cacheprovider tests benchmarks/reproducible/test_reference.py
```
From SEFI-PY root:
```
python research/2026-10-23/geometric-recovery/run.py
python SEFI-PY/benchmarks/displacement_recovery/run_benchmark.py --output research/2026-10-23/bosonic-reproduction/results
python research/2026-10-23/spherical-reproduction/run.py
```
The spherical source deliberately refuses to overwrite existing run tags; reproduce into a fresh output folder or retain the old folder under another name before rerunning. Core geometric/QEC scripts accept `--output` for separate reproduction folders. Stim reproducibility is version- and batch-sensitive: retain the saved circuits, detector error models, seed, shot count, and library version. Saved detector events are little-endian packed; logical observations are scoring-only.

## Failures and limitations

{
  "initial_git_clone": "Sandbox DNS restriction; succeeded with expanded permissions.",
  "evolution_tests": "Initial sandbox run: 11 failures, 35 passes, 2 errors due to temporary-directory permissions. Workspace temp rerun: 4 failures, 42 passes due to loopback restrictions. Final expanded-permission run: all 46 passed.",
  "spherical_test_invocation": "One requested test filename did not exist, so that invocation ran zero tests; corrected invocation passed all three existing curvature tests.",
  "environment_setup": "Two imports attempted before optional installation finished failed; surface suite subsequently ran after installation.",
  "v_sync": "Upstream additions collided with stashed local files; differing local versions and conflict copies retained beside repositories; all seven upstream comparisons ended at 0 ahead/0 behind, no unresolved conflicts.",
  "scientific_negative_results": "Geometric weighting did not beat calibrated conventional equivalents; arbitrary metric weights and inaccurate normal frames can worsen recovery. No hardware run or empirical foundational validation."
}

No hardware, cloud quantum service, external experimental dataset, or unpublished source outside the authorized repositories was used. Stim generated circuits are reference fixtures, not a realistic device calibration. Repetition results protect only the X-error channel; separate Pauli enumeration explicitly shows residual logical Z errors. No surface-code threshold fit is claimed from three distances and three noise values. No complete SEFI physical theory has been validated or falsified by these algorithm comparisons.

## Next experiments, with stopping criteria

1. Make calibration-budget efficiency the primary claim. Compare graph smoothing against pooled, independent, tuned conventional graph/kernel estimators with nested training-only tuning. Freeze a task distribution before confirmatory evaluation. Require a paired interval excluding zero against the strongest fair baseline and report all predefined tasks.
2. Replace synthetic smooth noise with an authorized public detector dataset, train only on its calibration split, then evaluate untouched acquisition periods. Seek a falsifiable prediction of spatial structure from SEFI equations rather than choosing a helpful metric afterward.
3. Add learned measurement-noise/correlation parameters to surface decoding, with equal calibration budgets and conventional correlated matching. Fixed ad hoc edge weighting already failed to establish a gain here.
4. Test erasure flags and soft analog measurements only when both decoders receive exactly the same side information and sensing costs are counted.
5. For dynamics, derive a justified geometric integrator and compare against symplectic and constraint-preserving conventional methods at matched error and function evaluations. Energy preservation alone is insufficient.
6. For the spherical branch, test more angular sectors, real-time perturbations, charge variation, full coupled dynamics, and continuum error bounds. Binding energy and finite-grid curvature remain conditional model results.

The exhaustive space of all possible advantages is not finite. Failure of these variants does not prove no advantage is possible; a favorable subset does not establish a broad advantage. A defensible result is the specific conditional gain above, together with its conventional equivalence and counterexample.

## Primary software references

- [Stim source and documentation](https://github.com/quantumlib/Stim)
- [PyMatching API and circuit-level example](https://pymatching.readthedocs.io/en/stable/api.html)
- [Stim reference circuits](https://github.com/quantumlib/Stim/blob/main/doc/file_format_stim_circuit.md)
