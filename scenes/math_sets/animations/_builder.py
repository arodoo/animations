# File: scenes/math_sets/animations/_builder.py
# Assembles the Mathematical Sets storyboard based on the 3 Acts.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List
from ._materials import generate_math_materials
from ._logic_blocks import build_number_pedestal
from ._venn_diagram import generate_set_boundaries


def build_math_sets(total_frames: int, num_sequence: int = 10) -> List[Dict]:
    """Calculate and return all commands to construct the philosophical sets.
    
    Act 1: Generation & Odds Proof (Frames 1-200)
    Act 2: Evens Counter-Proof (Frames 200-400)
    Act 3: Grid Reality Fusion (Frames 400+)
    """
    cmds = generate_math_materials()
    
    # Generate the sequence of numbers 1 through 10
    start_x = -10.0
    spacing = 2.2
    
    for i in range(1, num_sequence + 1):
        loc_x = start_x + (i * spacing)
        loc_y = 0.0
        loc_z = 0.0
        
        cmds += build_number_pedestal(i, loc_x, loc_y, loc_z, total_frames)
        
    # Draw the Didactic Sets (Venn Diagram loops) on the floor
    # based on the geometric boundaries of the sequence
    end_x = start_x + (num_sequence * spacing)
    cmds += generate_set_boundaries(total_frames, start_x, end_x, loc_z=-0.5)
        
    return cmds
