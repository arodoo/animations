# Negative integers — third ring, violet.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Tuple

from ..domain.reveal import text_reveal
from ..domain.motion import build_idle_bob
from ..domain.spiral import pos_slot, display_sz, INT_START
from ..domain.layout import slots_advance, _GROWTH_STEP

_NUMS = list(range(-1, -61, -1))   # -1,-2,...-60 (60 numbers)
_STAGGER = 8
_TOTAL_FRAMES = 2400


def build_integers(
    appear_frame: int,
    total_frames: int = _TOTAL_FRAMES,
    start_slot: int = INT_START,
    start_index: int = 0,
) -> Tuple[List[Dict], int, int]:
    """60 negative integers, violet, sequential."""
    cmds: List[Dict] = []
    slot = start_slot
    for i, num in enumerate(_NUMS):
        x, y, _ = pos_slot(slot)
        growth = 1.0 + (start_index + i) * _GROWTH_STEP
        sz = display_sz(slot) * growth
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Int{i}', str(num), x, y, 'MatInt', f,
            sz=sz, extrude=sz * 0.18, bounce=1.3,
        )
        cmds += build_idle_bob(
            f'Int{i}', x, y, f,
            total_frames, amplitude=sz * 0.18,
        )
        slot += slots_advance(slot, num)
    return cmds, slot, start_index + len(_NUMS)
