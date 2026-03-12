# File: tests/runners/butterfly_runner.py
# Debug runner: butterfly build + flight path.
# Run: python tests/runners/butterfly_runner.py
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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

_SEP = '-' * 50


def _kf_summary(obj) -> str:
    props = obj.animation_data.get_all_properties()
    if not props:
        return 'no keyframes'
    parts = []
    for p in props:
        kfs = obj.animation_data.get_keyframes(p)
        n = len(kfs)
        frames = sorted(kfs)
        f0, fN = frames[0], frames[-1]
        parts.append(f'{p}:{n}kf [{f0}..{fN}]')
    return ' | '.join(parts)


def _print_obj(name: str) -> None:
    obj = data.objects.get(name)
    if not obj:
        print(f'  [MISSING] {name}')
        return
    loc = obj.location.to_tuple()
    sc = obj.scale.to_tuple()
    par = obj.parent.name if obj.parent else 'none'
    print(f'  {name}')
    print(f'    loc=({loc[0]:.2f},{loc[1]:.2f},{loc[2]:.2f})')
    print(f'    scale=({sc[0]:.2f},{sc[1]:.2f},{sc[2]:.2f})')
    print(f'    parent={par}')
    print(f'    kf: {_kf_summary(obj)}')


_PARTS = [
    'Butterfly_Torso', 'Butterfly_Head',
    'Butterfly_AntennaL', 'Butterfly_AntennaR',
    'Butterfly_WingL', 'Butterfly_WingR',
]


def main() -> None:
    reset()
    timing = Timing(flight_start=1, flight_end=120)
    cmds = build_butterfly(end_f=120, half_cycle=6)
    cmds += build_flight_path(
        timing, altitude=8.0,
        half_cycle=6, speed=0.5,
    )
    results = dispatch_batch(cmds)

    ok = sum(1 for r in results if r.success)
    total = len(results)
    print(_SEP)
    print(f'Commands: {ok}/{total} OK')

    failed = [r for r in results if not r.success]
    if failed:
        print('FAILURES:')
        for r in failed[:20]:
            print(f'  [{r.command_name}] {r.error}')

    print(_SEP)
    print('Object state:')
    for p in _PARTS:
        _print_obj(p)

    torso = data.objects.get('Butterfly_Torso')
    if torso:
        print(_SEP)
        print('Torso location kf sample:')
        kfs = torso.animation_data.get_keyframes('location')
        for f in sorted(kfs)[:5]:
            v = kfs[f]
            print(
                f'  f{f}: ({v[0]:.2f},'
                f'{v[1]:.2f},{v[2]:.2f})'
            )

    print(_SEP)


if __name__ == '__main__':
    main()
