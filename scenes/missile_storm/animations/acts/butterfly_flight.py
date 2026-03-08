# File: scenes/missile_storm/animations/acts/butterfly_flight.py
# Act 1: Butterfly flies over meadow for 20 seconds.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.objects import (
    build_butterfly_body,
    build_butterfly_wings,
    build_meadow,
)
from ..domain.timing import Timing
from .flight_path import build_flight_path

_WING_MATS = [
    ('Butterfly_WingL', 'MatButterflyWing'),
    ('Butterfly_WingR', 'MatButterflyWing'),
]


def build_flight(timing: Timing) -> List[Dict]:
    """Full Act 1: meadow + butterfly + path."""
    cmds: List[Dict] = []
    cmds += build_meadow()
    cmds += build_butterfly_body()
    cmds += build_butterfly_wings(
        end_f=timing.flight_end,
    )
    cmds.append({
        'cmd': 'assign_material',
        'args': {
            'object': 'Butterfly_Torso',
            'material': 'MatButterfly',
        },
    })
    for obj, mat in _WING_MATS:
        cmds.append({
            'cmd': 'assign_material',
            'args': {
                'object': obj,
                'material': mat,
            },
        })
    cmds += build_flight_path(timing)
    return cmds
