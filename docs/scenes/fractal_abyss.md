# Scene: Fractal Abyss

**Path:** `scenes/fractal_abyss/`
**Launcher:** `scenes/fractal_abyss/launcher.py`

A mathematical journey from natural numbers through rationals and irrationals,
into fractal geometry, ending in an abstract infinite descent. Five acts
build visual density progressively using 3D text on spirals and Sierpinski
triangles.

---

## Scene Elements

| Element | Object(s) | Notes |
|---------|-----------|-------|
| Natural numbers | `Nat0`..`Nat14` (3D text) | 15 numbers on Archimedean spiral |
| Rational fractions | `Rat0`..`Rat19` (3D text) | 20 fractions filling gaps |
| Irrational constants | `Irr0`..`Irr9` (3D text) | pi, e, sqrt2, phi... spiral inward |
| Fractal symbols | `Frac0`..`Frac26` (3D text) | 27 Sierpinski-triangle positions |
| Abyss symbols | `Aby0`..`Aby26` + `Fin0-2` | Inner fractal + final symbols |
| Labels | `LblNat`, `LblRat`... | One per act, white emission |
| Camera | `AbyssCam` | Orbiting dive toward origin |
| Lights | `Key`, `Fill`, `Rim` | Three-point, high energy |

---

## 5-Act Structure

```
Act 1        Act 2        Act 3        Act 4        Act 5
Naturals     Rationals    Irrationals  Fractal      Abyss
|------------|------------|------------|------------|------------|
1           576         1152         1728         2304        2880
```

| Act | Frames | Content | Layout |
|-----|--------|---------|--------|
| 1 | 1-575 | 15 naturals (1-15) | Archimedean spiral, r0=3, growth=0.4 |
| 2 | 576-1151 | 20 fractions | Spiral, r0=2, growth=0.3, smaller text |
| 3 | 1152-1727 | 10 irrationals | Circle r=12, cubic spiral inward |
| 4 | 1728-2303 | 27 Sierpinski pts | Depth-3 triangle, size=18 |
| 5 | 2304-2880 | 27 inner + 3 finals | Inner triangle size=6, z=-0.5 |

---

## Camera: Orbiting Dive

```python
radius = 35.0
azimuth = t * 3pi         # 1.5 full rotations
z = 40.0 -> 10.0          # dives starting at Act 4

x = radius * cos(azimuth)
y = radius * sin(azimuth)
```

Track To constraint keeps camera on origin. Keyframes every 6 frames.
The radius is constant; the dive effect comes from z-height reduction
during Acts 4-5, creating a sense of falling into the fractal.

---

## Materials

| Material | RGB | Emission | Represents |
|----------|-----|----------|------------|
| `MatNat` | (0.3, 0.7, 1.0) | 30x | Natural numbers |
| `MatRat` | (0.1, 1.0, 0.4) | 30x | Rational numbers |
| `MatIrr` | (1.0, 0.1, 0.6) | 30x | Irrational numbers |
| `MatFrac` | (1.0, 0.85, 0.1) | 30x | Fractal geometry |
| `MatAbyss` | (1.0, 0.05, 0.15) | 30x | Infinite descent |
| `MatLabel` | (1.0, 1.0, 1.0) | 30x | Act labels |

---

## Animation Mechanics

**Spawn stagger:** Each number appears sequentially with a delay:
- Naturals: 36 frames apart
- Rationals: 24 frames apart
- Irrationals: 48 frames apart
- Fractal: 16 frames apart
- Abyss: 12 frames apart

**Idle drift:** After spawn, numbers bob gently:
```python
amplitude = 0.12  # naturals, varies per act
offset = spawn_frame + 60
```

**Irrational spiral-in:** 120-frame cubic easing from radius 12 to
radius 4.8, rotating pi radians. Keyframes every 8 frames.

---

## Lighting

Three-point setup for deep-space aesthetic:

| Light | Type | Energy | Position |
|-------|------|--------|----------|
| Key | POINT | 3000 W | (0, 0, 50) |
| Fill | POINT | 1200 W | (25, -20, 40) |
| Rim | POINT | 800 W | (-15, 25, 35) |

---

## Running

```python
# scenes/fractal_abyss/launcher.py
TOTAL_FRAMES = 2880     # 2 min at 24 fps
TIMING = Timing(act1=1, act2=576, act3=1152, act4=1728, act5=2304)
```

Paste `launcher.py` into Blender > Scripting > Run Script.

1. Press **Z** > **Rendered** to see emission glow
2. Press **Space** to play
3. Adjust `TIMING` to shift act boundaries

---

## Customisation

- **Add numbers:** Edit `act1_naturals.py`, extend `_NUMS` list
- **Change spiral:** Modify `r0`, `growth` params in each act
- **Adjust pacing:** Change `TIMING` in launcher
- **New act:** Create `act6_*.py`, import in `builder.py`

---

## File Structure

```
fractal_abyss/
├── launcher.py              # Config: TIMING, TOTAL_FRAMES
├── scene.py                 # Orchestrator: env + builder + camera
└── animations/
    ├── builder.py           # Assembles 5 acts + staging
    ├── domain/
    │   └── timing.py        # Timing NamedTuple (5 act markers)
    ├── staging/
    │   ├── camera.py        # Orbiting dive camera
    │   ├── lights.py        # Three-point lighting
    │   ├── materials.py     # 6 emission materials
    │   └── labels.py        # Per-act text labels
    └── acts/
        ├── act1_naturals.py    # 15 natural numbers
        ├── act2_rationals.py   # 20 fractions
        ├── act3_irrationals.py # 10 constants + spiral
        ├── act4_fractal.py     # 27 Sierpinski points
        └── act5_abyss.py       # Inner fractal + finals
```
