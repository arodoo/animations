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
    emit = bool(args.get('emit', False))
    emit_strength = float(args.get('emit_strength', 5.0))
    use_noise = bool(args.get('use_noise_texture', False))
    roughness = float(args.get('roughness', 0.4))
    normal_strength = float(args.get('normal_strength', 0.0))

    mat = data.materials.new(mat_name)
    mat.diffuse_color = color  # solid viewport color

    if not is_mock():
        # Node-based PBR material using Principled BSDF
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        principled = nodes.new('ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = color
        principled.inputs['Roughness'].default_value = roughness

        final_shader_output = principled.outputs['BSDF']

        # Optional emission mix for glowing rings/particles
        if emit:
            emit_node = nodes.new('ShaderNodeEmission')
            emit_node.inputs['Color'].default_value = color
            emit_node.inputs['Strength'].default_value = emit_strength
            mix_shader = nodes.new('ShaderNodeMixShader')
            # Fac = 1.0: full emission output (no BSDF bleed)
            mix_shader.inputs['Fac'].default_value = 1.0
            links.new(emit_node.outputs['Emission'], mix_shader.inputs[1])
            links.new(principled.outputs['BSDF'], mix_shader.inputs[2])
            final_shader_output = mix_shader.outputs[0]
            # Disable back-face culling so emission is visible from ALL
            # camera angles — critical for JetSouth whose normals face -Z
            # and would be invisible when camera is in the +Z hemisphere.
            try:
                mat.use_backface_culling = False
            except AttributeError:
                pass  # Older Blender builds — safe to ignore


        # Optional normal/bump generated from a noise texture for subtle detail
        if use_noise and normal_strength > 0.0:
            noise = nodes.new('ShaderNodeTexNoise')
            noise.inputs['Scale'].default_value = 6.0
            bump = nodes.new('ShaderNodeBump')
            bump.inputs['Strength'].default_value = normal_strength
            links.new(noise.outputs['Fac'], bump.inputs['Height'])
            links.new(bump.outputs['Normal'], principled.inputs['Normal'])

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(final_shader_output, output.inputs['Surface'])

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
        # Replace slot 0 if it exists (avoids default grey material blocking
        # our custom emission shader), otherwise append.
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
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
