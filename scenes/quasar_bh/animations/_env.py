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
    cmds.append({'cmd': 'set_world_color', 'args': {'color': (0.0, 0.0, 0.0)}})
    cmds.append({'cmd': 'create_light', 'args': {'name': 'KeyLight', 'type': 'AREA'}})
    cmds.append({'cmd': 'create_light', 'args': {'name': 'FillLight', 'type': 'POINT'}})
    return cmds
