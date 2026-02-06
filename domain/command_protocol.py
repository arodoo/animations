# File: domain/command_protocol.py
# Protocol definition for commands in the dispatch system. All commands must
# implement execute() method receiving args dict and returning DispatchResult.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, Protocol

from .dispatch_result import DispatchResult


class CommandProtocol(Protocol):
    """Protocol that all commands must follow."""

    @staticmethod
    def execute(args: Dict[str, Any]) -> DispatchResult:
        """Execute command with given arguments."""
        ...
