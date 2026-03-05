# File: tests/runners/euler_runner.py
# Runner for the Expanding Euler Diagram animation.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
  sys.path.insert(0, str(project_root))

from tests.demos.euler_demo import (
  create_euler_animation,
)


def main() -> None:
  """Run the Euler diagram animation and verify."""
  print("=" * 80)
  print("EULER DIAGRAM ANIMATION - RUNNER")
  print("=" * 80)

  result = create_euler_animation(quality='low')

  success_count = sum(
    1 for r in result['results'] if r.success
  )
  total = len(result['results'])

  print(f"Total commands: {total}")
  print(f"Successful: {success_count}/{total}")

  if success_count < total:
    print("\n--- ERRORS ---")
    for i, r in enumerate(result['results'], 1):
      if not r.success:
        print(f"  {i}. [{r.command_name}]: {r.error}")
  else:
    print("\nAll commands executed!")

  print(f"\nFrames: {result.get('frames')}")
  print("=" * 80)


if __name__ == "__main__":
  main()
