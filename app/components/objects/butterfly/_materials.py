# File: app/components/objects/butterfly/_materials.py
# Private: material assignments for butterfly parts.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_PART_MATS = [
    ('Torso',    'MatButterfly'),
    ('Head',     'MatButterfly'),
    ('AntennaL', 'MatTrunk'),
    ('AntennaR', 'MatTrunk'),
    ('WingFL',   'MatButterflyWing'),
    ('WingFR',   'MatButterflyWing'),
    ('WingHL',   'MatButterflyWing'),
    ('WingHR',   'MatButterflyWing'),
]


def assign_materials(name: str) -> List[Dict]:
    """Assign materials to all butterfly parts."""
    return [
        {'cmd': 'assign_material', 'args': {
            'object': f'{name}_{sfx}',
            'material': mat,
        }}
        for sfx, mat in _PART_MATS
    ]
