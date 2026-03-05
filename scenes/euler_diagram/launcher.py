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

# --- Spacing (1.0 = default, >1 more space, <1 less) ---
SPIRAL_SCALE = 1.0

# --- Label size ('0' and set names like 'Impares') ---
LABEL_SIZE = 1.60

# --- Per-set config: color (R,G,B), emit strength, size ---
SETS = {
    'odds':      {'color': (1.0, 0.85, 0.00), 'emit': 28.0, 'size': 0.92},
    'naturals':  {'color': (0.0, 1.00, 0.85), 'emit': 14.0, 'size': 0.92},
    'integers':  {'color': (0.55, 0.0, 1.00), 'emit': 14.0, 'size': 0.80},
    'rationals': {'color': (1.0, 0.45, 0.00), 'emit': 14.0, 'size': 0.70},
    'reals':     {'color': (1.0, 0.10, 0.55), 'emit': 14.0, 'size': 0.70},
}

# --- Act timings (frames at 24fps ≈ 2 min) ---
TIMING = Timing(
    odds_start=60,
    nat_start=540,
    int_start=1200,
    rat_start=1830,
    real_start=2460,
    finale=2720,
)


def run():
    print("--- Starting Euler Diagram Scene ---")
    results = create_scene(
        total_frames=2880,
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
