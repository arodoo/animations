# File: scenes/math_sets/scene.py
# Orchestrator for the Mathematical Sets animation.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands  # triggers all command registrations

from app.components.env_builder import build_environment
from .animations._builder import build_math_sets
from .animations._camera import build_camera
from .animations._timing import Timing


def create_scene(
    total_frames: int = 900,
    camera_radius: float = 30.0,
    timing: Timing = None,
) -> Dict[str, Any]:
    """Build and dispatch the Math Sets animation."""
    batch = []
    batch += build_environment({
        'total_frames': total_frames,
        'world_color': (0.001, 0.001, 0.001),
        'grid': False,
        'lights': [
            {'name': 'KeyLight', 'type': 'POINT'},
        ],
    })
    batch.append({'cmd': 'create_space_world', 'args': {
        'star_density': 400,
        'star_brightness': 2.0,
    }})
    batch.append({'cmd': 'animate_space_world', 'args': {}})
    batch.append({'cmd': 'configure_eevee', 'args': {
        'samples': 16,
        'width': 1280,
        'height': 720,
    }})
    batch += build_math_sets(
        total_frames, timing=timing,
    )
    batch += build_camera(camera_radius, total_frames)
    results = dispatch_batch(batch)
    return {
        'results': results,
        'frames': total_frames,
        'status': 'OK',
    }
