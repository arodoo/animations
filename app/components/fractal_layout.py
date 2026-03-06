# Sierpinski triangle and spiral position generators.
# All Rights Reserved Arodi Emmanuel

import math
from typing import List, Tuple

Pt = Tuple[float, float]

_TRI_H = 0.866


def sierpinski(
    cx: float,
    cy: float,
    size: float,
    depth: int,
) -> List[Pt]:
    """Recursive Sierpinski triangle centers."""
    if depth == 0:
        return [(cx, cy)]
    h = size * _TRI_H / 2
    sub = size / 2
    top = sierpinski(
        cx, cy + h, sub, depth - 1,
    )
    left = sierpinski(
        cx - sub / 2, cy - h / 2,
        sub, depth - 1,
    )
    right = sierpinski(
        cx + sub / 2, cy - h / 2,
        sub, depth - 1,
    )
    return top + left + right


def spiral_pos(
    count: int,
    r0: float = 2.0,
    growth: float = 0.5,
    step: float = 0.4,
) -> List[Pt]:
    """Archimedean spiral positions."""
    pts: List[Pt] = []
    for i in range(count):
        a = i * step
        r = r0 + growth * a
        pts.append(
            (r * math.cos(a), r * math.sin(a))
        )
    return pts
