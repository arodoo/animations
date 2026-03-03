# Math Sets Animation — Quick Reference

## Launch

```bash
cd D:\zProyectos\01Python\animations
python scenes/math_sets/launcher.py
```

## Tweak Timeline

Edit `launcher.py` line ~20:

```python
TIMING = Timing(
    act1=150,   # "x in N" tags
    act2=270,   # "in Odds?" check
    act3=360,   # Rings appear
    act4=410,   # Migration
    act5=600,   # Proof text
)
```

**Guideline**: `act4 - act3` controls gap between rings and flight.

## Key Files

| Path | Edit For |
|------|----------|
| `launcher.py` | Timing, num_sequence, total_frames |
| `_timing.py` | Default act frame offsets |
| `_materials.py` | Colors (OddMat, EvenMat, etc.) |
| `_camera.py` | Camera orbit angle, speed |
| `world_animation.py` | Star rotation speed (`_ROT_PER_FRAME`) |
| `_number_row.py` | Block position offset |

## Structure

```
scenes/math_sets/
├── scene.py              # Main orchestrator
├── launcher.py           # Entry point
└── animations/
    ├── _timing.py        # Timing config (NamedTuple)
    ├── _builder.py       # 5-act assembly
    ├── _number_row.py    # Blocks spawn
    ├── _membership_acts.py
    ├── _logic_blocks.py  # Migration targets
    ├── _venn_diagram.py  # Rings
    ├── _kinematics.py    # Hover + spin
    ├── _post_sort.py     # Spin/bounce after migration
    ├── _proof_text.py    # Logic notation
    ├── _camera.py        # Camera orbit
    ├── _materials.py     # Colors
    ├── _equations.py     # Membership check tags
    └── _timing.py        # Timeline constants
```

## Common Tweaks

**Slow migration gap**:
```python
Timing(act3=360, act4=500)  # gap: 140 frames instead of 50
```

**Faster stars**:
```python
_ROT_PER_FRAME = 0.01  # in world_animation.py
```

**More blocks**:
```python
build_math_sets(900, num_sequence=15)  # in launcher.py
```

**Tighter proof text**:
```python
Timing(act5=750)  # was 600, leave more time
```

**Bigger camera sweep**:
```python
sweep = math.radians(45)  # in _camera.py (was 15)
```

## Output

- **816 commands** dispatched to Blender
- **900 frames** @ 30fps = 30 seconds
- **Real-time playback** in Blender
- **No Cycles required**: EEVEE with bloom

## Verify Build

```bash
python -c "
from scenes.math_sets.scene import create_scene
from scenes.math_sets.animations._timing import Timing
r = create_scene(900, timing=Timing())
print(f'✓ {len(r[\"results\"])} commands, {r[\"status\"]}')
"
```

## Debug

Add print to `launcher.py` run():
```python
print(f"TIMING: {TIMING}")
print(f"Results: {len(results['results'])} commands")
```

Or check command count by type:
```python
from collections import Counter
types = Counter(c['cmd'] for c in cmds)
print(types)
```
