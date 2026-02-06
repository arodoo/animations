# File: tests/e2e/test_hierarchy_commands.py
# E2E tests for hierarchy and parenting commands. Tests object relationships,
# parent/unparent operations, and complex multi-object scenarios.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import pytest
from app.infra.bridge import data, reset
from app.kernel.dispatcher import dispatch_single, dispatch_batch
import app.commands  # noqa: F401


@pytest.fixture(autouse=True)
def clean_state():
    reset()
    yield
    reset()


def create_objects(*names):
    """Helper to create multiple objects."""
    for name in names:
        dispatch_single({
            'cmd': 'spawn_primitive',
            'args': {'type': 'cube', 'name': name}
        })


class TestParentObject:
    """Tests for parent_object command."""

    def test_parent_child_relationship(self):
        """Parenting sets child.parent reference."""
        create_objects('Parent', 'Child')
        result = dispatch_single({
            'cmd': 'parent_object',
            'args': {'child': 'Child', 'parent': 'Parent'}
        })
        assert result.success
        child = data.objects.get('Child')
        assert child.parent is not None
        assert child.parent.name == 'Parent'

    def test_unparent_object(self):
        """Unparenting clears parent reference."""
        create_objects('Parent', 'Child')
        dispatch_single({
            'cmd': 'parent_object',
            'args': {'child': 'Child', 'parent': 'Parent'}
        })
        result = dispatch_single({
            'cmd': 'parent_object',
            'args': {'child': 'Child', 'parent': None}
        })
        assert result.success
        child = data.objects.get('Child')
        assert child.parent is None

    def test_parent_nonexistent_child_fails(self):
        """Parenting nonexistent child fails."""
        create_objects('Parent')
        result = dispatch_single({
            'cmd': 'parent_object',
            'args': {'child': 'Ghost', 'parent': 'Parent'}
        })
        assert not result.success

    def test_parent_to_nonexistent_parent_fails(self):
        """Parenting to nonexistent parent fails."""
        create_objects('Child')
        result = dispatch_single({
            'cmd': 'parent_object',
            'args': {'child': 'Child', 'parent': 'Ghost'}
        })
        assert not result.success

    def test_hierarchical_chain(self):
        """Create chain: GrandParent -> Parent -> Child."""
        create_objects('GrandParent', 'Parent', 'Child')
        dispatch_batch([
            {'cmd': 'parent_object', 'args': {
                'child': 'Parent', 'parent': 'GrandParent'
            }},
            {'cmd': 'parent_object', 'args': {
                'child': 'Child', 'parent': 'Parent'
            }},
        ])
        child = data.objects.get('Child')
        parent = data.objects.get('Parent')
        assert child.parent.name == 'Parent'
        assert parent.parent.name == 'GrandParent'
