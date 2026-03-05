# File: scenes/euler_diagram/launcher.py
# Launcher — edit TIMING here to tune the animation.
# All Rights Reserved Arodi Emmanuel

import sys

PROJECT_PATH = r"d:\zProyectos\01Python\animations"
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

for m in list(sys.modules.keys()):
    if m.startswith('app.') or m.startswith('scenes.'):
        del sys.modules[m]

from scenes.euler_diagram.scene import create_scene
from scenes.euler_diagram.animations._timing import Timing

# --- Tune here without opening animation files ---
TIMING = Timing(
    ring_inner=60,
    odds_appear=120,
    zoom_start=250,
    ring_outer=380,
    outer_nums=440,
    zoom_end=560,
    labels=590,
)
TOTAL_FRAMES = 700


def run():
    """Execute the Expanding Euler Diagram animation."""
    print("--- Expanding Euler Diagram ---")
    result = create_scene(
        total_frames=TOTAL_FRAMES,
        timing=TIMING,
    )
    print(f"Commands: {len(result['results'])}")
    print(f"Frames: {result['frames']}")
    print("--- Done ---")

    try:
        import bpy
        for area in bpy.context.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            for space in area.spaces:
                if space.type != 'VIEW_3D':
                    continue
                sh = space.shading
                sh.type = 'RENDERED'
                sh.use_scene_lights = True
        bpy.context.scene.frame_set(1)
        bpy.ops.screen.animation_play()
    except Exception as exc:
        print(f"Blender viewport skipped: {exc}")


if __name__ == "__main__":
    run()
