# File: tests/e2e/test_dispatch_system.py
# E2E tests for the dispatcher and registry system. Tests command lookup,
# batch processing, error handling, and unknown command handling.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import pytest
from app.infra.bridge import reset
from app.kernel.dispatcher import dispatch_single, dispatch_batch
from app.kernel.dispatcher import dispatch_batch_stop_on_error
from app.kernel.registry import list_commands
import app.commands  # noqa: F401


@pytest.fixture(autouse=True)
def clean_state():
    reset()
    yield
    reset()


class TestDispatcher:
    """Tests for the dispatch system."""

    def test_dispatch_unknown_command_fails(self):
        """Unknown command returns failure result."""
        result = dispatch_single({'cmd': 'fly_to_moon', 'args': {}})
        assert not result.success
        assert 'Unknown command' in result.error

    def test_dispatch_missing_cmd_key(self):
        """Missing cmd key returns failure."""
        result = dispatch_single({'args': {}})
        assert not result.success
        assert "Missing 'cmd'" in result.error

    def test_batch_processes_all_commands(self):
        """Batch processes all commands in order."""
        results = dispatch_batch([
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'sphere'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'plane'}},
        ])
        assert len(results) == 3
        assert all(r.success for r in results)

    def test_batch_stop_on_error(self):
        """Batch with stop on error stops at first failure."""
        results = dispatch_batch_stop_on_error([
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube'}},
            {'cmd': 'move_object', 'args': {'name': 'Ghost'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'sphere'}},
        ])
        assert len(results) == 2
        assert results[0].success
        assert not results[1].success

    def test_all_commands_registered(self):
        """All expected commands are registered."""
        commands = list_commands()
        expected = [
            'spawn_primitive', 'move_object', 'rotate_object',
            'scale_object', 'set_keyframe', 'delete_object', 'parent_object'
        ]
        for cmd in expected:
            assert cmd in commands
