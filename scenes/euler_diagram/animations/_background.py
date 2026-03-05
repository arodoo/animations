# File: scenes/euler_diagram/animations/_background.py
# Glowing 3D math grid + colored coordinate axes.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

_AXES = [
    ('AxisX', (0, math.pi / 2, 0), 'MatAxisX'),
    ('AxisY', (math.pi / 2, 0, 0), 'MatAxisY'),
    ('AxisZ', (0, 0, 0),           'MatAxisZ'),
]


def build_background() -> List[Dict]:
    """Bright grid floor + glowing XYZ axis lines."""
    cmds: List[Dict] = [
        {'cmd': 'create_cartesian_grid', 'args': {
            'size': 300,
            'grid_scale': 8,
            'z_offset': -2.0,
            'bg_color': (0.008, 0.01, 0.022, 1.0),
            'line_color': (0.08, 0.12, 0.30, 1.0),
        }},
    ]
    for name, rot, mat in _AXES:
        cmds.append({'cmd': 'spawn_primitive', 'args': {
            'type': 'cylinder',
            'name': name,
            'location': (0, 0, 0),
            'rotation': rot,
            'radius': 0.06,
            'depth': 80,
        }})
        cmds.append({'cmd': 'assign_material', 'args': {
            'object': name,
            'material': mat,
        }})
    return cmds
