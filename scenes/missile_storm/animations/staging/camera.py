# File: scenes/missile_storm/animations/staging/camera.py
# Camera: follow butterfly, then dramatic pullback.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.timing import Timing
from .camera_follow import build_follow_phase
from .camera_pullback import build_pullback_phase


def build_storm_camera(
    timing: Timing,
    step: int = 4,
) -> List[Dict]:
    """Full camera rig: create + animate."""
    cmds: List[Dict] = [
        {
            'cmd': 'create_camera',
            'args': {'name': 'StormCam'},
        },
        {
            'cmd': 'set_focal_length',
            'args': {
                'name': 'StormCam',
                'focal_length': 50.0,
            },
        },
    ]
    cmds += build_follow_phase(timing, step)
    cmds += build_pullback_phase(timing, step)
    cmds.append({
        'cmd': 'set_camera_target',
        'args': {
            'name': 'StormCam',
            'target': (0, 0, 0),
        },
    })
    return cmds
