# File: tests/demos/erratic_orbit_demo.py
# Erratic orbit demo with procedural space atmosphere. 30-second perpetual
# chaotic orbit using Perlin-like noise for unpredictable but smooth motion.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List
from app.kernel.dispatcher import dispatch_batch
from app.scene.atmospheres.space_atmosphere import generate_starfield

# Import commands to trigger registration
import app.commands  # noqa: F401


def _perlin_noise_1d(x: float, octaves: int = 3) -> float:
    """Simple 1D Perlin-like noise using sine waves."""
    value = 0.0
    amplitude = 1.0
    frequency = 1.0
    
    for _ in range(octaves):
        value += amplitude * math.sin(frequency * x)
        amplitude *= 0.5
        frequency *= 2.0
    
    return value


def crear_orbita_erratica() -> Dict[str, Any]:
    """
    Create a 30-second erratic orbit animation with space atmosphere.
    900 frames at 30fps, chaotic but perpetual orbit.
    """
    batch: List[Dict[str, Any]] = []
    
    # 1. Generate starfield atmosphere (1150 stars)
    print("Generating starfield atmosphere...")
    starfield_commands = generate_starfield(
        star_count=1150,
        min_size=0.01,
        max_size=0.05,
        radius=50.0,
        num_clusters=8
    )
    batch.extend(starfield_commands)
    
    # 2. Setup materials
    batch.append({'cmd': 'create_material', 'args': {'name': 'SunMat', 'color': (1, 0.3, 0, 1)}})
    batch.append({'cmd': 'create_material', 'args': {'name': 'SatMat', 'color': (0.2, 0.5, 1, 1)}})
    
    # 3. Spawn Sun (Center)
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'Sun'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'Sun', 'material': 'SunMat'}})
    batch.append({'cmd': 'scale_object', 'args': {'name': 'Sun', 'scale': (1.5, 1.5, 1.5)}})
    
    # 4. Spawn Satellite
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'Satellite'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'Satellite', 'material': 'SatMat'}})
    batch.append({'cmd': 'scale_object', 'args': {'name': 'Satellite', 'scale': (0.5, 0.5, 0.5)}})
    
    # 5. Animate Erratic Orbit (30 seconds = 900 frames)
    total_frames = 900
    base_radius = 9.0
    
    for f in range(1, total_frames + 1, 3):  # Keyframe every 3 frames
        t = (f - 1) / (total_frames - 1)
        
        # Base circular orbit
        angle = t * 4 * math.pi  # 2 full rotations
        
        # Add erratic motion using Perlin-like noise
        noise_x = _perlin_noise_1d(t * 10.0, octaves=3)
        noise_y = _perlin_noise_1d(t * 10.0 + 100, octaves=3)
        noise_z = _perlin_noise_1d(t * 10.0 + 200, octaves=2)
        
        # Combine base orbit with chaos
        radius = base_radius + noise_x * 2.0
        x = radius * math.cos(angle) + noise_x * 1.5
        y = radius * math.sin(angle) + noise_y * 1.5
        z = noise_z * 2.0
        
        batch.append({
            'cmd': 'move_object',
            'args': {'name': 'Satellite', 'location': (x, y, z), 'frame': f}
        })
    
    # 6. Set frame range for 30 seconds at 30fps
    batch.append({'cmd': 'set_frame_range', 'args': {'start': 1, 'end': 900}})
    
    results = dispatch_batch(batch)
    
    return {
        'results': results,
        'frames': total_frames,
        'stars': 1150,
        'duration_seconds': 30
    }
