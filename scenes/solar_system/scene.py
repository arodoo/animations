# File: scenes/solar_system/scene.py
# Solar System scene — thin orchestrator, consumes parent components.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands  # triggers all command registrations

from app.components.env_builder import build_environment
from app.components.camera_builder import build_camera
from app.components.bodies.compact_object import build_compact_object

from .materials._presets import PRESETS
from .animations._orbit import build_orbits


def create_scene(quality: str = 'low') -> Dict[str, Any]:
    """Build and dispatch the Solar System animation.

    Args:
        quality: 'low' | 'medium' | 'high' | 'ultra'

    Returns:
        Dict with 'results', 'frames', and 'quality'.
    """
    if quality not in PRESETS:
        raise ValueError(
            f"quality must be one of {list(PRESETS)};"
            f" got '{quality}'"
        )
    p = PRESETS[quality]

    batch = []
    batch += build_environment({
        'total_frames': p['total_frames'],
        'world_color':  (0.01, 0.01, 0.015),
        'grid':         False,
        'lights': [
            {'name': 'SunLight', 'type': 'POINT'},
        ],
    })
    batch += build_compact_object({
        'name':          'Sun',
        'material_name': 'SunMat',
        'color':         (1.0, 0.95, 0.70, 1.0),
        'r_s':           1.0,
        'segments':      64,
        'ring_count':    32,
        'subsurf':       True,
    })
    batch += build_orbits(
        p['planets'], p['total_frames'], step=p['cam_step'],
    )
    batch += build_camera({
        'name':          'SceneCamera',
        'total_frames':  p['total_frames'],
        'cam_step':      p['cam_step'],
        'radius':        60.0,
        'focal_length':  55.0,
        'dof':           p['dof'],
        'dof_focus_dist': 14.0,
        'dof_fstop':      4.0,
        'el_base_deg':   50.0,
        'el_amp_deg':    20.0,
        'el_freq':        2.0,
        'breathe_amp':   0.15,
        'breathe_freq':   1.5,
    })

    results = dispatch_batch(batch)
    return {
        'results': results,
        'frames':  p['total_frames'],
        'quality': quality,
    }
