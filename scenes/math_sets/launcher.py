# File: scenes/math_sets/launcher.py
# Independent launcher for the Mathematical Sets animation.
# All Rights Reserved Arodi Emmanuel

import sys
import os

# ── 1. Project path ────────────────────────────────────────────────────────
PROJECT_PATH = r"d:\zProyectos\01Python\animations"
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

# Force reload engine modules to flush PyCache during Blender run
for m in list(sys.modules.keys()):
    if m.startswith('app.') or m.startswith('scenes.'):
        del sys.modules[m]

from scenes.math_sets.scene import create_scene


def run():
    print("--- Starting Mathematical Sets Scene Generation ---")
    
    results = create_scene(total_frames=900, camera_radius=30.0)
    
    print(f"Generated {len(results['results'])} commands.")
    print(f"Frames: {results['frames']}")
    print("--- Done ---")
    
    # Viewport configurations
    try:
        import bpy
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'RENDERED'
                        space.shading.use_scene_lights = True
                        space.shading.use_scene_world = True
        
        bpy.context.scene.frame_set(1)
        bpy.ops.screen.animation_play()
    except Exception:
        pass

if __name__ == "__main__":
    run()
