# File: blender_launcher.py
# Blender launcher script for the spiral orbit demo. Run this inside Blender's
# scripting tab to execute the animation with real 3D objects and materials.
# All Rights Reserved Arodi Emmanuel

import sys
import os

# 1. Add project path to Python's module search path
project_path = r"d:\zProyectos\01Python\animations"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# 2. Import the demo logic (will use real bpy automatically via bridge)
# Choose which demo to run:
# Option 1: Simple spiral orbit (250 frames, 5 turns)
# from tests.demos.orbit_demo import crear_orbita_espiral as run_demo

# Option 2: Erratic orbit with starfield (900 frames, 30 seconds, 1150 stars)
from tests.demos.erratic_orbit_demo import crear_orbita_erratica as run_demo

# 3. Execute the animation
if __name__ == "__main__":
    print("=" * 60)
    print("EXECUTING ANIMATION IN BLENDER")
    print("=" * 60)
    
    result = run_demo()
    
    success_count = sum(1 for r in result['results'] if r.success)
    print(f"\nTotal comandos ejecutados: {len(result['results'])}")
    print(f"Comandos exitosos: {success_count}/{len(result['results'])}")
    
    if success_count < len(result['results']):
        print("\n--- ERRORES ---")
        for i, r in enumerate(result['results'], 1):
            if not r.success:
                print(f"  {i}. [FAIL] {r.command_name}: {r.error}")
    
    print("\n" + "=" * 60)
    print("ANIMATION READY - Press PLAY to see it!")
    print("=" * 60)
