# Fractal Abyss launcher.
# Run inside Blender or standalone.
# All Rights Reserved Arodi Emmanuel

import sys

_PATH = r"d:\zProyectos\01Python\animations"
if _PATH not in sys.path:
    sys.path.insert(0, _PATH)

for m in list(sys.modules.keys()):
    if m.startswith(('app.', 'scenes.')):
        del sys.modules[m]

from scenes.fractal_abyss.scene import create_scene
from scenes.fractal_abyss.animations.domain.timing import (
    Timing,
)

TOTAL_FRAMES = 2880

TIMING = Timing(
    act1=1,
    act2=576,
    act3=1152,
    act4=1728,
    act5=2304,
)


def run():
    print("--- Fractal Abyss ---")
    res = create_scene(
        total_frames=TOTAL_FRAMES,
        timing=TIMING,
    )
    n = len(res['results'])
    print(f"Commands: {n}")
    print(f"Frames: {res['frames']}")
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
        print(f"Viewport skip: {exc}")


if __name__ == "__main__":
    run()
