# File: tests/e2e/test_modifiers.py
# E2E tests for modifier commands: add, remove, configure. Tests modifier
# lifecycle and property configuration for mesh deformations.
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


def spawn(name: str):
    dispatch_single({'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': name}})


class TestModifiers:
    def test_add_modifier(self):
        spawn('Cube')
        result = dispatch_single({
            'cmd': 'add_modifier',
            'args': {'object': 'Cube', 'type': 'SUBSURF', 'name': 'Subdiv'}
        })
        assert result.success
        assert len(data.objects.get('Cube').modifiers) == 1

    def test_modifier_has_properties(self):
        spawn('Cube')
        dispatch_single({
            'cmd': 'add_modifier',
            'args': {'object': 'Cube', 'type': 'SUBSURF'}
        })
        mod = data.objects.get('Cube').modifiers[0]
        assert mod.levels == 1  # default for SUBSURF

    def test_remove_modifier(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'add_modifier', 'args': {
                'object': 'Cube', 'type': 'SUBSURF', 'name': 'Sub'
            }},
            {'cmd': 'remove_modifier', 'args': {'object': 'Cube', 'name': 'Sub'}},
        ])
        assert len(data.objects.get('Cube').modifiers) == 0

    def test_configure_modifier(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'add_modifier', 'args': {
                'object': 'Cube', 'type': 'SUBSURF', 'name': 'Sub'
            }},
            {'cmd': 'configure_modifier', 'args': {
                'object': 'Cube', 'modifier': 'Sub', 'property': 'levels', 'value': 3
            }},
        ])
        mod = data.objects.get('Cube').modifiers[0]
        assert mod.levels == 3

    def test_add_multiple_modifiers(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'add_modifier', 'args': {'object': 'Cube', 'type': 'SUBSURF'}},
            {'cmd': 'add_modifier', 'args': {'object': 'Cube', 'type': 'MIRROR'}},
            {'cmd': 'add_modifier', 'args': {'object': 'Cube', 'type': 'BEVEL'}},
        ])
        assert len(data.objects.get('Cube').modifiers) == 3
