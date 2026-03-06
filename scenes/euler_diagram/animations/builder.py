# Orchestrates all sub-builders for the Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from .domain.timing import Timing
from .domain.spiral import configure as _cfg_spiral
from .staging.materials import build_materials, build_label_materials
from .staging.background import build_background
from .staging.labels import build_labels
from .sets.odds import build_odds
from .sets.naturals import build_naturals
from .sets.integers import build_integers
from .sets.rationals import build_rationals
from .sets.irrationals import build_irrationals


def build_euler_diagram(
    total_frames: int,
    timing: Timing = None,
    spiral_scale: float = 1.0,
    emit_overrides: dict = None,
    label_size: float = 1.80,
) -> List[Dict]:
    """Build all commands for the 5-act spiral."""
    _cfg_spiral(spiral_scale)
    t = timing or Timing()
    cmds: List[Dict] = build_materials(emit_overrides)
    cmds += build_label_materials()
    cmds += build_background()

    odds_cmds, slot = build_odds(
        t.odds_start, total_frames=total_frames, start_slot=0,
    )
    cmds += odds_cmds
    nat_cmds, slot = build_naturals(
        t.nat_start, total_frames=total_frames, start_slot=slot,
    )
    cmds += nat_cmds
    int_cmds, slot = build_integers(
        t.int_start, total_frames=total_frames, start_slot=slot,
    )
    cmds += int_cmds
    rat_cmds, slot = build_rationals(
        t.rat_start, total_frames=total_frames, start_slot=slot,
    )
    cmds += rat_cmds
    real_cmds, _ = build_irrationals(
        t.real_start, total_frames=total_frames, start_slot=slot,
    )
    cmds += real_cmds
    cmds += build_labels(t, label_sz=label_size)
    return cmds
