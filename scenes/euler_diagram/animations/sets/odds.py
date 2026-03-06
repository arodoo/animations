# Odd numbers on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal, reveal_duration
from ..domain.spiral import pos, ODDS_START, sz_at
from ..domain.motion import build_idle_bob

_NUMS = list(range(1, 40, 2))   # 20 odd numbers: 1,3,5...39
_STAGGER = 15
_BOUNCE = 1.4
_TOTAL_FRAMES = 2400


def build_odds(
    appear_frame: int,
    base_sz: float = 1.0,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """20 odd numbers, sequential, golden yellow."""
    cmds: List[Dict] = []
    for i, num in enumerate(_NUMS):
        x, y = pos(ODDS_START + i)
        sz = sz_at(ODDS_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Odd{i}', str(num),
            x, y, 'MatOdds', f,
            sz=sz, bounce=_BOUNCE,
            extrude=0.012,
        )
        cmds += build_idle_bob(
            f'Odd{i}', x, y, f,
            total_frames, amplitude=0.03,
        )
    return cmds
