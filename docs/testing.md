# Testing Guide

Comprehensive guide for testing the animation engine.

---

## Quick Start

```bash
# Run all E2E tests
python -m pytest tests/e2e/ -v

# Run specific test file
python -m pytest tests/e2e/test_collections.py -v

# Run with coverage
python -m pytest tests/e2e/ --cov=app --cov-report=html
```

---

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── mocks/                # Blender API mocks
│   ├── mock_object.py
│   ├── mock_camera.py
│   ├── mock_light.py
│   ├── mock_material.py
│   ├── mock_modifier.py
│   ├── mock_collection.py
│   ├── bpy_data.py
│   ├── bpy_ops.py
│   └── ...
└── e2e/                  # End-to-end tests
    ├── test_spawn_commands.py
    ├── test_transform_commands.py
    ├── test_keyframe_commands.py
    ├── test_hierarchy_commands.py
    ├── test_object_management.py
    ├── test_materials.py
    ├── test_camera_lights.py
    ├── test_modifiers.py
    ├── test_collections.py
    └── test_professional_workflows.py
```

---

## Writing Tests

### Basic Test Structure

```python
import pytest
from app.dispatcher import dispatch_single
from infra.bridge import data

class TestMyCommand:
    def test_basic(self):
        result = dispatch_single({
            'cmd': 'my_command',
            'args': {'name': 'Test'}
        })
        assert result.success
        assert 'Test' in data.objects
```

### Test Fixtures

The `conftest.py` provides automatic reset:

```python
@pytest.fixture(autouse=True, scope='function')
def reset_engine_state():
    from infra.bridge import reset
    reset()
    import app.commands
    yield
    reset()
```

---

## Mock System

The mock system replicates Blender's API:

| Mock | Simulates |
|------|-----------|
| `MockObject` | bpy.types.Object |
| `MockCamera` | bpy.types.Camera |
| `MockLight` | bpy.types.Light |
| `MockMaterial` | bpy.types.Material |
| `MockModifier` | bpy.types.Modifier |
| `MockCollection` | bpy.types.Collection |

---

## Test Categories

| Category | Tests | Focus |
|----------|-------|-------|
| Spawn | 5 | Object creation |
| Transform | 6 | Position/rotation/scale |
| Keyframe | 6 | Animation data |
| Hierarchy | 5 | Parent/child |
| Management | 9 | Clone/rename/select |
| Materials | 5 | Material system |
| Camera/Lights | 8 | Cinematography |
| Modifiers | 5 | Mesh deformation |
| Collections | 5 | Scene organization |
| Workflows | 3 | Integration tests |

**Total: 75 tests**

---

## Best Practices

1. **One assertion per test** when possible
2. **Use descriptive names**: `test_clone_preserves_transforms`
3. **Test error cases**: Missing args, not found
4. **Reset state**: Use conftest fixture
5. **Keep tests fast**: No I/O, no sleep
