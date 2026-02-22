# Blender Integration Guide

How to run animations inside Blender and how the engine abstracts the API.

---

## Running a Scene in Blender

1. Open Blender → **Scripting** tab → **New** text block
2. Paste the contents of the scene launcher, e.g.
   `scenes/quasar_bh/launcher.py`
3. Set `QUALITY = 'low'` (start here — safe for any machine)
4. Press **Run Script**
5. When done: press **Z → Material Preview** (or Rendered) to see colours
6. Press **Space** to play

> **Tip — viewport mode matters.**
> Emission materials and world shaders only show in
> Material Preview (`Z`) or Rendered mode. Solid mode shows flat colours.

---

## Quality Presets

All scenes expose a `quality` parameter that scales every expensive setting
proportionally. Start low; upgrade once you confirm it runs without crashing.

| Preset | Frames | Duration | Disk rings | Samples | Safe for |
|--------|--------|----------|------------|---------|----------|
| `'low'` | 900 | 30 s | 5 | 8 | Any machine |
| `'medium'` | 1 800 | 60 s | 7 | 16 | i7 + 24 GB RAM |
| `'high'` | 3 600 | 120 s | 9 | 32 | Workstation |

```python
# scenes/quasar_bh/launcher.py
QUALITY = 'low'   # change to 'medium' or 'high'
```

---

## The Bridge (`app/infra/bridge.py`)

The bridge is the single point of contact with Blender's Python API:

```
import bpy        ──▶ success → use real bpy.data / bpy.ops / bpy.context
                  ──▶ ImportError → fall back to tests/mocks/core/bpy_mock
```

Commands never import `bpy` directly — they import from the bridge:

```python
from app.infra.bridge import data, ops, context, is_mock
```

This makes every command testable outside Blender with zero changes.

### `is_mock()` branching

Some Blender API calls differ between the mock and real Blender.
Use `is_mock()` to branch cleanly:

```python
if is_mock():
    ops.camera.add_camera(location=location)   # mock API
else:
    ops.object.camera_add(location=location)   # real Blender API
```

---

## Blender API Gotchas

These are real differences between the mock and Blender that the bridge
already handles — documented here for reference.

| Issue | Mock | Real Blender | Fix applied |
|-------|------|--------------|-------------|
| Camera creation | `ops.camera.add_camera()` | `ops.object.camera_add()` | `is_mock()` branch |
| Light creation | `ops.light.add_light()` | `ops.object.light_add()` | `is_mock()` branch |
| Object rename | `data.objects._objects[k]` | `obj.name = name` only | Use `context.active_object` |
| Material assign | `obj.material_slots.append()` | `obj.data.materials.append()` | `is_mock()` branch |
| Material colours | `diffuse_color` (solid view) | Node tree required | `use_nodes=True` + BSDF/Emission |
| World background | dict storage | World node tree | `world.node_tree.nodes` |
| Starfield | Individual sphere objects | World Voronoi shader | `create_space_world` command |

---

## Blender Version Compatibility

The engine targets **Blender 3.x** and **4.x**. Where the API changed,
`try/except` guards are used:

```python
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'   # 4.x
except Exception:
    scene.render.engine = 'BLENDER_EEVEE'         # 3.x

try:
    eevee.use_bloom = True    # 3.x Eevee property
except AttributeError:
    pass                      # 4.x Eevee Next: bloom via compositor
```

---

## Adding a New Scene

```
scenes/
└── my_scene/
    ├── __init__.py
    ├── scene.py       ← animation logic (import app.commands, dispatch_batch)
    └── launcher.py    ← paste this into Blender
```

`scene.py` structure:

```python
import app.commands          # registers all commands
from app.kernel.dispatcher import dispatch_batch

def create_scene(quality='low'):
    batch = []
    batch.append({'cmd': 'clear_scene',     'args': {}})
    batch.append({'cmd': 'configure_eevee', 'args': {'samples': 8}})
    # ... build scene ...
    results = dispatch_batch(batch)
    return {'results': results}
```
