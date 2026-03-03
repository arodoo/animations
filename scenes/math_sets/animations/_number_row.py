# File: scenes/math_sets/animations/_number_row.py
# Spawns numbers 1-N as labeled blocks in an elevated row.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Tuple

_SPACING = 2.2
_ROW_Y = 0.0
_ROW_Z = 4.0


def number_position(
    index: int,
    total: int = 10
) -> Tuple[float, float, float]:
    """Center-aligned XYZ position for a number index."""
    sx = -((total - 1) / 2.0) * _SPACING
    return (sx + (index - 1) * _SPACING, _ROW_Y, _ROW_Z)


def build_number_block(
    number: int,
    total: int,
    appear_frame: int
) -> List[Dict]:
    """Spawn a labeled cube for a discrete number."""
    cmds: List[Dict] = []
    is_odd = (number % 2 != 0)
    name = f"Block_{number}"
    loc = number_position(number, total)
    mat = 'OddMat' if is_odd else 'EvenMat'
    cmds.append({'cmd': 'spawn_primitive', 'args': {
        'type': 'cube', 'name': name,
        'location': loc,
        'scale': (0.7, 0.7, 0.7),
        'shade_smooth': True,
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': name, 'material': mat,
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': name, 'scale': (0, 0, 0), 'frame': 1,
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': name,
        'scale': (0.7, 0.7, 0.7),
        'frame': appear_frame,
    }})
    lx, ly, lz = loc
    label = f"Label_{number}"
    cmds.append({'cmd': 'spawn_text', 'args': {
        'name': label, 'text': str(number),
        'location': (lx, ly, lz + 1.0),
        'extrude': 0.04,
        'align_x': 'CENTER',
        'align_y': 'BOTTOM',
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': label, 'material': 'TextMat',
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': label, 'scale': (0, 0, 0), 'frame': 1,
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': label,
        'scale': (1.0, 1.0, 1.0),
        'frame': appear_frame + 5,
    }})
    return cmds


def build_number_row(num_sequence: int = 10) -> List[Dict]:
    """Build the initial row of number blocks."""
    cmds: List[Dict] = []
    for i in range(1, num_sequence + 1):
        appear = 10 + i * 12
        cmds += build_number_block(i, num_sequence, appear)
    return cmds
