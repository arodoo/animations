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
LABEL_SIZE = 1.0

SETS = {
    'odds':      {'color': (1.0,  0.92, 0.10),
                  'emit': 5.0,  'size': 1.00},
    'naturals':  {'color': (0.10, 1.00, 0.85),
                  'emit': 4.0,  'size': 1.00},
    'integers':  {'color': (0.55, 0.25, 1.00),
                  'emit': 4.5,  'size': 1.00},
    'rationals': {'color': (0.15, 1.00, 0.35),
                  'emit': 4.0,  'size': 1.00},
    'reals':     {'color': (1.0,  0.15, 0.60),
                  'emit': 4.5,  'size': 1.00},
}

TIMING = Timing(
    odds_start=48,
    nat_start=348,
    int_start=798,
    rat_start=1248,
    real_start=1698,
    finale=2100,
)


def run():
    print("--- Starting Euler Scene ---")
    results = create_scene(
        total_frames=2400,
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
