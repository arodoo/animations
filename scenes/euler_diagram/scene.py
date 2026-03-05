# File: scenes/euler_diagram/scene.py
# Orchestrator for the Expansive Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands  # triggers all command registrations

from app.components.env_builder import build_environment
from .animations._builder import build_euler_diagram
from .animations._camera import build_camera
from .animations._timing import Timing


def create_scene(
    total_frames: int = 2880,
    timing: Timing = None,
    spiral_scale: float = 1.0,
    sets: dict = None,
    label_size: float = 1.60,
) -> Dict[str, Any]:
    """Build and dispatch the Euler Diagram animation."""
    batch = []
    batch += build_environment({
        'total_frames': total_frames,
        'world_color': (0.005, 0.006, 0.015),
        'grid': False,
        'lights': [
            {'name': 'KeyLight', 'type': 'POINT'},
        ],
    })
    batch.append({'cmd': 'configure_eevee', 'args': {
        'samples': 16,
        'width': 1280,
        'height': 720,
    }})
    batch += build_euler_diagram(
        total_frames, timing=timing,
        spiral_scale=spiral_scale,
        sets=sets, label_size=label_size,
    )
    batch += build_camera(total_frames, scale=spiral_scale)
    results = dispatch_batch(batch)
    return {
        'results': results,
        'frames': total_frames,
        'status': 'OK',
    }
