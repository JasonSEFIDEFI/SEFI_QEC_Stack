SEFI‑QEC Stack
A modular quantum‑error‑correction engine built on geometric identity principles from the SEFI canon. The stack provides stabilizer acquisition, syndrome transport, multi‑decoder correction, Pauli‑frame routing, and warp‑residual geometric analysis in a clean, dependency‑free architecture. All directories include __init__.py to support package‑level imports and orchestrated pipeline execution.

Purpose
The SEFI‑QEC Stack serves as the dedicated quantum‑error‑correction engine for SEFI and GWFM research. It is designed for real‑time decoding pipelines, low‑latency correction, deterministic transport, and geometric consistency across worldline‑based field models. The architecture demonstrates autonomous systems‑level development suitable for high‑level technical evaluation.

Features
Stabilizer parity evaluation

Syndrome extraction and transport

Majority‑vote and stabilizer‑energy decoders

Pauli‑frame consistency and correction routing

Warp‑residual geometry analysis

Unified stack.py orchestrator for full‑pipeline coordination

Package‑ready directory structure using __init__.py in all modules

Repository Structure
Code
qec_stack/
│
├── stack.py
│
├── stabilizers/
│   ├── __init__.py
│   ├── stabilizer_core.py
│   └── parity_eval.py
│
├── syndromes/
│   ├── __init__.py
│   ├── extract.py
│   └── transport.py
│
├── decoders/
│   ├── __init__.py
│   ├── majority_vote.py
│   └── energy_min.py
│
├── pauli_frame/
│   ├── __init__.py
│   └── frame_router.py
│
└── warp_geometry/
    ├── __init__.py
    └── residual_analysis.py
Usage
Import the stack as a package:

python
from qec_stack import stack

engine = stack.QECStack()
engine.run()
Call individual modules directly:

python
from qec_stack.stabilizers import parity_eval
from qec_stack.decoders import majority_vote
License
MIT License.

Azure Quantum
-------------
Install the optional Azure integration with:

    pip install -e ".[azure]"

Set these workspace variables before running an Azure job:

    AZURE_QUANTUM_SUBSCRIPTION_ID
    AZURE_QUANTUM_RESOURCE_GROUP
    AZURE_QUANTUM_WORKSPACE_NAME
    AZURE_QUANTUM_LOCATION
    AZURE_QUANTUM_TARGET
    AZURE_QUANTUM_PROVIDER_ID (optional)

Authenticate through the standard Azure credential chain, for example with
`az login`. The Python integration generates a 20-qubit OpenQASM circuit and
supports submission, status refresh, result retrieval, and cancellation:

    from quantum.azure_job import AzureSEFIJob
    from quantum.circuits import build_circuit

    job = AzureSEFIJob()
    job.connect()
    job.submit_register(build_circuit(phi))
    job.refresh()
    results = job.result()

The Q# source files are under `quantum/qsharp/` and are included as package
data for downstream QDK workflows.

Status
Active development as part of the SEFI and GWFM research platform.