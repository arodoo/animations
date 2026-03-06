# Negative integers on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal, reveal_duration
from ..domain.spiral import pos, INT_START, sz_at
from ..domain.motion import build_idle_bob

_NUMS = list(range(-1, -31, -1))   # 30 negatives: -1,-2,...-30
_STAGGER = 15
_BOUNCE = 1.3
_TOTAL_FRAMES = 2400


def build_integers(
    appear_frame: int,
    base_sz: float = 1.0,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """30 negative integers, sequential, violet."""
    cmds: List[Dict] = []
    for i, num in enumerate(_NUMS):
        x, y = pos(INT_START + i)
        sz = sz_at(INT_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Int{i}', str(num),
            x, y, 'MatInt', f,
            sz=sz, bounce=_BOUNCE,
            extrude=0.012,
        )
        cmds += build_idle_bob(
            f'Int{i}', x, y, f,
            total_frames, amplitude=0.02,
        )
    return cmds
