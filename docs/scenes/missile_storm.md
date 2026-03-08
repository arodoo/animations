# Scene: Missile Storm

**Path:** `scenes/missile_storm/`
**Launcher:** `scenes/missile_storm/launcher.py`

A butterfly glides over a meadow for 20 seconds. A single missile strikes it in the second 20.
The camera pulls back to reveal a 2 km village as 80 more missiles rain down,
destroying everything. 

---

## Scene Elements

| Element | Object(s) | Notes |
|---------|-----------|-------|
| Butterfly | `Butterfly_Torso`, `_Head`, `_WingL/R` | Spheres + planes, wing flap |
| Meadow | `Meadow` | 2 km plane, grass material |
| First missile | `Strike0_Body`, `_Nose` | Cylinder + cone, smoke trail |
| Barrage | `Barrage0`..`Barrage79` | 80 staggered missiles |
| Explosions | `Explosion0`, `Exp0`..`Exp79` | Scaling spheres, emission |
| Village | 40 buildings (houses + barns) | 8 clusters, ~2 km spread |
| Trees | `Tree0`..`Tree39` | Cylinder trunk + sphere canopy |
| Fences | `Fence0`..`Fence15` | Thin cubes around clusters |
| Camera | `StormCam` | Follow phase + quadratic pullback |
| Lights | `Sun`, `FillLight` | SUN + POINT |

---

## Timeline (24 fps, 50 s)

```
Act 1: Flight    Act 2: Strike   Act 3: Barrage + Pullback
|----------------|-------|--------|--------------------------|
1              480  500  600                              1200
```

| Act | Frames | Duration | Description |
|-----|--------|----------|-------------|
| Flight | 1-480 | 20 s | Butterfly sinusoidal path, camera follows |
| Strike | 481-500 | 0.8 s | Missile descends, butterfly destroyed |
| Barrage | 600-1080 | 20 s | 80 missiles staggered, camera pulls back |
| Finale | 1080-1200 | 5 s | Final explosions, full village revealed |

---

## Butterfly Flight Path

```python
x = progress * 200 - 100       # sweeps 200 m
y = 30 * sin(p * 4pi)          # lateral oscillation
z = 3 + sin(p * 6pi)           # altitude wobble
yaw = atan2(cos(p*4pi)*4, 1)   # faces direction of travel
```

Wings flap via rotation keyframes every 4 frames with 0.6 rad amplitude.

---

## Camera Phases

**Follow (frames 1-480):** Offset `(-8, -3, +2)` from butterfly position.
Tracks the flight smoothly.

**Pullback (frames 500-1200):** Quadratic acceleration:
```python
altitude = 10 + 600 * p^2      # 10 m -> 610 m
distance = 50 + 1200 * p^2     # 50 m -> 1250 m
angle = p * pi/2                # sweeps 90 degrees
```

This reveals the full 2 km village from above as missiles strike.

---

## Village Layout

80 clusters arranged in a ring of radius ~800 m. Each cluster contains:
- barns (size 3.0) + houses (size 1.5)
- Trees scattered at varying radii (100-500 m)
- Fences at ring radius 200-400 m

---

## Missile Barrage

80 missiles arrive staggered across frames 600-984:

```python
hit_frame = barrage_start + (i / 80) * span * 0.8
```

- First 40 target buildings directly
- Remaining 40 hit random positions within 900 m spread
- Each missile descends 50 frames from altitude 120-200 m
- Each explosion scales to radius 8-16 m over 40 frames

---

## Materials

| Material | RGB | Emission | Used by |
|----------|-----|----------|---------|
| `MatGrass` | (0.15, 0.35, 0.08) | - | Meadow |
| `MatButterfly` | (0.9, 0.5, 0.1) | 2x | Torso |
| `MatButterflyWing` | (0.95, 0.6, 0.15) | 3x | Wings |
| `MatMissile` | (0.3, 0.3, 0.32) | - | Missile bodies |
| `MatMissileNose` | (0.7, 0.1, 0.1) | - | Missile cones |
| `MatExplosion` | (1.0, 0.6, 0.05) | 40x | Explosions |
| `MatHouseWall` | (0.85, 0.8, 0.7) | - | Houses |
| `MatRoof` | (0.45, 0.18, 0.1) | - | Roofs |
| `MatBarnWood` | (0.5, 0.3, 0.15) | - | Barns |
| `MatTrunk` | (0.35, 0.2, 0.1) | - | Tree trunks |
| `MatCanopy` | (0.1, 0.4, 0.08) | - | Tree canopies |
| `MatFence` | (0.6, 0.45, 0.25) | - | Fences |

---

## Running

```python
# scenes/missile_storm/launcher.py
TIMING = Timing(
    flight_start=1, flight_end=480,
    strike_frame=481, strike_explode=500,
    pullback_start=500, barrage_start=600,
    barrage_end=1080, finale_end=1200,
)
CAM_STEP = 4
```

Paste into Blender > Scripting > Run Script.

1. Press **Z** > **Material Preview**
2. Press **Space** to play
3. Adjust `TIMING` to change pacing

---

## Reusable Components

All objects are in `app/components/objects/` and reusable:

| Component | Function | Returns |
|-----------|----------|---------|
| `build_butterfly_body()` | Torso + head | List[Dict] |
| `build_butterfly_wings()` | Wings + flap keyframes | List[Dict] |
| `build_missile()` | Cylinder body + cone nose | List[Dict] |
| `build_missile_trail()` | Particle smoke trail | List[Dict] |
| `build_explosion()` | Scaling sphere + material | List[Dict] |
| `build_house()` | Cube + cone roof | List[Dict] |
| `build_barn()` | Wide cube + tall roof | List[Dict] |
| `build_tree()` | Trunk + canopy | List[Dict] |
| `build_meadow()` | Large ground plane | List[Dict] |
| `build_fence()` | Thin cube section | List[Dict] |

---

## File Structure

```
missile_storm/
├── launcher.py                # Config: TIMING, CAM_STEP
├── scene.py                   # Orchestrator: env + builder
└── animations/
    ├── builder.py             # Assembles all acts
    ├── domain/
    │   ├── timing.py          # 8-field NamedTuple
    │   └── layout.py          # Village cluster positions
    ├── staging/
    │   ├── camera.py          # Follow + pullback compositor
    │   ├── camera_follow.py   # Follow-butterfly keyframes
    │   ├── camera_pullback.py # Quadratic pullback keyframes
    │   ├── lights.py          # Sun + fill light
    │   └── materials.py       # 12 materials
    └── acts/
        ├── butterfly_flight.py  # Act 1 orchestrator
        ├── flight_path.py       # Sinusoidal path keyframes
        ├── first_strike.py      # Act 2: strike + explosion
        ├── strike_descent.py    # Missile descent animation
        ├── village.py           # Buildings + trees + fences
        ├── barrage.py           # 80 missiles orchestrator
        └── barrage_targets.py   # Target selection + stagger
```
