# File: tests/demos/orbit_demo.py
# Demo script creating a spiral orbit: a sphere orbits another while radius
# decreases over time. Demonstrates batch dispatch and math orchestration.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List
from app.kernel.dispatcher import dispatch_batch

# Import commands to trigger registration
import app.commands  # noqa: F401

def crear_orbita_espiral() -> Dict[str, Any]:
    """Crea una escena con una esfera orbitando en espiral."""
    batch: List[Dict[str, Any]] = []
    
    # 1. Setup materials
    batch.append({'cmd': 'create_material', 'args': {'name': 'SunMat', 'color': (1, 0, 0, 1)}})
    batch.append({'cmd': 'create_material', 'args': {'name': 'SatMat', 'color': (0, 0, 1, 1)}})
    
    # 2. Spawn Sun (Center)
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'Sun'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'Sun', 'material': 'SunMat'}})
    
    # 3. Spawn Satellite
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'Satellite'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'Satellite', 'material': 'SatMat'}})
    batch.append({'cmd': 'scale_object', 'args': {'name': 'Satellite', 'scale': (0.4, 0.4, 0.4)}})
    
    # 4. Animate Spiral (5 turns, 250 frames)
    # Radius 10 -> 2, Turns: 5 * 2pi
    total_frames = 250
    start_radius = 10.0
    end_radius = 2.0
    turns = 5
    
    for f in range(1, total_frames + 1, 5): # Keyframe every 5 frames
        t = (f - 1) / (total_frames - 1)
        radius = start_radius + (end_radius - start_radius) * t
        angle = t * turns * 2 * math.pi
        
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        batch.append({
            'cmd': 'move_object', 
            'args': {'name': 'Satellite', 'location': (x, y, 0), 'frame': f}
        })

    results = dispatch_batch(batch)
    
    return {
        'results': results,
        'frames': total_frames,
        'final_radius': end_radius
    }
