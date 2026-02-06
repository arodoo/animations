# File: app/commands/object_mgmt.py
# Object management commands: clone, rename, select, hide, show. Essential
# commands for scene organization and object manipulation workflows.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data, context


@register_command('clone_object')
def clone_object(args: Dict[str, Any]) -> DispatchResult:
    """Clone an object with optional new name."""
    src_name = args.get('name')
    new_name = args.get('new_name')

    if not src_name:
        return DispatchResult.fail("Missing 'name'", command='clone_object')

    src = data.objects.get(src_name)
    if not src:
        return DispatchResult.fail(f"Not found: {src_name}", command='clone_object')

    clone = data.objects.new(new_name or f"{src_name}_copy", src.data)
    clone.location = src.location
    clone.rotation_euler = src.rotation_euler
    clone.scale = src.scale

    return DispatchResult.ok({'name': clone.name}, command='clone_object')


@register_command('rename_object')
def rename_object(args: Dict[str, Any]) -> DispatchResult:
    """Rename an object."""
    old_name = args.get('name')
    new_name = args.get('new_name')

    if not old_name or not new_name:
        return DispatchResult.fail("Missing arguments", command='rename_object')

    obj = data.objects.get(old_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {old_name}", command='rename_object')

    del data.objects._objects[old_name]
    obj.name = new_name
    data.objects._objects[new_name] = obj

    return DispatchResult.ok({'old': old_name, 'new': new_name}, command='rename_object')


@register_command('select_object')
def select_object(args: Dict[str, Any]) -> DispatchResult:
    """Set object as active selection."""
    obj_name = args.get('name')

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='select_object')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='select_object')

    context.active_object = obj
    return DispatchResult.ok({'name': obj_name}, command='select_object')
