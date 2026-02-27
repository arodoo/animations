# File: scenes/math_sets/scene.py
# Orchestrator for the Mathematical Sets animation (Numbers vs Odds).
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.dispatcher import dispatch_batch
import app.commands  # triggers all command registrations

from app.components.env_builder import build_environment
import math

from .animations._builder import build_math_sets


def create_scene(
    total_frames: int = 900,
    camera_radius: float = 30.0,
    cam_step: int = 1
) -> Dict[str, Any]:
    """Build and dispatch the Math Sets animation."""
    batch = []
    
    # Very dark, minimalist environment to make the math pop
    batch += build_environment({
        'total_frames': total_frames,
        'world_color':  (0.005, 0.005, 0.005), 
        'grid':         False,
        'lights': [
            {'name': 'SunLight', 'type': 'POINT', 'energy': 1000.0}
        ],
    })
    
    # We don't need stars, we want pure abstraction
    batch += build_math_sets(total_frames, num_sequence=10)
    
    # Camera: Completely fixed and static to serve as a pure mathematical canvas
    batch += [
        {'cmd': 'create_camera', 'args': {'name': 'SceneCamera'}},
        {'cmd': 'set_focal_length', 'args': {'name': 'SceneCamera', 'focal_length': 40.0}},
        {'cmd': 'move_object', 'args': {
            'name': 'SceneCamera', 'location': (0.0, -camera_radius, camera_radius * 0.4), 'frame': 1
        }},
        {'cmd': 'rotate_object', 'args': {
            'name': 'SceneCamera', 'rotation': (math.radians(70.0), 0, 0), 'frame': 1
        }},
        {'cmd': 'set_camera_target', 'args': {
            'name': 'SceneCamera', 'target': (0, 0, 0)
        }},
        {'cmd': 'set_depth_of_field', 'args': {
            'name': 'SceneCamera', 'enabled': True, 
            'focus_distance': camera_radius, 'fstop': 2.8
        }}
    ]

    results = dispatch_batch(batch)
    return {
        'results': results,
        'frames':  total_frames,
        'status': 'OK'
    }
