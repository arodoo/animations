# File: scenes/missile_storm/animations/staging/camera_follow.py
# Camera follows butterfly along straight +Y path.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing

_CAM_BACK = 12      # units behind butterfly
_CAM_UP = 5         # units above butterfly
_LOOK_AHEAD = 5     # units ahead of butterfly
_BOB = 0.35         # must match flight_path._BOB


def _butterfly_pos(
    f: int,
    half_cycle: int,
    speed: float,
    altitude: float,
    start: int,
):
    """Butterfly world pos at frame f (straight +Y)."""
    t = f - start
    bob = _BOB * math.sin(math.pi * f / half_cycle)
    return 0.0, t * speed, altitude + bob


def build_follow_phase(
    timing: Timing,
    step: int = 4,
    half_cycle: int = 6,
    speed: float = 0.5,
    altitude: float = 8.0,
) -> List[Dict]:
    """Camera tracks butterfly from behind and above."""
    cmds: List[Dict] = []
    for f in range(
        timing.flight_start, timing.flight_end, step,
    ):
        bx, by, bz = _butterfly_pos(
            f, half_cycle, speed,
            altitude, timing.flight_start,
        )
        cmds.append({'cmd': 'move_object', 'args': {
            'name': 'StormCam',
            'location': (bx, by - _CAM_BACK, bz + _CAM_UP),
            'frame': f,
        }})
        cmds.append({'cmd': 'move_object', 'args': {
            'name': '_target_StormCam',
            'location': (bx, by + _LOOK_AHEAD, bz),
            'frame': f,
        }})
    return cmds
