# File: scenes/missile_storm/animations/acts/butterfly_flight.py
# Butterfly flies over meadow and village for 2 minutes.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.objects import (
    build_butterfly_body,
    build_butterfly_wings,
    build_meadow,
)
from ..domain.timing import Timing
from .flight_path import build_flight_path

_PART_MATS = [
    ('Butterfly_Torso', 'MatButterfly'),
    ('Butterfly_Head', 'MatButterfly'),
    ('Butterfly_AntennaL', 'MatTrunk'),
    ('Butterfly_AntennaR', 'MatTrunk'),
    ('Butterfly_WingL', 'MatButterflyWing'),
    ('Butterfly_WingR', 'MatButterflyWing'),
]


def build_flight(timing: Timing) -> List[Dict]:
    """Full butterfly flight: meadow + body + path."""
    cmds: List[Dict] = []
    cmds += build_meadow()
    cmds += build_butterfly_body()
    cmds += build_butterfly_wings(
        end_f=timing.flight_end,
    )
    for obj, mat in _PART_MATS:
        cmds.append({
            'cmd': 'assign_material',
            'args': {
                'object': obj,
                'material': mat,
            },
        })
    cmds += build_flight_path(timing)
    return cmds
