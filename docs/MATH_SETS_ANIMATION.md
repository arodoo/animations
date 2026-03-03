# Mathematical Sets Animation (Odds ⊂ Numbers)

## Overview

Visual proof of: "Where there's an odd, there's always a number. But where there's a number, there's not always an odd."

**Scene**: `scenes/math_sets/` — A 5-act animated proof showing that `Odds ⊂ ℕ` (odd numbers are a strict subset of natural numbers).

## Architecture

### Animations (`scenes/math_sets/animations/`)

| Module | Purpose |
|--------|---------|
| `_timing.py` | `Timing` NamedTuple — tunable act frame offsets |
| `_number_row.py` | Spawns 10 numbered cubes in a row (z=4, colored by parity) |
| `_membership_acts.py` | Acts 1-2: shows membership in ℕ and Odds |
| `_venn_diagram.py` | Acts 3+: concentric torus rings (N outer, Odds inner) |
| `_logic_blocks.py` | Migration: blocks fly to their set circles |
| `_kinematics.py` | Pre-migration hover + ring spin animation |
| `_post_sort.py` | Post-migration: evens spin, odds bounce |
| `_proof_text.py` | Act 5: formal logical notation |
| `_camera.py` | Camera orbit (15° sweep over 900F) |
| `_builder.py` | Orchestrates all components via `Timing` |

### World & Rendering

- **Stars**: `create_space_world` (Voronoi) + `animate_space_world` (continuous rotation driver)
- **Bloom**: `configure_eevee` — emissive materials glow
- **Environment**: Dark background (RGB 0.001) + white point light

## Timeline

All frame offsets are tunable via `Timing` (defaults in parentheses):

```
F1 ────── Act1(150) ────── Act2(300) ────── Act3(450) ────── Act4(560) ────── Act5(700) ────── F900

Numbers appear    Membership check    Venn rings    Migration    Final proof
"x ∈ N"          "x ∈ Odds?"        reveals       into circles  formal notation
(hover)          (✓/✗ tags)         (spin)        (stagger)     (scroll up)
```

## Visual Behavior by Phase

| Phase | What Happens |
|-------|--------------|
| **Pre-Act1** | Scene empty; stars rotate (loop) |
| **Act1-Act2** | 10 blocks hover in row; tags appear proving membership |
| **Act3** | Concentric rings appear; blocks still in row |
| **Act4** | Blocks migrate to circles; evens→outer, odds→inner |
| **Post-Act4** | Evens spin; odds bounce; rings slowly rotate |
| **Act5** | Proof text fades in; all elements settle |

## Parameters

### Timing (seconds → frames, assuming 30fps)

Edit `launcher.py` `TIMING` tuple:

```python
TIMING = Timing(
    act1=150,   # Numbers appear + "x in N" tag
    act2=270,   # "x in Odds?" checks (default was 300; tightened to 270)
    act3=360,   # Rings reveal (was 450)
    act4=410,   # Migration starts (was 560)
    act5=600,   # Proof text (was 700)
)
```

- Smaller `act4 - act3` gap = less waiting between rings and migration
- Larger `act5` value = longer time for proof text to remain visible

### Camera

In `_camera.py`:
- `sweep = math.radians(15)` — total orbit angle (degrees)
- `range(..., 100)` — keyframe interval (frames)

### Star Rotation

In `app/commands/scene/world_animation.py`:
- `_ROT_PER_FRAME = 0.003` — rad/frame (1 full rotation ≈ 70 seconds at 30fps)
- Always continuous; never stops (driver, no keyframes)

## Launch

```bash
cd D:\zProyectos\01Python\animations
python scenes/math_sets/launcher.py
```

Blender opens, plays animation in viewport (RENDERED mode), loops (timeline cycles).

## Key Design Decisions

1. **DDD**: Each animation concern is a separate <80L file
2. **Timing as data**: `Timing` NamedTuple allows easy tweaking
3. **Stars loop infinitely**: Driver-based rotation, not keyframes → no "static at end"
4. **Reusable components**: `build_number_row`, `odd_target`, `even_target` etc. can be used in other scenes
5. **Clean migration**: Numbers don't just appear in circles — they FLY there, showing implication direction

## Extensions

- Add more numbers: Change `num_sequence=10` → `num_sequence=20` in `launcher.py`
- Change colors: Edit `_materials.py` RGB tuples
- Slower proof text: Increase `act5` frame value
- Faster migration: Decrease `act4` value
