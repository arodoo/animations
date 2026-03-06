# File: scenes/euler_diagram/launcher.py
# Independent launcher: run inside Blender or standalone.
# All Rights Reserved Arodi Emmanuel

import sys

PROJECT_PATH = r"d:\zProyectos\01Python\animations"
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

for m in list(sys.modules.keys()):
    if m.startswith('app.') or m.startswith('scenes.'):
        del sys.modules[m]

from scenes.euler_diagram.scene import create_scene
from scenes.euler_diagram.animations.domain.timing import Timing

SPIRAL_SCALE = 1.0
LABEL_SIZE = 1.0

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
        label_size=LABEL_SIZE,
    )
    n = len(results['results'])
    print(f"Generated {n} commands.")
    print(f"Frames: {results['frames']}")
    print("--- Done ---")

    try:
        import bpy
        for area in bpy.context.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            for sp in area.spaces:
                if sp.type != 'VIEW_3D':
                    continue
                sp.shading.type = 'RENDERED'
                sp.shading.use_scene_lights = True
                sp.shading.use_scene_world = True
        bpy.context.scene.frame_set(1)
        bpy.ops.screen.animation_play()
    except Exception as exc:
        print(f"Viewport setup skipped: {exc}")


if __name__ == "__main__":
    run()
