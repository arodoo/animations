# File: app/commands/transform_utils.py
# Transform utility commands: reset, apply, set origin. Advanced transform
# operations for cleanup and preparation of objects in animation pipelines.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from domain.dispatch_result import DispatchResult
from app.registry import register_command
from infra.bridge import data


@register_command('reset_transform')
def reset_transform(args: Dict[str, Any]) -> DispatchResult:
    """Reset object transform to identity."""
    obj_name = args.get('name')
    reset_loc = args.get('location', True)
    reset_rot = args.get('rotation', True)
    reset_scale = args.get('scale', True)

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='reset_transform')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='reset_transform')

    if reset_loc:
        obj.location = (0, 0, 0)
    if reset_rot:
        obj.rotation_euler = (0, 0, 0)
    if reset_scale:
        obj.scale = (1, 1, 1)

    return DispatchResult.ok({'name': obj_name, 'reset': True}, command='reset_transform')


@register_command('apply_transform')
def apply_transform(args: Dict[str, Any]) -> DispatchResult:
    """Apply object transform (bake to mesh)."""
    obj_name = args.get('name')

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='apply_transform')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='apply_transform')

    # In mock, we just reset values (real Blender transforms mesh data)
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)

    return DispatchResult.ok({'name': obj_name, 'applied': True}, command='apply_transform')


@register_command('set_origin')
def set_origin(args: Dict[str, Any]) -> DispatchResult:
    """Set object origin point."""
    obj_name = args.get('name')
    origin_type = args.get('type', 'CENTER')  # CENTER, CURSOR, GEOMETRY

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='set_origin')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='set_origin')

    # Mock implementation - just store the origin type
    return DispatchResult.ok(
        {'name': obj_name, 'origin': origin_type},
        command='set_origin'
    )
