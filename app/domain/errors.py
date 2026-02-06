# File: domain/errors.py
# Domain error types for animation engine. Defines standardized exceptions
# and error codes for consistent error handling across all layers.
# All Rights Reserved Arodi Emmanuel

from enum import Enum
from typing import Optional


class ErrorCode(Enum):
    """Standardized error codes for the animation engine."""
    NOT_FOUND = "NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    MISSING_ARGUMENT = "MISSING_ARGUMENT"
    INVALID_ARGUMENT = "INVALID_ARGUMENT"
    INVALID_TYPE = "INVALID_TYPE"
    INVALID_STATE = "INVALID_STATE"
    OPERATION_FAILED = "OPERATION_FAILED"


class AnimationError(Exception):
    """Base exception for all animation engine errors."""

    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.OPERATION_FAILED,
        details: Optional[dict] = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

    def __str__(self) -> str:
        return f"[{self.code.value}] {self.message}"


class NotFoundError(AnimationError):
    """Raised when a requested resource is not found."""

    def __init__(self, resource_type: str, name: str):
        super().__init__(
            message=f"{resource_type} not found: {name}",
            code=ErrorCode.NOT_FOUND,
            details={"resource_type": resource_type, "name": name}
        )


class AlreadyExistsError(AnimationError):
    """Raised when trying to create a resource that already exists."""

    def __init__(self, resource_type: str, name: str):
        super().__init__(
            message=f"{resource_type} exists: {name}",
            code=ErrorCode.ALREADY_EXISTS,
            details={"resource_type": resource_type, "name": name}
        )


class MissingArgumentError(AnimationError):
    """Raised when a required argument is missing."""

    def __init__(self, arg_name: str):
        super().__init__(
            message=f"Missing required: '{arg_name}'",
            code=ErrorCode.MISSING_ARGUMENT,
            details={"argument": arg_name}
        )


class InvalidArgumentError(AnimationError):
    """Raised when an argument has an invalid value."""

    def __init__(self, arg_name: str, reason: str):
        super().__init__(
            message=f"Invalid '{arg_name}': {reason}",
            code=ErrorCode.INVALID_ARGUMENT,
            details={"argument": arg_name, "reason": reason}
        )
