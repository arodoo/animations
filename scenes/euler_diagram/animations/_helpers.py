# File: scenes/euler_diagram/animations/_helpers.py
# Shared command builders for text reveals.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def text_reveal(
    name: str,
    text: str,
    x: float,
    y: float,
    mat: str,
    frame: int,
    sz: float = 0.8,
) -> List[Dict]:
    """Scale-reveal commands for a 3D text number."""
    return [
        {'cmd': 'spawn_text', 'args': {
            'name': name,
            'text': text,
            'location': (x, y, 0.1),
            'extrude': 0.06,
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
            'scale': (sz, sz, sz),
            'frame': frame,
        }},
    ]
