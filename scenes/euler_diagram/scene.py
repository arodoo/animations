# File: scenes/euler_diagram/scene.py
# Orchestrator for the Expanding Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands  # triggers registrations

from app.components.env_builder import build_environment
from .animations._builder import build_euler_diagram
from .animations._camera import build_camera
from .animations._timing import Timing
from .animations._background import build_scalable_grid


def create_scene(
    total_frames: int = 700,
    timing: Timing = None,
) -> Dict[str, Any]:
    """Build and dispatch the Euler diagram animation."""
    t = timing or Timing()
    batch = build_environment({
        'total_frames': total_frames,
        'world_color': (0.001, 0.001, 0.002),
        'grid': False,
        'lights': [
            {'name': 'KeyLight', 'type': 'POINT'},
        ],
    })
    batch += build_scalable_grid(
        t.zoom_start, t.zoom_end,
    )
    batch += build_euler_diagram(total_frames, timing=t)
    batch += build_camera(
        total_frames, t.zoom_start, t.zoom_end,
    )
    batch.append({'cmd': 'configure_eevee', 'args': {
        'samples': 16,
        'width': 1280,
        'height': 720,
    }})
    return {
        'results': dispatch_batch(batch),
        'frames': total_frames,
        'status': 'OK',
    }
