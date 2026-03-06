# Fractal Abyss scene orchestrator.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands

from app.components.env_builder import (
    build_environment,
)
from .animations.builder import build_fractal_abyss
from .animations.staging.camera import build_camera
from .animations.staging.lights import build_lights
from .animations.domain.timing import Timing


def create_scene(
    total_frames: int = 2880,
    timing: Timing = None,
) -> Dict[str, Any]:
    """Build and dispatch the Fractal Abyss."""
    t = timing or Timing()
    batch = []
    batch += build_environment({
        'total_frames': total_frames,
        'world_color': (0.01, 0.01, 0.03),
        'grid': False,
        'lights': [
            {'name': 'Key', 'type': 'POINT'},
            {'name': 'Fill', 'type': 'POINT'},
            {'name': 'Rim', 'type': 'POINT'},
        ],
    })
    batch += build_lights()
    batch.append({
        'cmd': 'configure_eevee',
        'args': {
            'samples': 32,
            'width': 1920,
            'height': 1080,
        },
    })
    batch += build_fractal_abyss(
        total_frames, t,
    )
    batch += build_camera(total_frames, t)
    results = dispatch_batch(batch)
    return {
        'results': results,
        'frames': total_frames,
        'status': 'OK',
    }
