# File: scenes/quasar_bh/scene.py
# Quasar black-hole scene — thin orchestrator.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands  # triggers all command registrations

from ._presets import PRESETS
from ._physics import DISK_RINGS
from ._env import build_environment
from ._bh_jets import build_black_hole, build_jets
from ._disk_build import build_ring
from ._disk_animate import build_disk_animation
from ._cam import build_camera


def create_scene(quality: str = 'low') -> Dict[str, Any]:
    """
    Build and dispatch the quasar black-hole animation.

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
    disk_rings = DISK_RINGS[:p['disk_ring_count']]

    batch = []
    batch += build_environment(p)
    batch += build_black_hole()
    for i, ring in enumerate(disk_rings):
        batch += build_ring(i, ring)
    batch += build_disk_animation(
        disk_rings,
        p['total_frames'],
        p['disk_rotations'],
        p['disk_step'],
        p['pulse_inner'],
        p['particles'],
    )
    batch += build_jets(p['particles'])
    batch += build_camera(
        p['total_frames'], p['cam_step'], p['dof'],
    )

    results = dispatch_batch(batch)
    return {
        'results': results,
        'frames': p['total_frames'],
        'quality': quality,
    }
