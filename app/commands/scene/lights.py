# File: app/commands/lights.py
# Lighting commands: create, energy, color, type. Foundation for procedural
# lighting setups in 3D animation scenes and cinematographic workflows.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.registry import register_command
from app.commands.result_helpers import ok, fail_not_found, fail_missing
from app.infra.bridge import data, ops, context, is_mock


@register_command('create_light')
def create_light(args: Dict[str, Any]):
    """Create a light object with optional color and energy."""
    name = args.get('name', 'Light')
    light_type = args.get('type', 'POINT').upper()
    location = tuple(args.get('location', (0, 0, 5)))
    color = args.get('color', (1.0, 1.0, 1.0))
    energy = float(args.get('energy', 1000.0))

    if is_mock():
        ops.light.add_light(light_type=light_type, location=location)
    else:
        # Real Blender: lights live under bpy.ops.object, not bpy.ops.light
        ops.object.light_add(type=light_type, location=location)

    obj = context.active_object
    if obj and name:
        obj.name = name
        if obj.data:
            obj.data.name = name
            # Set color (RGB only — Blender lights don't use alpha) and energy
            obj.data.color = tuple(color)[:3]
            obj.data.energy = energy

    return ok({'name': name, 'type': light_type, 'energy': energy}, 'create_light')


@register_command('set_light_energy')
def set_light_energy(args: Dict[str, Any]):
    """Set light intensity."""
    light_name = args.get('name')
    energy = args.get('energy', 1000.0)

    if not light_name:
        return fail_missing('name', 'set_light_energy')

    obj = data.objects.get(light_name)
    if not obj or not hasattr(obj.data, 'energy'):
        return fail_not_found(light_name, 'set_light_energy', 'Light')

    obj.data.energy = float(energy)
    return ok({'name': light_name, 'energy': energy}, 'set_light_energy')


@register_command('set_light_color')
def set_light_color(args: Dict[str, Any]):
    """Set light RGB color."""
    light_name = args.get('name')
    color = args.get('color', (1.0, 1.0, 1.0))

    if not light_name:
        return fail_missing('name', 'set_light_color')

    obj = data.objects.get(light_name)
    if not obj or not hasattr(obj.data, 'color'):
        return fail_not_found(light_name, 'set_light_color', 'Light')

    obj.data.color = tuple(color)
    return ok({'name': light_name, 'color': color}, 'set_light_color')


@register_command('set_light_type')
def set_light_type(args: Dict[str, Any]):
    """Change light type."""
    light_name = args.get('name')
    light_type = args.get('type', 'POINT')

    if not light_name:
        return fail_missing('name', 'set_light_type')

    obj = data.objects.get(light_name)
    if not obj or obj.type != 'LIGHT':
        return fail_not_found(light_name, 'set_light_type', 'Light')

    if hasattr(obj.data, 'type'):
        obj.data.type = light_type

    return ok({'name': light_name, 'type': light_type}, 'set_light_type')
