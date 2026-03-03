# File: scenes/math_sets/animations/_venn_diagram.py
# Concentric Venn rings: N (superset) and Odds (subset).
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_R_N = 8.0
_R_ODDS = 3.2


def _ring_cmds(
    name: str,
    radius: float,
    mat: str,
    label: str,
    reveal: int
) -> List[Dict]:
    cmds = []
    cmds.append({'cmd': 'spawn_primitive', 'args': {
        'type': 'torus', 'name': name,
        'location': (0.0, 0.0, 0.0),
        'major_radius': radius,
        'minor_radius': 0.07,
        'major_segments': 64,
        'minor_segments': 8,
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
        'scale': (1, 1, 1), 'frame': reveal,
    }})
    lname = f"LabelRing_{name}"
    cmds.append({'cmd': 'spawn_text', 'args': {
        'name': lname, 'text': label,
        'location': (0.0, radius + 1.0, 0.1),
        'extrude': 0.03,
        'align_x': 'CENTER',
        'align_y': 'BOTTOM',
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': lname, 'material': mat,
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': lname, 'scale': (0, 0, 0), 'frame': 1,
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': lname,
        'scale': (1.2, 1.2, 1.2),
        'frame': reveal + 12,
    }})
    return cmds


def generate_set_rings(reveal_frame: int) -> List[Dict]:
    """Generate N (outer) and Odds (inner) rings."""
    cmds = _ring_cmds(
        'Ring_N', _R_N,
        'TextMat', 'N', reveal_frame,
    )
    cmds += _ring_cmds(
        'Ring_Odds', _R_ODDS,
        'OddMat', 'Odds', reveal_frame + 15,
    )
    return cmds
