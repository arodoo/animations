# File moved: scenes/quasar_bh/_bh_jets.py -> animations/_bh_jets.py
# Black hole sphere and polar relativistic jet commands.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List
from app.kernel.registry import register_command
from . import _physics


_JET_SPECS = [('JetNorth', 28), ('JetSouth', -28)]


def build_black_hole() -> List[Dict]:
    """Central black hole — pure black, non-emissive sphere.

    Spawn a higher-resolution, smooth sphere sized to the Schwarzschild
    radius so it aligns visually with the relativistic disk geometry.
    """
    # Use the scene-normalised Schwarzschild radius for visual scale.
    r_s = float(_physics.SCHWARZSCHILD_RADIUS)
    scale_val = max(0.05, r_s)  # guard against zero/too-small values

    return [
        {'cmd': 'create_material', 'args': {
            'name': 'BlackHoleMat', 'color': (0, 0, 0, 1),
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'sphere',
            'name': 'BlackHole',
            # Request higher tessellation and smooth shading for a clean rim
            'segments': 64,
            'ring_count': 32,
            'shade_smooth': True,
            'subsurf_levels': 2,
        }},
        {'cmd': 'assign_material', 'args': {
            'object': 'BlackHole', 'material': 'BlackHoleMat',
        }},
        {'cmd': 'scale_object', 'args': {
            'name': 'BlackHole', 'scale': (scale_val, scale_val, scale_val),
        }},
    ]


def build_jets(use_particles: bool) -> List[Dict]:
    """Polar jets — electric-blue cones with optional particle stream."""
    cmds: List[Dict] = [
        {'cmd': 'create_material', 'args': {
            'name':          'JetMat',
            'color':         (0.7, 0.9, 1.0, 1.0),
            'emit':          True,
            'emit_strength': 12.0,
        }},
    ]
    for jet_name, z_pos in _JET_SPECS:
        cmds += [
            {'cmd': 'spawn_primitive', 'args': {
                'type': 'cone', 'name': jet_name}},
            {'cmd': 'assign_material', 'args': {
                'object': jet_name, 'material': 'JetMat'}},
            {'cmd': 'scale_object', 'args': {
                'name': jet_name, 'scale': (0.18, 0.18, 55)}},
            {'cmd': 'move_object', 'args': {
                'name': jet_name, 'location': (0, 0, z_pos)}},
            {'cmd': 'parent_object', 'args': {
                'child': jet_name, 'parent': 'BlackHole'}},
        ]
        if use_particles:
            cmds.append({'cmd': 'add_particle_system', 'args': {
                'object':        jet_name,
                'name':          f'{jet_name}Particles',
                'count':         800,
                'lifetime':      90,
                'emit_from':     'FACE',
                'normal_factor': 2.0,
                'gravity':       0.0,
                'size':          0.08,
                'render_type':   'HALO',
            }})
    return cmds
