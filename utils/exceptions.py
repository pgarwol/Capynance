from enum import StrEnum


class Errors(StrEnum):
    INVALID_COMPONENT = "Invalid component has been provided."
    INVALID_CONTROL_TYPE = "Provided Control must be of type flet.Control."
    USER_NOT_FOUND = "User could not be initialized."


class Warnings(StrEnum):
    INVALID_INDEX = "Provided index is invalid."


class CapynanceException(Exception):
    """
    Summary:
    Custom exception class for Capynance.

    Explanation:
    This class defines a custom exception with specific error types and corresponding error messages. It allows raising exceptions with predefined error types.

    Args:
    - error_type: A string representing the type of error to raise.

    Returns:
    - The error message corresponding to the specified error type.
    """

    _DEFAULT_ERROR = "Error has not been specified"

    def __init__(self, error_type: str):
        self.error_type = error_type if error_type in Errors else self._DEFAULT_ERROR

    def __str__(self):
        return self.error_type
