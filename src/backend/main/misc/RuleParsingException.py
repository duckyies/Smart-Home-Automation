class RuleParsingException(Exception):

    def __init__(self, message: str = "Rule parsing error", cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        return f"RuleParsingException: {super().__str__()}"