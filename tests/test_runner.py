# File: test_runner.py
# Main test runner script that executes crear_escena_prueba() and displays
# results. Run directly: python test_runner.py (no Blender required).
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.core.logic import crear_escena_prueba


def main() -> None:
    """Run the test scene and display results."""
    print("=" * 60)
    print("PROCEDURAL ANIMATION ENGINE - TEST RUNNER")
    print("=" * 60)

    result = crear_escena_prueba()

    print(f"\nObjetos en escena: {result['objects']}")
    print(f"Posición final: {result['position']}")
    print(f"Keyframes guardados: {result['keyframes']}")

    print("\n--- Resultados de Dispatch ---")
    for i, r in enumerate(result['results'], 1):
        status = "OK" if r.success else "FAIL"
        print(f"  {i}. [{status}] {r.command_name}: {r.data or r.error}")

    print("\n" + "=" * 60)
    print("TEST COMPLETE - All operations executed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
