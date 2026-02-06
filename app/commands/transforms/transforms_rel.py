# File: app/commands/transforms_rel.py
# Relative transform commands for delta-based movements. Essential for
# incremental animations and procedural positioning without absolutes.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data


@register_command('translate_relative')
def translate_relative(args: Dict[str, Any]) -> DispatchResult:
    """Move object by delta offset."""
    obj_name = args.get('name')
    delta = args.get('delta', (0, 0, 0))

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='translate_relative')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='translate_relative')

    obj.location.x += delta[0]
    obj.location.y += delta[1]
    obj.location.z += delta[2]

    frame = args.get('frame')
    if frame:
        obj.keyframe_insert('location', frame=int(frame))

    return DispatchResult.ok(
        {'name': obj_name, 'location': obj.location.to_tuple()},
        command='translate_relative'
    )


@register_command('rotate_relative')
def rotate_relative(args: Dict[str, Any]) -> DispatchResult:
    """Rotate object by delta angles."""
    obj_name = args.get('name')
    delta = args.get('delta', (0, 0, 0))

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='rotate_relative')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='rotate_relative')

    obj.rotation_euler.x += delta[0]
    obj.rotation_euler.y += delta[1]
    obj.rotation_euler.z += delta[2]

    frame = args.get('frame')
    if frame:
        obj.keyframe_insert('rotation_euler', frame=int(frame))

    return DispatchResult.ok(
        {'name': obj_name, 'rotation': obj.rotation_euler.to_tuple()},
        command='rotate_relative'
    )


@register_command('scale_relative')
def scale_relative(args: Dict[str, Any]) -> DispatchResult:
    """Scale object by delta factors."""
    obj_name = args.get('name')
    delta = args.get('delta', (1, 1, 1))

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='scale_relative')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='scale_relative')

    obj.scale.x *= delta[0]
    obj.scale.y *= delta[1]
    obj.scale.z *= delta[2]

    frame = args.get('frame')
    if frame:
        obj.keyframe_insert('scale', frame=int(frame))

    return DispatchResult.ok(
        {'name': obj_name, 'scale': obj.scale.to_tuple()},
        command='scale_relative'
    )
