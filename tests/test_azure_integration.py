from core.identity_types import Phi
from quantum.azure_bridge import AzureBridge
from quantum.azure_job import AzureSEFIJob
from quantum.azure_qec import azure_qec_pipeline


class FakeJob:
    id = "job-1"

    def __init__(self, results):
        self.results = results
        self.cancelled = False

    def get_status(self):
        return "Succeeded"

    def get_results(self):
        return self.results

    def cancel(self):
        self.cancelled = True


class FakeTarget:
    def __init__(self, results):
        self.job = FakeJob(results)
        self.submission = None

    def submit(self, **kwargs):
        self.submission = kwargs
        return self.job


class FakeWorkspace:
    def __init__(self, **kwargs):
        self.target = FakeTarget({"00010010001101000101": 4})

    def get_targets(self, **kwargs):
        return self.target

    def get_job(self, job_id):
        assert job_id == "job-1"
        return self.target.job


def test_azure_job_lifecycle_with_injected_workspace():
    bridge = AzureBridge("subscription", "resource-group", "workspace", "eastus", FakeWorkspace)
    job = AzureSEFIJob(bridge=bridge, target_name="simulator")

    assert job.connect()
    info = job.submit_register(type("Register", (), {"bits": [0] * 20})())

    assert info["job_id"] == "job-1"
    assert bridge.target.submission["input_data_format"] == "qasm"
    assert len(bridge.target.submission["input_data"].splitlines()) == 24
    assert job.result()["00010010001101000101"] == 4
    assert job.refresh()["status"] == "Succeeded"

    job.cancel()
    assert bridge.target.job.cancelled


def test_azure_pipeline_decodes_histogram_results():
    bridge = AzureBridge("subscription", "resource-group", "workspace", "eastus", FakeWorkspace)
    result = azure_qec_pipeline(
        Phi("1", "2", "3", "4", "5"),
        bridge=bridge,
        target_name="simulator",
    )

    assert result.rx_bits == [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1]
    assert result.phi_corr.__dict__ == Phi("1", "2", "3", "4", "5").__dict__
