# File: scenes/math_sets/animations/_post_sort.py
# Post-migration: even blocks spin, odd blocks bounce.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ._logic_blocks import odd_target

_SPIN_STEP = 20    # spin keyframe interval
_BOUNCE_STEP = 12  # bounce keyframe interval
_BOUNCE_AMP = 0.6  # bounce amplitude (units)


def build_even_spin(
    number: int,
    start_frame: int,
    end_frame: int
) -> List[Dict]:
    """Slow full Z-rotation for an even block."""
    cmds: List[Dict] = []
    step = _SPIN_STEP
    span = max(end_frame - start_frame, 1)
    for f in range(start_frame, end_frame + 1, step):
        t = (f - start_frame) / span
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': f"Block_{number}",
            'rotation': (0, 0, t * math.tau),
            'frame': f,
        }})
    return cmds


def build_odd_bounce(
    number: int,
    odd_idx: int,
    start_frame: int,
    end_frame: int
) -> List[Dict]:
    """Vertical sine bounce for an odd block."""
    cmds: List[Dict] = []
    tx, ty = odd_target(odd_idx)
    phase = (number / 10.0) * math.tau
    step = _BOUNCE_STEP
    for f in range(start_frame, end_frame + 1, step):
        t = (f - start_frame) / step
        bz = math.sin(t + phase) * _BOUNCE_AMP
        cmds.append({'cmd': 'move_object', 'args': {
            'name': f"Block_{number}",
            'location': (tx, ty, bz),
            'frame': f,
        }})
    return cmds


def build_post_sort(
    num_sequence: int,
    act4: int,
    total_frames: int
) -> List[Dict]:
    """Assemble post-migration block animations."""
    cmds: List[Dict] = []
    start = act4 + 90
    odd_idx = 0
    for i in range(1, num_sequence + 1):
        is_odd = (i % 2 != 0)
        if is_odd:
            cmds += build_odd_bounce(
                i, odd_idx, start, total_frames,
            )
            odd_idx += 1
        else:
            cmds += build_even_spin(
                i, start, total_frames,
            )
    return cmds
