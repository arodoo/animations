# File: scenes/math_sets/animations/_equations.py
# Generates 3D typography corresponding to mathematical logic states.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def generate_math_label(
    number: int,
    loc_x: float,
    loc_y: float,
    loc_z: float,
    active_frame: int
) -> List[Dict]:
    """Generate the base number ID text over a block."""
    text_name = f"Text_ID_{number}"
    cmds: List[Dict] = []
    
    cmds.append({'cmd': 'spawn_text', 'args': {
        'name': text_name,
        'text': str(number),
        'location': (loc_x, loc_y, loc_z),
        'extrude': 0.04,
        'align_x': 'CENTER',
        'align_y': 'BOTTOM'
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': text_name, 'material': 'TextMat'
    }})
    cmds.append({'cmd': 'rotate_object', 'args': {
        'name': text_name, 'rotation': (1.5708, 0, 0), 'frame': 1  # Stand upright (PI/2)
    }})
    
    # Hide before it appears
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': text_name, 'scale': (0, 0, 0), 'frame': 1
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': text_name, 'scale': (1, 1, 1), 'frame': active_frame
    }})
    
    return cmds


def generate_formula_proof(
    number: int,
    is_odd: bool,
    loc_x: float,
    loc_y: float,
    loc_z: float,
    reveal_frame: int
) -> List[Dict]:
    """Generate the algebraic proof above the base number."""
    formula_name = f"Formula_{number}"
    cmds: List[Dict] = []
    
    # Mathematical logic: an odd number is 2k + 1
    if is_odd:
        k = number // 2
        formula_str = f"{number} = 2({k}) + 1"
    else:
        formula_str = f"{number} != 2k + 1"
        
    cmds.append({'cmd': 'spawn_text', 'args': {
        'name': formula_name,
        'text': formula_str,
        'location': (loc_x, loc_y, loc_z),
        'scale': (0.5, 0.5, 0.5), # Smaller subtext
        'extrude': 0.02,
        'align_x': 'CENTER',
        'align_y': 'BOTTOM'
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': formula_name, 'material': 'TextMat'
    }})
    cmds.append({'cmd': 'rotate_object', 'args': {
        'name': formula_name, 'rotation': (1.5708, 0, 0), 'frame': 1
    }})
    
    # Hide before reveal frame
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': formula_name, 'scale': (0, 0, 0), 'frame': 1
    }})
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': formula_name, 'scale': (0.5, 0.5, 0.5), 'frame': reveal_frame
    }})
    
    return cmds
