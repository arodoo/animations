# File: scenes/missile_storm/animations/acts/village.py
# Build village structures and trees spread over 2km.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from app.components.objects import (
    build_house,
    build_barn,
    build_tree,
    build_fence,
)
from ..domain.layout import VILLAGE_LAYOUT

_TREE_COUNT = 40
_FENCE_COUNT = 16


def _build_trees() -> List[Dict]:
    """Scatter trees around the village."""
    cmds: List[Dict] = []
    for i in range(_TREE_COUNT):
        angle = (2 * math.pi * i) / _TREE_COUNT
        r = 100 + 400 * ((i * 7) % 11) / 10
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        h = 2.5 + (i % 5) * 0.5
        cmds += build_tree(
            f'Tree{i}', (x, y, 0), h,
        )
    return cmds


def _build_fences() -> List[Dict]:
    """Place fences near village clusters."""
    cmds: List[Dict] = []
    for i in range(_FENCE_COUNT):
        angle = (2 * math.pi * i) / _FENCE_COUNT
        r = 200 + 100 * (i % 3)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        cmds += build_fence(
            f'Fence{i}', (x, y, 0),
            length=8.0,
            rotation_z=angle,
        )
    return cmds


def build_village() -> List[Dict]:
    """All village structures."""
    cmds: List[Dict] = []
    for b in VILLAGE_LAYOUT:
        if b['kind'] == 'barn':
            cmds += build_barn(
                b['name'], b['pos'], b['size'],
            )
        else:
            cmds += build_house(
                b['name'], b['pos'], b['size'],
            )
    cmds += _build_trees()
    cmds += _build_fences()
    return cmds
