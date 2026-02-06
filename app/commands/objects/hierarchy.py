# File: app/commands/objects/hierarchy.py
# Hierarchy commands: delete object and parent/unparent relationships.
# Essential for scene cleanup and object groupings in animations.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data, context


@register_command('delete_object')
def delete_object(args: Dict[str, Any]) -> DispatchResult:
    """Delete an object from the scene."""
    obj_name = args.get('name')

    if not obj_name:
        return DispatchResult.fail(
            "Missing 'name' argument",
            command='delete_object'
        )

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Object not found: {obj_name}",
            command='delete_object'
        )

    data.objects.remove(obj)
    if obj in context.view_layer.objects:
        context.view_layer.objects.remove(obj)

    return DispatchResult.ok(
        data={'name': obj_name},
        command='delete_object'
    )


@register_command('parent_object')
def parent_object(args: Dict[str, Any]) -> DispatchResult:
    """Set parent-child relationship between objects."""
    child_name = args.get('child')
    parent_name = args.get('parent')

    if not child_name:
        return DispatchResult.fail(
            "Missing 'child' argument",
            command='parent_object'
        )

    child = data.objects.get(child_name)
    if not child:
        return DispatchResult.fail(
            f"Child not found: {child_name}",
            command='parent_object'
        )

    if parent_name is None:
        child.parent = None
        return DispatchResult.ok(
            data={'child': child_name, 'parent': None},
            command='parent_object'
        )

    parent = data.objects.get(parent_name)
    if not parent:
        return DispatchResult.fail(
            f"Parent not found: {parent_name}",
            command='parent_object'
        )

    child.parent = parent

    return DispatchResult.ok(
        data={'child': child_name, 'parent': parent_name},
        command='parent_object'
    )
