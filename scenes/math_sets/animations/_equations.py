# File: scenes/math_sets/animations/_equations.py
# Acts 1 & 2: membership check tags per number.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._number_row import number_position


def _spawn_tag(
    name: str,
    text: str,
    loc: tuple,
    mat: str,
    frame: int,
    scale: float = 0.55
) -> List[Dict]:
    cmds = []
    cmds.append({'cmd': 'spawn_text', 'args': {
        'name': name, 'text': text,
        'location': loc,
        'extrude': 0.03,
        'align_x': 'CENTER',
        'align_y': 'BOTTOM',
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': name, 'material': mat,
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': name, 'scale': (0, 0, 0), 'frame': 1,
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': name,
        'scale': (scale, scale, scale),
        'frame': frame,
    }})
    return cmds


def build_membership_acts(
    num_sequence: int,
    act1_start: int,
    act2_start: int
) -> List[Dict]:
    """
    Act 1: 'x in N' for every number.
    Act 2: 'x in Odds' check — true/false per parity.
    """
    cmds: List[Dict] = []
    for i in range(1, num_sequence + 1):
        bx, by, bz = number_position(i, num_sequence)
        is_odd = (i % 2 != 0)
        delay = i * 10
        cmds += _spawn_tag(
            f"TagN_{i}", f"{i} in N",
            (bx, by, bz + 1.8), 'TextMat',
            act1_start + delay,
        )
        txt2 = (
            f"{i} in Odds" if is_odd
            else f"{i} not Odds"
        )
        mat2 = 'TrueMat' if is_odd else 'FalseMat'
        cmds += _spawn_tag(
            f"TagOdd_{i}", txt2,
            (bx, by, bz + 2.6), mat2,
            act2_start + delay,
        )
    return cmds
