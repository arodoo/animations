# File: app/components/objects/butterfly/_wings.py
# Single polygon wing per side; proper butterfly shape.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Tuple

_UP, _DOWN = 0.65, -0.38
_SX_UP, _SY_UP = 0.90, 0.86
_SX_DW, _SY_DW = 1.08, 1.06
_BODY_EDGE = 0.22

# Wing silhouette in local XY plane.
# Attachment at origin (body edge), extends +X.
# Mirrors to -X for right side.
_BASE: Tuple = (
    (0.00,  0.12),   # top body attachment
    (0.40,  0.50),   # forewing leading curve
    (0.85,  0.58),   # forewing apex
    (1.20,  0.22),   # forewing outer tip
    (1.10, -0.06),   # forewing lower
    (0.90, -0.30),   # outer notch
    (0.75, -0.55),   # hindwing outer
    (0.45, -0.62),   # hindwing tip
    (0.16, -0.50),   # hindwing inner curve
    (0.00, -0.22),   # bottom body attachment
)
_SIDES = [('WingL', 1), ('WingR', -1)]


def _verts(sx: int) -> List:
    pts = [(sx * x, y) for x, y in _BASE]
    return list(reversed(pts)) if sx < 0 else pts


def _spawn(
    wn: str, sx: int, torso: str,
) -> List[Dict]:
    return [
        {'cmd': 'spawn_polygon', 'args': {
            'name': wn,
            'verts': _verts(sx),
            'location': (sx * _BODY_EDGE, 0.0, 0.22),
        }},
        {'cmd': 'parent_object', 'args': {
            'child': wn, 'parent': torso,
        }},
    ]


def _kf(
    wn: str, sx: int, f: int, up: bool,
) -> List[Dict]:
    a = sx * (_UP if up else _DOWN)
    mx = _SX_UP if up else _SX_DW
    my = _SY_UP if up else _SY_DW
    return [
        {'cmd': 'rotate_object', 'args': {
            'name': wn, 'frame': f,
            'rotation': (0, a, 0),
        }},
        {'cmd': 'scale_object', 'args': {
            'name': wn, 'frame': f,
            'scale': (mx, my, 1.0),
        }},
    ]


def _flap(
    wn: str, sx: int,
    start: int, end: int, half: int,
) -> List[Dict]:
    cmds: List[Dict] = []
    up, f = False, start
    while f <= end:
        cmds += _kf(wn, sx, f, up)
        up, f = not up, f + half
    return cmds


def build_wings(
    name: str,
    start_f: int,
    end_f: int,
    half_cycle: int,
) -> List[Dict]:
    """Single polygon wing per side; squash+stretch."""
    torso = f'{name}_Torso'
    cmds: List[Dict] = []
    for sfx, sx in _SIDES:
        wn = f'{name}_{sfx}'
        cmds += _spawn(wn, sx, torso)
        cmds += _flap(
            wn, sx, start_f, end_f, half_cycle,
        )
    return cmds
