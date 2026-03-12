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

**In Blender:** open any `scenes/*/launcher.py` in the Scripting tab
and press **Run Script**. See [`docs/blender.md`](blender.md) for details.

---

## Project Structure

```
animations/
├── app/                  # Application layer
│   ├── commands/         # Registered commands by concern
│   │   ├── objects/      # spawn, hierarchy, visibility
│   │   ├── transforms/   # move, rotate, scale
│   │   ├── scene/        # materials, cameras, lights
│   │   └── advanced/     # modifiers, collections, rigid body
│   ├── components/       # Reusable builders
│   │   └── objects/      # 3D object builders (butterfly, missile...)
│   ├── kernel/           # dispatcher + registry
│   ├── domain/           # DispatchResult, errors
│   └── infra/            # Blender bridge (bpy <> mock)
├── scenes/               # Standalone animation scenes
│   ├── quasar_bh/        # Black-hole quasar
│   ├── fractal_abyss/    # Mathematical number descent
│   ├── missile_storm/    # Butterfly + missile barrage
│   ├── euler_diagram/    # Mathematical set hierarchy
│   ├── solar_system/     # Procedural solar system
│   └── resonance_box/    # Standing wave visualisation
├── tests/
│   ├── mocks/            # Full Blender API mock
│   └── e2e/              # End-to-end tests (75 passing)
└── docs/
```

---

## Command Categories

| Category | Doc | Commands |
|----------|-----|----------|
| Objects | [`commands/objects.md`](commands/objects.md) | spawn, clear, parent, clone, visibility |
| Transforms | [`commands/transforms.md`](commands/transforms.md) | move, rotate, scale, relative, utils |
| Scene | [`commands/scene.md`](commands/scene.md) | materials, cameras, lights, world, eevee |
| Animation | [`commands/animation.md`](commands/animation.md) | keyframes, frame range |
| Advanced | [`commands/advanced.md`](commands/advanced.md) | modifiers, collections, rigid body |

---

## Scenes

| Scene | Path | Description |
|-------|------|-------------|
| Quasar Black Hole | `scenes/quasar_bh/` | Keplerian accretion disk, jets, orbit camera |
| Fractal Abyss | `scenes/fractal_abyss/` | 5-act mathematical descent into fractals |
| Missile Storm | `scenes/missile_storm/` | Butterfly + 80-missile village destruction |
| Euler Diagram | `scenes/euler_diagram/` | Mathematical set hierarchy spiral |

See [`docs/scenes/`](scenes/) for per-scene documentation.

---

## Reusable Components

| Category | Doc | Contents |
|----------|-----|----------|
| Objects | [`components/objects.md`](components/objects.md) | butterfly, missile, explosion, house, barn, tree, meadow, fence |
| Butterfly | [`components/butterfly.md`](components/butterfly.md) | Character design, wing mechanics, SOLID architecture |

---

## Key Design Principles

- **DDD** -- domain / application / infrastructure separation
- **SOLID** -- single-responsibility per file, open for extension
- **Bridge pattern** -- same commands run on real Blender or the offline mock
- **Reusable farm** -- complex scenes = combinations of simple components

---

## License

All Rights Reserved Arodi Emmanuel
