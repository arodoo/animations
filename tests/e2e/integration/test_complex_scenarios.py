# File: tests/e2e/test_complex_scenarios.py
# E2E tests for complex real-world scenarios. Tests complete animation
# workflows, object lifecycle, and multi-command sequences.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import pytest
from app.infra.bridge import data, reset
from app.kernel.dispatcher import dispatch_batch
import app.commands  # noqa: F401


@pytest.fixture(autouse=True)
def clean_state():
    reset()
    yield
    reset()


class TestComplexScenarios:
    """Tests for complex multi-step scenarios."""

    def test_full_animation_workflow(self):
        """Complete animation: spawn, move, keyframe at multiple frames."""
        results = dispatch_batch([
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'A'}},
            {'cmd': 'set_keyframe', 'args': {
                'name': 'A', 'property': 'location', 'frame': 1
            }},
            {'cmd': 'move_object', 'args': {
                'name': 'A', 'location': (5, 0, 0), 'frame': 30
            }},
            {'cmd': 'move_object', 'args': {
                'name': 'A', 'location': (10, 0, 0), 'frame': 60
            }},
        ])
        assert all(r.success for r in results)
        obj = data.objects.get('A')
        keyframes = obj.animation_data.get_keyframes('location')
        assert len(keyframes) == 3

    def test_multi_object_scene(self):
        """Create scene with multiple objects and transforms."""
        results = dispatch_batch([
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'C1'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'S'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'plane', 'name': 'P'}},
            {'cmd': 'move_object', 'args': {
                'name': 'C1', 'location': (0, 0, 2)
            }},
            {'cmd': 'move_object', 'args': {
                'name': 'S', 'location': (5, 0, 0)
            }},
            {'cmd': 'scale_object', 'args': {
                'name': 'P', 'scale': (10, 10, 1)
            }},
        ])
        assert all(r.success for r in results)
        assert len(data.objects) == 3

    def test_object_lifecycle(self):
        """Spawn, modify, delete object lifecycle."""
        dispatch_batch([
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Temp'}},
            {'cmd': 'move_object', 'args': {
                'name': 'Temp', 'location': (1, 1, 1)
            }},
            {'cmd': 'delete_object', 'args': {'name': 'Temp'}},
        ])
        assert data.objects.get('Temp') is None
        assert len(data.objects) == 0

    def test_transform_sequence(self):
        """Apply multiple transforms to same object."""
        dispatch_batch([
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Tx'}},
            {'cmd': 'move_object', 'args': {'name': 'Tx', 'location': (1, 2, 3)}},
            {'cmd': 'rotate_object', 'args': {'name': 'Tx', 'rotation': (0, 0, 1.57)}},
            {'cmd': 'scale_object', 'args': {'name': 'Tx', 'scale': (2, 2, 2)}},
        ])
        obj = data.objects.get('Tx')
        assert obj.location == (1, 2, 3)
        assert obj.scale == (2, 2, 2)

    def test_rigging_hierarchy(self):
        """Create simple armature-like hierarchy."""
        dispatch_batch([
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Root'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Upper'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Lower'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Hand'}},
            {'cmd': 'parent_object', 'args': {
                'child': 'Upper', 'parent': 'Root'
            }},
            {'cmd': 'parent_object', 'args': {
                'child': 'Lower', 'parent': 'Upper'
            }},
            {'cmd': 'parent_object', 'args': {
                'child': 'Hand', 'parent': 'Lower'
            }},
        ])
        hand = data.objects.get('Hand')
        assert hand.parent.name == 'Lower'
        assert hand.parent.parent.name == 'Upper'
        assert hand.parent.parent.parent.name == 'Root'
