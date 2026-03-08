# File: scenes/missile_storm/animations/domain/layout.py
# Village layout positions (~2km spread).
# All Rights Reserved Arodi Emmanuel

import math
from typing import List, Tuple

_R = 800
_CLUSTER_COUNT = 8
_HOUSES_PER_CLUSTER = 5


def _cluster_center(i: int) -> Tuple[float, float]:
    """Place clusters in a ring around origin."""
    angle = (2 * math.pi * i) / _CLUSTER_COUNT
    r = _R * (0.3 + 0.7 * ((i % 3) / 2))
    return r * math.cos(angle), r * math.sin(angle)


def _house_offset(j: int) -> Tuple[float, float]:
    """Scatter houses within a cluster."""
    angle = (2 * math.pi * j) / _HOUSES_PER_CLUSTER
    r = 30 + 20 * (j % 3)
    return r * math.cos(angle), r * math.sin(angle)


def generate_village() -> List[dict]:
    """Return list of building dicts."""
    buildings: List[dict] = []
    idx = 0
    for i in range(_CLUSTER_COUNT):
        cx, cy = _cluster_center(i)
        for j in range(_HOUSES_PER_CLUSTER):
            ox, oy = _house_offset(j)
            kind = 'barn' if j == 0 else 'house'
            buildings.append({
                'name': f'{kind.title()}{idx}',
                'kind': kind,
                'pos': (cx + ox, cy + oy, 0),
                'size': 3.0 if kind == 'barn' else 1.5,
            })
            idx += 1
    return buildings


VILLAGE_LAYOUT = generate_village()
