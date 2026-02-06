# File: app/commands/visibility.py
# Visibility commands: hide, show, set render visibility. Controls object
# visibility in viewport and render for complex scene management.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data


@register_command('hide_object')
def hide_object(args: Dict[str, Any]) -> DispatchResult:
    """Hide object from viewport."""
    obj_name = args.get('name')

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='hide_object')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='hide_object')

    obj.hide_viewport = True
    return DispatchResult.ok({'name': obj_name, 'hidden': True}, command='hide_object')


@register_command('show_object')
def show_object(args: Dict[str, Any]) -> DispatchResult:
    """Show object in viewport."""
    obj_name = args.get('name')

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='show_object')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='show_object')

    obj.hide_viewport = False
    return DispatchResult.ok({'name': obj_name, 'hidden': False}, command='show_object')


@register_command('set_render_visibility')
def set_render_visibility(args: Dict[str, Any]) -> DispatchResult:
    """Set object render visibility."""
    obj_name = args.get('name')
    visible = args.get('visible', True)

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='set_render_visibility')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='set_render_visibility')

    obj.hide_render = not visible
    return DispatchResult.ok({'name': obj_name, 'render': visible}, command='set_render_visibility')


@register_command('set_object_color')
def set_object_color(args: Dict[str, Any]) -> DispatchResult:
    """Set object viewport display color."""
    obj_name = args.get('name')
    color = args.get('color', (1.0, 1.0, 1.0, 1.0))

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='set_object_color')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='set_object_color')

    obj.color = tuple(color)
    return DispatchResult.ok({'name': obj_name, 'color': color}, command='set_object_color')
