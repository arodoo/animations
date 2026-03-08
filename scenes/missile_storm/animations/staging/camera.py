# File: scenes/missile_storm/animations/staging/camera.py
# Camera follows butterfly throughout the scene.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.timing import Timing
from .camera_follow import build_follow_phase


def build_storm_camera(
    timing: Timing,
    step: int = 4,
) -> List[Dict]:
    """Camera rig: create + follow butterfly."""
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
    cmds.append({
        'cmd': 'set_camera_target',
        'args': {
            'name': 'StormCam',
            'target': (0, 0, 8),
        },
    })
    return cmds
