# Architecture

## Overview

The engine turns plain-dict instructions into Blender operations through a
registry-based dynamic dispatcher. The same command definitions run against
the real Blender Python API (`bpy`) or a lightweight mock — with zero
conditional logic in the commands themselves.

```
Instruction dict
    └─▶ Dispatcher ──▶ Registry lookup ──▶ Command fn ──▶ DispatchResult
                                                ↑
                                          Bridge (bpy / mock)
```

---

## DDD Layers

### Domain — `app/domain/`
Pure business entities with no external dependencies.

- **`DispatchResult`** — typed result: `success`, `data`, `error`, `command_name`
- **`errors.py`** — typed exception hierarchy (`AnimationError` → subclasses)

### Application — `app/`
Orchestration and command logic.

- **`kernel/registry.py`** — `@register_command` decorator; command lookup
- **`kernel/dispatcher.py`** — `dispatch_single` / `dispatch_batch`
- **`commands/`** — individual command implementations, grouped by concern
- **`scene/`** — reusable scene helpers (procedural starfields, etc.)

### Infrastructure — `app/infra/`
Isolates the Blender dependency.

- **`bridge.py`** — attempts `import bpy`; falls back to mock automatically
- Exports `data`, `ops`, `context`, `is_mock()` used by every command

---

## SOLID Application

| Principle | Where applied |
|-----------|---------------|
| **S** — Single Responsibility | One command per function; commands grouped by domain area |
| **O** — Open / Closed | New commands add a file + registration; no existing code changes |
| **L** — Liskov | Mock implements the same interface as real `bpy` objects |
| **I** — Interface Segregation | Commands import only `data`, `ops`, or `context` as needed |
| **D** — Dependency Inversion | Commands depend on the bridge abstraction, never on `bpy` directly |

---

## Command Registration

```python
from app.kernel.registry import register_command
from app.domain.dispatch_result import DispatchResult

@register_command('my_command')
def my_command(args: dict) -> DispatchResult:
    name = args.get('name')
    return DispatchResult.ok({'name': name}, command='my_command')
```

Registration is triggered by import. Each `commands/*/` subpackage imports
its modules in `__init__.py`; `app/commands/__init__.py` imports all
subpackages; scenes import `app.commands` to bootstrap everything.

---

## Bridge Pattern

```python
# app/infra/bridge.py
try:
    import bpy as _bpy          # real Blender
except ImportError:
    from tests.mocks.core import bpy_mock as _bpy   # offline mock

data    = _bpy.data
ops     = _bpy.ops
context = _bpy.context

def is_mock() -> bool: ...
```

Commands that need Blender-specific behaviour branch with `is_mock()`:

```python
if is_mock():
    ops.camera.add_camera(location=location)   # mock path
else:
    ops.object.camera_add(location=location)   # real Blender path
```

---

## Error Handling

### Exception hierarchy (`app/domain/errors.py`)

```
AnimationError
├── NotFoundError          # object / material / modifier not found
├── AlreadyExistsError     # duplicate name
├── MissingArgumentError   # required arg absent
├── InvalidArgumentError   # arg present but invalid
└── OperationFailedError   # generic Blender failure
```

### Result helpers (`app/commands/result_helpers.py`)

```python
from app.commands.result_helpers import ok, fail_not_found, fail_missing

def my_command(args):
    name = args.get('name')
    if not name:
        return fail_missing('name', 'my_command')
    obj = data.objects.get(name)
    if not obj:
        return fail_not_found(name, 'my_command')
    return ok({'name': name}, 'my_command')
```

| Helper | When to use |
|--------|-------------|
| `ok(data, cmd)` | Command succeeded |
| `fail_missing(arg, cmd)` | Required argument absent |
| `fail_not_found(name, cmd)` | Resource does not exist |
| `fail_exists(name, cmd)` | Resource already exists |
| `fail_invalid(arg, reason, cmd)` | Argument present but invalid |

---

## Extending the Engine

1. Create `app/commands/<category>/my_command.py`
2. Implement with `@register_command('my_command')`
3. Import in `app/commands/<category>/__init__.py`
4. Add tests in `tests/e2e/<category>/`
5. Document in `docs/commands/<category>.md`

---

## Directory Rules

| Rule | Limit |
|------|-------|
| Lines per source file | 120 max |
| Chars per line | 80 recommended |
| Files per source folder | 6 max |
