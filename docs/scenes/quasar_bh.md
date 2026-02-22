# Scene: Quasar Black Hole

**Path:** `scenes/quasar_bh/`
**Launcher:** `scenes/quasar_bh/launcher.py` — paste into Blender Scripting tab

A physically-motivated animation of a quasar: a supermassive black hole
surrounded by a Keplerian accretion disk and polar relativistic jets.

---

## Scene Elements

| Element | Object(s) | Notes |
|---------|-----------|-------|
| Black hole | `BlackHole` (UV sphere, r=2) | Pure black, non-emissive |
| Accretion disk | `Ring_0` … `Ring_N` (tori) | Keplerian differential rotation |
| Relativistic jets | `JetNorth`, `JetSouth` (cones) | Electric-blue emission, parented to BH |
| Camera | `SceneCamera` | Spherical orbit with Track To constraint |
| Accent light | `AccretionLight` | Warm golden POINT light |
| Starfield | World node tree | Procedural Voronoi — zero object cost |

---

## Physics: Keplerian Rotation

In Newtonian gravity, the circular-orbit angular velocity obeys:

```
ω ∝ r^(-3/2)          (Kepler's third law)
```

Each ring's speed relative to the innermost ring (`r_ref = 3.0`) is:

```python
def keplerian_speed(r: float) -> float:
    return (r_ref / r) ** 1.5
```

| Ring | Radius | Relative speed | Colour |
|------|--------|----------------|--------|
| 0 (innermost) | 3.0 | 1.000 | White-blue (hottest) |
| 1 | 4.2 | 0.611 | Warm white |
| 2 | 5.5 | 0.413 | Yellow |
| 3 | 7.0 | 0.290 | Orange |
| 4 | 8.5 | 0.220 | Orange-red |
| 5 | 10.0 | 0.169 | Red |
| 6 | 11.5 | 0.132 | Dark red |
| 7 | 13.0 | 0.106 | Very dark red |
| 8 (outermost) | 14.5 | 0.085 | Near-invisible |

The cizallamiento (differential rotation) is clearly visible: inner rings
lap the outer ones many times during the animation.

---

## Camera: Spherical Orbit

The camera moves on the surface of a sphere of radius 22 units:

```python
azimuth   = t * 2π * 0.75          # sweeps 270° over the full animation
elevation = 20° + 25° * sin(t * π) # oscillates 20° → 45° → 20°

x = r * cos(elevation) * cos(azimuth)
y = r * cos(elevation) * sin(azimuth)
z = r * sin(elevation)
```

A **Track To** constraint (`TRACK_NEGATIVE_Z`, `UP_Y`) keeps the camera
pointed at the black hole at all times without rotation keyframes.

---

## Starfield

Stars are not individual objects — they live in the **world node tree**:

```
TexCoord.Generated
    → Voronoi(F1, scale=350)
    → 1 − Distance              (invert)
    → x^30                      (sharpen to bright dots)
    → MixShader(black_bg, star_emission)
    → WorldOutput
```

This costs zero draw calls and scales to any resolution.
To see it: **Z → Material Preview** or **Rendered** mode.

---

## Quality Presets

| Preset | Frames | Duration | Rings | Samples | Recommended for |
|--------|--------|----------|-------|---------|-----------------|
| `'low'` | 900 | 30 s | 5 | 8 | Any machine |
| `'medium'` | 1 800 | 60 s | 7 | 16 | i7 + 24 GB RAM |
| `'high'` | 3 600 | 120 s | 9 | 32 | Workstation |

---

## Running

```python
# scenes/quasar_bh/launcher.py
QUALITY = 'low'   # start here
```

Paste `launcher.py` into Blender → Scripting tab → Run Script.

After completion:
1. Press **Z** → **Material Preview** to activate Eevee bloom and colours
2. Press **Space** to play
3. Change `QUALITY = 'medium'` for more detail once you confirm it runs

---

## Customisation

```python
from scenes.quasar_bh.scene import create_scene, PRESETS

# Inspect what a preset contains
print(PRESETS['medium'])

# Run with a preset
result = create_scene(quality='medium')
```

All disc ring templates are in `_DISK_RINGS` at the top of `scene.py`.
Adjust radius, colour, or add rings to taste.
