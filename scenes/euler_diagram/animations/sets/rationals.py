# Rational fractions on the nautilus spiral.
# All Rights Reserved Arodi Emmanuel

from fractions import Fraction as _F
from typing import Dict, List

from ..domain.reveal import text_reveal, reveal_duration
from ..domain.spiral import pos, RAT_START, sz_at
from ..domain.motion import build_idle_bob

_STAGGER = 15
_BOUNCE = 1.3
_TOTAL_FRAMES = 2400
_COUNT = 30


def _gen() -> List[str]:
    """30 unique reduced fractions, simple denominators first."""
    seen, out = set(), []
    for d in range(2, 20):
        for n in range(1, d * 2 + 1):
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
                if len(out) == _COUNT:
                    return out
    return out


_NUMS = _gen()


def build_rationals(
    appear_frame: int,
    base_sz: float = 1.0,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """30 fractions, sequential, green."""
    cmds: List[Dict] = []
    for i, text in enumerate(_NUMS):
        x, y = pos(RAT_START + i)
        sz = sz_at(RAT_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Rat{i}', text,
            x, y, 'MatRat', f,
            sz=sz, bounce=_BOUNCE,
            extrude=0.012,
        )
        cmds += build_idle_bob(
            f'Rat{i}', x, y, f,
            total_frames, amplitude=0.02,
        )
    return cmds
