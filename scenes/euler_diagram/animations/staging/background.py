# Grid floor + XY axes sized for tight spiral.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

_AXES = [
    ('AxisX', (0, math.pi / 2, 0), 'MatAxisX'),
    ('AxisY', (math.pi / 2, 0, 0), 'MatAxisY'),
]


def build_background() -> List[Dict]:
    """30-BU grid + thin XY axis lines. No Z axis."""
    cmds: List[Dict] = [
        {'cmd': 'create_cartesian_grid', 'args': {
            'size': 30,
            'grid_scale': 1,
            'z_offset': -0.1,
            'bg_color': (0.01, 0.012, 0.03, 1.0),
            'line_color': (0.08, 0.12, 0.30, 1.0),
        }},
    ]
    for name, rot, mat in _AXES:
        cmds.append({'cmd': 'spawn_primitive', 'args': {
            'type': 'cylinder',
            'name': name,
            'location': (0, 0, -0.08),
            'rotation': rot,
            'radius': 0.025,
            'depth': 28,
        }})
        cmds.append({'cmd': 'assign_material', 'args': {
            'object': name,
            'material': mat,
        }})
    return cmds
