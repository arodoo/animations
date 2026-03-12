# File: scenes/missile_storm/animations/acts/butterfly_flight.py
# Butterfly flies over meadow in one direction.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.objects import build_butterfly, build_meadow
from ..domain.timing import Timing
from .flight_path import build_flight_path


def build_flight(
    timing: Timing,
    half_cycle: int = 6,
    altitude: float = 8.0,
    speed: float = 0.5,
) -> List[Dict]:
    """Meadow + butterfly character + straight flight."""
    cmds: List[Dict] = []
    cmds += build_meadow()
    cmds += build_butterfly(
        end_f=timing.flight_end,
        half_cycle=half_cycle,
    )
    cmds += build_flight_path(
        timing,
        altitude=altitude,
        half_cycle=half_cycle,
        speed=speed,
    )
    return cmds
