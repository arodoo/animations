# File: app/commands/scene/material_anim.py
# Material animation: keyframe emission node strength for hot spots.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data, is_mock


@register_command('keyframe_material_emission')
def keyframe_material_emission(
    args: Dict[str, Any],
) -> DispatchResult:
    """
    Set and keyframe an Emission node's Strength on a material.

    Args:
        material: Material name (must have use_nodes=True)
        strength: Emission strength value to set
        frame:    Timeline frame to insert the keyframe at
    """
    if is_mock():
        return DispatchResult.ok(
            {}, command='keyframe_material_emission'
        )

    mat_name = args.get('material')
    strength = float(args.get('strength', 5.0))
    frame = int(args.get('frame', 1))

    if not mat_name:
        return DispatchResult.fail(
            "Missing 'material'",
            command='keyframe_material_emission',
        )

    mat = data.materials.get(mat_name)
    if not mat or not mat.use_nodes:
        return DispatchResult.fail(
            f"Not found or no nodes: {mat_name}",
            command='keyframe_material_emission',
        )

    for node in mat.node_tree.nodes:
        if node.type == 'EMISSION':
            inp = node.inputs.get('Strength')
            if inp:
                inp.default_value = strength
                inp.keyframe_insert(
                    'default_value', frame=frame
                )
            break

    return DispatchResult.ok(
        {'material': mat_name, 'frame': frame},
        command='keyframe_material_emission',
    )
