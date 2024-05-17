from enum import Enum


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

    errors = {
        "default": "I am placeholder, please change me.",
        "invalid_components": "Invalid components provided.",
        "unknown index": "Provided str index is invalid.",
        "invalid index": "Provided index is invalid.",
        "control not flet.Control": "Provided Control must be of type flet.Control",
    }

    def __init__(self, error_type: str):
        self.error_type = error_type if error_type in self.errors.keys() else "default"

    def __str__(self):
        return self.errors[self.error_type]


class Errors(Enum): ...


class Warnings(Enum): ...
