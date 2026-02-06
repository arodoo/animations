# File: domain/dispatch_result.py
# Value Object representing the result of a command execution. Contains
# success status, optional data payload, and error message if failed.
# All Rights Reserved Arodi Emmanuel

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class DispatchResult:
    """Immutable result of command execution."""

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    command_name: Optional[str] = None

    @classmethod
    def ok(cls, data: Any = None, command: str = None) -> 'DispatchResult':
        """Create successful result."""
        return cls(success=True, data=data, command_name=command)

    @classmethod
    def fail(cls, error: str, command: str = None) -> 'DispatchResult':
        """Create failed result."""
        return cls(success=False, error=error, command_name=command)

    def __bool__(self) -> bool:
        return self.success
