# File: scenes/missile_storm/animations/acts/flight_path.py
# Butterfly: straight +Y flight with body bob arc.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing

_OBJ = 'Butterfly_Torso'
_BOB = 0.35      # body bob amplitude (m)


def _mv(f, loc):
    return {'cmd': 'move_object', 'args': {
        'name': _OBJ, 'location': loc, 'frame': f,
    }}


def _rot(f, rot):
    return {'cmd': 'rotate_object', 'args': {
        'name': _OBJ, 'rotation': rot, 'frame': f,
    }}


def build_flight_path(
    timing: Timing,
    step: int = 2,
    altitude: float = 8.0,
    half_cycle: int = 6,
    speed: float = 0.5,
) -> List[Dict]:
    """Butterfly flies straight along +Y with body bob."""
    cmds: List[Dict] = []
    for f in range(
        timing.flight_start, timing.flight_end, step,
    ):
        t = f - timing.flight_start
        bob = _BOB * math.sin(math.pi * f / half_cycle)
        cmds.append(_mv(f, (0.0, t * speed, altitude + bob)))
        cmds.append(_rot(f, (0, 0, 0)))
    return cmds
