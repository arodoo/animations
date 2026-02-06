# File: app/commands/collections.py
# Collection commands: create, link, unlink. Essential for scene organization
# and batch operations on groups of objects in complex animations.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.registry import register_command
from app.commands.result_helpers import (
    ok, fail_not_found, fail_missing_args, fail_exists
)
from app.infra.bridge import data


class _SimpleCollection:
    """Minimal collection for object grouping."""
    def __init__(self, name: str):
        self.name = name
        self._objects: Dict[str, Any] = {}

    def link(self, obj: Any) -> None:
        self._objects[obj.name] = obj

    def unlink(self, obj: Any) -> None:
        self._objects.pop(obj.name, None)

    def __len__(self) -> int:
        return len(self._objects)

    def __bool__(self) -> bool:
        return True


@register_command('create_collection')
def create_collection(args: Dict[str, Any]):
    """Create a new collection."""
    name = args.get('name', 'Collection')

    if name in data.collections:
        return fail_exists(name, 'create_collection')

    data.collections[name] = _SimpleCollection(name)
    return ok({'name': name}, 'create_collection')


@register_command('link_to_collection')
def link_to_collection(args: Dict[str, Any]):
    """Link object to collection."""
    obj_name = args.get('object')
    coll_name = args.get('collection')

    if not obj_name or not coll_name:
        return fail_missing_args('link_to_collection')

    obj = data.objects.get(obj_name)
    if not obj:
        return fail_not_found(obj_name, 'link_to_collection')

    coll = data.collections.get(coll_name)
    if not coll:
        return fail_not_found(coll_name, 'link_to_collection', 'Collection')

    coll.link(obj)
    return ok({'object': obj_name, 'collection': coll_name}, 'link_to_collection')


@register_command('unlink_from_collection')
def unlink_from_collection(args: Dict[str, Any]):
    """Unlink object from collection."""
    obj_name = args.get('object')
    coll_name = args.get('collection')

    if not obj_name or not coll_name:
        return fail_missing_args('unlink_from_collection')

    obj = data.objects.get(obj_name)
    if not obj:
        return fail_not_found(obj_name, 'unlink_from_collection')

    coll = data.collections.get(coll_name)
    if not coll:
        return fail_not_found(coll_name, 'unlink_from_collection', 'Collection')

    coll.unlink(obj)
    return ok({'object': obj_name, 'collection': coll_name}, 'unlink_from_collection')
