# File: app/components/objects/__init__.py
# Reusable 3D object builders for scene composition.
# All Rights Reserved Arodi Emmanuel

from .butterfly_body import build_butterfly_body
from .butterfly_wings import build_butterfly_wings
from .missile_body import build_missile
from .missile_trail import build_missile_trail
from .explosion import build_explosion
from .house import build_house
from .barn import build_barn
from .tree import build_tree
from .meadow import build_meadow
from .fence import build_fence

__all__ = [
    'build_butterfly_body',
    'build_butterfly_wings',
    'build_missile',
    'build_missile_trail',
    'build_explosion',
    'build_house',
    'build_barn',
    'build_tree',
    'build_meadow',
    'build_fence',
]
