# File: scenes/missile_storm/animations/acts/butterfly_flight.py
# Butterfly flies over meadow and village for 2 minutes.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.objects import build_butterfly, build_meadow
from ..domain.timing import Timing
from .flight_path import build_flight_path


def build_flight(
    timing: Timing,
    half_cycle: int = 6,
) -> List[Dict]:
    """Meadow + butterfly character + flight path."""
    cmds: List[Dict] = []
    cmds += build_meadow()
    cmds += build_butterfly(
        end_f=timing.flight_end,
        half_cycle=half_cycle,
    )
    cmds += build_flight_path(
        timing, half_cycle=half_cycle,
    )
    return cmds
