# Mathematical Sets Animation Documentation

## What Is This?

A 5-act animated proof in Blender that visualizes:

**"Where there's an odd number, there's always a number. But where there's a number, there's not always an odd number."**

Formally: `Odds ⊂ ℕ` (odd numbers are a subset of natural numbers).

## Documentation Files

### 1. **MATH_SETS_ANIMATION.md** ← START HERE
- Overview & architecture
- 5 acts timeline
- Visual behavior by phase
- Tunable parameters
- How to launch & extend

### 2. **MATH_SETS_TECHNICAL.md** ← Deep Dive
- Command flow & data structures
- Animation mechanics (hover, spin, bounce)
- Star rotation (driver-based, infinite loop)
- DDD layer structure
- Performance notes
- Testing patterns

### 3. **MATH_SETS_QUICKREF.md** ← Cheat Sheet
- Quick launch command
- Common tweaks
- File edit locations
- Debug tips

## Quick Start

```bash
python scenes/math_sets/launcher.py
```

Then in Blender: Play (spacebar) or use timeline (900 frames @ 30fps = 30 sec).

## Key Insight: Why It Works Visually

1. **Numbers 1-10 appear in a row** — establishes the universal set (ℕ)
2. **Tags prove membership** — "x ∈ N" (all true), "x ∈ Odds?" (mixed)
3. **Concentric rings reveal** — outer=N, inner=Odds
4. **Numbers fly to their circles** — implication becomes physical: odds land inside, evens land outside
5. **Motion continues** — evens spin (in their region), odds bounce (in their region), rings slowly rotate
6. **Formal notation appears** — "Odds ⊂ ℕ", "x ∈ Odds → x ∈ ℕ", etc.

## Architecture Principles

- **DDD**: Each animation concern in separate <80L file
- **Timing as Data**: `Timing` NamedTuple allows easy tweaking
- **Reusable**: Components like `odd_target()`, `even_target()` can be used in other scenes
- **Infinite Loop**: Stars never stop (driver, not keyframes)
- **Clean Migration**: Numbers don't teleport; they fly, showing implication direction

## Files at a Glance

| File | Lines | Purpose |
|------|-------|---------|
| `scene.py` | 50 | Orchestrator |
| `launcher.py` | 56 | Entry point |
| `_builder.py` | 47 | Act assembly |
| `_timing.py` | 14 | Timeline config |
| `_number_row.py` | 78 | Block spawning |
| `_membership_acts.py` | 69 | Membership tags |
| `_logic_blocks.py` | 71 | Migration targets |
| `_kinematics.py` | 72 | Pre-migration animation |
| `_post_sort.py` | 76 | Post-migration animation |
| `_proof_text.py` | 43 | Logic notation |
| `_venn_diagram.py` | 70 | Rings |
| `_camera.py` | 44 | Camera orbit |
| `_materials.py` | 46 | Colors |
| `world_animation.py` | 80 | Star rotation |

**Total**: ~816 commands, all under 80L/60C per file.

## Customization Roadmap

### Immediate
1. Edit `TIMING` in `launcher.py` to adjust pacing
2. Change colors in `_materials.py`
3. Adjust `num_sequence` for more/fewer numbers

### Intermediate
1. Modify `_camera.py` for different camera move
2. Tweak `_post_sort.py` spin/bounce parameters
3. Extend `_proof_text.py` with more logical steps

### Advanced
1. Add a 6th act (new file `_finale.py`)
2. Create variant scene (e.g., proving `Primes ⊂ Odds ⊂ ℕ`)
3. Integrate with other animations in pipeline

## Testing

```bash
# Verify build
python -c "
from scenes.math_sets.scene import create_scene
r = create_scene(900)
print(f'✓ {len(r[\"results\"])} commands')
"

# Check timeline
from scenes.math_sets.animations._timing import Timing
t = Timing(act1=100, act2=200, act3=300, act4=350, act5=500)
# Smaller values = faster pacing
```

## References

- **Scene**: `scenes/math_sets/`
- **Commands**: `app/commands/scene/` (world_settings, world_animation, etc.)
- **Animation Components**: `app/components/` (env_builder, etc.)
- **Blender API**: Assumes Blender 3.5+, EEVEE render engine

## Notes

- **30fps assumed** for timing calculations
- **Bloom enabled** so emissive materials glow
- **Stars loop infinitely** via shader driver (not keyframes)
- **All timing tunable** via `Timing` NamedTuple in launcher

---

**Last Updated**: 2026-03-03
**Status**: Production-ready
**License**: All Rights Reserved Arodi Emmanuel
