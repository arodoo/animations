# Butterfly Component

**Path:** `app/components/objects/butterfly/`

A reusable, self-contained character component following SOLID principles. The butterfly is an animated character with realistic wing mechanics and body proportions. The translational flight path remains scene-specific.

---

## Architecture

The butterfly component is organized as a Python package with a single public API:

```
butterfly/
├── __init__.py        # re-exports build_butterfly
├── builder.py         # assembles body + wings + materials
├── _body.py           # private: torso, head, antennae
├── _wings.py          # private: 4-wing BEZIER flapping
└── _materials.py      # private: material table
```

**Key principle:** External code **only sees** `build_butterfly()`. Internal modules are prefixed with `_` to signal "private — do not import directly."

---

## Public API

```python
from app.components.objects import build_butterfly

cmds = build_butterfly(
    name='Butterfly',           # part prefix
    pos=(0, 0, 3),              # initial spawn position
    start_f=1,                  # flap start frame
    end_f=2880,                 # flap end frame
    half_cycle=6,               # frames per half-stroke
)
```

**Returns:** `List[Dict]` — command batch for the dispatcher.

**Root object:** `{name}_Torso` — animate this externally for world position changes.

---

## Part Hierarchy

```
{name}_Torso (root, animated externally)
├── {name}_Head (parented, local offset)
├── {name}_AntennaL (parented, local offset)
├── {name}_AntennaR (parented, local offset)
├── {name}_WingFL (parented, BEZIER flap)
├── {name}_WingFR (parented, BEZIER flap)
├── {name}_WingHL (parented, BEZIER flap)
└── {name}_WingHR (parented, BEZIER flap)
```

All parts are parented to the torso. External rotation keyframes on the torso propagate to all children automatically.

---

## Disney's 12 Principles Applied

| Principle | Where | How |
|-----------|-------|-----|
| **#1 Squash & Stretch** | `_wings.py` | Wings scale X×0.90/Y×0.86 at upstroke peak; X×1.08/Y×1.06 at downstroke |
| **#2 Anticipation** | `_wings.py` | First keyframe is DOWN stroke — wings dip before the first dramatic upstroke |
| **#5 Follow Through** | `_wings.py` | Hindwings lag 2 frames behind forewings |
| **#6 Slow In/Out** | `_wings.py` | BEZIER peak/trough keyframes give ease-in/out free via Blender interpolation |
| **#7 Arcs** | `flight_path.py` | Spiral path + body bob (±0.35 m at wing frequency) + pitch on climbs/descents |
| **#8 Secondary Action** | `flight_path.py` | Body bobs vertically in sync with wingbeat; baking/pitching reinforces direction |
| **#10 Exaggeration** | `_wings.py` | UP: 0.65 rad (~37°), DOWN: −0.38 rad (~22°) — more dramatic than real anatomy |

---

## Wing Animation

### 4-Wing Geometry

The butterfly uses **4 separate wing planes** (not a symmetric pair):

- **Forewings (FL/FR):** Larger planes at Y+0.30, scale (1.2, 1.0, 0.05)
- **Hindwings (HL/HR):** Smaller planes at Y-0.40, scale (0.85, 0.72, 0.05)

**Inner-edge-at-zero design:** Each wing's X offset = its scale[0], ensuring wings meet exactly at the torso (X=0) with zero overlap.

### Peak/Trough Keyframes + Squash & Stretch

Each keyframe sets **both rotation AND scale** simultaneously:

- **Upstroke peak:** rotates to `_UP` (0.65 rad), squashes X×0.90 / Y×0.86 (wings gather up, appear narrower)
- **Downstroke trough:** rotates to `_DOWN` (−0.38 rad), stretches X×1.08 / Y×1.06 (wings spread wide and flat)

BEZIER interpolation between peaks gives ease-in/out, follow-through, and organic squash/stretch transitions for free.

### Asymmetric Dihedral

- **Up angle:** 0.65 rad (~37°) — exaggerated upstroke for appeal
- **Down angle:** −0.38 rad (~22°) — strong power stroke

Asymmetry ensures wings spend more time in the passive upstroke glide than the active downstroke.

### Overlapping Action + Anticipation

- Hindwings are **phase-delayed by 2 frames** (overlapping action)
- Animation starts at the **downstroke** (`up=False` first) so the butterfly dips before the first dramatic upstroke (anticipation)

---

## Body Proportions

| Part | Geometry | Purpose |
|------|----------|---------|
| **Torso** | Sphere, scale (0.22, 0.72, 0.22) | Elongated, circular cross-section; not a flat disc |
| **Head** | Sphere, scale (0.22, 0.22, 0.22) | Slightly larger than old design; positioned forward |
| **Antennae** | Cylinders, radius 0.02, depth 0.5 | Subtle details at head |

The torso is **not** scaled uniformly; it's deliberately elongated in the Y direction (body forward axis) but circular in the X-Z plane.

---

## Material Assignment

All parts are assigned materials via the private `_materials.py` module:

```
Torso       → MatButterfly (orange/tan, 2.0 emission)
Head        → MatButterfly
AntennaL/R  → MatTrunk (dark brown)
WingFL/FR   → MatButterflyWing (bright tan, 3.0 emission)
WingHL/HR   → MatButterflyWing
```

Materials must be pre-created in the scene's material staging. The butterfly component only **assigns** existing materials; it doesn't create them.

---

## Usage in a Scene

```python
from scenes.my_scene.animations.domain.timing import Timing
from app.components.objects import build_butterfly
from app.components.objects import build_meadow

timing = Timing(flight_start=1, flight_end=2880)

cmds = []
cmds += build_meadow()
cmds += build_butterfly(
    end_f=timing.flight_end,
    half_cycle=6,  # 2 flaps/sec at 24fps
)
# Scene adds: flight path keyframes on Butterfly_Torso
cmds += build_flight_path(timing)

dispatch_batch(cmds)
```

The scene is responsible for:
1. Creating materials
2. Creating lights
3. Placing the butterfly via `build_butterfly()`
4. Animating `Butterfly_Torso` position/rotation (flight path)

The component is responsible for:
1. Body structure
2. Wing flapping (internal to the torso)
3. Material assignments

---

## Customization

### Change Flap Speed

Modify `WING_HALF_CYCLE` in your scene's launcher:

```python
WING_HALF_CYCLE = 8   # slower: more frames per half-stroke
WING_HALF_CYCLE = 4   # faster
```

### Change Flap Amplitude

Edit `_UP` and `_DOWN` in `butterfly/_wings.py`:

```python
_UP = 0.70      # larger upstroke angle
_DOWN = -0.15   # smaller downstroke angle
```

### Tune Body Bob Amplitude

In `flight_path.py`, adjust `_BOB` to control how much the body rises/falls per wingbeat:

```python
_BOB = 0.35   # subtle (default)
_BOB = 0.60   # more pronounced
```

### Tune Banking Sensitivity

Adjust `_ROLL_K` (banking sharpness on turns) and `_MAX_ROLL` (max bank angle):

```python
_ROLL_K = 6.0     # default
_MAX_ROLL = 0.45  # ~26° max bank
```

---

## SOLID Principles Applied

| Principle | How | Benefit |
|-----------|-----|---------|
| **S** — Single | Each private module owns one concern (body, wings, materials) | Easy to modify one aspect without affecting others |
| **O** — Open/Closed | Public API accepts parameters; can extend without modifying | Scenes set `half_cycle`, materials, timing without changing component code |
| **L** — Liskov | Component returns `List[Dict]` like all builders; obeys the interface contract | Interchangeable with other character components |
| **I** — Interface Segregation | Scene only imports `build_butterfly()`; ignores internal modules | Clean dependency graph; internal refactoring doesn't affect callers |
| **D** — Dependency Inversion | Scene depends on abstraction (`build_butterfly`), not concrete body/wings | Changes to wing implementation don't cascade to scenes |

---

## Performance Notes

- **4 wings** instead of 2: minimal cost (4 planes vs. 2, same hierarchy)
- **Peak/trough keyframes** vs. sine sampling: **60% fewer keyframes**, faster Blender evaluation
- **BEZIER interpolation**: Blender handles it, no Python overhead

---

## See Also

- **[Animation Principles](../architecture.md)** — SOLID and DDD patterns
- **[Flight Path](../../scenes/missile_storm.md)** — how to animate the torso's translation
- **[Materials](../../commands/scene.md)** — how to define MatButterfly, MatButterflyWing, etc.
