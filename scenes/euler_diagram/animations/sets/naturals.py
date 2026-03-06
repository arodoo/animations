# Even naturals on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal, reveal_duration
from ..domain.spiral import pos, NAT_START, sz_at
from ..domain.motion import build_idle_bob

_NUMS = list(range(2, 302, 2))
_STAGGER = reveal_duration() + 1
_BOUNCE = 1.3
_TOTAL_FRAMES = 4800


def build_naturals(
    appear_frame: int,
    base_sz: float = 0.88,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """150 even naturals, strictly sequential, teal."""
    cmds: List[Dict] = []
    for i, num in enumerate(_NUMS):
        x, y = pos(NAT_START + i)
        sz = sz_at(NAT_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Nat{i}', str(num),
            x, y, 'MatNat', f,
            sz=sz, bounce=_BOUNCE,
            extrude=0.015,
        )
        cmds += build_idle_bob(
            f'Nat{i}', x, y, f,
            total_frames, amplitude=0.02,
        )
    return cmds
