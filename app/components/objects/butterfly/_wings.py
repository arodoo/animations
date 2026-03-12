# File: app/components/objects/butterfly/_wings.py
# 4-wing flap: squash+stretch+BEZIER anticipation.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_UP, _DOWN = 0.65, -0.38        # exaggerated angles
_SX_UP, _SY_UP = 0.90, 0.86    # squash at peak
_SX_DW, _SY_DW = 1.08, 1.06    # stretch at trough
_WINGS = [
    ('WingFL',  1,  0.30, (1.2,  1.0,  0.05)),
    ('WingFR', -1,  0.30, (1.2,  1.0,  0.05)),
    ('WingHL',  1, -0.40, (0.85, 0.72, 0.05)),
    ('WingHR', -1, -0.40, (0.85, 0.72, 0.05)),
]
_PHASES = [0, 0, 2, 2]  # hindwings lag 2f


def _spawn(wn, sx, oy, sc, torso):
    xo = sx * sc[0]
    return [
        {'cmd': 'spawn_primitive', 'args': {
            'name': wn, 'type': 'plane',
            'location': (xo, oy, 0),
        }},
        {'cmd': 'scale_object', 'args': {
            'name': wn, 'scale': sc,
        }},
        {'cmd': 'parent_object', 'args': {
            'child': wn, 'parent': torso,
        }},
    ]


def _kf(wn, sx, sc, f, up):
    a = sx * (_UP if up else _DOWN)
    mx = _SX_UP if up else _SX_DW
    my = _SY_UP if up else _SY_DW
    s = (sc[0] * mx, sc[1] * my, sc[2])
    return [
        {'cmd': 'rotate_object', 'args': {
            'name': wn, 'frame': f,
            'rotation': (0, a, 0),
        }},
        {'cmd': 'scale_object', 'args': {
            'name': wn, 'frame': f,
            'scale': s,
        }},
    ]


def _flap(wn, sx, start, end, half, ph, sc):
    cmds: List[Dict] = []
    # DOWN first -> anticipation before 1st upstroke
    up, f = False, start + ph
    while f <= end:
        cmds += _kf(wn, sx, sc, f, up)
        up, f = not up, f + half
    return cmds


def build_wings(
    name: str,
    start_f: int,
    end_f: int,
    half_cycle: int,
) -> List[Dict]:
    """4 wings fore+hind; squash+stretch BEZIER."""
    torso = f'{name}_Torso'
    cmds: List[Dict] = []
    for (sfx, sx, oy, sc), ph in zip(
        _WINGS, _PHASES,
    ):
        wn = f'{name}_{sfx}'
        cmds += _spawn(wn, sx, oy, sc, torso)
        cmds += _flap(
            wn, sx, start_f, end_f,
            half_cycle, ph, sc,
        )
    return cmds
