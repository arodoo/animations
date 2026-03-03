# File: scenes/math_sets/launcher.py
# Independent launcher for the Mathematical Sets animation.
# All Rights Reserved Arodi Emmanuel

import sys

PROJECT_PATH = r"d:\zProyectos\01Python\animations"
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

for m in list(sys.modules.keys()):
    if m.startswith('app.') or m.startswith('scenes.'):
        del sys.modules[m]

from scenes.math_sets.scene import create_scene
from scenes.math_sets.animations._timing import Timing

# --- Tune act timings (frames) ---
TIMING = Timing(
    act1=150,   # N membership tags appear
    act2=270,   # Odds check tags appear
    act3=360,   # Venn rings reveal
    act4=410,   # Block migration (tight after rings)
    act5=600,   # Formal proof text
)


def run():
    print("--- Starting Mathematical Sets Scene ---")
    results = create_scene(
        total_frames=900,
        camera_radius=30.0,
        timing=TIMING,
    )
    print(f"Generated {len(results['results'])} commands.")
    print(f"Frames: {results['frames']}")
    print("--- Done ---")

    try:
        import bpy
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        sh = space.shading
                        sh.type = 'RENDERED'
                        sh.use_scene_lights = True
                        sh.use_scene_world = True
        bpy.context.scene.frame_set(1)
        bpy.ops.screen.animation_play()
    except Exception as exc:
        print(f"Blender viewport setup skipped: {exc}")


if __name__ == "__main__":
    run()
