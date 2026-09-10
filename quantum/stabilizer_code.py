from typing import Any, Callable, Dict, List
from quantum.logical_register import LogicalPhiRegister


class SEFIStabilizerCode:
    """
    Geometric stabilizer structure for SEFI logical registers.
    Provides constraint checks and evaluation hooks.
    """

    def __init__(self) -> None:
        self.stabilizers: List[Dict[str, Any]] = []

    def add(self, name: str, check: Callable[[LogicalPhiRegister], bool]) -> None:
        """
        Add a stabilizer check function.

        name: human-readable label
        check: callable taking LogicalPhiRegister -> bool
        """
        self.stabilizers.append(
            {
                "name": name,
                "check": check,
            }
        )

    def evaluate(self, register: LogicalPhiRegister) -> Dict[str, bool]:
        """
        Evaluate all stabilizers against a logical register.
        Returns a dict of {name: passed}.
        """
        results: Dict[str, bool] = {}

        for stabilizer in self.stabilizers:
            results[stabilizer["name"]] = stabilizer["check"](register)

        return results
