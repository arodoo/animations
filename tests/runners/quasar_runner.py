# File: tests/runners/quasar_runner.py
# Runner for the quasar animation demo. Executes the full 3-minute animation
# sequence and verifies the successful execution of all generated commands.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tests.demos.quasar_demo import create_quasar_animation
from app.infra.bridge import data

def main() -> None:
    """Run the quasar animation demo and verify the results."""
    print("=" * 80)
    print("QUASAR ANIMATION DEMO - RUNNER")
    print("=" * 80)

    result = create_quasar_animation()
    
    success_count = sum(1 for r in result['results'] if r.success)
    total_commands = len(result['results'])
    
    print(f"
Total commands dispatched: {total_commands}")
    print(f"Successful commands: {success_count}/{total_commands}")
    
    if success_count < total_commands:
        print("
--- ERRORS DETECTED ---")
        for i, r in enumerate(result['results'], 1):
            if not r.success:
                print(f"  {i}. [FAIL] {r.command_name}: {r.error}")
    else:
        print("
All commands executed successfully!")

    # Verification of scene elements
    print("
--- SCENE VERIFICATION ---")
    elements = result.get('scene_elements', [])
    for element_name in elements:
        # A bit of a simplification, as the 'AccretionDisk' is multiple objects
        if 'AccretionDisk' in element_name:
             found = data.objects.get('InnerRing') and data.objects.get('MidRing') and data.objects.get('OuterRing')
             status = "OK" if found else "FAIL"
             print(f"  - {element_name}: {status}")
        elif 'Jets' in element_name:
             found = data.objects.get('JetNorth') and data.objects.get('JetSouth')
             status = "OK" if found else "FAIL"
             print(f"  - {element_name}: {status}")
        else:
            obj = data.objects.get(element_name)
            status = "OK" if obj else "FAIL"
            print(f"  - {element_name}: {status}")

    print(f"
Animation frames: {result.get('frames')}")
    print(f"Duration: {result.get('duration_seconds')} seconds")
    print("
" + "=" * 80)
    print("QUASAR DEMO COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
