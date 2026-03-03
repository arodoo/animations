# File: scenes/math_sets/animations/_camera.py
# Camera orbit for the Math Sets scene.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List


def build_camera(
    camera_radius: float,
    total_frames: int
) -> List[Dict]:
    """15-deg slow orbit, slight rise over full duration."""
    sweep = math.radians(15)
    cmds: List[Dict] = [
        {'cmd': 'create_camera',
         'args': {'name': 'SceneCamera'}},
        {'cmd': 'set_focal_length', 'args': {
            'name': 'SceneCamera',
            'focal_length': 40.0,
        }},
        {'cmd': 'set_camera_target', 'args': {
            'name': 'SceneCamera',
            'target': (0, 0, 0),
        }},
        {'cmd': 'set_depth_of_field', 'args': {
            'name': 'SceneCamera',
            'enabled': True,
            'focus_distance': camera_radius,
            'fstop': 2.8,
        }},
    ]
    for f in range(1, total_frames + 1, 100):
        t = (f - 1) / total_frames
        a = math.radians(-90) + t * sweep
        cx = math.cos(a) * camera_radius
        cy = math.sin(a) * camera_radius
        cz = camera_radius * 0.4 + t * 1.5
        cmds.append({'cmd': 'move_object', 'args': {
            'name': 'SceneCamera',
            'location': (cx, cy, cz),
            'frame': f,
        }})
    return cmds
