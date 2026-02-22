# File moved: scenes/quasar_bh/_disk_animate.py -> animations/_disk_animate.py
# Accretion disk animation: Keplerian rotation, emission pulses, particles.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

from ._physics import keplerian_speed
from ._disk_build import ring_emit_strength

_PULSE_CYCLES = 4  # emission hotspot oscillations per animation

def _rotation_keys(
    i: int, ring: Dict, total_frames: int,
    rotations: int, step: int,
) -> List[Dict]:
    speed = keplerian_speed(ring['radius'])
    keys = []
    for f in range(1, total_frames + 1, step):
        angle = (
            (f / total_frames)
            * 2 * math.pi * rotations * speed
        )
        keys.append({'cmd': 'rotate_object', 'args': {
            'name':     f"Ring_{i}",
            'rotation': (0, 0, angle),
            'frame':    f,
        }})
    return keys

def build_disk_animation(disk_rings: List[Dict], total_frames: int,
                         rotations: int, step: int, pulse_inner: bool,
                         particles: bool) -> List[Dict]:
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
