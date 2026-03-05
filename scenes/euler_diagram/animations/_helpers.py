# File: scenes/euler_diagram/animations/_helpers.py
# Shared bounce-reveal builder for text numbers.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

# Rx(pi/2): text stands upright (local up = world Z)
# Rz(3pi/4): face points toward camera at azimuth pi/4
_TEXT_ROT = (math.pi / 2, 0.0, 3 * math.pi / 4)


def text_reveal(
    name: str,
    text: str,
    x: float,
    y: float,
    mat: str,
    frame: int,
    sz: float = 0.45,
    bounce: float = 1.3,
) -> List[Dict]:
    """Spawn text + bounce scale-in (upright, facing camera)."""
    ov = sz * bounce
    return [
        {'cmd': 'spawn_text', 'args': {
            'name': name,
            'text': text,
            'location': (x, y, 1.0),
            'rotation': _TEXT_ROT,
            'extrude': 0.0,
            'align_x': 'CENTER',
            'align_y': 'CENTER',
        }},
        {'cmd': 'assign_material', 'args': {
            'object': name,
            'material': mat,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': name,
            'scale': (0, 0, 0),
            'frame': 1,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': name,
            'scale': (ov, ov, ov),
            'frame': frame,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': name,
            'scale': (sz, sz, sz),
            'frame': frame + 20,
        }},
    ]
