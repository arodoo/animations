# Rational fractions — fourth ring, green.
# All Rights Reserved Arodi Emmanuel

from fractions import Fraction as _F
from typing import Dict, List

from ..domain.reveal import text_reveal
from ..domain.motion import build_idle_bob
from ..domain.spiral import pos_slot, sz_at_slot, slot_width, RAT_START

_STAGGER = 15
_TOTAL_FRAMES = 2400


def _gen() -> List[str]:
    """30 reduced fractions, simple denominators first."""
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
                    f'{frac.numerator}/{frac.denominator}'
                )
                if len(out) == 30:
                    return out
    return out


_NUMS = _gen()


def build_rationals(
    appear_frame: int,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """30 fractions, green, sequential."""
    cmds: List[Dict] = []
    slot = RAT_START
    for i, text in enumerate(_NUMS):
        x, y, _ = pos_slot(slot)
        sz = sz_at_slot(slot)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Rat{i}', text, x, y, 'MatRat', f,
            sz=sz, extrude=sz * 0.18, bounce=1.3,
        )
        cmds += build_idle_bob(
            f'Rat{i}', x, y, f,
            total_frames, amplitude=sz * 0.18,
        )
        slot += slot_width(text)
    return cmds
