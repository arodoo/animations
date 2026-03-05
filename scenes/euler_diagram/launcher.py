# File: scenes/euler_diagram/launcher.py
# Independent launcher: run inside Blender or standalone.
# All Rights Reserved Arodi Emmanuel

import sys

PROJECT_PATH = (
    r"d:\zProyectos\01Python\animations"
)
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

for m in list(sys.modules.keys()):
    if m.startswith('app.') or m.startswith('scenes.'):
        del sys.modules[m]

from scenes.euler_diagram.scene import (
    create_scene,
)
from scenes.euler_diagram.animations.domain.timing import (
    Timing,
)

SPIRAL_SCALE = 1.0
LABEL_SIZE = 1.80

SETS = {
    'odds':      {'color': (1.0, 0.95, 0.15),
                  'emit': 48.0, 'size': 0.92},
    'naturals':  {'color': (0.1, 1.00, 0.95),
                  'emit': 30.0, 'size': 0.92},
    'integers':  {'color': (0.6, 0.30, 1.00),
                  'emit': 34.0, 'size': 0.80},
    'rationals': {'color': (0.2, 1.00, 0.40),
                  'emit': 30.0, 'size': 0.70},
    'reals':     {'color': (1.0, 0.20, 0.70),
                  'emit': 34.0, 'size': 0.70},
}

TIMING = Timing(
    odds_start=60,
    nat_start=600,
    int_start=1500,
    rat_start=2400,
    real_start=3600,
    finale=4600,
)


def run():
    print("--- Starting Euler Scene ---")
    results = create_scene(
        total_frames=4800,
        timing=TIMING,
        spiral_scale=SPIRAL_SCALE,
        sets=SETS,
        label_size=LABEL_SIZE,
    )
    n = len(results['results'])
    print(f"Generated {n} commands.")
    print(f"Frames: {results['frames']}")
    print("--- Done ---")

    try:
        import bpy
        areas = bpy.context.screen.areas
        for area in areas:
            if area.type != 'VIEW_3D':
                continue
            for sp in area.spaces:
                if sp.type != 'VIEW_3D':
                    continue
                sh = sp.shading
                sh.type = 'RENDERED'
                sh.use_scene_lights = True
                sh.use_scene_world = True
        bpy.context.scene.frame_set(1)
        bpy.ops.screen.animation_play()
    except Exception as exc:
        print(f"Viewport setup skipped: {exc}")


if __name__ == "__main__":
    run()
