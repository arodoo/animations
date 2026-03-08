# File: scenes/missile_storm/animations/builder.py
# Main orchestrator: assembles all acts into a batch.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from .domain.timing import Timing
from .staging import (
    build_storm_camera,
    build_storm_lights,
    build_storm_materials,
)
from .acts import (
    build_flight,
    build_first_strike,
    build_village,
    build_barrage,
)


def build_missile_storm(
    timing: Timing,
    cam_step: int = 4,
) -> List[Dict]:
    """Assemble the full missile storm animation."""
    cmds: List[Dict] = []
    cmds += build_storm_materials()
    cmds += build_storm_lights()
    cmds += build_flight(timing)
    cmds += build_village()
    cmds += build_first_strike(timing)
    cmds += build_barrage(timing)
    cmds += build_storm_camera(timing, cam_step)
    return cmds
