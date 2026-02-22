# File: scenes/quasar_bh/_cam.py
# Camera: spherical orbit with depth of field.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

_CAM_RADIUS = 22      # orbital sphere radius (Blender units)
_FOCAL_LENGTH = 35.0  # mm — wide cinematic lens


def build_camera(
    total_frames: int, cam_step: int, dof: bool,
) -> List[Dict]:
    """
    Spherical orbit: azimuth sweeps 270°, elevation oscillates
    20° → 45° → 20°. Track To constraint faces the origin.
    """
    r = _CAM_RADIUS
    cmds: List[Dict] = [
        {'cmd': 'create_camera', 'args': {
            'name': 'SceneCamera',
        }},
        {'cmd': 'set_focal_length', 'args': {
            'name':         'SceneCamera',
            'focal_length': _FOCAL_LENGTH,
        }},
    ]
    for f in range(1, total_frames + 1, cam_step):
        t = (f - 1) / max(total_frames - 1, 1)
        az = t * 2 * math.pi * 0.75
        el = math.radians(20 + 25 * math.sin(t * math.pi))
        x = r * math.cos(el) * math.cos(az)
        y = r * math.cos(el) * math.sin(az)
        z = r * math.sin(el)
        cmds.append({'cmd': 'move_object', 'args': {
            'name':     'SceneCamera',
            'location': (x, y, z),
            'frame':    f,
        }})
    cmds.append({'cmd': 'set_camera_target', 'args': {
        'name': 'SceneCamera', 'target': (0, 0, 0),
    }})
    if dof:
        cmds.append({'cmd': 'set_depth_of_field', 'args': {
            'name':           'SceneCamera',
            'enabled':        True,
            'focus_distance': float(_CAM_RADIUS),
            'fstop':          2.8,
        }})
    return cmds
