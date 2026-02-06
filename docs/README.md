# Animation Engine Documentation

Procedural animation engine with dynamic dispatch for Blender.

## Quick Start

```bash
# Run tests
python -m pytest tests/e2e/ -v

# Demo
python test_runner.py
```

## Architecture

```
animations/
├── app/           # Application layer (commands, registry, dispatcher)
├── domain/        # Domain entities (DispatchResult)
├── infra/         # Infrastructure (Blender bridge)
├── core/          # Core logic
├── tests/         # Test suite
│   ├── mocks/     # Blender API mocks
│   └── e2e/       # End-to-end tests
└── docs/          # Documentation
```

## Available Commands

| Category | Commands |
|----------|----------|
| **Primitives** | spawn_primitive |
| **Transforms** | move_object, rotate_object, scale_object |
| **Relative** | translate_relative, rotate_relative, scale_relative |
| **Utils** | reset_transform, apply_transform, set_origin |
| **Keyframes** | set_keyframe, delete_keyframe, clear_animation |
| **Animation** | set_current_frame, set_frame_range |
| **Hierarchy** | parent_object, delete_object |
| **Management** | clone_object, rename_object, select_object |
| **Visibility** | hide_object, show_object, set_render_visibility |
| **Locks** | lock_transforms, unlock_transforms |
| **Materials** | create_material, assign_material, set_material_color |
| **Cameras** | create_camera, set_camera_target, set_focal_length |
| **Lights** | create_light, set_light_energy, set_light_color |
| **Modifiers** | add_modifier, remove_modifier, configure_modifier |
| **Collections** | create_collection, link_to_collection, unlink |

## Usage Example

```python
from app.dispatcher import dispatch_batch
import app.commands

results = dispatch_batch([
    {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Box'}},
    {'cmd': 'move_object', 'args': {'name': 'Box', 'location': (0, 0, 2)}},
    {'cmd': 'set_keyframe', 'args': {'name': 'Box', 'frame': 1}},
])
```

## Quality Standards

- **120/80 Rule**: Max 120 lines/file, 80 chars/line
- **DDD Pattern**: domain/app/infra separation
- **SOLID Principles**: Single responsibility per file
- **Headers**: All files have location, function, copyright

## License

All Rights Reserved Arodi Emmanuel
