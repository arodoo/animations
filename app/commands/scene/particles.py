# File: app/commands/scene/particles.py
# Particle system command for emission effects (disk, jets).
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data, context, ops, is_mock


@register_command('add_particle_system')
def add_particle_system(args: Dict[str, Any]) -> DispatchResult:
    """
    Add and configure an emitter particle system on an object.

    Args:
        object:         Target object name
        name:           Particle system name
        count:          Number of particles (default 1000)
        lifetime:       Particle lifetime in frames (default 60)
        emit_from:      'FACE' | 'VOLUME' | 'VERT' (default 'FACE')
        normal_factor:  Speed along surface normal (default 0.0)
        tangent_factor: Speed along tangent/circular (default 0.5)
        gravity:        Gravity scale 0–1 (default 0, space)
        size:           Halo render size (default 0.05)
        render_type:    'HALO' | 'OBJECT' (default 'HALO')
    """
    if is_mock():
        return DispatchResult.ok({}, command='add_particle_system')

    obj_name = args.get('object')
    if not obj_name:
        return DispatchResult.fail(
            "Missing 'object'", command='add_particle_system'
        )

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Not found: {obj_name}", command='add_particle_system'
        )

    context.view_layer.objects.active = obj
    ops.object.particle_system_add()

    ps = obj.particle_systems[-1]
    ps.name = args.get('name', 'ParticleSystem')
    s = ps.settings
    s.count = int(args.get('count', 1000))
    s.lifetime = float(args.get('lifetime', 60))
    s.emit_from = args.get('emit_from', 'FACE')
    s.normal_factor = float(args.get('normal_factor', 0.0))
    s.tangent_factor = float(args.get('tangent_factor', 0.5))
    s.effector_weights.gravity = float(args.get('gravity', 0.0))
    s.particle_size = float(args.get('size', 0.05))
    s.render_type = args.get('render_type', 'HALO')

    return DispatchResult.ok(
        {'object': obj_name, 'system': ps.name},
        command='add_particle_system',
    )
