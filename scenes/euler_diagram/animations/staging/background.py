# Grid floor + XY axes only (no Z tube).
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

_AXES = [
    ('AxisX', (0, math.pi / 2, 0), 'MatAxisX'),
    ('AxisY', (math.pi / 2, 0, 0), 'MatAxisY'),
]


def build_background() -> List[Dict]:
    """Grid floor and thin XY axis lines. No Z axis."""
    cmds: List[Dict] = [
        {'cmd': 'create_cartesian_grid', 'args': {
            'size': 400,
            'grid_scale': 10,
            'z_offset': -2.5,
            'bg_color': (0.01, 0.012, 0.03, 1.0),
            'line_color': (0.06, 0.09, 0.22, 1.0),
        }},
    ]
    for name, rot, mat in _AXES:
        cmds.append({'cmd': 'spawn_primitive', 'args': {
            'type': 'cylinder',
            'name': name,
            'location': (0, 0, -2.0),
            'rotation': rot,
            'radius': 0.04,
            'depth': 120,
        }})
        cmds.append({'cmd': 'assign_material', 'args': {
            'object': name,
            'material': mat,
        }})
    return cmds
