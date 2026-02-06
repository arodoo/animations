# File: core/logic.py
# Core logic module with scene creation functions. Uses the dispatcher to
# execute instruction batches. Primary entry point for animation logic.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List

from app.infra.bridge import data, reset
from app.kernel.dispatcher import dispatch_batch

# Import commands to trigger registration
import app.commands  # noqa: F401


def crear_escena_prueba() -> Dict[str, Any]:
    """
    Create a test scene demonstrating the dispatch system.
    Creates a cube at origin, moves it, and adds keyframes.
    """
    reset()

    instructions: List[Dict[str, Any]] = [
        {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Cube'}},
        {'cmd': 'set_keyframe', 'args': {'name': 'Cube', 'frame': 1}},
        {'cmd': 'move_object', 'args': {
            'name': 'Cube',
            'location': (5.0, 3.0, 1.0),
            'frame': 10
        }},
    ]

    results = dispatch_batch(instructions)

    # Gather scene info
    obj = data.objects.get('Cube')
    keyframes = {}
    if obj:
        keyframes = obj.animation_data.get_keyframes('location')

    return {
        'objects': data.objects.keys(),
        'position': obj.location.to_tuple() if obj else None,
        'keyframes': keyframes,
        'results': results,
    }
