# File: scenes/quasar_bh/_env.py
# Environment commands: Eevee, timeline, starfield, dual accent lights.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List


def build_environment(p: Dict[str, Any]) -> List[Dict]:
    """Eevee, starfield and warm/cool dual-light rig."""
    return [
        {'cmd': 'clear_scene', 'args': {}},
        {'cmd': 'configure_eevee', 'args': {
            'width':   p['width'],
            'height':  p['height'],
            'samples': p['eevee_samples'],
        }},
        {'cmd': 'set_frame_range', 'args': {
            'start': 1, 'end': p['total_frames'],
        }},
        {'cmd': 'create_space_world', 'args': {
            'star_density':    500,
            'star_brightness': 3.5,
        }},
        # Warm golden key light — illuminates disk from above-right
        {'cmd': 'create_light', 'args': {
            'name':     'AccretionLight',
            'type':     'POINT',
            'location': (8, -4, 18),
            'color':    (1.0, 0.85, 0.3),
            'energy':   6000,
        }},
        # Cool blue rim light — below disk plane for fill
        {'cmd': 'create_light', 'args': {
            'name':     'RimLight',
            'type':     'SPOT',
            'location': (-10, 6, -12),
            'color':    (0.4, 0.6, 1.0),
            'energy':   3000,
        }},
    ]
