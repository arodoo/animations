# Component Reference -- Reusable Objects

**Path:** `app/components/objects/`

Builders that return `List[Dict]` command batches. Each constructs
a 3D object from primitives. Import from `app.components.objects`.

---

## build_butterfly

Complete butterfly character: body + 4-wing system + materials.
Root object `{name}_Torso` for external animation (flight path).

```python
from app.components.objects import build_butterfly

cmds = build_butterfly(
    name='Butterfly',       # part prefix
    pos=(0, 0, 3),          # initial spawn
    start_f=1,              # flap start frame
    end_f=2880,             # flap end frame
    half_cycle=6,           # frames per half-stroke
)
# Creates: Butterfly_Torso (root)
#          ├─ Butterfly_Head, AntennaL, AntennaR
#          └─ WingFL, WingFR, WingHL, WingHR
```

**Key points:**
- 4-wing design: forewings (larger) + hindwings (smaller)
- Peak/trough keyframes with BEZIER interpolation (60% fewer keys)
- Asymmetric dihedral: up=0.52 rad, down=-0.28 rad
- Hindwings phase-delayed 2 frames (overlapping action)

**See:** `docs/components/butterfly.md` for full architecture & customization.

---

## build_missile

Cylinder body + cone nose, parented. Oriented along Y axis.

```python
from app.components.objects import build_missile

cmds = build_missile(
    name='Missile',
    pos=(0, 0, 50),         # spawn position
)
# Creates: Missile_Body, Missile_Nose
```

Body: radius 0.15, depth 2.0. Nose: radius 0.15, depth 0.5.

---

## build_missile_trail

Particle emitter on missile body for smoke effect.

```python
from app.components.objects import build_missile_trail

cmds = build_missile_trail(
    name='Missile',         # must match missile name
    count=200,              # particle count
    lifetime=30,            # frames
)
```

Emits from faces, negative normal direction, slight gravity.

---

## build_explosion

Expanding sphere with emission material.

```python
from app.components.objects import build_explosion

cmds = build_explosion(
    name='Explosion',
    pos=(0, 0, 0),          # center
    frame=100,              # start frame
    radius=3.0,             # peak radius
    duration=30,            # total frames
)
```

Scale keyframes: 0.01 at start, `radius` at 1/3 duration,
0.01 at end. Assigns `MatExplosion` material.

---

## build_house

Cube base + cone roof, parented. Materials: `MatHouseWall`, `MatRoof`.

```python
from app.components.objects import build_house

cmds = build_house(
    name='House',
    pos=(10, 20, 0),        # ground position
    size=1.5,               # scale factor
)
# Creates: House_Base, House_Roof
```

---

## build_barn

Wide cube + tall cone roof. Materials: `MatBarnWood`, `MatRoof`.

```python
from app.components.objects import build_barn

cmds = build_barn(
    name='Barn',
    pos=(50, 30, 0),
    size=3.0,
)
# Creates: Barn_Base, Barn_Roof
```

---

## build_tree

Cylinder trunk + sphere canopy. Materials: `MatTrunk`, `MatCanopy`.

```python
from app.components.objects import build_tree

cmds = build_tree(
    name='Tree',
    pos=(5, 5, 0),
    height=3.0,             # total height
)
# Creates: Tree_Trunk, Tree_Canopy
```

---

## build_meadow

Large ground plane. Material: `MatGrass`.

```python
from app.components.objects import build_meadow

cmds = build_meadow(
    name='Meadow',
    size=2000.0,            # plane size in meters
    pos=(0, 0, 0),
)
```

---

## build_fence

Thin cube scaled as fence section. Material: `MatFence`.

```python
from app.components.objects import build_fence

cmds = build_fence(
    name='Fence',
    pos=(0, 0, 0),
    length=5.0,             # horizontal length
    rotation_z=0.0,         # radians
)
```
