from quantum.azure_bridge import AzureBridge


class AzureSEFIJob:
    """
    Azure Quantum submission wrapper.
    """

    def __init__(self, bridge=None, target_name=None, provider_id=None, shots=100):

        self.bridge = bridge or AzureBridge()
        self.target_name = target_name
        self.provider_id = provider_id
        self.shots = shots
        self.job = None

    def connect(self):

        return self.bridge.connect(self.target_name, self.provider_id)

    def status(self):

        return self.bridge.status()

    def submit_register(self, register, name="sefi-qec-job", shots=None):

        if len(register.bits) != 20:
            raise ValueError("SEFI Azure jobs require a 20-bit register")

        if not self.bridge.connected:
            raise RuntimeError("Connect to Azure Quantum before submitting a register")

        if self.bridge.target is None:
            raise RuntimeError("Select an Azure Quantum target before submitting a register")

        qasm = self._register_to_qasm(register.bits)
        self.job = self.bridge.submit(
            qasm,
            name=name,
            shots=shots or self.shots,
            input_data_format="qasm",
        )
        return self.job_info()

    def job_info(self):

        if self.job is None:
            return {"submitted": False, "status": "not_submitted"}

        job_id = getattr(self.job, "id", None)
        status = self._job_status(self.job)
        return {
            "submitted": True,
            "job_id": job_id,
            "status": status,
        }

    def refresh(self):

        if self.job is None:
            raise RuntimeError("No Azure Quantum job has been submitted")
        job_id = getattr(self.job, "id", None)
        self.job = self.bridge.get_job(job_id)
        return self.job_info()

    def result(self):

        if self.job is None:
            raise RuntimeError("No Azure Quantum job has been submitted")
        return self.job.get_results()

    def cancel(self):

        if self.job is None:
            raise RuntimeError("No Azure Quantum job has been submitted")
        self.job.cancel()
        return self.job_info()

    @staticmethod
    def _job_status(job):
        if hasattr(job, "get_status"):
            return job.get_status()
        if hasattr(job, "status"):
            return job.status
        if hasattr(job, "details") and getattr(job.details, "status", None):
            return job.details.status
        return "submitted"

    @staticmethod
    def _register_to_qasm(bits):

        lines = [
            "OPENQASM 2.0;",
            'include "qelib1.inc";',
            "qreg q[20];",
            "creg c[20];",
        ]
        lines.extend(f"x q[{index}];" for index, bit in enumerate(bits) if bit)
        lines.extend(f"measure q[{index}] -> c[{index}];" for index in range(20))
        return "\n".join(lines)
