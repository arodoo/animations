# File: scenes/euler_diagram/animations/_outer_circle.py
# Outer ring with diverse number types.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ._helpers import text_reveal

_RING_R = 15.0
_NUM_R = 11.0
_NUMS = [
    ('2', 0), ('4', 45),
    ('-1', 90), ('-5', 135),
    ('1/2', 180), ('3/4', 225),
    ('pi', 270), ('v2', 315),
]


def build_outer_circle(
    ring_frame: int,
    nums_frame: int,
) -> List[Dict]:
    """Large torus ring + diverse numbers staggered."""
    cmds: List[Dict] = [
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'torus',
            'name': 'AllNumsRing',
            'location': (0, 0, 0),
            'major_radius': _RING_R,
            'minor_radius': 0.12,
            'major_segments': 128,
        }},
        {'cmd': 'assign_material', 'args': {
            'object': 'AllNumsRing',
            'material': 'MatOuterRing',
        }},
        {'cmd': 'scale_object', 'args': {
            'name': 'AllNumsRing',
            'scale': (0, 0, 0),
            'frame': 1,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': 'AllNumsRing',
            'scale': (1, 1, 1),
            'frame': ring_frame,
        }},
    ]
    for i, (text, deg) in enumerate(_NUMS):
        a = math.radians(deg)
        x = _NUM_R * math.cos(a)
        y = _NUM_R * math.sin(a)
        f = nums_frame + i * 15
        cmds += text_reveal(
            f'All{i}', text, x, y, 'MatAll', f,
        )
    return cmds
