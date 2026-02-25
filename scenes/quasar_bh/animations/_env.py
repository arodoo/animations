# File: scenes/quasar_bh/animations/_env.py
# Quasar environment wrapper — delegates to app.components.env_builder.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List

from app.components.env_builder import build_environment as _build


def build_environment(p: Dict[str, Any]) -> List[Dict]:
    """Build quasar scene environment using the generic env_builder."""
    return _build({
        'total_frames':  p['total_frames'],
        'world_color':   (0.02, 0.02, 0.025),
        'grid':          True,
        'grid_size':     500,
        'grid_scale':    10,
        'grid_z_offset': -80.0,
        'grid_bg_color':   (0.03, 0.03, 0.04, 1.0),
        'grid_line_color': (0.12, 0.14, 0.22, 1.0),
        'lights': [
            {'name': 'KeyLight',  'type': 'AREA'},
            {'name': 'FillLight', 'type': 'POINT'},
        ],
    })
