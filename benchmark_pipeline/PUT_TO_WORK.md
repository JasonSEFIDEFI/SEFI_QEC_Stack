# Putting the pipeline to work for Jason's research

## Start with a stable public reference

Run the reproducibility example once and preserve its output and package
revision. Share the exported state NPZ files and decoder JSONL files so others
can test their tools against the same inputs. Include the README's state,
noise and metric conventions. All standard generators work without SEFI
geometry. Call them seeded synthetic quantum datasets, not hardware qubits.

```sh
python examples/reproduce.py runs/reference-v1
```

Run that from `benchmark_pipeline/` after installation. Published seed 42 makes
this a reproducibility demo; it is not a secret test set.

## Test a specific idea against controls

Write the proposed decoder as a function accepting only `DecoderInput` and
returning n binary correction bits. Train any parameters using training data
only. Compare against identity, minimum-weight and training-only lookup on a
fresh held-out dataset. Record the exact hypothesis, noise assumptions, seed
handling, sample count and comparison metric before inspecting test results.

For independent matched X/Z errors with p<0.5, minimum-weight is already
optimal for these repetition codes. A new geometric feature should not be
expected to beat it. A result claiming improvement would first require a
leakage and scoring audit. These models are useful controls, not evidence of
new physics. An interesting future study could use independently justified
correlated noise or additional physical measurements, with those changes
declared and validated before decoder comparison.

The optional descriptors currently summarize conventional state purity and
entropy. They are exploratory state-analysis features, not a SEFI decoder.
There is no SEFI performance result to publish from the present demo.

## Keep every outcome in the public research record

For each experiment, add a dated ledger entry with the research question,
revision, environment, generator configuration, train/test policy, commands,
checksums, measured counts, uncertainty and limitations. Include failures and
null outcomes. Link the entry from the relevant manuscript version, regardless
of review or publication outcome. Avoid copying private reviewer/editor
correspondence into this software ledger.

Keep active challenge seeds and test truth private. After evaluation closes,
release the evaluator provenance for reproduction and use a fresh seed for
the next held-out test. A malicious decoder needs separate process/container
isolation; the callback API alone cannot enforce secrecy.

## Use it in publication and collaboration

The immediate deliverable is a reproducible software/methods supplement:
generation methods, physical checks, code definitions, decoder interface,
baseline results and explicit limits. Collaborators can submit decoders
against the same schema. Claims about SEFI dynamics, hardware performance,
general QEC or publication acceptance require additional evidence and are
outside the present pipeline. Cite the actual repository commit; a DOI or
archival release would be a separate publication step.
