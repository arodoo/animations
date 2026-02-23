# File moved: scenes/quasar_bh/_cam.py -> animations/_cam.py
# Camera: spherical orbit with depth of field.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

_CAM_RADIUS = 150     # wide orbital radius — jets must fit in frame
_FOCAL_LENGTH = 85.0  # mm — telephoto for compression and emphasis on center


def build_camera(
    total_frames: int, cam_step: int, dof: bool,
) -> List[Dict]:
    """
    Spherical orbit: azimuth sweeps full 360° over the full timeline.
    Elevation oscillates slightly to capture different angles. The camera
    is placed at a modest distance for an intimate cinematic orbit.
    """
    r = _CAM_RADIUS
    cmds: List[Dict] = [
        {'cmd': 'create_camera', 'args': {
            'name': 'SceneCamera',
        }},
        {'cmd': 'set_focal_length', 'args': {
            'name':         'SceneCamera',
            'focal_length': _FOCAL_LENGTH,
        }},
    ]
    # Use the full timeline for a complete orbit; keyframe density controlled
    # by `cam_step`. We avoid placing the camera on the polar axis (where
    # jets originate). Instead we keep an off-axis top-down viewpoint so the
    # jets remain visible, and the camera orbits panoramically around the
    # center. A brief dolly-in near the middle reveals the singularity but
    # not along the jet axis.
    for f in range(1, total_frames + 1, cam_step):
        t = (f - 1) / max(total_frames - 1, 1)
        az = t * 2 * math.pi          # full 360° azimuth sweep
        # Elevation uses a different frequency (3/2 of azimuth) so the
        # camera traces a 3-D Lissajous path — X, Y and Z all vary
        # continuously and the orbit never collapses to a flat circle.
        el = math.radians(35 + 25 * math.sin(t * 3 * math.pi))

        # Slow radial breathing: 2.5 full in-out cycles over the animation,
        # ±25% of base radius — independent of the elevation frequency so
        # the camera never repeats the same distance/angle combination.
        breathe = 0.25 * math.sin(t * 2.5 * 2 * math.pi)
        dodge = math.exp(-((t - 0.5) / 0.08) ** 2)
        r_local = r * (1.0 - breathe - 0.15 * dodge)

        x = r_local * math.cos(el) * math.cos(az)
        y = r_local * math.cos(el) * math.sin(az)
        z = r_local * math.sin(el)
        cmds.append({'cmd': 'move_object', 'args': {
            'name':     'SceneCamera',
            'location': (x, y, z),
            'frame':    f,
        }})
    cmds.append({'cmd': 'set_camera_target', 'args': {
        'name': 'SceneCamera', 'target': (0, 0, 0),
    }})
    if dof:
        # Focus near the inner disk radius to emphasize the singularity.
        cmds.append({'cmd': 'set_depth_of_field', 'args': {
            'name':           'SceneCamera',
            'enabled':        True,
            'focus_distance': 3.0,
            'fstop':          1.8,
        }})
    return cmds
