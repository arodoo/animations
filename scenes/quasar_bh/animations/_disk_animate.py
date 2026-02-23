# File moved: scenes/quasar_bh/_disk_animate.py -> animations/_disk_animate.py
# Accretion disk animation: relativistic rotation, emission pulses.
# Angular velocities follow the Paczyński–Wiita pseudo-Newtonian model so
# inner rings spin dramatically faster than outer ones, matching the
# super-Keplerian runaway near the ISCO.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ._physics import pw_angular_velocity, DISK_RINGS
from ._disk_build import ring_emit_strength

_PULSE_CYCLES = 4


def _frame_dt(total_frames: int, rotations: int) -> float:
    """Scene time units per frame.

    Calibrated so the innermost ring (DISK_RINGS[0]) completes exactly
    `rotations` full orbits over `total_frames`.
    """
    omega_inner = pw_angular_velocity(DISK_RINGS[0]['radius'])
    total_angle = 2.0 * math.pi * rotations
    return total_angle / (omega_inner * total_frames)


def _rotation_keys(
    i: int, ring: Dict, total_frames: int,
    rotations: int, step: int,
) -> List[Dict]:
    omega = pw_angular_velocity(ring['radius'])
    dt = _frame_dt(total_frames, rotations)
    keys = []
    for f in range(1, total_frames + 1, step):
        angle = omega * f * dt
        keys.append({'cmd': 'rotate_object', 'args': {
            'name':     f"Ring_{i}",
            'rotation': (0, 0, angle),
            'frame':    f,
        }})
    return keys


def build_disk_animation(
    disk_rings: List[Dict], total_frames: int,
    rotations: int, step: int,
    pulse_inner: bool, particles: bool,
) -> List[Dict]:
    cmds: List[Dict] = []
    for i, ring in enumerate(disk_rings):
        cmds += _rotation_keys(i, ring, total_frames, rotations, step)
        if pulse_inner and i == 0:
            for cycle in range(_PULSE_CYCLES):
                f = 1 + cycle * (total_frames // _PULSE_CYCLES)
                cmds.append({'cmd': 'keyframe_material_emission', 'args': {
                    'material': f"RingMat_{i}",
                    'strength': ring_emit_strength(i) * 1.6,
                    'frame':    f,
                }})
    return cmds
