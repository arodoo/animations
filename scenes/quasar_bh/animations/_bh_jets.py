# File: scenes/quasar_bh/animations/_bh_jets.py
# Relativistic polar jet geometry, materials and animation.
# Black hole sphere lives in _black_hole.py.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from . import _jet_physics as jp


def _jet_materials() -> List[Dict]:
    """Jet materials: both jets glow visibly as ejected plasma.

    North (approaching): blue, boosted by relativistic Doppler D³.
    South (receding):    red-orange, matched to north emission so
    both jets are visually prominent — physical suppression (D³≪1)
    would render it invisible at animation distances.
    """
    north_emit = round(jp.JET_BASE_EMISSION * jp.doppler_factor(True), 2)
    # Mirror north brightness; color (orange-red) marks the recession
    south_emit = north_emit
    return [
        {'cmd': 'create_material', 'args': {
            'name': 'JetNorthMat',
            'color': (0.55, 0.85, 1.0, 1.0),
            'emit': True, 'emit_strength': north_emit,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'JetSouthMat',
            'color': (1.0, 0.40, 0.15, 1.0),
            'emit': True, 'emit_strength': south_emit,
        }},
    ]


def _jet_geometry() -> List[Dict]:
    """Two cylinders along ±Z, mirrored about the BH origin.

    All transforms (scale, location) applied while the object is still
    unparented — world space == local space for an origin-parented object.
    Parent is set last so Blender does not reinterpret existing transforms.
    North: center at +length/2  → extends from  0  to +length.
    South: center at -length/2  → extends from -length to  0.
    """
    length = jp.observed_length()
    r_mid = jp.collimation_radius(length * 0.5)
    specs = [
        ('JetNorth',  length * 0.5, 'JetNorthMat'),
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
                'name': name, 'scale': (r_mid, r_mid, 1.0),
            }},
            {'cmd': 'move_object', 'args': {
                'name': name, 'location': (0, 0, z_pos),
            }},
            # Parent last: BlackHole is at world origin with no rotation,
            # so obj.location already equals its desired local offset.
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
