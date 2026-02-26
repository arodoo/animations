# File: app/components/bodies/dyson_sphere.py
# Parametric builder for a structural, non-intersecting Dyson Sphere cage.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List


def build_dyson_sphere(cfg: Dict[str, Any]) -> List[Dict]:
    """Return commands to create a parametric, non-intersecting Dyson Sphere.

    Args:
        cfg: dict with configuration:
            base_radius (float): The inner clearance radius of the sphere.
            ring_thickness (float): The minor_radius of the toruses.
            materials (List[str]): List of materials to alternate.
            meridians (int): Number of longitudinal vertical rings.
            parallels (int): Number of latitudinal horizontal rings.
            clearance (float): Delta radius added per ring to prevent Z-fighting.
            total_frames (int): Animation parameter.
            step (int): Animation frame step.
    """
    cmds: List[Dict] = []
    
    base_r = float(cfg.get('base_radius', 1.0))
    thickness = float(cfg.get('ring_thickness', 0.008))
    mats = cfg.get('materials', ['MetalMat'])
    meridians = int(cfg.get('meridians', 4))
    parallels = int(cfg.get('parallels', 3))
    clearance = float(cfg.get('clearance', 0.01))
    
    total_frames = int(cfg.get('total_frames', 1200))
    step = int(cfg.get('step', 1))
    
    current_radius = base_r
    
    # 1. Vertical Meridians (Orbiting around Z)
    for i in range(meridians):
        ring_name = f"DysonMeridian_{i}"
        
        # Variance: each ring has a slightly different structural thickness
        var_thickness = thickness * (0.8 + (i * 0.3))
        
        cmds.append({'cmd': 'spawn_primitive', 'args': {
            'type': 'torus', 'name': ring_name,
            'major_segments': 128, 'minor_segments': 8,
            'major_radius': current_radius,
            'minor_radius': var_thickness,
            'shade_smooth': True
        }})
        cmds.append({'cmd': 'assign_material', 'args': {
            'object': ring_name, 'material': mats[i % len(mats)]
        }})
        
        # Initial angular distribution on Z
        start_angle = math.radians(i * (180.0 / max(1, meridians)))
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': ring_name, 'rotation': (math.pi/2, 0, start_angle), 'frame': 1
        }})
        
        # Animate Meridians - Independent geared spin
        speed_mult = 1.0 + (i * 0.6)
        for f in range(1, total_frames + 1, step):
            t = (f - 1) / max(1, total_frames - 1)
            spin = t * math.pi * 2.0 * speed_mult  # revolutions
            cmds.append({'cmd': 'rotate_object', 'args': {
                'name': ring_name, 'rotation': (math.pi/2, 0, start_angle + spin), 'frame': f
            }})
            
        current_radius += clearance

    # 2. Horizontal Parallels
    # We distribute parallels from equator (z=0) outwards to the poles.
    # To keep them on the sphere's surface, r = sqrt(R^2 - z^2)
    # The first parallel is the equator.
    if parallels > 0:
        # Generate Z heights symmetrically around 0.
        # e.g., for 3 parallels: 0, +0.6, -0.6
        z_heights = [0.0]
        if parallels > 1:
            step_z = (base_r * 0.7) / (parallels // 2)
            for j in range(1, (parallels // 2) + 1):
                z_heights.append(step_z * j)
                z_heights.append(-step_z * j)
                
        # Ensure we don't exceed requested parallels (if even number)
        z_heights = z_heights[:parallels]

        for i, z_val in enumerate(z_heights):
            ring_name = f"DysonParallel_{i}"
            
            # The radius of the slice at height Z on a sphere of radius R
            # adding clearance to ensure outer wrapping
            slice_r = math.sqrt(max(0.1, current_radius**2 - z_val**2))
            
            var_thickness = thickness * (0.6 + (i * 0.4))
            
            cmds.append({'cmd': 'spawn_primitive', 'args': {
                'type': 'torus', 'name': ring_name,
                'major_segments': 128, 'minor_segments': 8,
                'major_radius': slice_r,
                'minor_radius': var_thickness,
                'shade_smooth': True
            }})
            cmds.append({'cmd': 'assign_material', 'args': {
                'object': ring_name, 'material': mats[i % len(mats)]
            }})
            cmds.append({'cmd': 'move_object', 'args': {
                'name': ring_name, 'location': (0, 0, z_val), 'frame': 1
            }})
            
            # Animate Parallels - Independent counter-rotation
            # Alternating speeds/directions per parallel
            direction = 1 if i % 2 == 0 else -1
            speed_mult = 0.5 + (i * 0.8)
            for f in range(1, total_frames + 1, step):
                t = (f - 1) / max(1, total_frames - 1)
                spin = direction * t * math.pi * 2.0 * speed_mult
                cmds.append({'cmd': 'rotate_object', 'args': {
                    'name': ring_name, 'rotation': (0, 0, spin), 'frame': f
                }})
                
            current_radius += clearance

    return cmds
