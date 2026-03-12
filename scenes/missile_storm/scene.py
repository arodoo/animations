# File: scenes/missile_storm/scene.py
# Butterfly meadow scene orchestrator.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
from app.components.env_builder import build_environment
import app.commands

from .animations.domain.timing import Timing
from .animations.builder import build_missile_storm


def create_scene(
    timing: Timing = Timing(),
    cam_step: int = 4,
    wing_half_cycle: int = 6,
    flight_speed: float = 0.5,
    flight_altitude: float = 8.0,
) -> Dict[str, Any]:
    """Build and dispatch butterfly meadow scene."""
    total = timing.flight_end
    batch = [{'cmd': 'configure_eevee', 'args': {
        'width': 1920, 'height': 1080,
        'samples': 32,
    }}]
    batch += build_environment({
        'total_frames': total,
        'world_color': (0.45, 0.65, 0.85),
        'grid': False,
        'lights': [],
    })
    batch += build_missile_storm(
        timing, cam_step, wing_half_cycle,
        flight_speed, flight_altitude,
    )
    results = dispatch_batch(batch)
    return {
        'results': results,
        'frames': total,
        'status': 'OK',
    }
