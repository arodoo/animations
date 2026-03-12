# File: scenes/missile_storm/animations/builder.py
# Assembles butterfly meadow scene.
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
    build_village,
)


def build_missile_storm(
    timing: Timing,
    cam_step: int = 4,
    wing_half_cycle: int = 6,
    flight_speed: float = 0.5,
    flight_altitude: float = 8.0,
) -> List[Dict]:
    """Assemble butterfly meadow animation."""
    cmds: List[Dict] = []
    cmds += build_storm_materials()
    cmds += build_storm_lights()
    cmds += build_flight(
        timing, wing_half_cycle,
        flight_altitude, flight_speed,
    )
    cmds += build_village()
    cmds += build_storm_camera(
        timing, cam_step,
        wing_half_cycle, flight_speed, flight_altitude,
    )
    return cmds
