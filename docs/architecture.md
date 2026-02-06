# Architecture Guide

## Overview

The animation engine uses **Dynamic Dispatch** to execute commands from
plain-text instructions without conditional chains.

## Layers (DDD Pattern)

### Domain Layer (`domain/`)
Pure business entities without dependencies.

- `DispatchResult`: Command execution result with success/error

### Application Layer (`app/`)
Business logic and command orchestration.

- `registry.py`: Command registration via decorators
- `dispatcher.py`: Instruction processing
- `commands/`: Individual command implementations
- `core/`: High-level workflows (e.g., `logic.py`)

## Command Registration

```python
from app.registry import register_command
from domain.dispatch_result import DispatchResult

@register_command('my_command')
def my_command(args: Dict[str, Any]) -> DispatchResult:
    # Implementation
    return DispatchResult.ok({'result': 'value'}, command='my_command')
```

## Dispatch Flow

```
Instruction -> Dispatcher -> Registry Lookup -> Command Execute -> Result
```

## Mock System

The `tests/mocks/` folder provides complete Blender API mocks:

| Mock | Purpose |
|------|---------|
| `MockObject` | Scene object with transforms |
| `AnimationData` | Keyframe storage |
| `MaterialsCollection` | Material management |
| `MockCamera/Light` | Camera and light data |

## Extensibility

Adding new commands:

1. Create file in subpackage of `app/commands/`
2. Use `@register_command` decorator
3. Import in the subpackage `__init__.py`
4. Add tests in `tests/e2e/`

## Quality Rules

| Rule | Limit |
|------|-------|
| Lines per file | 120 max |
| Chars per line | 80 max |
| Files per folder | 6 max |
