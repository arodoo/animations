import types
import builtins
from unittest.mock import MagicMock, patch

from app.commands.objects import spawn_primitive
from scenes.quasar_bh.animations import _bh_jets, _physics


def test_spawn_primitive_forwards_kwargs_and_applies_smooth(monkeypatch):
    calls = {}

    # Create fake ops entry that records kwargs
    fake_op = MagicMock()

    monkeypatch.setitem(spawn_primitive.PRIMITIVE_MAP, 'sphere', fake_op)

    # Create a fake context.active_object to simulate Blender behavior
    fake_obj = types.SimpleNamespace()
    fake_obj.data = types.SimpleNamespace()
    fake_obj.data.polygons = [types.SimpleNamespace(use_smooth=False) for _ in range(3)]
    fake_obj.modifiers = {}

    fake_context = types.SimpleNamespace(active_object=fake_obj)

    # Patch the context used by the module
    monkeypatch.setattr(spawn_primitive, 'context', fake_context)

    args = {
        'type': 'sphere',
        'name': 'BH_Test',
        'location': (0, 0, 0),
        'segments': 48,
        'ring_count': 24,
        'shade_smooth': True,
        'subsurf_levels': 1,
    }

    res = spawn_primitive.spawn_primitive(args)

    # Verify op called with forwarded kwargs
    fake_op.assert_called()
    called_kwargs = fake_op.call_args.kwargs
    assert called_kwargs.get('location') == (0, 0, 0)
    assert called_kwargs.get('segments') == 48
    assert called_kwargs.get('ring_count') == 24

    # Verify the object was renamed
    assert fake_obj.name == 'BH_Test'
    assert fake_obj.data.name == 'BH_Test'

    # Verify smooth shading applied
    assert all(p.use_smooth for p in fake_obj.data.polygons)


def test_build_black_hole_requests_highres_and_scaled():
    # Ensure SCHWARZSCHILD_RADIUS is non-default for test
    _physics.set_schwarzschild_radius(2.0)
    cmds = _bh_jets.build_black_hole()

    # Find spawn_primitive command
    spawn_cmds = [c for c in cmds if c['cmd'] == 'spawn_primitive']
    assert spawn_cmds, 'spawn_primitive command missing'

    spawn_args = spawn_cmds[0]['args']
    # Check requested primitive type and high tessellation hints
    assert spawn_args.get('type') == 'sphere'
    assert spawn_args.get('segments', 0) >= 32
    assert spawn_args.get('ring_count', 0) >= 16
    assert spawn_args.get('shade_smooth') is True
    assert spawn_args.get('subsurf_levels', 0) >= 1

    # Check scale command uses SCHWARZSCHILD_RADIUS
    scale_cmds = [c for c in cmds if c['cmd'] == 'scale_object']
    assert scale_cmds, 'scale_object command missing'
    scale_vals = scale_cmds[0]['args']['scale']
    assert all(abs(s - 2.0) < 1e-6 for s in scale_vals)
