# Bounce-reveal builder for 3D text numbers.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

# Flat on XY plane, glyphs pointing +Y (readable top-down)
_TEXT_ROT = (1.5708, 0.0, 0.0)
_REVEAL_FRAMES = 18


def text_reveal(
    name: str,
    text: str,
    x: float,
    y: float,
    mat: str,
    frame: int,
    sz: float = 0.45,
    bounce: float = 1.3,
    extrude: float = 0.015,
) -> List[Dict]:
    """Spawn text with bounce scale-in and 3D depth."""
    ov = sz * bounce
    return [
        {'cmd': 'spawn_text', 'args': {
            'name': name,
            'text': text,
            'location': (x, y, 0.0),
            'rotation': _TEXT_ROT,
            'extrude': extrude,
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
            'frame': frame + _REVEAL_FRAMES,
        }},
    ]


def reveal_duration() -> int:
    """Total frames one reveal takes to complete."""
    return _REVEAL_FRAMES
