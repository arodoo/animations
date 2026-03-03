# Mathematical Sets Animation — Technical Details

## Command Flow

1. `launcher.py` → calls `create_scene(timing=TIMING)`
2. `scene.py` → orchestrates:
   - `build_environment()` — world setup
   - `create_space_world()` — Voronoi stars
   - `animate_space_world()` — driver rotation
   - `configure_eevee()` — bloom enabled
   - `build_math_sets(timing=t)` — all math animation
   - `build_camera()` — 15° sweep orbit
3. `_builder.py` (via `Timing`) → assembles 5 acts:
   - `build_number_row()` — spawn blocks (z=4, y=0)
   - `build_membership_acts()` — text tags
   - `generate_set_rings()` — torus (N r=8, Odds r=3.2)
   - `build_all_migrations()` — blocks fly to circles
   - `build_kinematics()` → `build_block_hover()` + `build_ring_spin()`
   - `build_post_sort()` → `build_even_spin()` + `build_odd_bounce()`
   - `generate_proof_statements()` — logic text

## Data Structures

### Timing (NamedTuple)
```python
class Timing(NamedTuple):
    act1: int = 150   # membership tags appear
    act2: int = 300   # odds check
    act3: int = 450   # rings reveal
    act4: int = 560   # migration start
    act5: int = 700   # proof text
```

### Number Positioning

**Row** (Acts 1-3):
- `number_position(i, total=10)` → center-aligned X, y=0, z=4
- Spacing: 2.2 units
- Range: x ∈ [-9.9, 9.9]

**Migration** (Act 4+):
- Odds: `odd_target(idx)` → inside circle (r=2)
- Evens: `even_target(idx)` → N-only ring (r=5.5)
- Both at z=0 (ground level)

### Materials

| Name | RGB | Emit | Purpose |
|------|-----|------|---------|
| OddMat | (1.0, 0.55, 0.0) | 4.0 | Odd blocks (golden) |
| EvenMat | (0.1, 0.2, 0.4) | 0.8 | Even blocks (steel) |
| TextMat | (1.0, 1.0, 1.0) | 1.5 | Labels |
| TrueMat | (0.0, 0.9, 0.3) | 3.0 | ✓ tags |
| FalseMat | (1.0, 0.1, 0.1) | 3.0 | ✗ tags |

## Animation Mechanics

### Pre-Migration Hover (Acts 1-3)

Each block i oscillates in Z:
```
hz = bz + sin(t * 2π + phase[i]) * 0.2
```
- Period: 60 frames
- Amplitude: 0.2 units
- Phase offset: `(i/10) * 2π` — prevents sync

### Ring Spin (Acts 3+)

- Ring_N: rotates +60° over 900-450=450 frames
- Ring_Odds: rotates −90° over same span
- Creates counter-rotation effect emphasizing subset

### Post-Migration (Act 4+)

**Even Spin** (block 2,4,6,8,10):
```
rotate_z = t * 2π  (one full rotation over 340 frames)
```
Keyframe every 20 frames.

**Odd Bounce** (block 1,3,5,7,9):
```
hz = sin(t + phase[i]) * 0.6
```
Keyframe every 12 frames.

### Star Animation (Global)

**Driver expression**: `frame * 0.003` radians/frame on Mapping.Z rotation
- Inserted by `animate_space_world` command
- Idempotent: checks if `StarRotation` node exists
- Infinite: no keyframe endpoint, scales to any duration

## Constraint Compliance

### File Structure (CLAUDE.md: 80L/60C)

All files ≤80 lines, max 60 chars per line:

```
✓ _timing.py (14L)
✓ _number_row.py (78L)
✓ _membership_acts.py (69L)
✓ _logic_blocks.py (71L)
✓ _kinematics.py (72L)
✓ _post_sort.py (76L)
✓ _proof_text.py (43L)
✓ _venn_diagram.py (70L)
✓ _camera.py (44L)
✓ _builder.py (47L)
✓ scene.py (50L)
✓ world_animation.py (80L)
```

### DDD Layers

- **Domain**: `Timing` (value object)
- **App**: Commands in `app/commands/`
- **Infra**: `world_animation` driver setup via bridge
- **Scene**: `scenes/math_sets/` orchestrates via dispatcher

## Extending

### Add a 6th Act (e.g., rotation finale)

1. Create `_finale.py` (~40L)
2. Define `build_finale(total_frames, final_start_frame)`
3. Add `act6: int = 800` to `Timing`
4. Call in `_builder.py`: `cmds += build_finale(...)`

### Change Number Count

1. Modify `launcher.py`: `build_math_sets(num_sequence=15)`
2. Adjust circle radius in `_logic_blocks.py` if crowded:
   - `_SPIN_STEP`, `_BOUNCE_STEP` tuning in `_post_sort.py`

### Customize Camera

`_camera.py` `build_camera()`:
- Change `sweep = math.radians(X)` for larger/smaller orbit
- Change keyframe `step=100` to `step=50` for smoother
- Add vertical rise: increase `cz = ... + t * 1.5`

## Performance Notes

- **816 commands** for default 900F animation
- **~80% are keyframes** (`move_object`, `rotate_object`, `scale_object`)
- **0 procedural overhead**: stars are world shader (no scene objects)
- **Real-time playback**: Blender 3.5+ handles 4-5 minute animations smoothly

## Testing

```bash
python -c "
from scenes.math_sets.animations._timing import Timing
from scenes.math_sets.scene import create_scene

t = Timing(act1=100, act2=200, act3=300, act4=350, act5=500)
r = create_scene(600, timing=t)
print(f'Commands: {len(r[\"results\"])}, Status: {r[\"status\"]}')
"
```

All components load independently; dispatcher handles command execution.
