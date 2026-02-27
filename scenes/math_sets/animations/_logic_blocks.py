# File: scenes/math_sets/animations/_logic_blocks.py
# Constructs the physical manifestation of Numbers and their properties.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List
from ._equations import generate_math_label, generate_formula_proof


def build_number_pedestal(
    number: int,
    loc_x: float,
    loc_y: float,
    loc_z: float,
    total_frames: int
) -> List[Dict]:
    """Build a geometric pedestal representing a discrete number."""
    cmds: List[Dict] = []
    
    is_odd = (number % 2 != 0)
    name = f"Pedestal_{number}"
    
    # 1. Base Geometry
    cmds.append({'cmd': 'spawn_primitive', 'args': {
        'type': 'cube',
        'name': name,
        'location': (loc_x, loc_y, loc_z),
        'scale': (0.8, 0.8, 0.8),
        'shade_smooth': True
    }})
    
    # Apply Subdivision for a sleek look
    cmds.append({'cmd': 'add_modifier', 'args': {
        'object': name,
        'type': 'SUBSURF',
        'properties': {'levels': 2, 'render_levels': 3}
    }})
    
    # Material Assignment
    mat_name = 'OddMat' if is_odd else 'EvenMat'
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': name, 'material': mat_name
    }})
    
    # 2. Timing the appearance
    # Evens and Odds appear in sequence (e.g. 1, 2, 3...)
    appear_frame = 20 + (number * 10)
    
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': name, 'scale': (0, 0, 0), 'frame': 1
    }})
    # Easing into existence
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': name, 'scale': (0.8, 0.8, 0.8), 'frame': appear_frame
    }})
    
    # 3. Add Typography
    text_z = loc_z + 1.2
    cmds += generate_math_label(number, loc_x, loc_y, text_z, appear_frame + 5)
    
    # Add proof formula higher up
    formula_z = loc_z + 2.5
    # The odds prove themselves quickly. Evens delay their proof for Act 2.
    proof_frame = appear_frame + 15 if is_odd else 200 + (number * 5)
    cmds += generate_formula_proof(number, is_odd, loc_x, loc_y, formula_z, proof_frame)
    
    # 4. Act 3: The Reality Grid Fusion
    fusion_start = 600
    
    # 3.5 Kinetic Hover (Acts 1 & 2)
    for f in range(appear_frame, fusion_start + 1, 15):
        t = f / 30.0
        # Z floating offset
        hover_z = loc_z + math.sin(t * 2.0 + number) * 0.2
        # Y rotation (spinning slowly)
        spin_y = t * 0.8 + (number * 0.2)
        cmds.append({'cmd': 'move_object', 'args': {
            'name': name, 'location': (loc_x, loc_y, hover_z), 'frame': f
        }})
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': name, 'rotation': (0, spin_y, 0), 'frame': f
        }})

    if total_frames > fusion_start:
        # Move them to a circular matrix layout to represent "Reality structure"
        radius = 5.0
        angle = (number / 10.0) * math.pi * 2.0
        new_x = math.cos(angle) * radius
        new_y = math.sin(angle) * radius
        
        # Disappear the text to focus on pure geometry
        text_name = f"Text_ID_{number}"
        formula_name = f"Formula_{number}"
        cmds.append({'cmd': 'scale_object', 'args': {'name': text_name, 'scale': (0,0,0), 'frame': fusion_start}})
        cmds.append({'cmd': 'scale_object', 'args': {'name': formula_name, 'scale': (0,0,0), 'frame': fusion_start}})
        
        # Move the pedestal into its orbital launch position
        cmds.append({'cmd': 'move_object', 'args': {
            'name': name, 'location': (new_x, new_y, loc_z), 'frame': fusion_start + 60
        }})
        
        # Continuously orbit the reality grid until the animation ends
        orbit_speed = 0.8
        for f in range(fusion_start + 60, total_frames + 1, 15):
            t = (f - (fusion_start + 60)) / 30.0
            orbital_angle = angle + (t * orbit_speed)
            
            ox = math.cos(orbital_angle) * radius
            oy = math.sin(orbital_angle) * radius
            
            spin_y = t * 3.0
            cmds.append({'cmd': 'move_object', 'args': {
                'name': name, 'location': (ox, oy, loc_z), 'frame': f
            }})
            cmds.append({'cmd': 'rotate_object', 'args': {
                'name': name, 'rotation': (spin_y, spin_y, spin_y), 'frame': f
            }})
        
    return cmds
