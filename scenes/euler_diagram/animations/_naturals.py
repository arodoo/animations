# File: scenes/euler_diagram/animations/_naturals.py
# Even naturals 2..180 on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._helpers import text_reveal
from ._spiral import pos, NAT_START, sz_at

_NUMS = list(range(2, 182, 2))   # 90 evens
_BASE_SZ = 0.40
_STAGGER = 7
_BOUNCE = 1.3


def build_naturals(appear_frame: int) -> List[Dict]:
    """90 even naturals, stagger 7f, teal."""
    cmds: List[Dict] = []
    for i, num in enumerate(_NUMS):
        x, y = pos(NAT_START + i)
        sz = sz_at(NAT_START + i, _BASE_SZ)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Nat{i}', str(num),
            x, y, 'MatNat', f,
            sz=sz, bounce=_BOUNCE,
        )
    return cmds
