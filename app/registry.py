# File: app/registry.py
# Command registry with decorator for auto-registration. Central dictionary
# maps command names to handler functions. Zero-friction command addition.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Callable, Dict

from domain.dispatch_result import DispatchResult


# Global command registry
_commands: Dict[str, Callable[[Dict[str, Any]], DispatchResult]] = {}


def register_command(name: str) -> Callable:
    """Decorator to register a command handler function."""
    def decorator(func: Callable[[Dict[str, Any]], DispatchResult]) -> Callable:
        _commands[name] = func
        return func
    return decorator


def get_command(name: str) -> Callable | None:
    """Get command handler by name."""
    return _commands.get(name)


def list_commands() -> list:
    """List all registered command names."""
    return list(_commands.keys())


def clear_commands() -> None:
    """Clear all commands (for testing)."""
    _commands.clear()


def get_registry() -> Dict[str, Callable]:
    """Get the raw registry dict."""
    return _commands
