# File: app/commands/scene/world_settings.py
# New commands for controlling the world environment, such as background color.
# Essential for setting the overall mood and atmosphere of a scene.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import context, data, is_mock

@register_command('set_world_background')
def set_world_background(args: Dict[str, Any]) -> DispatchResult:
    """Sets the world background color."""
    color = args.get('color', (0.05, 0.05, 0.05))

    if is_mock():
        if not hasattr(context.scene, '_world_mock'):
            context.scene._world_mock = {}
        context.scene._world_mock['color'] = tuple(color)
    else:
        # Real Blender: configure the world node tree
        world = context.scene.world
        if world is None:
            world = data.worlds.new("World")
            context.scene.world = world
        world.use_nodes = True
        bg_node = world.node_tree.nodes.get("Background")
        if bg_node:
            r, g, b = color[0], color[1], color[2]
            bg_node.inputs[0].default_value = (r, g, b, 1.0)
            bg_node.inputs[1].default_value = 1.0  # strength

    return DispatchResult.ok(
        {'background_color': color},
        command='set_world_background'
    )


@register_command('create_space_world')
def create_space_world(args: Dict[str, Any]) -> DispatchResult:
    """
    Build a space world shader: pure black background + procedural Voronoi
    starfield. No individual star objects — the stars live in the world node
    tree (zero scene-object overhead, infinite resolution).

    Args:
        star_density:    Voronoi scale → higher = more stars (default 350)
        star_brightness: Emission strength of visible stars (default 2.5)
    """
    if is_mock():
        return DispatchResult.ok({}, command='create_space_world')

    star_density = float(args.get('star_density', 350))
    star_brightness = float(args.get('star_brightness', 2.5))

    world = context.scene.world
    if world is None:
        world = data.worlds.new("World")
        context.scene.world = world

    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    # ── Texture coordinate (Generated = direction in world space) ──────────
    coord = nodes.new('ShaderNodeTexCoord')

    # ── Voronoi: each cell's nearest-feature-distance becomes a potential star
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.voronoi_dimensions = '3D'
    voronoi.feature = 'F1'
    voronoi.inputs['Scale'].default_value = star_density
    voronoi.inputs['Randomness'].default_value = 1.0

    # ── Invert distance: 0 at star → 1; 1 away from star → 0 ──────────────
    invert = nodes.new('ShaderNodeMath')
    invert.operation = 'SUBTRACT'
    invert.use_clamp = True
    invert.inputs[0].default_value = 1.0            # 1 - distance

    # ── Power: sharpens the dot so only the very centre is bright ──────────
    sharp = nodes.new('ShaderNodeMath')
    sharp.operation = 'POWER'
    sharp.use_clamp = True
    sharp.inputs[1].default_value = 30.0

    # ── Multiply by brightness for the emission strength ───────────────────
    brightness = nodes.new('ShaderNodeMath')
    brightness.operation = 'MULTIPLY'
    brightness.inputs[1].default_value = star_brightness

    # ── Black background shader (strength 0 = no world light leaks) ────────
    black_bg = nodes.new('ShaderNodeBackground')
    black_bg.inputs['Color'].default_value = (0.0, 0.0, 0.0, 1.0)
    black_bg.inputs['Strength'].default_value = 0.0

    # ── Star emission: cool-white points ───────────────────────────────────
    star_emit = nodes.new('ShaderNodeEmission')
    star_emit.inputs['Color'].default_value = (0.9, 0.95, 1.0, 1.0)

    # ── Mix: black everywhere, star emission at Voronoi feature centres ────
    mix = nodes.new('ShaderNodeMixShader')

    # ── World output ───────────────────────────────────────────────────────
    output = nodes.new('ShaderNodeOutputWorld')

    # ── Wire ──────────────────────────────────────────────────────────────
    links.new(coord.outputs['Generated'],    voronoi.inputs['Vector'])
    links.new(voronoi.outputs['Distance'],   invert.inputs[1])
    links.new(invert.outputs['Value'],       sharp.inputs[0])
    links.new(sharp.outputs['Value'],        brightness.inputs[0])
    links.new(sharp.outputs['Value'],        mix.inputs['Fac'])
    links.new(brightness.outputs['Value'],   star_emit.inputs['Strength'])
    links.new(black_bg.outputs['Background'], mix.inputs[1])
    links.new(star_emit.outputs['Emission'], mix.inputs[2])
    links.new(mix.outputs['Shader'],         output.inputs['Surface'])

    return DispatchResult.ok(
        {'star_density': star_density, 'star_brightness': star_brightness},
        command='create_space_world'
    )


@register_command('configure_eevee')
def configure_eevee(args: Dict[str, Any]) -> DispatchResult:
    """
    Set up Eevee as the render engine with bloom and performance settings.
    Bloom makes emissive materials glow visually. Safe to call even on
    Blender 4.x (Eevee Next), where unsupported properties are skipped.
    """
    if is_mock():
        return DispatchResult.ok({}, command='configure_eevee')

    scene = context.scene
    width = int(args.get('width', 1280))
    height = int(args.get('height', 720))
    samples = int(args.get('samples', 16))

    # Try Eevee Next (Blender 4.x) first, fall back to legacy Eevee (3.x)
    try:
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
    except Exception:
        scene.render.engine = 'BLENDER_EEVEE'

    scene.render.resolution_x = width
    scene.render.resolution_y = height

    eevee = scene.eevee

    # Bloom — Blender 3.x Eevee property; Eevee Next uses the compositor
    try:
        eevee.use_bloom = True
        eevee.bloom_threshold = 0.5
        eevee.bloom_intensity = 1.2
        eevee.bloom_radius = 6.5
        eevee.bloom_color = (1.0, 1.0, 1.0)
    except AttributeError:
        pass  # Eevee Next — bloom is handled via compositor; skip silently

    # Sample counts for performance
    try:
        eevee.taa_render_samples = samples
        eevee.taa_samples = max(4, samples // 2)  # viewport samples
    except AttributeError:
        pass

    # Ambient occlusion adds depth to close geometry
    try:
        eevee.use_gtao = True
        eevee.gtao_distance = 0.5
    except AttributeError:
        pass

    return DispatchResult.ok(
        {'engine': 'eevee', 'width': width, 'height': height, 'samples': samples},
        command='configure_eevee'
    )
