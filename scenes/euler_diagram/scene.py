# File: scenes/euler_diagram/scene.py
# Orchestrator for the Expansive Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands

from app.components.env_builder import build_environment
from .animations.builder import build_euler_diagram
from .animations.staging.camera import build_camera
from .animations.domain.timing import Timing


def create_scene(
    total_frames: int = 2400,
    timing: Timing = None,
    spiral_scale: float = 1.0,
    emit_overrides: dict = None,
    label_size: float = 1.0,
) -> Dict[str, Any]:
    """Build and dispatch the Euler Diagram animation."""
    batch = []
    batch += build_environment({
        'total_frames': total_frames,
        'world_color': (0.008, 0.009, 0.02),
        'grid': False,
        'lights': [
            {'name': 'KeyLight',  'type': 'POINT'},
            {'name': 'FillLight', 'type': 'POINT'},
        ],
    })
    batch.append({'cmd': 'set_light_energy', 'args': {
        'name': 'KeyLight', 'energy': 2000.0,
    }})
    batch.append({'cmd': 'move_object', 'args': {
        'name': 'KeyLight', 'location': (0, 0, 60),
    }})
    batch.append({'cmd': 'set_light_energy', 'args': {
        'name': 'FillLight', 'energy': 700.0,
    }})
    batch.append({'cmd': 'move_object', 'args': {
        'name': 'FillLight', 'location': (20, -20, 45),
    }})
    batch.append({'cmd': 'configure_eevee', 'args': {
        'samples': 32, 'width': 1920, 'height': 1080,
    }})
    batch += build_euler_diagram(
        total_frames,
        timing=timing,
        spiral_scale=spiral_scale,
        emit_overrides=emit_overrides,
        label_size=label_size,
    )
    batch += build_camera(total_frames, scale=spiral_scale)
    results = dispatch_batch(batch)
    return {'results': results, 'frames': total_frames, 'status': 'OK'}
