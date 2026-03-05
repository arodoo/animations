# File: scenes/euler_diagram/animations/_builder.py
# Orchestrates the 3-act Euler diagram proof.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._materials import build_materials
from ._inner_circle import build_inner_circle
from ._outer_circle import build_outer_circle
from ._timing import Timing


def build_euler_diagram(
    total_frames: int,
    timing: Timing = None,
) -> List[Dict]:
    """
    Act 1: Inner ring scales in, odds 1/3/5/7 pop in.
    Act 2: Camera pulls back (handled by scene).
    Act 3: Outer ring + diverse numbers revealed.
    """
    t = timing or Timing()
    cmds: List[Dict] = build_materials()
    cmds += build_inner_circle(t.ring_inner, t.odds_appear)
    cmds += build_outer_circle(t.ring_outer, t.outer_nums)
    return cmds
