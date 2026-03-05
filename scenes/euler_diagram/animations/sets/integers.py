# Negative integers on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal, reveal_duration
from ..domain.spiral import pos, INT_START, sz_at
from ..domain.motion import build_idle_bob

_NUMS = list(range(-1, -181, -1))
_STAGGER = reveal_duration()
_BOUNCE = 1.3
_TOTAL_FRAMES = 4800


def build_integers(
    appear_frame: int,
    base_sz: float = 0.80,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """180 negatives, strictly sequential, violet."""
    cmds: List[Dict] = []
    for i, num in enumerate(_NUMS):
        x, y = pos(INT_START + i)
        sz = sz_at(INT_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Int{i}', str(num),
            x, y, 'MatInt', f,
            sz=sz, bounce=_BOUNCE,
            extrude=0.10,
        )
        cmds += build_idle_bob(
            f'Int{i}', x, y, f,
            total_frames, amplitude=0.15,
        )
    return cmds
