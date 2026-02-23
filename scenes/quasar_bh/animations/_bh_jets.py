# File: scenes/quasar_bh/animations/_bh_jets.py
# Relativistic polar jet geometry, materials and animation.
# Black hole sphere lives in _black_hole.py.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from . import _jet_physics as jp


def _jet_materials() -> List[Dict]:
    """Beaming-corrected materials: blue north (D³≫1), red south (D³≪1)."""
    north_emit = round(jp.JET_BASE_EMISSION * jp.doppler_factor(True), 2)
    south_emit = round(jp.JET_BASE_EMISSION * jp.doppler_factor(False), 2)
    return [
        {'cmd': 'create_material', 'args': {
            'name': 'JetNorthMat',
            'color': (0.55, 0.85, 1.0, 1.0),
            'emit': True, 'emit_strength': north_emit,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'JetSouthMat',
            'color': (1.0, 0.45, 0.20, 1.0),
            'emit': True, 'emit_strength': south_emit,
        }},
    ]


def _jet_geometry() -> List[Dict]:
    """Cylinders with MHD collimation radius + Lorentz-contracted length.

    Each cylinder has depth=length and is displaced ±length/2 along Z
    so its near cap sits at the BH origin and far cap at ±length.
    """
    length = jp.observed_length()
    r_mid = jp.collimation_radius(length * 0.5)
    specs = [
        ('JetNorth', length * 0.5, 'JetNorthMat'),
        ('JetSouth', -length * 0.5, 'JetSouthMat'),
    ]
    cmds: List[Dict] = []
    for name, z_pos, mat in specs:
        cmds += [
            {'cmd': 'spawn_primitive', 'args': {
                'type': 'cylinder', 'name': name,
                'vertices': 32, 'depth': length,
            }},
            {'cmd': 'assign_material', 'args': {
                'object': name, 'material': mat,
            }},
            {'cmd': 'scale_object', 'args': {
                'name': name,
                'scale': (r_mid, r_mid, 1.0),
            }},
            {'cmd': 'move_object', 'args': {
                'name': name, 'location': (0, 0, z_pos),
            }},
            {'cmd': 'parent_object', 'args': {
                'child': name, 'parent': 'BlackHole',
            }},
        ]
    return cmds


def build_jets(
    _use_particles: bool = False,
    total_frames: int = 900,
) -> List[Dict]:
    """All jet commands: geometry, knot spawn + animation keyframes."""
    from ._jet_animate import build_jet_animation
    cmds: List[Dict] = []
    cmds += _jet_materials()
    cmds += _jet_geometry()
    cmds += build_jet_animation(total_frames)
    return cmds
