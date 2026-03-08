# File: scenes/missile_storm/launcher.py
# Paste in Blender > Scripting > Run Script.
# Adjust TIMING below. Z > Material Preview, SPACE.
# All Rights Reserved Arodi Emmanuel

import sys

PROJECT_PATH = r"d:\zProyectos\01Python\animations"
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# -- Timing configuration -------------------
from scenes.missile_storm.animations.domain.timing import Timing

TIMING = Timing(
    flight_start=1,
    flight_end=480,
    strike_frame=481,
    strike_explode=500,
    pullback_start=500,
    barrage_start=600,
    barrage_end=1080,
    finale_end=1200,
)
CAM_STEP = 4

# -- Purge cache -----------------------------
import shutil
from pathlib import Path

for _pc in Path(PROJECT_PATH).rglob('__pycache__'):
    shutil.rmtree(_pc, ignore_errors=True)
for _m in [
    k for k in sys.modules
    if k.startswith(('scenes', 'app'))
]:
    del sys.modules[_m]

# -- Run scene --------------------------------
from scenes.missile_storm.scene import create_scene


def _setup_viewport() -> None:
    try:
        import bpy
        for w in bpy.context.window_manager.windows:
            for a in w.screen.areas:
                if a.type != 'VIEW_3D':
                    continue
                for s in a.spaces:
                    if s.type == 'VIEW_3D':
                        s.shading.type = 'MATERIAL'
        bpy.ops.screen.animation_play()
    except Exception:
        pass


if __name__ == '__main__':
    print("=" * 50)
    print("  MISSILE STORM")
    print("=" * 50)
    result = create_scene(TIMING, CAM_STEP)
    ok_n = sum(
        1 for r in result['results'] if r.success
    )
    total = len(result['results'])
    print(f"\n  Frames: {result['frames']}")
    print(f"  Commands: {ok_n}/{total} OK")
    failed = [
        r for r in result['results']
        if not r.success
    ]
    if failed:
        for r in failed[:10]:
            print(f"  [FAIL] {r.command_name}")
    _setup_viewport()
    print("  Done.")
