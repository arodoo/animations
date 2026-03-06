# Negative integers — third ring, violet.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal
from ..domain.motion import build_idle_bob
from ..domain.spiral import pos_slot, display_sz, slot_width, INT_START

_NUMS = list(range(-1, -31, -1))   # -1,-2,...-30 (30 numbers)
_STAGGER = 15
_TOTAL_FRAMES = 2400


def build_integers(
    appear_frame: int,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """30 negative integers, violet, sequential."""
    cmds: List[Dict] = []
    slot = INT_START
    for i, num in enumerate(_NUMS):
        x, y, _ = pos_slot(slot)
        sz = display_sz(slot)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Int{i}', str(num), x, y, 'MatInt', f,
            sz=sz, extrude=sz * 0.18, bounce=1.3,
        )
        cmds += build_idle_bob(
            f'Int{i}', x, y, f,
            total_frames, amplitude=sz * 0.18,
        )
        slot += slot_width(num)
    return cmds
