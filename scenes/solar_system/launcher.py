# File: scenes/solar_system/launcher.py
# ─────────────────────────────────────────────────────────────────────────────
# HOW TO USE
#   1. Open Blender → Scripting tab → New text block
#   2. Paste this entire file
#   3. Set QUALITY below
#   4. Press "Run Script"
#   5. After it finishes: Z → Rendered (or Material Preview) to see planets
#      Press SPACE to play the animation
# ─────────────────────────────────────────────────────────────────────────────
# All Rights Reserved Arodi Emmanuel

import sys

# ── 1. Project path ────────────────────────────────────────────────────────
PROJECT_PATH = r"d:\zProyectos\01Python\animations"
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# ── 2. Quality setting ─────────────────────────────────────────────────────
#
#   'low'    → 4 planets, 3600 f  (30 fps = 2min)
#   'medium' → 6 planets, 3600 f
#   'high'   → 8 planets, 3600 f  + DoF
#   'ultra'  → 8 planets, 3600 f  + DoF, dense keyframes
#
QUALITY = 'ultra'

# ── 3. Purge stale bytecode + cached modules ───────────────────────────────
import importlib
import shutil
from pathlib import Path

for _pycache in Path(PROJECT_PATH).rglob('__pycache__'):
    shutil.rmtree(_pycache, ignore_errors=True)

for _mod in [k for k in sys.modules if k.startswith(('scenes', 'app'))]:
    del sys.modules[_mod]

# ── 4. Run ─────────────────────────────────────────────────────────────────
from scenes.solar_system.scene import create_scene


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
    print(f"  SOLAR SYSTEM  [quality = {QUALITY}]")
    print("=" * 60)

    result = create_scene(quality=QUALITY)

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
