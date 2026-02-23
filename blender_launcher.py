# File: blender_launcher.py
# ─────────────────────────────────────────────────────────────────────────────
# Root launcher — delegates to whichever scene is active.
# You can also paste the scene-specific launcher directly in Blender:
#   scenes/quasar_bh/launcher.py
# ─────────────────────────────────────────────────────────────────────────────
# All Rights Reserved Arodi Emmanuel

import sys

PROJECT_PATH = r"d:\zProyectos\01Python\animations"
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# ── Active scene ───────────────────────────────────────────────────────────
from scenes.quasar_bh.scene import create_scene as run_scene

# ── Quality ────────────────────────────────────────────────────────────────
#   'low'    →  5 rings, 3600 frames (120 s)
#   'medium' →  7 rings, 3600 frames (120 s)
#   'high'   →  9 rings, 3600 frames (120 s) + DoF + pulses
#   'ultra'  →  9 rings, 3600 frames (120 s) + particles
QUALITY = 'low'


def _setup_viewport() -> None:
    """Switch every 3-D viewport to Material Preview + start playback."""
    try:
        import bpy
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type != 'VIEW_3D':
                    continue
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
        bpy.ops.screen.animation_play()
    except Exception:
        pass


if __name__ == '__main__':
    print("=" * 60)
    print(f"  QUASAR BLACK HOLE  [quality = {QUALITY}]")
    print("=" * 60)

    result = run_scene(quality=QUALITY)

    ok_count = sum(1 for r in result['results'] if r.success)
    total    = len(result['results'])
    print(f"\n  Frames   : {result['frames']}")
    print(f"  Commands : {ok_count} / {total} OK")

    failed = [r for r in result['results'] if not r.success]
    if failed:
        print(f"\n  ── {len(failed)} errors ──")
        for r in failed:
            print(f"    [FAIL] {r.command_name}: {r.error}")

    _setup_viewport()

    print("\n" + "=" * 60)
    print("  Done — viewport set to Material Preview, playing")
    print("=" * 60)
