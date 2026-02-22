# File: scenes/quasar_bh/launcher.py
# ─────────────────────────────────────────────────────────────────────────────
# HOW TO USE
#   1. Open Blender → Scripting tab → New text block
#   2. Paste this entire file
#   3. Set QUALITY below
#   4. Press "Run Script"
#   5. After it finishes: Z → Rendered (or Material Preview) to see glow
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
#   'low'    →  5 rings,  900 f  ( 30 s) 1280×720   safe on any GPU
#   'medium' →  7 rings, 1800 f  ( 60 s) 1280×720   Intel i7 + 24 GB
#   'high'   →  9 rings, 3600 f  (120 s) 1920×1080  DoF + pulses
#   'ultra'  →  9 rings, 3600 f  (120 s) 1920×1080  + particles
#
QUALITY = 'ultra'

# ── 3. Run ────────────────────────────────────────────────────────────────
from scenes.quasar_bh.scene import create_scene

if __name__ == '__main__':
    print("=" * 60)
    print(f"  QUASAR BLACK HOLE  [quality = {QUALITY}]")
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

    print("\n" + "=" * 60)
    print("  Done — Z → Rendered mode, then SPACE to play")
    print("=" * 60)
