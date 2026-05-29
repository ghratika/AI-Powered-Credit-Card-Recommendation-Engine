"""Domain-level exceptions."""


class InputValidationError(Exception):
    """Raised when user input fails validation (maps to HTTP 400)."""

    def __init__(self, message: str, *, field: str | None = None) -> None:
        self.field = field
        super().__init__(message)


class DomainError(Exception):
    """Base for orchestration errors mapped to HTTP responses."""

    code: str = "DOMAIN_ERROR"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class AANotConnectedError(DomainError):
    """AA connection required but not established (HTTP 422)."""

    code = "AA_NOT_CONNECTED"

    def __init__(
        self,
        message: str = "Connect Account Aggregator to get personalized recommendations.",
    ) -> None:
        super().__init__(message)


class NoEligibleCardsError(DomainError):
    """No cards pass eligibility filters (HTTP 404)."""

    code = "NO_ELIGIBLE_CARDS"

    def __init__(
        self,
        message: str = "No eligible credit cards found for your profile.",
    ) -> None:
        super().__init__(message)


class LLMServiceError(DomainError):
    """LLM provider or response parsing failure (HTTP 502)."""

    code = "LLM_ERROR"

    def __init__(self, message: str = "Recommendation service temporarily unavailable.") -> None:
        super().__init__(message)


class DataUnavailableError(DomainError):
    """Card catalog or AA data cannot be loaded (HTTP 503)."""

    code = "DATA_UNAVAILABLE"

    def __init__(self, message: str = "Required data files are unavailable.") -> None:
        super().__init__(message)
