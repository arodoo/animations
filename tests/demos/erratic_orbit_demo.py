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


def _solve_kepler(m: float, e: float, iterations: int = 5) -> float:
    """Solve Kepler's Equation E - e*sin(E) = M using Newton's method."""
    ecc_anomaly = m
    for _ in range(iterations):
        ecc_anomaly = ecc_anomaly - (ecc_anomaly - e * math.sin(ecc_anomaly) - m) / (1 - e * math.cos(ecc_anomaly))
    return ecc_anomaly


def crear_orbita_relativista() -> Dict[str, Any]:
    """
    Create a 30-second relativistic orbit animation with space atmosphere.
    Uses Einstein's general relativity precession and Keplerian dynamics.
    """
    batch: List[Dict[str, Any]] = []
    
    # 1. Generate starfield atmosphere (1250 stars for more depth)
    print("Generating relativistic starfield atmosphere...")
    starfield_commands = generate_starfield(
        star_count=1250,
        min_size=0.01,
        max_size=0.06,
        radius=60.0,
        num_clusters=10
    )
    batch.extend(starfield_commands)
    
    # 2. Setup materials
    # Sun: Glowing Orange-Red
    batch.append({'cmd': 'create_material', 'args': {'name': 'SunMat', 'color': (1, 0.25, 0.05, 1)}})
    # Satellite: Scientific Blue-White
    batch.append({'cmd': 'create_material', 'args': {'name': 'SatMat', 'color': (0.4, 0.7, 1, 1)}})
    
    # 3. Spawn Sun (Center)
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'Sun'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'Sun', 'material': 'SunMat'}})
    batch.append({'cmd': 'scale_object', 'args': {'name': 'Sun', 'scale': (2.0, 2.0, 2.0)}})
    
    # 4. Spawn Satellite
    batch.append({'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'Satellite'}})
    batch.append({'cmd': 'assign_material', 'args': {'object': 'Satellite', 'material': 'SatMat'}})
    batch.append({'cmd': 'scale_object', 'args': {'name': 'Satellite', 'scale': (0.4, 0.4, 0.4)}})
    
    # 5. Animate Relativistic Orbit (30 seconds = 900 frames)
    total_frames = 900
    a = 10.0          # Semi-major axis
    e = 0.206         # Eccentricity (Mercury-like)
    precession_rate = 0.08  # Radians per orbit (exaggerated for effect)
    frames_per_orbit = 450
    
    for f in range(1, total_frames + 1, 2):  # Every 2 frames for smoothness
        # Time-based mean anomaly
        t_normalized = (f - 1) / frames_per_orbit
        mean_anomaly = 2 * math.pi * t_normalized
        
        # 1. Solve for Eccentric Anomaly
        ecc_anomaly = _solve_kepler(mean_anomaly, e)
        
        # 2. Calculate True Anomaly
        true_anomaly = 2 * math.atan2(
            math.sqrt(1 + e) * math.sin(ecc_anomaly / 2),
            math.sqrt(1 - e) * math.cos(ecc_anomaly / 2)
        )
        
        # 3. Distance from center (Keplerian)
        r = a * (1 - e**2) / (1 + e * math.cos(true_anomaly))
        
        # 4. Add Relativistic Precession (Ellipse rotation)
        phi = true_anomaly + (precession_rate * t_normalized)
        
        # 5. 3D Position with subtle inclination
        x = r * math.cos(phi)
        y = r * math.sin(phi)
        z = 0.8 * math.sin(true_anomaly * 0.5)
        
        batch.append({
            'cmd': 'move_object',
            'args': {'name': 'Satellite', 'location': (x, y, z), 'frame': f}
        })
        
        # Subtle scale variation (simulating relativistic length contraction/visual effect)
        # Faster at perihelion (r is smaller), look slightly "smeared" or compressed
        vel_factor = 1.0 - (0.1 * (a / r))
        batch.append({
            'cmd': 'scale_object',
            'args': {'name': 'Satellite', 'scale': (0.4, 0.4 * vel_factor, 0.4), 'frame': f}
        })

    # 6. Set frame range for 30 seconds at 30fps
    batch.append({'cmd': 'set_frame_range', 'args': {'start': 1, 'end': 900}})
    
    results = dispatch_batch(batch)
    
    return {
        'results': results,
        'frames': total_frames,
        'stars': 1250,
        'duration_seconds': 30
    }
