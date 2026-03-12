# File: app/components/objects/butterfly/builder.py
# Butterfly character component: body + wings + mats.
# Animate {name}_Torso externally for flight path.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._body import build_body
from ._wings import build_wings
from ._materials import assign_materials


def build_butterfly(
    name: str = 'Butterfly',
    pos: tuple = (0, 0, 3),
    start_f: int = 1,
    end_f: int = 480,
    half_cycle: int = 6,
) -> List[Dict]:
    """Butterfly character: body + wings + materials.

    Root object: {name}_Torso.
    Move it externally to control world position.
    """
    cmds: List[Dict] = []
    cmds += build_body(name, pos)
    cmds += build_wings(name, start_f, end_f, half_cycle)
    cmds += assign_materials(name)
    return cmds
