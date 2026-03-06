# Reusable text spawn with glow reveal animation.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_REVEAL = 12


def spawn_glow_text(
    name: str,
    text: str,
    x: float,
    y: float,
    z: float,
    mat: str,
    frame: int,
    sz: float = 0.5,
    ext: float = 0.04,
) -> List[Dict]:
    """Spawn text, assign material, scale reveal."""
    return [
        {'cmd': 'spawn_text', 'args': {
            'name': name,
            'text': text,
            'location': (x, y, z),
            'extrude': ext,
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
            'frame': frame + _REVEAL,
        }},
    ]
