# File: scenes/quasar_bh/animations/_bh_jets.py
# Quasar jet wrapper — delegates to app.components.bodies.jet_builder.
# All Rights Reserved Arodi Emmanuel

from typing import List

# Ensure quasar constants are applied before jet_builder reads them
from . import _jet_physics  # noqa: F401
from ._black_hole import build_black_hole  # noqa: F401 (for backward mapping)
from app.components.bodies.jet_builder import build_jets as _build
from app.components.bodies.jet_physics import JET_BASE_EMISSION


def build_jets(
    _use_particles: bool = False,
    total_frames: int = 900,
) -> List[dict]:
    """Build relativistic jets using the generic jet builder."""
    return _build({
        'parent_object': 'BlackHole',
        'north_name':    'JetNorth',
        'south_name':    'JetSouth',
        'north_mat':     'JetNorthMat',
        'south_mat':     'JetSouthMat',
        'north_color':   (0.55, 0.85, 1.0, 1.0),
        'south_color':   (1.0, 0.40, 0.15, 1.0),
        'base_emission': JET_BASE_EMISSION,
        'total_frames':  total_frames,
    })
