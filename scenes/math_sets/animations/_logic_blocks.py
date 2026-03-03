# File: scenes/math_sets/animations/_logic_blocks.py
# Migrates number blocks into their correct Venn set region.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List, Tuple


def odd_target(idx: int) -> Tuple[float, float]:
    """Position inside Odds circle for the idx-th odd."""
    angle = (idx / 5.0) * math.tau
    return math.cos(angle) * 2.0, math.sin(angle) * 2.0


def even_target(idx: int) -> Tuple[float, float]:
    """Position in N-only ring for the idx-th even."""
    angle = (idx / 5.0) * math.tau
    return math.cos(angle) * 5.5, math.sin(angle) * 5.5


def _migrate_one(
    number: int,
    odd_idx: int,
    even_idx: int,
    start_frame: int
) -> List[Dict]:
    """Fade tags and fly block into its set region."""
    is_odd = (number % 2 != 0)
    name = f"Block_{number}"
    cmds = []
    for tag in [
        f"Label_{number}",
        f"TagN_{number}",
        f"TagOdd_{number}",
    ]:
        cmds.append({'cmd': 'scale_object', 'args': {
            'name': tag,
            'scale': (0, 0, 0),
            'frame': start_frame,
        }})
    if is_odd:
        tx, ty = odd_target(odd_idx)
    else:
        tx, ty = even_target(even_idx)
    cmds.append({'cmd': 'move_object', 'args': {
        'name': name,
        'location': (tx, ty, 0.0),
        'frame': start_frame + 50,
    }})
    return cmds


def build_all_migrations(
    num_sequence: int,
    start_frame: int
) -> List[Dict]:
    """Migrate all blocks into their Venn set regions."""
    cmds: List[Dict] = []
    odd_idx = 0
    even_idx = 0
    for i in range(1, num_sequence + 1):
        is_odd = (i % 2 != 0)
        frame = start_frame + (i - 1) * 8
        cmds += _migrate_one(
            i, odd_idx, even_idx, frame
        )
        if is_odd:
            odd_idx += 1
        else:
            even_idx += 1
    return cmds
