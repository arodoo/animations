# Odd numbers on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal, reveal_duration
from ..domain.spiral import pos, ODDS_START, sz_at
from ..domain.motion import build_idle_bob

_NUMS = list(range(1, 120, 2))
_STAGGER = reveal_duration() + 2
_BOUNCE = 1.5
_TOTAL_FRAMES = 4800


def build_odds(
    appear_frame: int,
    base_sz: float = 1.0,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """60 golden odds, strictly sequential."""
    cmds: List[Dict] = []
    for i, num in enumerate(_NUMS):
        x, y = pos(ODDS_START + i)
        sz = sz_at(ODDS_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Odd{i}', str(num),
            x, y, 'MatOdds', f,
            sz=sz, bounce=_BOUNCE,
            extrude=0.015,
        )
        cmds += build_idle_bob(
            f'Odd{i}', x, y, f,
            total_frames, amplitude=0.04,
        )
    return cmds
