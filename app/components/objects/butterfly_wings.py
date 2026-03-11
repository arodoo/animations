# File: app/components/objects/butterfly_wings.py
# 4 wings fore+hind; BEZIER peak/trough flap.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_UP = 0.52      # wings-up radians (~30 deg)
_DOWN = -0.28   # wings-down radians (~16 deg)
# (sfx, sx, y_off, scale); x_off = scale[0]
_WINGS = [
    ('WingFL',  1,  0.30, (1.2, 1.0, 0.05)),
    ('WingFR', -1,  0.30, (1.2, 1.0, 0.05)),
    ('WingHL',  1, -0.40, (0.85, 0.72, 0.05)),
    ('WingHR', -1, -0.40, (0.85, 0.72, 0.05)),
]
_PHASES = [0, 0, 2, 2]  # hindwings lag 2 frames


def _spawn(
    wn: str, sx: int, oy: float,
    sc: tuple, torso: str,
) -> List[Dict]:
    """Spawn one wing plane, parent to torso."""
    xo = sx * sc[0]  # inner edge at body center
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


def _flap(
    wn: str, sx: int, start: int,
    end: int, half: int, ph: int,
) -> List[Dict]:
    """Keyframe at flap peaks and troughs."""
    cmds: List[Dict] = []
    up, f = True, start + ph
    while f <= end:
        a = sx * (_UP if up else _DOWN)
        cmds.append({
            'cmd': 'rotate_object',
            'args': {
                'name': wn, 'frame': f,
                'rotation': (0, a, 0),
            },
        })
        up, f = not up, f + half
    return cmds


def build_butterfly_wings(
    name: str = 'Butterfly',
    start_f: int = 1,
    end_f: int = 480,
    half_cycle: int = 6,
) -> List[Dict]:
    """4 wings fore+hind; BEZIER ease."""
    torso = f'{name}_Torso'
    cmds: List[Dict] = []
    for (sfx, sx, oy, sc), ph in zip(
        _WINGS, _PHASES,
    ):
        wn = f'{name}_{sfx}'
        cmds += _spawn(wn, sx, oy, sc, torso)
        cmds += _flap(
            wn, sx, start_f, end_f,
            half_cycle, ph,
        )
    return cmds
