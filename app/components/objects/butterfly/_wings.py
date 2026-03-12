# File: app/components/objects/butterfly/_wings.py
# Triangle wings: cone apex toward body, no overlap.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

_UP, _DOWN = 0.65, -0.38        # exaggerated angles
_SX_UP, _SY_UP = 0.90, 0.86    # squash at peak
_SX_DW, _SY_DW = 1.08, 1.06    # stretch at trough
_BODY_EDGE = 0.22               # torso radius in X/Z
# (sfx, sx, y_off, radius, y_scale, rot_z)
_WINGS = [
    ('WingFL',  1,  0.30, 1.00, 0.70, math.pi),
    ('WingFR', -1,  0.30, 1.00, 0.70, 0.0),
    ('WingHL',  1, -0.40, 0.65, 0.65, math.pi),
    ('WingHR', -1, -0.40, 0.65, 0.65, 0.0),
]
_PHASES = [0, 0, 2, 2]  # hindwings lag 2f


def _spawn(wn, sx, yo, r, ys, rz, torso):
    xo = sx * (_BODY_EDGE + r)
    return [
        {'cmd': 'spawn_primitive', 'args': {
            'name': wn, 'type': 'cone',
            'vertices': 3, 'radius1': r,
            'radius2': 0, 'depth': 0.04,
            'location': (xo, yo, 0.22),
        }},
        {'cmd': 'scale_object', 'args': {
            'name': wn, 'scale': (1.0, ys, 1.0),
        }},
        {'cmd': 'parent_object', 'args': {
            'child': wn, 'parent': torso,
        }},
    ]

def _kf(wn, sx, ys, rz, f, up):
    a = sx * (_UP if up else _DOWN)
    mx, my = (_SX_UP, _SY_UP) if up else (_SX_DW, _SY_DW)
    return [
        {'cmd': 'rotate_object', 'args': {
            'name': wn, 'frame': f,
            'rotation': (0, a, rz),
        }},
        {'cmd': 'scale_object', 'args': {
            'name': wn, 'frame': f,
            'scale': (mx, ys * my, 1.0),
        }},
    ]

def _flap(wn, sx, ys, rz, start, end, half, ph):
    cmds: List[Dict] = []
    up, f = False, start + ph  # DOWN = anticipation
    while f <= end:
        cmds += _kf(wn, sx, ys, rz, f, up)
        up, f = not up, f + half
    return cmds

def build_wings(
    name: str,
    start_f: int,
    end_f: int,
    half_cycle: int,
) -> List[Dict]:
    """Triangle wings; apex-toward-body; squash+stretch."""
    torso = f'{name}_Torso'
    cmds: List[Dict] = []
    for (sfx, sx, yo, r, ys, rz), ph in zip(
        _WINGS, _PHASES,
    ):
        wn = f'{name}_{sfx}'
        cmds += _spawn(wn, sx, yo, r, ys, rz, torso)
        cmds += _flap(
            wn, sx, ys, rz, start_f, end_f,
            half_cycle, ph,
        )
    return cmds
