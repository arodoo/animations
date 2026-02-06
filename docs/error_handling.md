# Error Handling Guide

The animation engine uses a robust error handling system with typed
exceptions and standardized result helpers.

---

## Architecture

```
domain/errors.py          → Exception types and error codes
app/commands/result_helpers.py → Standardized result builders
```

---

## Error Codes

| Code | Description | Example |
|------|-------------|---------|
| `NOT_FOUND` | Resource doesn't exist | Object, material, modifier |
| `ALREADY_EXISTS` | Resource name collision | Creating duplicate |
| `MISSING_ARGUMENT` | Required param missing | No 'name' provided |
| `INVALID_ARGUMENT` | Bad param value | Negative scale |
| `INVALID_TYPE` | Wrong resource type | Light as camera |
| `OPERATION_FAILED` | Generic failure | Blender API error |

---

## Exception Types

```python
from domain.errors import (
    AnimationError,     # Base exception
    NotFoundError,      # Resource not found
    AlreadyExistsError, # Duplicate name
    MissingArgumentError,
    InvalidArgumentError,
)

# Usage
try:
    result = dispatch_single(command)
    if not result.success:
        raise NotFoundError("Object", obj_name)
except AnimationError as e:
    print(f"Error: {e.code.value} - {e.message}")
```

---

## Result Helpers

Commands use `result_helpers` for consistent responses:

```python
from app.commands.result_helpers import (
    ok,              # Success with data
    fail_not_found,  # Resource missing
    fail_missing,    # Argument missing
    fail_exists,     # Already exists
    fail_invalid,    # Bad value
)

# Usage in commands
def my_command(args):
    name = args.get('name')
    if not name:
        return fail_missing('name', 'my_command')
    
    obj = data.objects.get(name)
    if not obj:
        return fail_not_found(name, 'my_command')
    
    return ok({'result': 'done'}, 'my_command')
```

---

## Helper Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `ok(data, cmd)` | Success result | `ok({'name': 'Cube'}, 'spawn')` |
| `fail_not_found(name, cmd)` | Not found | `fail_not_found('Box', 'move')` |
| `fail_missing(arg, cmd)` | Missing arg | `fail_missing('name', 'delete')` |
| `fail_missing_args(cmd)` | Multiple missing | `fail_missing_args('link')` |
| `fail_exists(name, cmd)` | Duplicate | `fail_exists('Mat1', 'create')` |
| `fail_invalid(arg, why, cmd)` | Bad value | `fail_invalid('scale', 'neg', 'scale')` |

---

## DispatchResult Structure

```python
@dataclass
class DispatchResult:
    success: bool        # True if command succeeded
    data: Optional[dict] # Result data on success
    error: Optional[str] # Error message on failure
    command_name: str    # Command that was executed
```

---

## Best Practices

1. **Always use helpers** - Never construct DispatchResult.fail() directly
2. **Validate early** - Check required args before expensive operations
3. **Be specific** - Use `fail_not_found(name, cmd, 'Light')` vs generic
4. **Keep messages short** - Max 40 chars for 80-char line compliance

---

## Error Flow

```
Command Execute
    ↓
Validate Args → fail_missing() if missing
    ↓
Lookup Resource → fail_not_found() if missing
    ↓
Execute Logic → fail_error() on exception
    ↓
Return ok(data)
```
