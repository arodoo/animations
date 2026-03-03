# File: app/commands/scene/world_animation.py
# Continuous star rotation via shader driver. No keyframes.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import context, is_mock

_MAPPING_NAME = 'StarRotation'
_ROT_PER_FRAME = 0.003  # rad/frame, ~1 rev/70s at 30fps


@register_command('animate_space_world')
def animate_space_world(
    args: Dict[str, Any]
) -> DispatchResult:
    """
    Inserts a Mapping node into the star world shader
    with a frame-driven Z rotation. No keyframes: works
    for any animation duration without stopping.
    """
    if is_mock():
        return DispatchResult.ok(
            {}, command='animate_space_world',
        )

    world = context.scene.world
    if world is None or not world.use_nodes:
        return DispatchResult.ok(
            {'skipped': 'no_world'},
            command='animate_space_world',
        )

    nodes = world.node_tree.nodes
    links = world.node_tree.links

    if _MAPPING_NAME in [n.name for n in nodes]:
        return DispatchResult.ok(
            {'skipped': 'already_applied'},
            command='animate_space_world',
        )

    coord = next(
        (n for n in nodes if n.type == 'TEX_COORD'), None
    )
    voronoi = next(
        (n for n in nodes if n.type == 'TEX_VORONOI'), None
    )
    if not coord or not voronoi:
        return DispatchResult.ok(
            {'skipped': 'no_voronoi'},
            command='animate_space_world',
        )

    mapping = nodes.new('ShaderNodeMapping')
    mapping.name = _MAPPING_NAME
    for lnk in list(links):
        from_ok = lnk.from_node is coord
        to_ok = lnk.to_node is voronoi
        if from_ok and to_ok:
            links.remove(lnk)
    links.new(
        coord.outputs['Generated'],
        mapping.inputs['Vector'],
    )
    links.new(
        mapping.outputs['Vector'],
        voronoi.inputs['Vector'],
    )
    fcu = mapping.inputs['Rotation'].driver_add(
        'default_value', 2
    )
    fcu.driver.type = 'SCRIPTED'
    fcu.driver.expression = f'frame * {_ROT_PER_FRAME}'
    return DispatchResult.ok(
        {'rot_per_frame': _ROT_PER_FRAME},
        command='animate_space_world',
    )
