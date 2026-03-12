# File: tests/e2e/objects/test_butterfly.py
# E2E tests for butterfly component and flight path.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).parent.parent.parent.parent)
)

import app.commands  # noqa: F401
from app.infra.bridge import data, reset
from app.kernel.dispatcher import dispatch_batch
from app.components.objects import build_butterfly
from scenes.missile_storm.animations.domain.timing import (
    Timing,
)
from scenes.missile_storm.animations.acts.flight_path import (
    build_flight_path,
)
from scenes.missile_storm.animations.staging.camera_follow\
    import build_follow_phase
from scenes.missile_storm.animations.staging.materials\
    import build_storm_materials

_PARTS = [
    'Butterfly_Torso',
    'Butterfly_Head',
    'Butterfly_AntennaL',
    'Butterfly_AntennaR',
    'Butterfly_WingL',
    'Butterfly_WingR',
]
_WINGS = ['Butterfly_WingL', 'Butterfly_WingR']
_TIMING = Timing(flight_start=1, flight_end=120)
_SPEED = 0.5
_ALT = 8.0
_HALF = 6


def _build():
    reset()
    cmds = build_storm_materials()
    cmds += build_butterfly(end_f=120, half_cycle=_HALF)
    return dispatch_batch(cmds)


def _build_with_flight():
    reset()
    cmds = build_storm_materials()
    cmds += build_butterfly(end_f=120, half_cycle=_HALF)
    cmds += build_flight_path(
        _TIMING, altitude=_ALT,
        half_cycle=_HALF, speed=_SPEED,
    )
    return dispatch_batch(cmds)


class TestButterflyBuild:
    def test_all_parts_spawned(self):
        _build()
        for name in _PARTS:
            assert data.objects.get(name), (
                f'missing: {name}'
            )

    def test_no_command_failures(self):
        results = _build()
        failed = [r for r in results if not r.success]
        assert not failed, [
            f'{r.command_name}: {r.error}'
            for r in failed
        ]

    def test_children_parented_to_torso(self):
        _build()
        torso = data.objects.get('Butterfly_Torso')
        for name in _PARTS[1:]:
            obj = data.objects.get(name)
            assert obj.parent is torso, (
                f'{name} parent={obj.parent}'
            )

    def test_wings_have_rotation_keyframes(self):
        _build()
        for name in _WINGS:
            obj = data.objects.get(name)
            kfs = obj.animation_data.get_keyframes(
                'rotation_euler'
            )
            assert len(kfs) >= 2, (
                f'{name} rotation kf={len(kfs)}'
            )

    def test_wings_have_scale_keyframes(self):
        _build()
        for name in _WINGS:
            obj = data.objects.get(name)
            kfs = obj.animation_data.get_keyframes(
                'scale'
            )
            assert len(kfs) >= 2, (
                f'{name} scale kf={len(kfs)}'
            )

    def test_only_two_wings(self):
        _build()
        old_wings = [
            'Butterfly_WingFL', 'Butterfly_WingFR',
            'Butterfly_WingHL', 'Butterfly_WingHR',
        ]
        for name in old_wings:
            assert not data.objects.get(name), (
                f'old wing still present: {name}'
            )

    def test_torso_has_body_dynamics(self):
        _build()
        torso = data.objects.get('Butterfly_Torso')
        kfs = torso.animation_data.get_keyframes('scale')
        assert len(kfs) >= 2


class TestFlightPath:
    def test_torso_has_location_keyframes(self):
        _build_with_flight()
        torso = data.objects.get('Butterfly_Torso')
        kfs = torso.animation_data.get_keyframes(
            'location'
        )
        assert len(kfs) >= 2

    def test_torso_altitude_at_frame_1(self):
        _build_with_flight()
        torso = data.objects.get('Butterfly_Torso')
        kfs = torso.animation_data.get_keyframes(
            'location'
        )
        loc1 = kfs.get(1)
        assert loc1 is not None, 'no kf at frame 1'
        assert 7.0 < loc1[2] < 9.0, (
            f'altitude at f1={loc1[2]}, expected ~8.0'
        )

    def test_no_flight_failures(self):
        results = _build_with_flight()
        failed = [r for r in results if not r.success]
        assert not failed, [
            f'{r.command_name}: {r.error}'
            for r in failed
        ]


class TestCameraFollow:
    def test_camera_tracks_butterfly_x(self):
        reset()
        cmds = build_follow_phase(
            _TIMING, step=4,
            half_cycle=_HALF,
            speed=_SPEED, altitude=_ALT,
        )
        dispatch_batch(cmds)
        cam = data.objects.get('StormCam')
        if not cam:
            return
        kfs = cam.animation_data.get_keyframes('location')
        for f, loc in kfs.items():
            assert loc[0] == 0.0, (
                f'f{f}: cam.x={loc[0]} != 0.0'
            )

    def test_camera_behind_butterfly(self):
        reset()
        cmds = build_follow_phase(
            _TIMING, step=4,
            half_cycle=_HALF,
            speed=_SPEED, altitude=_ALT,
        )
        dispatch_batch(cmds)
        cam = data.objects.get('StormCam')
        if not cam:
            return
        kfs = cam.animation_data.get_keyframes('location')
        for f, loc in kfs.items():
            t = f - _TIMING.flight_start
            butterfly_y = t * _SPEED
            assert loc[1] < butterfly_y, (
                f'f{f}: cam.y={loc[1]:.1f} '
                f'not < butterfly_y={butterfly_y:.1f}'
            )
