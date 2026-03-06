# Iconic irrationals — outermost ring, pink.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Tuple

from ..domain.reveal import text_reveal
from ..domain.motion import build_idle_bob
from ..domain.spiral import pos_slot, display_sz, REAL_START
from ..domain.layout import slots_advance

_NUMS = [
    'π', 'e', '√2', '√3', '√5',
    'φ', 'τ', 'γ', 'ln2', 'ln3',
    '√7', 'cbrt2', 'e²', 'π²', '1/π',
    'e^π', 'π^e', '2^√2', '√φ', 'ζ(3)',
]
_STAGGER = 15
_TOTAL_FRAMES = 2400


def build_irrationals(
    appear_frame: int,
    total_frames: int = _TOTAL_FRAMES,
    start_slot: int = REAL_START,
) -> Tuple[List[Dict], int]:
    """20 iconic irrationals, pink, sequential."""
    cmds: List[Dict] = []
    slot = start_slot
    for i, text in enumerate(_NUMS):
        x, y, _ = pos_slot(slot)
        sz = display_sz(slot)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Real{i}', text, x, y, 'MatReal', f,
            sz=sz, extrude=sz * 0.18, bounce=1.3,
        )
        cmds += build_idle_bob(
            f'Real{i}', x, y, f,
            total_frames, amplitude=sz * 0.18,
        )
        slot += slots_advance(slot, text)
    return cmds, slot
