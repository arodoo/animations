# Command Reference — Animation

Keyframe insertion, deletion, and timeline control.

---

## set_keyframe

Insert keyframes for location, rotation, and scale at a given frame.

```python
{'cmd': 'set_keyframe', 'args': {
    'name':  'ObjectName',
    'frame': 1,
}}
```

---

## delete_keyframe

Remove a specific keyframe for one property.

```python
{'cmd': 'delete_keyframe', 'args': {
    'name':     'ObjectName',
    'property': 'location|rotation_euler|scale',
    'frame':    10,
}}
```

---

## clear_animation

Remove all keyframes from an object, or all keyframes for one property.

```python
{'cmd': 'clear_animation', 'args': {
    'name':     'ObjectName',
    'property': 'location',   # optional — omit to clear everything
}}
```

---

## set_current_frame

Move the timeline scrubber to a specific frame.

```python
{'cmd': 'set_current_frame', 'args': {'frame': 42}}
```

---

## set_frame_range

Set the animation start and end frames.

```python
{'cmd': 'set_frame_range', 'args': {
    'start': 1,
    'end':   900,
}}
```

---

## Keyframe Tips

**Insert position + rotation in one step:**

```python
batch = [
    {'cmd': 'move_object',   'args': {'name': 'Obj', 'location': (1,0,0), 'frame': 1}},
    {'cmd': 'rotate_object', 'args': {'name': 'Obj', 'rotation': (0,0,0), 'frame': 1}},
    {'cmd': 'move_object',   'args': {'name': 'Obj', 'location': (5,0,0), 'frame': 90}},
]
```

**Keplerian orbit example (differential rotation):**

```python
import math

R_REF = 3.0
def keplerian(r): return (R_REF / r) ** 1.5

for f in range(1, total_frames + 1, step):
    t = (f - 1) / (total_frames - 1)
    angle = t * 2 * math.pi * rotations * keplerian(radius)
    batch.append({'cmd': 'rotate_object', 'args': {
        'name': ring_name, 'rotation': (0, 0, angle), 'frame': f,
    }})
```
