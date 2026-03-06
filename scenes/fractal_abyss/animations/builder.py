# Orchestrates all acts for Fractal Abyss.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from .domain.timing import Timing
from .staging.materials import build_materials
from .staging.labels import build_labels
from .acts.act1_naturals import build_naturals
from .acts.act2_rationals import build_rationals
from .acts.act3_irrationals import (
    build_irrationals,
)
from .acts.act4_fractal import build_fractal
from .acts.act5_abyss import build_abyss


def build_fractal_abyss(
    total: int,
    timing: Timing,
) -> List[Dict]:
    """Build all commands for 5-act animation."""
    cmds = build_materials()
    cmds += build_naturals(timing.act1, total)
    cmds += build_rationals(timing.act2, total)
    cmds += build_irrationals(
        timing.act3, total,
    )
    cmds += build_fractal(timing.act4, total)
    cmds += build_abyss(timing.act5, total)
    cmds += build_labels(timing)
    return cmds
