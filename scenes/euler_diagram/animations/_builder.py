# File: scenes/euler_diagram/animations/_builder.py
# Orchestrates all sub-builders for the Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._timing import Timing
from ._materials import build_materials
from ._background import build_background
from ._odds import build_odds
from ._naturals import build_naturals
from ._integers import build_integers
from ._rationals import build_rationals
from ._irrationals import build_irrationals
from ._labels import build_labels


def build_euler_diagram(
    total_frames: int,
    timing: Timing = None,
) -> List[Dict]:
    """Build all commands for the 5-act spiral."""
    t = timing or Timing()
    cmds: List[Dict] = build_materials()
    cmds += build_background()
    cmds += build_odds(t.odds_start)
    cmds += build_naturals(t.nat_start)
    cmds += build_integers(t.int_start)
    cmds += build_rationals(t.rat_start)
    cmds += build_irrationals(t.real_start)
    cmds += build_labels(t)
    return cmds
