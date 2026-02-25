# File: scenes/solar_system/commands/_metal.py
# A local command to generate high-quality metallic materials without modifying
# the core application's material builders.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data, is_mock


@register_command('create_metal_material')
def create_metal_material(args: Dict[str, Any]) -> DispatchResult:
    """Create a fully customizable Metallic PBR material.

    Args:
        name (str): Material name
        color (tuple): Base color (RGBA)
        roughness (float): Default 0.2
        metallic (float): Default 1.0
        emit_strength (float): Optional, defaults 0.0
    """
    mat_name = args.get('name', 'MetalMat')
    color = tuple(args.get('color', (0.8, 0.8, 0.8, 1.0)))
    roughness = float(args.get('roughness', 0.2))
    metallic = float(args.get('metallic', 1.0))
    emit_strength = float(args.get('emit_strength', 0.0))

    mat = data.materials.new(mat_name)
    mat.diffuse_color = color

    if not is_mock():
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        principled = nodes.new('ShaderNodeBsdfPrincipled')
        principled.inputs['Base Color'].default_value = color
        principled.inputs['Roughness'].default_value = roughness
        principled.inputs['Metallic'].default_value = metallic

        final_shader = principled.outputs['BSDF']

        if emit_strength > 0.0:
            emit_node = nodes.new('ShaderNodeEmission')
            emit_node.inputs['Color'].default_value = color
            emit_node.inputs['Strength'].default_value = emit_strength
            mix_shader = nodes.new('ShaderNodeMixShader')
            mix_shader.inputs['Fac'].default_value = 0.5
            links.new(emit_node.outputs['Emission'], mix_shader.inputs[1])
            links.new(principled.outputs['BSDF'], mix_shader.inputs[2])
            final_shader = mix_shader.outputs[0]

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(final_shader, output.inputs['Surface'])

    return DispatchResult.ok({'name': mat.name}, command='create_metal_material')
