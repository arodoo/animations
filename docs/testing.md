# Testing Guide

The test suite runs entirely without Blender using a full API mock.

---

## Quick Start

```bash
# All E2E tests
python -m pytest tests/e2e/ -v

# Single category
python -m pytest tests/e2e/scene/ -v

# With coverage
python -m pytest tests/e2e/ --cov=app --cov-report=html
```

---

## Structure

```
tests/
├── conftest.py           # Auto-reset fixture (runs before every test)
├── mocks/                # Full Blender API mock
│   ├── core/             # bpy_mock, bpy_data, bpy_context, vector3, anim_data
│   ├── data/             # Collection classes (objects, meshes, materials…)
│   ├── entities/         # MockObject, MockCamera, MockLight, MockMaterial…
│   └── ops/              # bpy_ops — mesh / object / camera / light operators
├── e2e/                  # End-to-end tests, one subfolder per command category
│   ├── objects/
│   ├── transforms/
│   ├── scene/
│   ├── advanced/
│   └── integration/
├── demos/                # Runnable demo scripts (not pytest)
└── runners/              # CLI runners for demos
```

---

## The Mock System

Every `bpy.*` access goes through `app/infra/bridge.py`. When Blender is
absent the bridge loads `tests/mocks/core/bpy_mock.py` instead.

| Mock class | Simulates |
|------------|-----------|
| `MockObject` | `bpy.types.Object` — transforms, keyframes, materials, parent |
| `MockCamera` | `bpy.types.Camera` — lens, dof |
| `MockLight` | `bpy.types.Light` — energy, color, type |
| `MockMaterial` | `bpy.types.Material` — diffuse_color |
| `ObjectsCollection` | `bpy.data.objects` — get, new, remove, link |
| `MeshOps` | `bpy.ops.mesh.*` — all primitive_*_add calls |
| `ObjectOps` | `bpy.ops.object.*` — camera_add, light_add, empty_add, delete |

### Ops coverage

```
MeshOps:   primitive_cube_add, primitive_uv_sphere_add, primitive_plane_add,
           primitive_torus_add, primitive_cone_add, primitive_cylinder_add

ObjectOps: camera_add, light_add, empty_add, delete, select_all
```

---

## Writing Tests

```python
from app.kernel.dispatcher import dispatch_single
from app.infra.bridge import data

class TestSpawnPrimitive:
    def test_sphere_is_named(self):
        result = dispatch_single({
            'cmd': 'spawn_primitive',
            'args': {'type': 'sphere', 'name': 'MySphere'}
        })
        assert result.success
        assert data.objects.get('MySphere') is not None

    def test_unknown_type_fails(self):
        result = dispatch_single({
            'cmd': 'spawn_primitive',
            'args': {'type': 'octahedron'}
        })
        assert not result.success
```

### Auto-reset fixture (`conftest.py`)

```python
@pytest.fixture(autouse=True, scope='function')
def reset_engine_state():
    from app.infra.bridge import reset
    reset()
    import app.commands
    yield
    reset()
```

---

## Test Categories

| Category | Tests | What is covered |
|----------|-------|----------------|
| Spawn / objects | 5 | Primitive creation, naming |
| Transforms | 6 | Absolute move / rotate / scale |
| Relative transforms | 5 | Delta move / rotate / scale |
| Keyframes | 6 | Insert, delete, clear |
| Hierarchy | 5 | Parent / child, delete |
| Management | 9 | Clone, rename, select, visibility |
| Materials | 5 | Create, assign, color |
| Camera & lights | 8 | Create, target, focal, DOF, energy |
| Modifiers | 5 | Add, remove, configure |
| Collections | 5 | Create, link, unlink |
| Integration | 3 | Multi-command workflows |

**Total: 75 tests**

---

## Best Practices

1. **One concept per test** — one behaviour, one failure mode
2. **Descriptive names** — `test_clone_preserves_location` not `test_clone`
3. **Test failure paths** — missing args, not found, wrong type
4. **Never rely on test order** — conftest resets state automatically
5. **No I/O, no sleep** — keep the suite under 1 second total
