# File: tests/runners/orbit_runner.py
# Runner for the spiral orbit demo. Executes animation logic and verifies
# command execution results in a mock Blender context.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tests.demos.orbit_demo import crear_orbita_espiral
from app.infra.bridge import data

def main() -> None:
    """Run the spiral orbit demo and verify state."""
    print("=" * 60)
    print("SPIRAL ORBIT DEMO - RUNNER")
    print("=" * 60)

    result = crear_orbita_espiral()
    
    success_count = sum(1 for r in result['results'] if r.success)
    print(f"\nTotal comandos enviados: {len(result['results'])}")
    print(f"Comandos exitosos: {success_count}/{len(result['results'])}")
    
    if success_count < len(result['results']):
        print("\n--- ERRORES DETECTADOS ---")
        for i, r in enumerate(result['results'], 1):
            if not r.success:
                print(f"  {i}. [FAIL] {r.command_name}: {r.error}")
    
    # Verify final satellite transform
    sat = data.objects.get('Satellite')
    if sat:
        loc = sat.location.to_tuple()
        print(f"\nPosición final Satélite: ({loc[0]:.2f}, {loc[1]:.2f}, {loc[2]:.2f})")
        print(f"Radio objetivo: {result['final_radius']}")
        
        # In frame 250 (angle = 5 * 2pi = 10pi), cos(10pi)=1, sin(10pi)=0
        # Expected pos: (radius, 0, 0)
        dist = math.sqrt(loc[0]**2 + loc[1]**2)
        print(f"Distancia al centro: {dist:.2f}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)

import math
if __name__ == "__main__":
    main()
