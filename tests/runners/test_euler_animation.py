# File: tests/runners/test_euler_animation.py
# Unit tests for the Expanding Euler Diagram animation.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
  sys.path.insert(0, str(project_root))

from tests.demos.euler_demo import (
  create_euler_animation,
)


def test_euler_animation_low_quality():
  """Test low-quality animation generation."""
  result = create_euler_animation('low')
  assert result is not None
  assert 'results' in result
  assert 'frames' in result
  assert len(result['results']) > 0
  assert result['frames'] == 600


def test_euler_animation_high_quality():
  """Test high-quality animation generation."""
  result = create_euler_animation('high')
  assert result is not None
  assert 'results' in result
  assert len(result['results']) > 0
  assert result['frames'] == 1200


def test_euler_all_commands_succeed():
  """Verify all commands execute without errors."""
  result = create_euler_animation('low')
  for cmd_result in result['results']:
    assert cmd_result.success, (
      f"Command {cmd_result.command_name} failed: "
      f"{cmd_result.error}"
    )


def test_euler_invalid_quality():
  """Test invalid quality parameter."""
  try:
    create_euler_animation('invalid')
    assert False, "Should raise ValueError"
  except ValueError:
    pass
