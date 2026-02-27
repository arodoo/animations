# File: scenes/math_sets/animations/_venn_diagram.py
# Draws physical Venn Diagrams to prove "All odds are numbers; not all numbers are odds".
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def generate_set_boundaries(
    total_frames: int,
    start_x: float,
    end_x: float,
    loc_z: float = -0.5
) -> List[Dict]:
    """Generate Torus boundaries representing logic Supersets and Subsets."""
    cmds: List[Dict] = []

    center_x = (start_x + end_x) / 2.0
    # The major radius needs to span all 10 blocks (e.g. from x=-10 to x=10 => radius 12)
    superset_radius = abs(end_x - start_x) / 2.0 + 1.5
    
    # 1. THE NARRATOR: "Allí donde hay un impar, habrá siempre un número"
    # Act 1 (Frame 150): The "NUMBERS" Superset appears, encapsulating EVERYTHING.
    cmds.append({'cmd': 'spawn_primitive', 'args': {
        'type': 'torus', 'name': 'Superset_Numbers',
        'location': (center_x, 0.0, loc_z),
        'major_radius': superset_radius, 'minor_radius': 0.05,
        'major_segments': 64, 'minor_segments': 16,
        'shade_smooth': True
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': 'Superset_Numbers', 'material': 'TextMat' # Pure White
    }})
    
    cmds.append({'cmd': 'scale_object', 'args': {'name': 'Superset_Numbers', 'scale': (0,0,0), 'frame': 1}})
    cmds.append({'cmd': 'scale_object', 'args': {'name': 'Superset_Numbers', 'scale': (1,2,1), 'frame': 150}})
    
    # Text Label for Superset
    cmds.append({'cmd': 'spawn_text', 'args': {
        'name': 'Label_Numbers', 'text': 'NUMBERS (Superset)',
        'location': (center_x, superset_radius * 2.2, loc_z),
        'extrude': 0.02, 'align_y': 'CENTER', 'align_x': 'CENTER'
    }})
    cmds.append({'cmd': 'assign_material', 'args': {'object': 'Label_Numbers', 'material': 'TextMat'}})
    cmds.append({'cmd': 'scale_object', 'args': {'name': 'Label_Numbers', 'scale': (0,0,0), 'frame': 1}})
    cmds.append({'cmd': 'scale_object', 'args': {'name': 'Label_Numbers', 'scale': (1.5,1.5,1.5), 'frame': 160}})


    # 2. THE NARRATOR: "Sin embargo, allí donde haya un número, no habrá siempre un impar."
    # Act 2 (Frame 300): The "ODDS" Subset appears. We must visually bend it or weave it
    # so it physically ONLY touches the Odds (1,3,5...) while leaving the Evens outside it.
    
    # We will represent the Subset as a secondary Torus that scales up, but is segmented
    # or positioned to highlight the exclusivity. Since they are linear, we will use a Torus
    # that encapsulates the odds, colored Orange.
    cmds.append({'cmd': 'spawn_primitive', 'args': {
        'type': 'torus', 'name': 'Subset_Odds',
        'location': (center_x - 1.1, 0.0, loc_z + 0.1), # Slightly offset
        'major_radius': superset_radius - 0.5, 'minor_radius': 0.08,
        'major_segments': 64, 'minor_segments': 16, 'shade_smooth': True
    }})
    cmds.append({'cmd': 'assign_material', 'args': {'object': 'Subset_Odds', 'material': 'OddMat'}})
    
    cmds.append({'cmd': 'scale_object', 'args': {'name': 'Subset_Odds', 'scale': (0,0,0), 'frame': 1}})
    # At frame 300, the ring appears and weaves through the logic
    cmds.append({'cmd': 'scale_object', 'args': {'name': 'Subset_Odds', 'scale': (1,0.5,1), 'frame': 300}})
    
    # Text Label for Subset
    cmds.append({'cmd': 'spawn_text', 'args': {
        'name': 'Label_Odds', 'text': 'ODDS (Subset)',
        'location': (center_x, -superset_radius, loc_z),
        'extrude': 0.02, 'align_y': 'CENTER', 'align_x': 'CENTER'
    }})
    cmds.append({'cmd': 'assign_material', 'args': {'object': 'Label_Odds', 'material': 'OddMat'}})
    cmds.append({'cmd': 'scale_object', 'args': {'name': 'Label_Odds', 'scale': (0,0,0), 'frame': 1}})
    cmds.append({'cmd': 'scale_object', 'args': {'name': 'Label_Odds', 'scale': (2,2,2), 'frame': 320}})


    # 3. Act 3 (Frame 600): The Fusion
    fusion_start = 600
    if total_frames > fusion_start:
        # Hide the rigid 2D sets as the reality grid becomes a 3D sphere
        for obj_name in ['Superset_Numbers', 'Subset_Odds', 'Label_Numbers', 'Label_Odds']:
            cmds.append({'cmd': 'scale_object', 'args': {'name': obj_name, 'scale': (0,0,0), 'frame': fusion_start}})

    return cmds
