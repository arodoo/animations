# Command Reference -- Advanced

Commands for modifiers, collections, and rigid body physics.

---

## add_modifier

Add a modifier to an object.

```python
{'cmd': 'add_modifier', 'args': {
    'object': 'ObjectName',
    'type':   'SUBSURF|MIRROR|ARRAY|BEVEL',
    'name':   'ModifierName',  # optional
}}
```

| Type | Defaults |
|------|----------|
| `SUBSURF` | levels=1, render_levels=2 |
| `MIRROR` | use_axis=(True, False, False) |
| `ARRAY` | count=2 |
| `BEVEL` | width=0.1, segments=1 |

---

## remove_modifier

Remove a named modifier from an object.

```python
{'cmd': 'remove_modifier', 'args': {
    'object': 'ObjectName',
    'name':   'ModifierName',
}}
```

---

## configure_modifier

Set a property on an existing modifier.

```python
{'cmd': 'configure_modifier', 'args': {
    'object':   'ObjectName',
    'modifier': 'ModifierName',
    'property': 'levels',
    'value':    3,
}}
```

---

## add_rigid_body

Add rigid body physics to an object. Requires Blender's rigid body
world (created automatically). Skipped silently in mock mode.

```python
{'cmd': 'add_rigid_body', 'args': {
    'object':      'ObjectName',
    'type':        'ACTIVE',   # or 'PASSIVE'
    'mass':        1.0,        # kg, default 1.0
    'friction':    0.5,        # default 0.5
    'restitution': 0.0,        # bounciness, default 0.0
    'kinematic':   False,      # default False
    'collision':   'CONVEX_HULL',
}}
```

| Type | Behaviour |
|------|-----------|
| `ACTIVE` | Simulated by physics engine (falls, collides) |
| `PASSIVE` | Stationary collider (ground, walls) |

| Collision shape | Use case |
|-----------------|----------|
| `CONVEX_HULL` | General purpose, fast |
| `MESH` | Exact shape, slow |
| `BOX` | Fastest, axis-aligned box |

> Set `kinematic=True` for objects that are animated (keyframed)
> but still participate in collisions. Blender bakes kinematic
> motion into the rigid body simulation.

---

## add_to_collection

Group objects into named collections.

```python
{'cmd': 'add_to_collection', 'args': {
    'object':     'ObjectName',
    'collection': 'CollectionName',
}}
```

> Collections are created automatically if they do not exist.
