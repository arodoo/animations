# File: scenes/missile_storm/animations/acts/flight_path.py
# Butterfly flight: banking + pitch + body bob arcs.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing

_OBJ = 'Butterfly_Torso'
_BOB = 0.35      # body bob amplitude (m)
_ROLL_K = 6.0    # banking sensitivity
_PITCH_K = 0.18  # pitch sensitivity
_MAX_ROLL = 0.45  # max bank angle (rad)


def _mv(f, loc):
    return {'cmd': 'move_object', 'args': {
        'name': _OBJ, 'location': loc, 'frame': f,
    }}


def _rot(f, rot):
    return {'cmd': 'rotate_object', 'args': {
        'name': _OBJ, 'rotation': rot, 'frame': f,
    }}


def _waypoint(p, radius, alt):
    angle = p * 6 * math.pi
    r = radius * (
        0.3 + 0.7 * abs(math.sin(p * 3 * math.pi))
    )
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    z = alt + 4 * math.sin(p * 12 * math.pi)
    return x, y, z, angle


def _pose(yaw, yaw_d, dz):
    roll = -yaw_d * _ROLL_K
    roll = max(-_MAX_ROLL, min(_MAX_ROLL, roll))
    pitch = max(-0.3, min(0.3, dz * _PITCH_K))
    return roll, pitch, yaw


def build_flight_path(
    timing: Timing,
    step: int = 2,
    radius: float = 600.0,
    altitude: float = 8.0,
    half_cycle: int = 6,
) -> List[Dict]:
    """Butterfly: banking, pitch, body bob arcs."""
    cmds: List[Dict] = []
    total = timing.flight_end - timing.flight_start
    prev_yaw, prev_z = 0.0, altitude
    for f in range(
        timing.flight_start, timing.flight_end, step,
    ):
        p = (f - timing.flight_start) / max(total, 1)
        x, y, z, angle = _waypoint(p, radius, altitude)
        bob = _BOB * math.sin(math.pi * f / half_cycle)
        dx, dy = -math.sin(angle), math.cos(angle)
        yaw = math.atan2(dy, dx)
        roll, pitch, yaw = _pose(
            yaw, yaw - prev_yaw, z - prev_z,
        )
        prev_yaw, prev_z = yaw, z
        cmds.append(_mv(f, (x, y, z + bob)))
        cmds.append(_rot(f, (roll, pitch, yaw)))
    return cmds
