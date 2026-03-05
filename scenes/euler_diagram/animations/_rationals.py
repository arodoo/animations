# File: scenes/euler_diagram/animations/_rationals.py
# 150 rational fractions on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from fractions import Fraction as _F
from typing import Dict, List

from ._helpers import text_reveal
from ._spiral import pos, RAT_START, sz_at

_BASE_SZ = 0.30
_STAGGER = 4
_BOUNCE = 1.3


def _gen() -> List[str]:
    """150 unique reduced fractions."""
    seen, out = set(), []
    for d in range(2, 60):
        for n in range(1, d * 3 + 1):
            if n == d:
                continue
            frac = _F(n, d)
            if frac.denominator == 1:
                continue
            if frac not in seen:
                seen.add(frac)
                out.append(
                    f'{frac.numerator}'
                    f'/{frac.denominator}'
                )
                if len(out) == 150:
                    return out
    return out


_NUMS = _gen()


def build_rationals(appear_frame: int) -> List[Dict]:
    """150 fractions, stagger 4f, orange."""
    cmds: List[Dict] = []
    for i, text in enumerate(_NUMS):
        x, y = pos(RAT_START + i)
        sz = sz_at(RAT_START + i, _BASE_SZ)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Rat{i}', text,
            x, y, 'MatRat', f,
            sz=sz, bounce=_BOUNCE,
        )
    return cmds
