# File: tests/demos/quasar_demo.py
# Quasar animation: a black hole consuming a star, with an accretion disk
# and relativistic jets. This 3-minute animation showcases advanced particle
# effects and complex, physics-inspired motion.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List
from app.kernel.dispatcher import dispatch_batch
from app.scene.atmospheres.space_atmosphere import generate_starfield

# Import commands to trigger registration
import app.commands

# ---------------------------------------------------------------------------
# Quality presets — pick 'low' on slow machines, 'high' on workstations.
#
#   low    → ~40 stars, 600 frames (20s),  keyframe every 30f  ← safe default
#   medium → ~150 stars, 1800 frames (1min), keyframe every 20f
#   high   → ~400 stars, 5400 frames (3min), keyframe every 10f
# ---------------------------------------------------------------------------
_PRESETS: Dict[str, Dict[str, Any]] = {
    'low': {
        'star_count':      40,
        'total_frames':    600,
        'disk_ring_count': 3,
        'disk_rotations':  6,     # full rotations the fastest ring completes
        'cam_step':        30,    # insert camera keyframe every N frames
        'star_step':       30,    # insert DyingStar keyframe every N frames
        'eevee_samples':   8,
    },
    'medium': {
        'star_count':      150,
        'total_frames':    1800,
        'disk_ring_count': 5,
        'disk_rotations':  10,
        'cam_step':        20,
        'star_step':       20,
        'eevee_samples':   16,
    },
    'high': {
        'star_count':      400,
        'total_frames':    5400,
        'disk_ring_count': 5,
        'disk_rotations':  16,
        'cam_step':        10,
        'star_step':       10,
        'eevee_samples':   32,
    },
}

_ALL_DISK_RINGS = [
    {'radius': 3.5, 'color': (1.0, 1.0, 0.8), 'speed': 2.8},
    {'radius': 4.5, 'color': (1.0, 0.9, 0.2), 'speed': 2.5},
    {'radius': 6.0, 'color': (1.0, 0.5, 0.1), 'speed': 2.0},
    {'radius': 7.5, 'color': (0.9, 0.2, 0.05), 'speed': 1.8},
    {'radius': 9.0, 'color': (0.8, 0.1, 0.0), 'speed': 1.5},
]


def create_quasar_animation(quality: str = 'low') -> Dict[str, Any]:
    """
    Creates a quasar animation (black hole + accretion disk + jets + dying star).

    Args:
        quality: 'low' | 'medium' | 'high'
                 Start with 'low' — upgrade once you confirm it runs smoothly.
    """
    if quality not in _PRESETS:
        raise ValueError(f"quality must be one of {list(_PRESETS)}; got '{quality}'")

    p = _PRESETS[quality]
    total_frames      = p['total_frames']
    star_count        = p['star_count']
    disk_ring_count   = p['disk_ring_count']
    disk_rotations    = p['disk_rotations']
    cam_step          = p['cam_step']
    star_step         = p['star_step']
    eevee_samples     = p['eevee_samples']
    disk_rings        = _ALL_DISK_RINGS[:disk_ring_count]

    batch: List[Dict[str, Any]] = []

    # 0. Clear default Blender scene (removes the default cube, light, camera)
    batch.append({'cmd': 'clear_scene', 'args': {}})

    # 1. Render engine + bloom — must come early so Blender uses these settings
    batch.append({'cmd': 'configure_eevee', 'args': {
        'width': 1280, 'height': 720, 'samples': eevee_samples,
    }})

    # 2. Scene Setup
    batch.append({'cmd': 'set_frame_range', 'args': {'start': 1, 'end': total_frames}})
    batch.append({'cmd': 'set_world_background', 'args': {'color': (0, 0, 0)}})

    # 3. Starfield
    batch.append({'cmd': 'create_material', 'args': {
        'name': 'StarGlowMat', 'color': (0.9, 0.9, 1.0, 1.0),
        'emit': True, 'emit_strength': 3.0,
    }})
    star_commands = generate_starfield(star_count=star_count, radius=150.0)
    for star_cmd in star_commands:
        batch.append(star_cmd)
        if star_cmd['cmd'] == 'spawn_primitive' and 'Star_' in star_cmd['args']['name']:
            batch.append({'cmd': 'assign_material', 'args': {
                'object': star_cmd['args']['name'], 'material': 'StarGlowMat',
            }})

    # 4. Black Hole — pure black sphere, no emission
    batch.append({'cmd': 'create_material', 'args': {'name': 'BlackHoleMat', 'color': (0, 0, 0, 1)}})
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'BlackHole'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'BlackHole', 'material': 'BlackHoleMat'}})
    batch.append({'cmd': 'scale_object', 'args': {'name': 'BlackHole', 'scale': (2, 2, 2)}})

    # 5. Accretion Disk
    #    Rotation is in RADIANS. Each ring completes `disk_rotations * speed`
    #    full turns over the entire animation — innermost ring spins fastest.
    for i, ring in enumerate(disk_rings):
        mat_name = f"RingMat{i}"
        batch.append({'cmd': 'create_material', 'args': {
            'name': mat_name, 'color': ring['color'] + (1.0,),
            'emit': True, 'emit_strength': 8.0,
        }})
        batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'torus', 'name': f"DiskRing{i}"}})
        batch.append({'cmd': 'assign_material', 'args': {'object': f"DiskRing{i}", 'material': mat_name}})
        batch.append({'cmd': 'scale_object', 'args': {'name': f"DiskRing{i}", 'scale': (ring['radius'], ring['radius'], 0.25)}})

        for f in range(1, total_frames + 1, cam_step):
            # radians — NOT degrees
            angle = (f / total_frames) * 2 * math.pi * disk_rotations * ring['speed']
            batch.append({'cmd': 'rotate_object', 'args': {
                'name': f"DiskRing{i}", 'rotation': (0, 0, angle), 'frame': f,
            }})

    # 6. Relativistic Jets (cones parented to the black hole)
    batch.append({'cmd': 'create_material', 'args': {
        'name': 'JetMat', 'color': (0.7, 0.9, 1.0, 1.0),
        'emit': True, 'emit_strength': 10.0,
    }})
    for direction, z_pos in [('North', 26), ('South', -26)]:
        jet_name = f'Jet{direction}'
        batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'cone', 'name': jet_name}})
        batch.append({'cmd': 'assign_material', 'args': {'object': jet_name, 'material': 'JetMat'}})
        batch.append({'cmd': 'scale_object', 'args': {'name': jet_name, 'scale': (0.2, 0.2, 50)}})
        batch.append({'cmd': 'move_object', 'args': {'name': jet_name, 'location': (0, 0, z_pos)}})
        batch.append({'cmd': 'parent_object', 'args': {'child': jet_name, 'parent': 'BlackHole'}})

    # 7. Consumed Star — spirals inward and shrinks (Newtonian inspiral)
    batch.append({'cmd': 'create_material', 'args': {
        'name': 'StarMat', 'color': (0.7, 0.9, 1.0, 1.0),
        'emit': True, 'emit_strength': 6.0,
    }})
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'DyingStar'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'DyingStar', 'material': 'StarMat'}})

    for f in range(1, total_frames + 1, star_step):
        t = (f - 1) / max(total_frames - 1, 1)
        # Radius shrinks quadratically: 15 → 2.5 units
        radius = 15.0 + (2.5 - 15.0) * (t ** 2)
        # 10 full orbits as the star falls in
        angle = t * 10 * 2 * math.pi
        z = 1.5 * math.sin(t * math.pi * 4)
        batch.append({'cmd': 'move_object', 'args': {
            'name': 'DyingStar',
            'location': (radius * math.cos(angle), radius * math.sin(angle), z),
            'frame': f,
        }})
        scale = max(0.01, 0.8 * (1 - t))  # clamp so it never goes negative
        batch.append({'cmd': 'scale_object', 'args': {
            'name': 'DyingStar', 'scale': (scale, scale, scale), 'frame': f,
        }})

    # 8. Orbiting Camera — position keyframes only;
    #    set_camera_target adds a Track To constraint so it always faces the BH.
    batch.append({'cmd': 'create_camera', 'args': {'name': 'SceneCamera'}})
    for f in range(1, total_frames + 1, cam_step):
        angle = (f / total_frames) * 2 * math.pi
        batch.append({'cmd': 'move_object', 'args': {
            'name': 'SceneCamera',
            'location': (25 * math.cos(angle), 25 * math.sin(angle), 8),
            'frame': f,
        }})
    batch.append({'cmd': 'set_camera_target', 'args': {'name': 'SceneCamera', 'target': (0, 0, 0)}})

    # 9. Dispatch
    results = dispatch_batch(batch)
    return {'results': results, 'frames': total_frames, 'quality': quality}
