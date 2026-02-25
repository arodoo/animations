# File: app/components/disk_animator.py
# Generic accretion-disk animator: PW rotation keys, emission pulses.
# Extracted from scenes/quasar_bh/animations/_disk_animate.py.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

from .disk_physics import pw_angular_velocity


_PULSE_CYCLES = 4


def _frame_dt(
    total_frames: int,
    rotations: int,
    innermost_radius: float,
) -> float:
    """Scene time units per frame, calibrated to innermost ring."""
    omega_inner = pw_angular_velocity(innermost_radius)
    total_angle = 2.0 * math.pi * rotations
    return total_angle / (omega_inner * total_frames)


def _rotation_keys(
    i: int,
    ring: Dict,
    total_frames: int,
    rotations: int,
    step: int,
    innermost_radius: float,
) -> List[Dict]:
    omega = pw_angular_velocity(ring['radius'])
    dt    = _frame_dt(total_frames, rotations, innermost_radius)
    keys  = []
    for f in range(1, total_frames + 1, step):
        angle = omega * f * dt
        keys.append({'cmd': 'rotate_object', 'args': {
            'name': f"Ring_{i}", 'rotation': (0, 0, angle), 'frame': f,
        }})
    return keys


def build_disk_animation(cfg: Dict[str, Any]) -> List[Dict]:
    """Return rotation + pulse keyframes for all active disk rings.

    Args:
        cfg: dict with keys:
            disk_rings       — list of ring dicts {radius, color}
            total_frames     (int)
            rotations        (int)
            step             (int) — keyframe interval
            pulse_inner      (bool)
            particles        (bool) — unused placeholder for parity
            emit_strength_fn — callable(i) -> float
    """
    disk_rings     = cfg['disk_rings']
    total_frames   = cfg['total_frames']
    rotations      = cfg['rotations']
    step           = cfg['step']
    pulse_inner    = cfg.get('pulse_inner', False)
    emit_fn        = cfg['emit_strength_fn']
    innermost_r    = disk_rings[0]['radius']

    cmds: List[Dict] = []
    for i, ring in enumerate(disk_rings):
        cmds += _rotation_keys(
            i, ring, total_frames, rotations, step, innermost_r,
        )
        if pulse_inner and i == 0:
            for cycle in range(_PULSE_CYCLES):
                f = 1 + cycle * (total_frames // _PULSE_CYCLES)
                cmds.append({'cmd': 'keyframe_material_emission', 'args': {
                    'material': f"RingMat_{i}",
                    'strength': emit_fn(i) * 1.6,
                    'frame':    f,
                }})
    return cmds
