# File: tests/runners/erratic_orbit_runner.py
# Runner for the erratic orbit demo. Executes 30-second chaotic orbit with
# procedural starfield atmosphere in a mock Blender context.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tests.demos.erratic_orbit_demo import crear_orbita_relativista
from app.infra.bridge import data

def main() -> None:
    """Run the erratic orbit demo and verify state."""
    print("=" * 60)
    print("ERRATIC ORBIT DEMO - 30 SECONDS WITH STARFIELD")
    print("=" * 60)

    result = crear_orbita_relativista()
    
    success_count = sum(1 for r in result['results'] if r.success)
    print(f"\nTotal comandos enviados: {len(result['results'])}")
    print(f"Comandos exitosos: {success_count}/{len(result['results'])}")
    print(f"Estrellas generadas: {result['stars']}")
    print(f"Duración: {result['duration_seconds']} segundos ({result['frames']} frames)")
    
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

    print("\n" + "=" * 60)
    print("DEMO COMPLETE - Ready for Blender!")
    print("=" * 60)

import math
if __name__ == "__main__":
    main()
