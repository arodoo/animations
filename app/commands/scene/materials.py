# File: app/commands/materials.py
# Material commands: create, assign, set color. Foundational commands for
# procedural material management and object appearance customization.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data, is_mock


@register_command('create_material')
def create_material(args: Dict[str, Any]) -> DispatchResult:
    """Create a new material with optional emission for glowing objects."""
    mat_name = args.get('name', 'Material')
    color = tuple(args.get('color', (0.8, 0.8, 0.8, 1.0)))
    emit = args.get('emit', False)
    emit_strength = float(args.get('emit_strength', 5.0))

    mat = data.materials.new(mat_name)
    mat.diffuse_color = color  # solid viewport color

    if not is_mock():
        # Configure node-based material so colors are visible in
        # Material Preview and Rendered modes.
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        if emit:
            shader = nodes.new('ShaderNodeEmission')
            shader.inputs['Color'].default_value = color
            shader.inputs['Strength'].default_value = emit_strength
        else:
            shader = nodes.new('ShaderNodeBsdfPrincipled')
            shader.inputs['Base Color'].default_value = color

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(shader.outputs[0], output.inputs['Surface'])

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

    if is_mock():
        obj.material_slots.append(mat)
    else:
        # In Blender, material_slots is read-only; append via the mesh data
        obj.data.materials.append(mat)

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
