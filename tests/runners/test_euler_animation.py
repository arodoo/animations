# File: tests/runners/test_euler_animation.py
# Tests for the Expanding Euler Diagram animation.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from tests.demos.euler_demo import create_euler_animation


def test_euler_low_quality():
    """Low quality generates valid commands."""
    result = create_euler_animation('low')
    assert result is not None
    assert len(result['results']) > 0
    assert result['frames'] == 480


def test_euler_high_quality():
    """High quality generates valid commands."""
    result = create_euler_animation('high')
    assert len(result['results']) > 0
    assert result['frames'] == 2880


def test_euler_all_commands_succeed():
    """Every dispatched command must succeed."""
    result = create_euler_animation('low')
    failed = [
        f"{r.command_name}: {r.error}"
        for r in result['results']
        if not r.success
    ]
    assert not failed, "\n".join(failed)


def test_euler_invalid_quality():
    """Invalid quality raises ValueError."""
    try:
        create_euler_animation('ultra')
        assert False, "Expected ValueError"
    except ValueError:
        pass
