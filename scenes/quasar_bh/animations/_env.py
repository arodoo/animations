# File moved: scenes/quasar_bh/_env.py -> animations/_env.py
# Environment, lights and world settings for the scene.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List


def build_environment(p: Dict[str, Any]) -> List[Dict]:
    cmds: List[Dict] = []
    cmds.append({'cmd': 'set_world_color', 'args': {'color': (0.01, 0.01, 0.02)}})
    cmds.append({'cmd': 'create_light', 'args': {'name': 'KeyLight', 'type': 'AREA'}})
    cmds.append({'cmd': 'create_light', 'args': {'name': 'FillLight', 'type': 'POINT'}})
    return cmds
