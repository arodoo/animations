# Odd numbers — innermost ring, golden yellow.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal
from ..domain.motion import build_idle_bob
from ..domain.spiral import pos_slot, display_sz, ODDS_START
from ..domain.layout import slots_advance

_NUMS = list(range(1, 40, 2))   # 1,3,5...39 (20 numbers)
_STAGGER = 15   # frames between each appearance
_TOTAL_FRAMES = 2400


def build_odds(
    appear_frame: int,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """20 odd numbers, golden, strictly sequential."""
    cmds: List[Dict] = []
    slot = ODDS_START
    for i, num in enumerate(_NUMS):
        x, y, _ = pos_slot(slot)
        sz = display_sz(slot)
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
    return cmds
