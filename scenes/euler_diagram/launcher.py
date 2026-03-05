# File: scenes/euler_diagram/launcher.py
# Independent launcher for the Expanding Euler Diagram.
# All Rights Reserved Arodi Emmanuel

import sys

PROJECT_PATH = r"d:\zProyectos\01Python\animations"
if PROJECT_PATH not in sys.path:
  sys.path.insert(0, PROJECT_PATH)

for m in list(sys.modules.keys()):
  if m.startswith('app.') or m.startswith('scenes.'):
    del sys.modules[m]

from scenes.euler_diagram.scene import (
  create_scene,
)
from scenes.euler_diagram.animations._timing import (
  Timing,
)

TIMING = Timing(
  odds_appear=100,
  zoom_start=200,
  zoom_end=500,
  text_appear=550,
)


def run():
  """Execute the Euler diagram animation."""
  print("--- Starting Euler Diagram Scene ---")
  results = create_scene(
    total_frames=700,
    timing=TIMING,
  )
  print(f"Generated {len(results['results'])} cmds")
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
