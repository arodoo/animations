# File: tests/e2e/test_collections.py
# E2E tests for collection commands: create, link, unlink. Tests scene
# organization and object grouping for batch operations.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import pytest
from infra.bridge import data, reset
from app.dispatcher import dispatch_single, dispatch_batch
import app.commands  # noqa: F401


@pytest.fixture(autouse=True)
def clean_state():
    reset()
    yield
    reset()


def spawn(name: str):
    dispatch_single({'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': name}})


class TestCollections:
    def test_create_collection(self):
        result = dispatch_single({
            'cmd': 'create_collection', 'args': {'name': 'Props'}
        })
        assert result.success
        assert 'Props' in data.collections

    def test_link_to_collection(self):
        spawn('Chair')
        dispatch_single({'cmd': 'create_collection', 'args': {'name': 'Furniture'}})
        result = dispatch_single({
            'cmd': 'link_to_collection',
            'args': {'object': 'Chair', 'collection': 'Furniture'}
        })
        assert result.success
        coll = data.collections['Furniture']
        assert len(coll) == 1

    def test_unlink_from_collection(self):
        spawn('Box')
        dispatch_batch([
            {'cmd': 'create_collection', 'args': {'name': 'Items'}},
            {'cmd': 'link_to_collection', 'args': {
                'object': 'Box', 'collection': 'Items'
            }},
            {'cmd': 'unlink_from_collection', 'args': {
                'object': 'Box', 'collection': 'Items'
            }},
        ])
        assert len(data.collections['Items']) == 0

    def test_multiple_objects_in_collection(self):
        spawn('A')
        spawn('B')
        spawn('C')
        dispatch_batch([
            {'cmd': 'create_collection', 'args': {'name': 'Group'}},
            {'cmd': 'link_to_collection', 'args': {'object': 'A', 'collection': 'Group'}},
            {'cmd': 'link_to_collection', 'args': {'object': 'B', 'collection': 'Group'}},
            {'cmd': 'link_to_collection', 'args': {'object': 'C', 'collection': 'Group'}},
        ])
        assert len(data.collections['Group']) == 3

    def test_object_in_multiple_collections(self):
        spawn('Shared')
        dispatch_batch([
            {'cmd': 'create_collection', 'args': {'name': 'Set1'}},
            {'cmd': 'create_collection', 'args': {'name': 'Set2'}},
            {'cmd': 'link_to_collection', 'args': {
                'object': 'Shared', 'collection': 'Set1'
            }},
            {'cmd': 'link_to_collection', 'args': {
                'object': 'Shared', 'collection': 'Set2'
            }},
        ])
        assert len(data.collections['Set1']) == 1
        assert len(data.collections['Set2']) == 1
