import os
from typing import Any


try:
    from azure.quantum import Workspace
except ImportError:
    Workspace = None


AZURE_AVAILABLE = Workspace is not None


class AzureBridge:

    def __init__(
        self,
        subscription_id: str | None = None,
        resource_group: str | None = None,
        workspace_name: str | None = None,
        location: str | None = None,
        workspace_factory: Any | None = None,
    ):

        self.subscription_id = subscription_id or os.getenv("AZURE_QUANTUM_SUBSCRIPTION_ID")
        self.resource_group = resource_group or os.getenv("AZURE_QUANTUM_RESOURCE_GROUP")
        self.workspace_name = workspace_name or os.getenv("AZURE_QUANTUM_WORKSPACE_NAME")
        self.location = location or os.getenv("AZURE_QUANTUM_LOCATION")
        self.default_target_name = os.getenv("AZURE_QUANTUM_TARGET")
        self.default_provider_id = os.getenv("AZURE_QUANTUM_PROVIDER_ID")
        self.workspace_factory = workspace_factory or Workspace
        self.workspace = None
        self.target = None
        self.target_name = None
        self.provider_id = None
        self.last_error = None

        self.connected = False

    def connect(self, target_name: str | None = None, provider_id: str | None = None):

        if self.workspace_factory is None:
            self.last_error = "azure-quantum is not installed"
            return False

        missing = [
            name
            for name, value in {
                "subscription_id": self.subscription_id,
                "resource_group": self.resource_group,
                "workspace_name": self.workspace_name,
                "location": self.location,
            }.items()
            if not value
        ]
        if missing:
            self.last_error = f"Missing Azure Quantum configuration: {', '.join(missing)}"
            return False

        try:
            self.workspace = self.workspace_factory(
                subscription_id=self.subscription_id,
                resource_group=self.resource_group,
                name=self.workspace_name,
                location=self.location,
            )
            target_name = target_name or self.default_target_name
            provider_id = provider_id or self.default_provider_id
            if target_name:
                self.select_target(target_name, provider_id)
            self.connected = True
            self.last_error = None
            return True
        except Exception as error:
            self.workspace = None
            self.connected = False
            self.last_error = str(error)
            return False

    def select_target(self, target_name: str, provider_id: str | None = None):
        if self.workspace is None:
            raise RuntimeError("Connect to Azure Quantum before selecting a target")

        targets = self.workspace.get_targets(
            name=target_name,
            provider_id=provider_id,
        )
        if isinstance(targets, (list, tuple)):
            if not targets:
                raise LookupError(f"Azure Quantum target not found: {target_name}")
            self.target = targets[0]
        else:
            self.target = targets
        self.target_name = target_name
        self.provider_id = provider_id
        return self.target

    def submit(self, input_data: str, **kwargs):
        if self.target is None:
            raise RuntimeError("Select an Azure Quantum target before submitting a job")
        return self.target.submit(input_data=input_data, **kwargs)

    def get_job(self, job_id: str):
        if self.workspace is None:
            raise RuntimeError("Connect to Azure Quantum before retrieving a job")
        return self.workspace.get_job(job_id)


    def status(self):

        return {
            "azure_available": AZURE_AVAILABLE,
            "connected": self.connected,
            "target": self.target_name,
            "provider_id": self.provider_id,
            "last_error": self.last_error,
        }