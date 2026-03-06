# Rational fractions — fourth ring, green.
# All Rights Reserved Arodi Emmanuel

from fractions import Fraction as _F
from typing import Dict, List, Tuple

from ..domain.reveal import text_reveal
from ..domain.motion import build_idle_bob
from ..domain.spiral import pos_slot, display_sz, RAT_START
from ..domain.layout import slots_advance, _GROWTH_STEP

_STAGGER = 8
_TOTAL_FRAMES = 2400


def _gen() -> List[str]:
    """60 reduced fractions, simple denominators first."""
    seen, out = set(), []
    for d in range(2, 30):
        for n in range(1, d * 2 + 1):
            if n == d:
                continue
            frac = _F(n, d)
            if frac.denominator == 1:
                continue
            if frac not in seen:
                seen.add(frac)
                out.append(f'{frac.numerator}/{frac.denominator}')
                if len(out) == 60:
                    return out
    return out


_NUMS = _gen()


def build_rationals(
    appear_frame: int,
    total_frames: int = _TOTAL_FRAMES,
    start_slot: int = RAT_START,
    start_index: int = 0,
) -> Tuple[List[Dict], int, int]:
    """60 fractions, green, sequential."""
    cmds: List[Dict] = []
    slot = start_slot
    for i, text in enumerate(_NUMS):
        x, y, _ = pos_slot(slot)
        growth = 1.0 + (start_index + i) * _GROWTH_STEP
        sz = display_sz(slot) * growth
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Rat{i}', text, x, y, 'MatRat', f,
            sz=sz, extrude=sz * 0.18,
        )
        cmds += build_idle_bob(
            f'Rat{i}', x, y, f,
            total_frames, amplitude=sz * 0.18,
        )
        slot += slots_advance(slot, text)
    return cmds, slot, start_index + len(_NUMS)
