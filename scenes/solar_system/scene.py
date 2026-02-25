# File: scenes/solar_system/scene.py
# Solar System scene — thin orchestrator, consumes parent components.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands  # triggers all command registrations

from app.components.env_builder import build_environment
from app.components.camera_builder import build_camera

# Bootstraps our local command registry for metals
import scenes.solar_system.commands  # noqa: F401

from .materials._presets import PRESETS
from .animations._orrery import build_orrery


def create_scene(
    quality: str = 'low',
    total_frames: int | None = None,
    camera_radius: float | None = None
) -> Dict[str, Any]:
    """Build and dispatch the Solar System animation.

    Args:
        quality: 'low' | 'medium' | 'high' | 'ultra'
        total_frames: Optional override for duration
        camera_radius: Optional override for camera distance

    Returns:
        Dict with 'results', 'frames', and 'quality'.
    """
    if quality not in PRESETS:
        raise ValueError(
            f"quality must be one of {list(PRESETS)};"
            f" got '{quality}'"
        )
    p = PRESETS[quality].copy()  # Clone preset
    if total_frames is not None:
        p['total_frames'] = total_frames
    
    rad = camera_radius if camera_radius is not None else 100.0

    batch = []
    batch += build_environment({
        'total_frames': p['total_frames'],
        'world_color':  (0.01, 0.01, 0.015),
        'grid':         False,
        'lights': [
            {'name': 'SunLight', 'type': 'POINT'},
        ],
    })
    batch.append({'cmd': 'create_space_world', 'args': {
        'star_density': 400.0,
        'star_brightness': 3.0,
    }})
    batch += build_orrery(
        p['planets'], p['total_frames'], step=p['cam_step'],
    )
    batch += build_camera({
        'name':          'SceneCamera',
        'total_frames':  p['total_frames'],
        'cam_step':      p['cam_step'],
        'radius':        rad,
        'focal_length':  55.0,
        'dof':           False,
        'dof_focus_dist': 14.0,
        'dof_fstop':      4.0,
        'el_base_deg':   0.0,
        'el_amp_deg':    70.0,
        'el_freq':        2.0,
        'breathe_amp':   0.0,
        'breathe_freq':  0.0,
    })

    results = dispatch_batch(batch)
    return {
        'results': results,
        'frames':  p['total_frames'],
        'quality': quality,
    }
