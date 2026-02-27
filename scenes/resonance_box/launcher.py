# File: scenes/resonance_box/launcher.py
# Independent launcher for the Rhythmic Resonance music box.
# All Rights Reserved Arodi Emmanuel

import sys
import os
import bpy

# Add project root to sys.path so 'app' module can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Force reload engine modules to flush PyCache during Blender run
for m in list(sys.modules.keys()):
    if m.startswith('app.') or m.startswith('scenes.'):
        del sys.modules[m]

from scenes.resonance_box.scene import create_scene


def run():
    print("--- Starting Resonance Box Scene Generation ---")
    
    # Render highly visible parameters by default to see the music box
    results = create_scene('ultra', total_frames=1200, camera_radius=90.0)
    
    print(f"Generated {len(results['results'])} commands.")
    print(f"Quality: {results['quality']}, Frames: {results['frames']}")
    print("--- Done ---")
    
    # Viewport configurations
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'
                    space.shading.use_scene_lights = True
                    space.shading.use_scene_world = True
    
    bpy.context.scene.frame_set(1)

if __name__ == "__main__":
    run()
