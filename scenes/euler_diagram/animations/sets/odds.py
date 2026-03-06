# Odd numbers — innermost ring, golden yellow.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Tuple

from ..domain.reveal import text_reveal
from ..domain.motion import build_idle_bob
from ..domain.spiral import pos_slot, display_sz, ODDS_START
from ..domain.layout import slots_advance, _GROWTH_STEP

_NUMS = list(range(1, 61, 2))   # 1,3,5...59 (30 numbers)
_STAGGER = 12
_TOTAL_FRAMES = 2400


def build_odds(
    appear_frame: int,
    total_frames: int = _TOTAL_FRAMES,
    start_slot: int = ODDS_START,
    start_index: int = 0,
) -> Tuple[List[Dict], int, int]:
    """30 odd numbers, golden, strictly sequential."""
    cmds: List[Dict] = []
    slot = start_slot
    for i, num in enumerate(_NUMS):
        x, y, _ = pos_slot(slot)
        growth = 1.0 + (start_index + i) * _GROWTH_STEP
        sz = display_sz(slot) * growth
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Odd{i}', str(num), x, y, 'MatOdds', f,
            sz=sz, extrude=sz * 0.18, bounce=1.4,
        )
        cmds += build_idle_bob(
            f'Odd{i}', x, y, f,
            total_frames, amplitude=sz * 0.20,
        )
        slot += slots_advance(slot, num)
    return cmds, slot, start_index + len(_NUMS)
