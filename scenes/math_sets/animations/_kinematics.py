# File: scenes/math_sets/animations/_kinematics.py
# Hover and spin animations for blocks and Venn rings.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ._number_row import number_position

_AMP = 0.2    # hover amplitude (units)
_PERIOD = 60  # frames per full hover cycle
_STEP = 15    # keyframe interval


def build_block_hover(
    number: int,
    total: int,
    start_frame: int,
    end_frame: int
) -> List[Dict]:
    """Sine-wave float for a block before migration."""
    cmds: List[Dict] = []
    bx, by, bz = number_position(number, total)
    phase = (number / total) * math.tau
    for f in range(start_frame, end_frame, _STEP):
        t = f / _PERIOD
        hz = bz + math.sin(t * math.tau + phase) * _AMP
        cmds.append({'cmd': 'move_object', 'args': {
            'name': f"Block_{number}",
            'location': (bx, by, hz),
            'frame': f,
        }})
    return cmds


def build_ring_spin(
    ring_reveal: int,
    end_frame: int
) -> List[Dict]:
    """Counter-rotating spin for both Venn rings."""
    cmds: List[Dict] = []
    span = max(end_frame - ring_reveal, 1)
    for f in range(ring_reveal, end_frame + 1, 20):
        t = (f - ring_reveal) / span
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': 'Ring_N',
            'rotation': (0, 0, t * math.radians(60)),
            'frame': f,
        }})
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': 'Ring_Odds',
            'rotation': (0, 0, -t * math.radians(90)),
            'frame': f,
        }})
    return cmds


def build_kinematics(
    num_sequence: int,
    total_frames: int,
    migration_start: int,
    ring_reveal: int
) -> List[Dict]:
    """Assemble all movement animations."""
    cmds: List[Dict] = []
    for i in range(1, num_sequence + 1):
        start = 10 + i * 12
        cmds += build_block_hover(
            i, num_sequence, start, migration_start,
        )
    cmds += build_ring_spin(ring_reveal, total_frames)
    return cmds
