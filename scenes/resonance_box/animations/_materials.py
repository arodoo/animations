# File: scenes/resonance_box/animations/_materials.py
# Materials for the music box: core sun, copper mechanisms, and dark planetary glass.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def generate_resonance_materials() -> List[Dict]:
    """Return commands to create foundational materials for Resonance mode."""
    return [
        {'cmd': 'create_metal_material', 'args': {
            'name': 'SunCoreMat',
            'color': (0.8, 0.6, 0.2, 1.0),
            'roughness': 0.15,
            'metallic': 1.0,
            'emit_strength': 2.0,  # Glowing core
        }},
        {'cmd': 'create_metal_material', 'args': {
            'name': 'CopperClockworkMat',
            'color': (0.85, 0.45, 0.20, 1.0),
            'roughness': 0.25,
            'metallic': 1.0,
            'emit_strength': 1.2, # Highly luminous tracks
        }},
        {'cmd': 'create_metal_material', 'args': {
            'name': 'SteelMat',
            'color': (0.4, 0.45, 0.5, 1.0),
            'roughness': 0.3,
            'metallic': 0.9,
        }},
    ]


def generate_glass_planet_material(name: str, color: tuple[float, float, float, float]) -> Dict:
    """Return command to create a dark glass material that supports emission bursts."""
    return {'cmd': 'create_material', 'args': {
        'name': f"{name}GlassMat",
        'color': color, 
        'roughness': 0.1,         # Glossy dark glass
        'emit': True,
        'emit_strength': 0.0      # Starts dark natively
    }}
