class LogicalErrorRate:

    def calculate(
        self,
        total_trials,
        logical_failures
    ):

        if total_trials == 0:
            return 0.0

        return logical_failures / total_trials