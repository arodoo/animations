# File: scenes/euler_diagram/animations/_inner_circle.py
# Inner ring with odd numbers 1, 3, 5, 7.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ._helpers import text_reveal

_RING_R = 3.0
_NUM_R = 2.0


def build_inner_circle(
    ring_frame: int,
    odds_frame: int,
) -> List[Dict]:
    """Torus ring scales in, then numbers pop staggered."""
    cmds: List[Dict] = [
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'torus',
            'name': 'OddsRing',
            'location': (0, 0, 0),
            'major_radius': _RING_R,
            'minor_radius': 0.08,
            'major_segments': 64,
        }},
        {'cmd': 'assign_material', 'args': {
            'object': 'OddsRing',
            'material': 'MatInnerRing',
        }},
        {'cmd': 'scale_object', 'args': {
            'name': 'OddsRing',
            'scale': (0, 0, 0),
            'frame': 1,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': 'OddsRing',
            'scale': (1, 1, 1),
            'frame': ring_frame,
        }},
    ]
    for i, n in enumerate([1, 3, 5, 7]):
        a = (i / 4) * math.tau
        x = _NUM_R * math.cos(a)
        y = _NUM_R * math.sin(a)
        f = odds_frame + i * 18
        cmds += text_reveal(
            f'Odd{n}', str(n), x, y, 'MatOdds', f,
        )
    return cmds
