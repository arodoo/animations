# Iconic irrationals — outermost ring, pink.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Tuple

from ..domain.reveal import text_reveal
from ..domain.motion import build_idle_bob
from ..domain.spiral import pos_slot, display_sz, REAL_START
from ..domain.layout import slots_advance, _GROWTH_STEP

_NUMS = [
    'π', 'e', '√2', '√3', '√5',
    'φ', 'τ', 'γ', 'ln2', 'ln3',
    '√7', 'cbrt2', 'e²', 'π²', '1/π',
    'e^π', 'π^e', '2^√2', '√φ', 'ζ(3)',
    'G', 'Ω', 'K', 'μ', 'δs',
    '√6', '√10', '√11', '√13', '√17',
    'ln5', 'ln7', 'ln10', 'log2', 'e^e',
    '1/e', '1/φ', 'π/4', 'π/3', 'π/6',
    'τ/4', '√π', '∛3', '∛5', '∛7',
    'Γ(½)', 'Li₂', 'ψ(1)', 'β(2)', 'η(2)',
]
_STAGGER = 8
_TOTAL_FRAMES = 2400


def build_irrationals(
    appear_frame: int,
    total_frames: int = _TOTAL_FRAMES,
    start_slot: int = REAL_START,
    start_index: int = 0,
) -> Tuple[List[Dict], int, int]:
    """50 iconic irrationals, pink, sequential."""
    cmds: List[Dict] = []
    slot = start_slot
    for i, text in enumerate(_NUMS):
        x, y, _ = pos_slot(slot)
        growth = 1.0 + (start_index + i) * _GROWTH_STEP
        sz = display_sz(slot) * growth
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Real{i}', text, x, y, 'MatReal', f,
            sz=sz, extrude=sz * 0.18,
        )
        cmds += build_idle_bob(
            f'Real{i}', x, y, f,
            total_frames, amplitude=sz * 0.18,
        )
        slot += slots_advance(slot, text)
    return cmds, slot, start_index + len(_NUMS)
