# File: app/dispatcher.py
# Core dispatcher that processes instruction lists without if/elif chains.
# Looks up commands in registry and executes them blindly. Command agnostic.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List

from app.domain.dispatch_result import DispatchResult
from .registry import get_command


def dispatch_single(instruction: Dict[str, Any]) -> DispatchResult:
    """Dispatch a single instruction to its command handler."""
    cmd_name = instruction.get('cmd')
    args = instruction.get('args', {})

    if not cmd_name:
        return DispatchResult.fail("Missing 'cmd' key in instruction")

    handler = get_command(cmd_name)
    if not handler:
        return DispatchResult.fail(
            f"Unknown command: {cmd_name}",
            command=cmd_name
        )

    try:
        return handler(args)
    except Exception as e:
        return DispatchResult.fail(str(e), command=cmd_name)


def dispatch_batch(instructions: List[Dict[str, Any]]) -> List[DispatchResult]:
    """Dispatch a batch of instructions in order."""
    results = []
    for instruction in instructions:
        result = dispatch_single(instruction)
        results.append(result)
    return results


def dispatch_batch_stop_on_error(
    instructions: List[Dict[str, Any]]
) -> List[DispatchResult]:
    """Dispatch batch, stopping on first error."""
    results = []
    for instruction in instructions:
        result = dispatch_single(instruction)
        results.append(result)
        if not result.success:
            break
    return results
