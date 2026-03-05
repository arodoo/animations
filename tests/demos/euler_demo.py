# File: tests/demos/euler_demo.py
# Expanding Euler Diagram demo.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scenes.euler_diagram.scene import create_scene
from scenes.euler_diagram.animations._timing import Timing

_PRESETS = {
    'low': {
        'total_frames': 600,
        'timing': Timing(
            ring_inner=60,
            odds_appear=120,
            zoom_start=200,
            ring_outer=300,
            outer_nums=360,
            zoom_end=480,
            labels=510,
        ),
    },
    'high': {
        'total_frames': 1200,
        'timing': Timing(
            ring_inner=80,
            odds_appear=160,
            zoom_start=320,
            ring_outer=540,
            outer_nums=620,
            zoom_end=900,
            labels=940,
        ),
    },
}


def create_euler_animation(
    quality: str = 'low',
) -> dict:
    """Create Expanding Euler Diagram animation."""
    if quality not in _PRESETS:
        raise ValueError(
            f"quality must be {list(_PRESETS)},"
            f" got '{quality}'"
        )
    p = _PRESETS[quality]
    result = create_scene(
        total_frames=p['total_frames'],
        timing=p['timing'],
    )
    return {**result, 'quality': quality}
