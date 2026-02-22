# File: scenes/quasar_bh/scene.py
# Black-hole quasar scene — accretion disk with Keplerian differential
# rotation, relativistic jets, and a slow spherical camera orbit.
# No secondary body. Starfield lives in the world shader (zero object cost).
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

from app.kernel.dispatcher import dispatch_batch
import app.commands  # triggers all command registrations

# ── Keplerian physics ──────────────────────────────────────────────────────
# In Newtonian gravity, circular-orbit angular velocity ω ∝ r^(-3/2).
# We normalise so the innermost ring (r = R_REF) has speed 1.0.
_R_REF = 3.0


def _keplerian_speed(r: float) -> float:
    """Angular velocity relative to the innermost ring — Kepler's 3rd law."""
    return (_R_REF / r) ** 1.5


# ── Accretion disk rings ───────────────────────────────────────────────────
# Colors follow a black-body gradient: white-blue (hottest) → dark red (cool).
_DISK_RINGS = [
    {'radius':  3.0, 'color': (1.00, 1.00, 1.00)},   # white-blue  (10 000 K+)
    {'radius':  4.2, 'color': (1.00, 0.97, 0.75)},   # warm white
    {'radius':  5.5, 'color': (1.00, 0.85, 0.35)},   # yellow
    {'radius':  7.0, 'color': (1.00, 0.60, 0.10)},   # orange
    {'radius':  8.5, 'color': (1.00, 0.35, 0.03)},   # orange-red
    {'radius': 10.0, 'color': (0.80, 0.15, 0.01)},   # red
    {'radius': 11.5, 'color': (0.55, 0.07, 0.01)},   # dark red
    {'radius': 13.0, 'color': (0.30, 0.03, 0.01)},   # very dark red
    {'radius': 14.5, 'color': (0.15, 0.01, 0.01)},   # near-invisible outer edge
]

# ── Quality presets ────────────────────────────────────────────────────────
# All frame counts assume 30 fps.
#
#   low    →  5 rings, 900 f  (30 s)  — safe for small GPUs
#   medium →  7 rings, 1800 f (60 s)  — Intel i7 + 24 GB RAM sweet spot
#   high   →  9 rings, 3600 f (2 min) — workstation
#
PRESETS: Dict[str, Dict[str, Any]] = {
    'low': {
        'total_frames':    900,
        'disk_ring_count': 5,
        'disk_rotations':  8,    # base rotations for innermost ring
        'cam_step':        30,   # insert keyframe every N frames
        'disk_step':       30,
        'eevee_samples':   8,
    },
    'medium': {
        'total_frames':    1800,
        'disk_ring_count': 7,
        'disk_rotations':  12,
        'cam_step':        20,
        'disk_step':       20,
        'eevee_samples':   16,
    },
    'high': {
        'total_frames':    3600,
        'disk_ring_count': 9,
        'disk_rotations':  18,
        'cam_step':        10,
        'disk_step':       10,
        'eevee_samples':   32,
    },
}


def create_scene(quality: str = 'low') -> Dict[str, Any]:
    """
    Build and dispatch the quasar black-hole animation.

    Args:
        quality: 'low' | 'medium' | 'high'
                 Start with 'low'. Upgrade once you confirm it runs smoothly.

    Returns:
        Dict with 'results', 'frames', and 'quality'.
    """
    if quality not in PRESETS:
        raise ValueError(f"quality must be one of {list(PRESETS)}; got '{quality}'")

    p = PRESETS[quality]
    total_frames    = p['total_frames']
    disk_rings      = _DISK_RINGS[:p['disk_ring_count']]
    disk_rotations  = p['disk_rotations']
    cam_step        = p['cam_step']
    disk_step       = p['disk_step']

    batch: List[Dict[str, Any]] = []

    # ── 0. Clean slate ──────────────────────────────────────────────────────
    # Removes Blender's default cube, lamp, and camera so nothing interferes.
    batch.append({'cmd': 'clear_scene', 'args': {}})

    # ── 1. Render: Eevee + bloom ────────────────────────────────────────────
    # Bloom is what makes the emissive materials actually glow visually.
    # Without it the disk looks like plain coloured rings.
    batch.append({'cmd': 'configure_eevee', 'args': {
        'width': 1280, 'height': 720, 'samples': p['eevee_samples'],
    }})

    # ── 2. Timeline ─────────────────────────────────────────────────────────
    batch.append({'cmd': 'set_frame_range', 'args': {'start': 1, 'end': total_frames}})

    # ── 3. World: pure black + procedural Voronoi starfield ────────────────
    # Stars are baked into the world shader — no individual sphere objects,
    # so they cost nothing in terms of scene complexity or GPU memory.
    batch.append({'cmd': 'create_space_world', 'args': {
        'star_density': 350,
        'star_brightness': 2.5,
    }})

    # ── 4. Yellow accent light ──────────────────────────────────────────────
    # Warm golden point light positioned above and to the side of the disk.
    # Gives the tori volume and makes the black hole visible as a dark absence.
    batch.append({'cmd': 'create_light', 'args': {
        'name':     'AccretionLight',
        'type':     'POINT',
        'location': (8, -4, 18),
        'color':    (1.0, 0.85, 0.3),   # warm golden yellow
        'energy':   5000,
    }})

    # ── 5. Black Hole ───────────────────────────────────────────────────────
    # Pure black, non-emissive sphere. The absence of light defines it.
    batch.append({'cmd': 'create_material', 'args': {
        'name': 'BlackHoleMat', 'color': (0, 0, 0, 1),
    }})
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'BlackHole'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'BlackHole', 'material': 'BlackHoleMat'}})
    batch.append({'cmd': 'scale_object',    'args': {'name': 'BlackHole', 'scale': (2, 2, 2)}})

    # ── 6. Accretion disk — Keplerian differential rotation ─────────────────
    # Inner rings rotate faster (ω ∝ r^-1.5). Colours follow a black-body
    # gradient from white-blue at the innermost ring to deep red at the outer.
    for i, ring in enumerate(disk_rings):
        r        = ring['radius']
        mat_name = f"RingMat_{i}"
        speed    = _keplerian_speed(r)

        # Emission strength fades for outer (cooler) rings
        emit_str = round(8.0 * max(0.3, 1.0 - i * 0.08), 2)

        batch.append({'cmd': 'create_material', 'args': {
            'name':          mat_name,
            'color':         ring['color'] + (1.0,),
            'emit':          True,
            'emit_strength': emit_str,
        }})
        batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'torus', 'name': f"Ring_{i}"}})
        batch.append({'cmd': 'assign_material', 'args': {'object': f"Ring_{i}", 'material': mat_name}})
        # Flatten torus into a thin disk plane
        batch.append({'cmd': 'scale_object', 'args': {'name': f"Ring_{i}", 'scale': (r, r, 0.12)}})

        # Animate Z-rotation (radians) with Keplerian speed
        for f in range(1, total_frames + 1, disk_step):
            angle = (f / total_frames) * 2 * math.pi * disk_rotations * speed
            batch.append({'cmd': 'rotate_object', 'args': {
                'name':     f"Ring_{i}",
                'rotation': (0, 0, angle),
                'frame':    f,
            }})

    # ── 7. Relativistic jets ────────────────────────────────────────────────
    # Narrow cones along the polar axis, parented to the black hole.
    # The electric-blue emission contrasts with the warm disk colours.
    batch.append({'cmd': 'create_material', 'args': {
        'name':          'JetMat',
        'color':         (0.7, 0.9, 1.0, 1.0),
        'emit':          True,
        'emit_strength': 10.0,
    }})
    for jet_name, z_pos in [('JetNorth', 28), ('JetSouth', -28)]:
        batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'cone', 'name': jet_name}})
        batch.append({'cmd': 'assign_material', 'args': {'object': jet_name, 'material': 'JetMat'}})
        batch.append({'cmd': 'scale_object',    'args': {'name': jet_name, 'scale': (0.18, 0.18, 55)}})
        batch.append({'cmd': 'move_object',     'args': {'name': jet_name, 'location': (0, 0, z_pos)}})
        batch.append({'cmd': 'parent_object',   'args': {'child': jet_name, 'parent': 'BlackHole'}})

    # ── 8. Camera — slow spherical orbit ────────────────────────────────────
    # The camera moves on the surface of a sphere: azimuth sweeps 270° while
    # elevation oscillates between 20° and 45°, giving a sense of depth.
    # A Track To constraint keeps it pointed at the black hole at all times.
    batch.append({'cmd': 'create_camera', 'args': {'name': 'SceneCamera'}})

    cam_r = 22  # orbital radius (units)
    for f in range(1, total_frames + 1, cam_step):
        t         = (f - 1) / max(total_frames - 1, 1)
        azimuth   = t * 2 * math.pi * 0.75                  # 270° sweep
        elevation = math.radians(20 + 25 * math.sin(t * math.pi))  # 20°→45°→20°

        x = cam_r * math.cos(elevation) * math.cos(azimuth)
        y = cam_r * math.cos(elevation) * math.sin(azimuth)
        z = cam_r * math.sin(elevation)

        batch.append({'cmd': 'move_object', 'args': {
            'name': 'SceneCamera', 'location': (x, y, z), 'frame': f,
        }})

    # Add Track To constraint — camera always faces the origin
    batch.append({'cmd': 'set_camera_target', 'args': {
        'name': 'SceneCamera', 'target': (0, 0, 0),
    }})

    # ── 9. Dispatch ─────────────────────────────────────────────────────────
    results = dispatch_batch(batch)
    return {'results': results, 'frames': total_frames, 'quality': quality}
