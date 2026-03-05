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
from scenes.euler_diagram.animations._timing import Timing

# --- Tune act timings (frames at 24fps ≈ 2 min) ---
TIMING = Timing(
    odds_start=60,    # Act 1: 45 gold odds
    nat_start=540,    # Act 2: 90 teal naturals
    int_start=1200,   # Act 3: 120 violet integers
    rat_start=1830,   # Act 4: 150 orange rationals
    real_start=2460,  # Act 5: 75 pink irrationals
    finale=2720,
)


def run():
    print("--- Starting Euler Diagram Scene ---")
    results = create_scene(
        total_frames=2880,
        timing=TIMING,
    )
    n = len(results['results'])
    print(f"Generated {n} commands.")
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
