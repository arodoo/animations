# Quasar Black Hole — Scene Reference

## How the animation is built

`scene.py` is the thin orchestrator. It reads a quality preset, slices
the ring list to the configured count, and dispatches a flat batch of
commands through the app dispatcher to Blender.

```
create_scene(quality)
  └─ build_environment   → clear_scene, world color, 2 lights
  └─ build_black_hole    → material + sphere (r_s scale) + jets parent
  └─ build_ring × N      → material + torus + assign_material  (per ring)
  └─ build_disk_animation→ rotate_object keyframes + emission pulses
  └─ build_jets          → 2 cones (JetNorth / JetSouth) + QuasarJetMat
  └─ build_camera        → camera orbit keyframes + optional DoF
```

---

## Physics model (`animations/_physics.py`)

Ring rotation uses the **Paczyński–Wiita** pseudo-Newtonian potential
(not plain Keplerian). This captures the ISCO runaway near the event
horizon so inner rings spin dramatically faster than outer ones.

```
Ω(r) = sqrt( 1 / ( r · (r - r_s)² ) )   [GM = 1, r_s = 1.0 scene unit]
```

Key constants:
| Symbol | Value | Meaning |
|--------|-------|---------|
| `SCHWARZSCHILD_RADIUS` | 1.0 | r_s in scene units |
| ISCO | 3 × r_s = 3.0 | innermost stable circular orbit |
| innermost ring | r = 1.20 | just outside r_s |

`keplerian_speed()` is kept for backwards compatibility but **deprecated**
— never use it for new code.

Emission per ring is modulated by two relativistic corrections:
- **Gravitational redshift**: `sqrt(1 - r_s/r)` — reduces observed flux
  for deep-potential rings.
- **Doppler boost**: `1 + 0.5·β` (view-averaged approximation) where
  `β = v/c` from the Paczyński–Wiita tangential velocity.

---

## Disk geometry (`animations/_disk_build.py`)

Each ring is a torus with:
- `major_segments = 192`, `minor_segments = 64` — high tessellation for
  smooth emission gradients.
- `minor_radius` is **computed** (not a fixed value). It is clamped so the
  inner tube edge never overlaps the black hole:

  ```
  max_allowed = r - (r_s + 0.05)
  minor_r = min(raw_gap × heat_factor, max_allowed)
  ```

Ring colours run white-hot → orange → deep red from inside to outside,
mirroring the thermal gradient of a real accretion disk.

---

## Disk animation (`animations/_disk_animate.py`)

`_frame_dt` calibrates a scene time unit so the **innermost ring**
completes exactly `disk_rotations` full orbits over `total_frames`.
Every other ring angle is then:

```
angle(r, f) = Ω(r) · f · dt
```

This guarantees the differential rotation ratio is exactly what the
Paczyński–Wiita potential predicts — no manual speed tweaking.

Emission pulses (`pulse_inner=True`) insert 4 keyframes on `RingMat_0`
at 1.6× base strength, simulating hotspot activity on the inner disk.

---

## Quality presets (`materials/_presets.py`)

| Quality | Rings | Frames | Rotations | Resolution | Particles | DoF |
|---------|-------|--------|-----------|------------|-----------|-----|
| low | 5 | 900 | 40 | 1280×720 | ✗ | ✗ |
| medium | 7 | 1800 | 60 | 1280×720 | ✗ | ✓ |
| high | 9 | 3600 | 90 | 1920×1080 | ✗ | ✓ |
| ultra | 9 | 3600 | 120 | 1920×1080 | ✓ | ✓ |

> **Rotation counts were the critical fix** — the original values (8/12/18/24)
> were too low relative to the Paczyński–Wiita angular velocity scale,
> causing the animation to appear nearly frozen. Correct values (40/60/90/120)
> produce visible differential rotation at all quality levels.

---

## Jets (`animations/_bh_jets.py` + `_jet_physics.py` + `_jet_animate.py`)

### Physics model

Jets are powered by the **Blandford–Znajek** mechanism and modelled with
full special-relativistic corrections:

| Parameter | Value | Source |
|-----------|-------|--------|
| Lorentz factor Γ | 7 | typical AGN quasar (Γ = 5–15) |
| β = v/c | `sqrt(1 - 1/Γ²) ≈ 0.990` | by definition |
| Rest-frame length | 55 scene units | tunable via `JET_REST_LENGTH` |
| Observed length | `55/Γ ≈ 7.86` | Lorentz contraction |

### Relativistic beaming

On-axis **Doppler/beaming factor** $D = \frac{1}{\Gamma(1 \mp \beta)}$:

- **North jet** (approaching observer): $D \gg 1$ → flux boosted by $D^3$,
  electric-blue colour `(0.55, 0.85, 1.0)`.
- **South jet** (receding): $D \ll 1$ → flux suppressed by $D^3$,
  orange-red colour `(1.0, 0.45, 0.20)`.

With Γ=7 and β≈0.990: $D_\text{north} \approx 14.1$, $D_\text{south} \approx 0.071$
— a factor ~200× brightness asymmetry, matching real radio-jet observations.

### Collimation profile

Jet radius follows an MHD parabolic-then-cylindrical model from
[Blandford & Payne 1982]:

$$r(z) = \begin{cases} r_b \cdot \sqrt{z / 5r_s} & z < 5r_s \quad \text{(parabolic funnel)} \\ r_b \cdot (1 + 0.015(z - 5r_s)) & z \ge 5r_s \quad \text{(slow cylindrical flare)} \end{cases}$$

The jet spawns as a `cylinder` with `depth = observed_length` and
`scale_x = scale_y = collimation_radius(length/2)`.

### Jet precession

Slow Lense-Thirring precession of the spin axis:

```
tilt(t) = 3.5° · sin(2π · t / 0.25)
```

Keyframed as `rotate_object` on `BlackHole` every 15 frames.
Period = 25% of the total animation (4 full precession cycles).

### Plasma knots

3 discrete knots per jet (`JET_KNOT_COUNT=3`), evenly phase-offset so
one knot is always mid-travel. Each knot:

- Spawns as a child sphere of its jet cylinder.
- Travels from `z=0` → `z=±0.9·length` over one full cycle.
- Scale shrinks from `s=0.07` (fresh) → `s=0.04` (aged) simulating
  adiabatic expansion of the plasma blob.
- Phase-staggered: knot k starts at `t = k/3` to avoid all knots
  ejecting simultaneously.

### File layout

| File | Responsibility |
|------|---------------|
| `_jet_physics.py` | Constants + pure functions (β, D, collimation, precession) |
| `_black_hole.py` | BH sphere geometry (no jet dependency) |
| `_bh_jets.py` | Jet materials + cylinder geometry |
| `_jet_animate.py` | Knot spawn + precession keyframes + knot travel |

---

## Camera (`animations/_cam.py`)

Spherical orbit at radius 60, focal length 85 mm (telephoto).

- Azimuth: full 360° sweep over the timeline.
- Elevation: 45° ± 10° (never on the polar/jet axis).
- Dolly-in: Gaussian close pass at t=0.5, reduces radius by 35% at peak.
- DoF: focus at 3.0 (inner disk), f/1.8.

---

## How to run in Blender

1. Open **Scripting** tab → paste `scenes/quasar_bh/launcher.py`.
2. Set `QUALITY` at the top of the file.
3. **Run Script** — the launcher purges `__pycache__` and stale module
   entries before importing, so edits are always picked up.
4. Viewport switches to **Material Preview** and playback starts
   automatically (`_setup_viewport()`).

---

## Key fixes applied (Feb 2026)

| File | What broke | Fix |
|------|-----------|-----|
| `_physics.py` | Used linear-spaced radii (3.0→14.5); no `SCHWARZSCHILD_RADIUS` | Replaced with logarithmic radii (1.20→19.35) starting near r_s; added full PW model |
| `_disk_animate.py` | Used `keplerian_speed` which ignored r_s; angle formula was relative not absolute | Switched to `pw_angular_velocity`; introduced `_frame_dt` calibration |
| `_disk_build.py` | Fixed `minor_radius=0.12` caused tori to overlap BH | Dynamic `_minor_radius()` clamped to `r - (r_s + 0.05)` |
| `_presets.py` | `disk_rotations` too low (8/12/18/24) → animation frozen | Raised to 40/60/90/120 |
| `_bh_jets.py` | Single static cone, one shared `QuasarJetMat`, no physics | Two cylinders with relativistic beaming, MHD collimation, knot animation |
| `_jet_physics.py` | Did not exist | New: Γ, β, D³ beaming factor, collimation radius, precession, knot emission |
| `_black_hole.py` | Did not exist | New: BH sphere extracted from _bh_jets for single responsibility |
| `_jet_animate.py` | Did not exist | New: knot spawn, precession keyframes, knot travel keyframes |
| `spawn_primitive.py` | Relied on `context.active_object` which races in mock/multi-object scenes | Name-diff approach: snapshot object names before/after op call |
| `_env.py` | Missing `clear_scene` at start → objects from prior runs accumulated | Added `clear_scene` as first command |
| `launcher.py` / `blender_launcher.py` | No auto-viewport switch; user had to manually hit Z+SPACE | Added `_setup_viewport()` that sets Material Preview + starts playback |
