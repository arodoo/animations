# File: app/commands/modifiers.py
# Modifier commands: add, remove, configure. Essential for procedural mesh
# deformations like subdivision, mirror, and array modifiers.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.registry import register_command
from app.commands.result_helpers import (
    ok, fail_not_found, fail_missing, fail_missing_args
)
from infra.bridge import data


class _SimpleModifier:
    """Simple modifier with name, type, and properties dict."""
    DEFAULTS = {
        'SUBSURF': {'levels': 1, 'render_levels': 2},
        'MIRROR': {'use_axis': (True, False, False)},
        'ARRAY': {'count': 2},
        'BEVEL': {'width': 0.1, 'segments': 1},
    }

    def __init__(self, name: str, mod_type: str):
        self.name = name
        self.type = mod_type
        self._props = dict(self.DEFAULTS.get(mod_type, {}))

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        return self._props.get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ('name', 'type', '_props'):
            super().__setattr__(name, value)
        else:
            self._props[name] = value


@register_command('add_modifier')
def add_modifier(args: Dict[str, Any]):
    """Add a modifier to object."""
    obj_name = args.get('object')
    mod_type = args.get('type', 'SUBSURF')
    mod_name = args.get('name', mod_type.capitalize())

    if not obj_name:
        return fail_missing('object', 'add_modifier')

    obj = data.objects.get(obj_name)
    if not obj:
        return fail_not_found(obj_name, 'add_modifier')

    modifier = _SimpleModifier(mod_name, mod_type)
    obj.modifiers.append(modifier)

    return ok(
        {'object': obj_name, 'modifier': mod_name, 'type': mod_type},
        'add_modifier'
    )


@register_command('remove_modifier')
def remove_modifier(args: Dict[str, Any]):
    """Remove modifier from object."""
    obj_name = args.get('object')
    mod_name = args.get('name')

    if not obj_name or not mod_name:
        return fail_missing_args('remove_modifier')

    obj = data.objects.get(obj_name)
    if not obj:
        return fail_not_found(obj_name, 'remove_modifier')

    for i, mod in enumerate(obj.modifiers):
        if mod.name == mod_name:
            obj.modifiers.pop(i)
            return ok({'object': obj_name, 'removed': mod_name}, 'remove_modifier')

    return fail_not_found(mod_name, 'remove_modifier', 'Modifier')


@register_command('configure_modifier')
def configure_modifier(args: Dict[str, Any]):
    """Configure modifier property."""
    obj_name = args.get('object')
    mod_name = args.get('modifier')
    prop_name = args.get('property')
    prop_value = args.get('value')

    if not all([obj_name, mod_name, prop_name]):
        return fail_missing_args('configure_modifier')

    obj = data.objects.get(obj_name)
    if not obj:
        return fail_not_found(obj_name, 'configure_modifier')

    for mod in obj.modifiers:
        if mod.name == mod_name:
            setattr(mod, prop_name, prop_value)
            return ok({'modifier': mod_name, 'property': prop_name}, 'configure_modifier')

    return fail_not_found(mod_name, 'configure_modifier', 'Modifier')
