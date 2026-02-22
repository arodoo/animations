# Animation Engine

Procedural animation engine for Blender with command-based dynamic dispatch,
a full Blender API mock for offline testing, and a growing library of scenes.

---

## Quick Start

```bash
# Run the full test suite (no Blender required)
python -m pytest tests/e2e/ -v

# Run a specific category
python -m pytest tests/e2e/scene/ -v
```

**In Blender:** open `scenes/quasar_bh/launcher.py` in the Scripting tab
and press **Run Script**. See [`docs/blender.md`](blender.md) for details.

---

## Project Structure

```
animations/
├── app/                  # Application layer
│   ├── commands/         # All registered commands, grouped by concern
│   │   ├── objects/      # spawn, clear_scene, hierarchy, management, visibility
│   │   ├── transforms/   # move, rotate, scale (absolute + relative)
│   │   ├── scene/        # materials, cameras, lights, world, render
│   │   └── advanced/     # modifiers, collections
│   ├── kernel/           # dispatcher + registry
│   ├── domain/           # DispatchResult, errors
│   ├── infra/            # Blender bridge (real bpy ↔ mock)
│   └── scene/            # Reusable scene helpers (atmospheres, etc.)
├── scenes/               # Standalone animation scenes
│   └── quasar_bh/        # Black-hole quasar (scene.py + launcher.py)
├── tests/
│   ├── mocks/            # Full Blender API mock
│   └── e2e/              # End-to-end tests (75 passing)
└── docs/
    ├── architecture.md   # DDD layers, SOLID, dispatch flow, error handling
    ├── blender.md        # Running in Blender, bridge, quality presets
    ├── testing.md        # Test structure, mocks, best practices
    ├── commands/         # Command reference, one file per concern
    └── scenes/           # Per-scene documentation
```

---

## Command Categories

| Category | Doc | Commands |
|----------|-----|----------|
| Objects | [`commands/objects.md`](commands/objects.md) | spawn_primitive, clear_scene, parent, clone… |
| Transforms | [`commands/transforms.md`](commands/transforms.md) | move, rotate, scale, relative, utils |
| Scene | [`commands/scene.md`](commands/scene.md) | materials, cameras, lights, world, eevee |
| Animation | [`commands/animation.md`](commands/animation.md) | keyframes, frame range, timeline |

---

## Scenes

| Scene | Path | Description |
|-------|------|-------------|
| Quasar Black Hole | `scenes/quasar_bh/` | Keplerian accretion disk, jets, spherical camera |

See [`docs/scenes/quasar_bh.md`](scenes/quasar_bh.md).

---

## Key Design Principles

- **DDD** — domain / application / infrastructure separation
- **SOLID** — single-responsibility per file, open for extension
- **Bridge pattern** — same commands run on real Blender or the offline mock
- **Quality presets** — `'low'` / `'medium'` / `'high'` scale cost to hardware

---

## License

All Rights Reserved Arodi Emmanuel
