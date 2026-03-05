# File: scenes/euler_diagram/animations/_camera.py
# Camera with cinematic zoom-out from inner to outer.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

_ANGLE = math.radians(30)


def build_camera(
    total_frames: int,
    zoom_start: int,
    zoom_end: int,
) -> List[Dict]:
    """Camera pulls back from inner circle to full view."""
    cmds: List[Dict] = [
        {'cmd': 'create_camera',
         'args': {'name': 'SceneCamera'}},
        {'cmd': 'set_focal_length', 'args': {
            'name': 'SceneCamera',
            'focal_length': 70.0,
        }},
        {'cmd': 'set_camera_target', 'args': {
            'name': 'SceneCamera',
            'target': (0, 0, 0),
        }},
    ]
    for f in range(1, total_frames + 1, 20):
        if f <= zoom_start:
            dist, h = 15.0, 10.0
        elif f >= zoom_end:
            dist, h = 70.0, 35.0
        else:
            t = (
                (f - zoom_start)
                / (zoom_end - zoom_start)
            )
            dist = 15.0 + 55.0 * t
            h = 10.0 + 25.0 * t
        cx = math.cos(_ANGLE) * dist
        cy = math.sin(_ANGLE) * dist
        cmds.append({'cmd': 'move_object', 'args': {
            'name': 'SceneCamera',
            'location': (cx, cy, h),
            'frame': f,
        }})
    return cmds
