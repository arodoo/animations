# File: app/commands/objects/spawn_text.py
# Command to spawn 3D text objects and modify their geometry.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import ops, data, context


@register_command('spawn_text')
def spawn_text(args: Dict[str, Any]) -> DispatchResult:
    """Spawn a 3D text object.
    
    Args:
        text (str): The string content to render.
        name (str): The object name.
        location (tuple): X,Y,Z placement.
        extrude (float): 3D thickness (depth).
        align_x (str): Horizontal alignment ('LEFT', 'CENTER', 'RIGHT').
        align_y (str): Vertical alignment ('TOP', 'CENTER', 'BOTTOM').
        scale (list): X,Y,Z scale multiplier.
        rotation (list): X,Y,Z rotation (radians).
    """
    text_content = str(args.get('text', 'Tex'))
    name = args.get('name', 'TextGen')
    location = tuple(args.get('location', (0, 0, 0)))
    scale = tuple(args.get('scale', (1.0, 1.0, 1.0)))
    rotation = tuple(args.get('rotation', (0.0, 0.0, 0.0)))
    
    # Text-specific parameters
    extrude = args.get('extrude', 0.05)
    align_x = args.get('align_x', 'CENTER')
    align_y = args.get('align_y', 'CENTER')

    # Record object names before creating so we can identify the new text
    def _object_names():
        try:
            return set(data.objects.keys())
        except Exception:
            return set()

    prev_names = _object_names()

    try:
        ops.object.text_add(
            location=location,
            rotation=rotation,
            scale=scale,
            enter_editmode=False
        )
    except Exception as e:
        return DispatchResult.fail(str(e), command='spawn_text')

    # Identify created object
    created_obj = None
    try:
        new_names = _object_names()
        created_names = new_names - prev_names
        if created_names:
            created_name = next(iter(created_names))
            created_obj = data.objects.get(created_name)
    except Exception:
        pass

    if created_obj is None:
        created_obj = getattr(context, 'active_object', None)

    if created_obj and getattr(created_obj, 'type', '') == 'FONT':
        try:
            # Set the actual text string
            created_obj.data.body = text_content
            
            # Setup 3D thickness
            created_obj.data.extrude = extrude
            
            # Alignment configuration
            if align_x in ['LEFT', 'CENTER', 'RIGHT', 'JUSTIFY', 'FLUSH']:
                created_obj.data.align_x = align_x
            if align_y in ['TOP', 'TOP_BASELINE', 'CENTER', 'BOTTOM', 'BOTTOM_BASELINE']:
                created_obj.data.align_y = align_y
            
            # Try to name it
            created_obj.name = name
            created_obj.data.name = f"{name}_FontData"
            
        except Exception as e:
            return DispatchResult.fail(f"Failed configuring text properties: {str(e)}", command='spawn_text')

    return DispatchResult.ok(
        data={'text': text_content, 'location': location, 'name': name},
        command='spawn_text'
    )
