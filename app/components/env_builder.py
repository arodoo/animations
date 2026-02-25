# File: app/components/env_builder.py
# Generic scene environment builder — lights, world background, grid.
# Extracted from scenes/quasar_bh/animations/_env.py.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List


def build_environment(cfg: Dict[str, Any]) -> List[Dict]:
    """Return commands to initialise the scene environment.

    Args:
        cfg: dict with keys:
            total_frames   (int)  — frame range end
            world_color    (tuple[float,3]) — RGB world background
            grid           (bool) — whether to add a cartesian grid
            grid_size      (int)
            grid_scale     (int)
            grid_z_offset  (float)
            grid_bg_color  (tuple[float,4])
            grid_line_color(tuple[float,4])
            lights         (list[dict]) — each: {name, type}
    """
    cmds: List[Dict] = []
    cmds.append({'cmd': 'clear_scene', 'args': {}})
    cmds.append({'cmd': 'set_frame_range', 'args': {
        'start': 1, 'end': cfg['total_frames'],
    }})
    cmds.append({'cmd': 'set_world_background', 'args': {
        'color': cfg['world_color'],
    }})
    if cfg.get('grid', False):
        cmds.append({'cmd': 'create_cartesian_grid', 'args': {
            'size':       cfg.get('grid_size', 500),
            'grid_scale': cfg.get('grid_scale', 10),
            'z_offset':   cfg.get('grid_z_offset', 0.0),
            'bg_color':   cfg.get('grid_bg_color', (0.03, 0.03, 0.04, 1.0)),
            'line_color': cfg.get('grid_line_color', (0.12, 0.14, 0.22, 1.0)),
        }})
    for light in cfg.get('lights', []):
        cmds.append({'cmd': 'create_light', 'args': {
            'name': light['name'],
            'type': light['type'],
        }})
    return cmds
