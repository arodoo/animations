# File moved: scenes/quasar_bh/_env.py -> animations/_env.py
# Environment, lights and world settings for the scene.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List


def build_environment(p: Dict[str, Any]) -> List[Dict]:
    cmds: List[Dict] = []
    cmds.append({'cmd': 'clear_scene', 'args': {}})
    cmds.append({'cmd': 'set_frame_range', 'args': {
        'start': 1, 'end': p['total_frames'],
    }})
    # Near-black world so the sky/void stays dark but not pure black
    cmds.append({'cmd': 'set_world_background', 'args': {
        'color': (0.02, 0.02, 0.025),
    }})
    # Cartesian grid floor — placed BELOW all scene geometry.
    # JetSouth tip ≈ -43 BU; z_offset=-80 keeps the plane out of sight-lines.
    cmds.append({'cmd': 'create_cartesian_grid', 'args': {
        'size':       500,
        'grid_scale': 10,
        'z_offset':   -80.0,
        'bg_color':   (0.03, 0.03, 0.04, 1.0),
        'line_color': (0.12, 0.14, 0.22, 1.0),
    }})
    cmds.append({'cmd': 'create_light', 'args': {'name': 'KeyLight', 'type': 'AREA'}})
    cmds.append({'cmd': 'create_light', 'args': {'name': 'FillLight', 'type': 'POINT'}})
    return cmds
