"""
Application-specific exceptions following HackSoft style guide.
"""


class ApplicationError(Exception):
    """
    Base exception for application errors.
    Used to distinguish between expected business logic errors and unexpected system errors.
    """

    def __init__(self, message: str, extra: dict = None):
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


class ValidationError(ApplicationError):
    """Raised when input validation fails."""
    pass


class NotFoundError(ApplicationError):
    """Raised when a requested resource is not found."""
    pass


class PermissionDeniedError(ApplicationError):
    """Raised when user doesn't have permission to perform an action."""
    pass
