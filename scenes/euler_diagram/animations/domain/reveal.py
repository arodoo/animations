# Bounce-reveal: text pops up from Z, settles flat on XY plane.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

# Rotation: flat on XY, readable top-down (pi/2 on X axis)
_TEXT_ROT = (1.5708, 0.0, 0.0)
_REVEAL_FRAMES = 12


def text_reveal(
    name: str,
    text: str,
    x: float,
    y: float,
    mat: str,
    frame: int,
    sz: float,
    extrude: float = 0.04,
    bounce: float = 1.35,
) -> List[Dict]:
    """Spawn text flat on XY with bounce scale-in.

    scale goes 0 -> sz*bounce -> sz over _REVEAL_FRAMES.
    Starts invisible (scale=0 at frame 1).
    """
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
            'name': name, 'scale': (0, 0, 0), 'frame': 1,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': name, 'scale': (ov, ov, ov), 'frame': frame,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': name, 'scale': (sz, sz, sz),
            'frame': frame + _REVEAL_FRAMES,
        }},
    ]


def reveal_duration() -> int:
    """Frames the reveal animation takes."""
    return _REVEAL_FRAMES
