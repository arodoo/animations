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
        'total_frames': 480,
        'timing': Timing(
            odds_start=10,
            nat_start=60,
            int_start=130,
            rat_start=210,
            real_start=340,
            finale=430,
        ),
    },
    'high': {
        'total_frames': 2880,
        'timing': Timing(),   # default timing
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
