# File: scenes/missile_storm/animations/staging/materials.py
# Materials for butterfly meadow scene.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_MATS = [
    ('MatGrass', (0.15, 0.35, 0.08), 0),
    ('MatButterfly', (0.9, 0.5, 0.1), 2),
    ('MatButterflyWing', (0.95, 0.6, 0.15), 3),
    ('MatHouseWall', (0.85, 0.8, 0.7), 0),
    ('MatRoof', (0.45, 0.18, 0.1), 0),
    ('MatBarnWood', (0.5, 0.3, 0.15), 0),
    ('MatTrunk', (0.35, 0.2, 0.1), 0),
    ('MatCanopy', (0.1, 0.4, 0.08), 0),
    ('MatFence', (0.6, 0.45, 0.25), 0),
]

_EXTRA: Dict[str, Dict] = {
    'MatGrass': {
        'roughness': 0.9,
        'use_noise_texture': True,
        'normal_strength': 0.25,
    },
}


def build_storm_materials() -> List[Dict]:
    """Create all scene materials."""
    cmds: List[Dict] = []
    for name, color, emit in _MATS:
        args: Dict = {
            'name': name,
            'color': color,
        }
        if emit > 0:
            args['emit'] = True
            args['emit_strength'] = float(emit)
        args.update(_EXTRA.get(name, {}))
        cmds.append({
            'cmd': 'create_material',
            'args': args,
        })
    return cmds
