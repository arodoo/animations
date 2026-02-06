# File: app/commands/materials.py
# Material commands: create, assign, set color. Foundational commands for
# procedural material management and object appearance customization.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data


@register_command('create_material')
def create_material(args: Dict[str, Any]) -> DispatchResult:
    """Create a new material."""
    mat_name = args.get('name', 'Material')
    color = args.get('color', (0.8, 0.8, 0.8, 1.0))

    mat = data.materials.new(mat_name)
    mat.diffuse_color = tuple(color)

    return DispatchResult.ok({'name': mat.name}, command='create_material')


@register_command('assign_material')
def assign_material(args: Dict[str, Any]) -> DispatchResult:
    """Assign material to object."""
    obj_name = args.get('object')
    mat_name = args.get('material')

    if not obj_name or not mat_name:
        return DispatchResult.fail(
            "Missing arguments", command='assign_material')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Not found: {obj_name}", command='assign_material')

    mat = data.materials.get(mat_name)
    if not mat:
        return DispatchResult.fail(
            f"Mat not found: {mat_name}", command='assign_material')

    obj.material_slots.append(mat)
    return DispatchResult.ok(
        {'object': obj_name, 'material': mat_name},
        command='assign_material'
    )


@register_command('set_material_color')
def set_material_color(args: Dict[str, Any]) -> DispatchResult:
    """Set material base color."""
    mat_name = args.get('name')
    color = args.get('color', (0.8, 0.8, 0.8, 1.0))

    if not mat_name:
        return DispatchResult.fail(
            "Missing 'name'", command='set_material_color')

    mat = data.materials.get(mat_name)
    if not mat:
        return DispatchResult.fail(
            f"Not found: {mat_name}", command='set_material_color')

    mat.diffuse_color = tuple(color)
    result_data = {'name': mat_name, 'color': color}
    return DispatchResult.ok(result_data, command='set_material_color')
