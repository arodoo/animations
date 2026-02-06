# File: app/commands/result_helpers.py
# Helper functions for creating standardized DispatchResult responses.
# Eliminates 80-char violations and provides consistent error messages.
# All Rights Reserved Arodi Emmanuel

from app.domain.dispatch_result import DispatchResult
from app.domain.errors import ErrorCode


def ok(data: dict, command: str) -> DispatchResult:
    """Create successful result with data."""
    return DispatchResult.ok(data, command=command)


def fail_not_found(
    name: str,
    command: str,
    resource: str = "Object"
) -> DispatchResult:
    """Create failure result for resource not found."""
    return DispatchResult.fail(
        f"{resource} not found: {name}",
        command=command
    )


def fail_missing(arg: str, command: str) -> DispatchResult:
    """Create failure result for missing argument."""
    return DispatchResult.fail(
        f"Missing '{arg}'",
        command=command
    )


def fail_missing_args(command: str) -> DispatchResult:
    """Create failure result for missing multiple arguments."""
    return DispatchResult.fail("Missing arguments", command=command)


def fail_exists(name: str, command: str) -> DispatchResult:
    """Create failure result for resource already exists."""
    return DispatchResult.fail(f"Exists: {name}", command=command)


def fail_invalid(
    arg: str,
    reason: str,
    command: str
) -> DispatchResult:
    """Create failure result for invalid argument."""
    return DispatchResult.fail(
        f"Invalid '{arg}': {reason}",
        command=command
    )


def fail_error(message: str, command: str) -> DispatchResult:
    """Create failure result with custom message."""
    return DispatchResult.fail(message, command=command)
