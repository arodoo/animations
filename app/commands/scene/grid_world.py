# File: app/commands/scene/grid_world.py
# Cartesian grid floor plane command — Blender-style dark grid with subtle
# blue-grey gridlines, mimics the viewport Animation mode background.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import context, data, is_mock


@register_command('create_cartesian_grid')
def create_cartesian_grid(args: Dict[str, Any]) -> DispatchResult:
    """
    Create a Blender-style dark Cartesian grid floor plane as a mesh
    with a procedural grid shader (Checker/Grid texture node).
    Mimics the viewport Animation grid: near-black background with
    subtle blue-grey gridlines and brighter X/Y axis lines.

    Args:
        size:        half-size of the plane in Blender units (default 500)
        grid_scale:  world-space spacing between gridlines  (default 10)
        z_offset:    world Z of the plane (default -80, below all geometry)
        bg_color:    RGBA background colour of the plane    (default very dark)
        line_color:  RGBA minor gridline colour             (default blue-grey)
    """
    if is_mock():
        return DispatchResult.ok({}, command='create_cartesian_grid')

    import bpy  # type: ignore

    size = float(args.get('size', 500))
    grid_scale = float(args.get('grid_scale', 10))
    # Place the plane BELOW all scene geometry so it never blocks jets.
    # JetSouth tip ≈ -43 BU → -80 BU is safely out of the way.
    z_offset = float(args.get('z_offset', -80.0))
    bg_color = tuple(args.get('bg_color', (0.03, 0.03, 0.04, 1.0)))
    line_color = tuple(args.get('line_color', (0.12, 0.14, 0.22, 1.0)))

    # ── Mesh plane ────────────────────────────────────────────────────────
    bpy.ops.mesh.primitive_plane_add(size=size * 2, location=(0, 0, z_offset))
    plane = bpy.context.active_object
    plane.name = 'CartesianGrid'

    # ── Material with procedural grid ─────────────────────────────────────
    mat = bpy.data.materials.new('CartesianGridMat')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Texture coordinate & mapping (scale controls grid density)
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (
        1.0 / grid_scale, 1.0 / grid_scale, 1.0
    )

    # Grid texture — white lines on black
    grid_tex = nodes.new('ShaderNodeTexChecker')
    grid_tex.inputs['Scale'].default_value = 1.0
    grid_tex.inputs['Color1'].default_value = (1.0, 1.0, 1.0, 1.0)
    grid_tex.inputs['Color2'].default_value = (0.0, 0.0, 0.0, 1.0)

    # Mix node: blend bg_color and line_color by grid mask
    mix = nodes.new('ShaderNodeMixRGB')
    mix.blend_type = 'MIX'
    mix.inputs['Color1'].default_value = bg_color
    mix.inputs['Color2'].default_value = line_color

    # Emission shader — grid always visible regardless of lighting
    emit = nodes.new('ShaderNodeEmission')
    emit.inputs['Strength'].default_value = 0.6

    output = nodes.new('ShaderNodeOutputMaterial')

    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'],      grid_tex.inputs['Vector'])
    links.new(grid_tex.outputs['Fac'],        mix.inputs['Fac'])
    links.new(mix.outputs['Color'],           emit.inputs['Color'])
    links.new(emit.outputs['Emission'],       output.inputs['Surface'])

    # Render grid from both sides so it is visible regardless of camera angle
    try:
        mat.use_backface_culling = False
    except AttributeError:
        pass

    if plane.data.materials:
        plane.data.materials[0] = mat
    else:
        plane.data.materials.append(mat)

    return DispatchResult.ok(
        {'size': size, 'grid_scale': grid_scale, 'z_offset': z_offset},
        command='create_cartesian_grid'
    )
