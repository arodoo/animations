from typing import Any, Dict, List, Set

from app.kernel.registry import list_commands

from .core import Issue


def _load_known_primitives() -> Set[str]:
    try:
        from app.commands.objects.spawn_primitive import PRIMITIVE_MAP

        return {k.lower() for k in PRIMITIVE_MAP}
    except Exception:
        return {"cube", "sphere", "torus", "cone", "ico_sphere"}


KNOWN_PRIMITIVES = _load_known_primitives()


# Mapping of command -> arg keys and their type (obj/mat/prim)
COMMAND_ARG_TYPES = {
    "create_material": {"name": "mat"},
    "spawn_primitive": {"name": "obj", "type": "prim"},
    "assign_material": {"object": "obj", "material": "mat"},
    "scale_object": {"name": "obj", "object": "obj"},
    "move_object": {"name": "obj", "object": "obj"},
    "rotate_object": {"name": "obj", "object": "obj"},
    "add_particle_system": {"object": "obj"},
}


def _check_registered_command(cmd: str, regs: Set[str]) -> bool:
    return cmd in regs


def validate_batch(batch: List[Dict[str, Any]]) -> List[Issue]:
    issues: List[Issue] = []
    created_objs: Set[str] = set()
    created_mats: Set[str] = set()
    regs = set(list_commands())

    for i, instr in enumerate(batch):
        cmd = instr.get("cmd")
        args = instr.get("args") or {}

        if not cmd:
            issues.append(Issue(i, "<none>", "missing 'cmd'", "error"))
            continue

        if not _check_registered_command(cmd, regs):
            issues.append(Issue(i, cmd, "unknown command", "error"))

        # Generic create_* handling (skip explicit create_material to avoid
        # double-processing)
        if cmd.startswith("create_") and cmd != "create_material":
            name = args.get("name")
            if not name:
                issues.append(Issue(i, cmd, "create_* without name", "warning"))
            else:
                if "material" in cmd:
                    if name in created_mats:
                        issues.append(Issue(i, cmd, f"material '{name}' redefined", "warning"))
                    created_mats.add(name)
                else:
                    if name in created_objs:
                        issues.append(Issue(i, cmd, f"object '{name}' redefined", "warning"))
                    created_objs.add(name)

        # spawn_primitive specifics
        if cmd == "spawn_primitive":
            typ = (args.get("type") or "").lower()
            name = args.get("name")
            if typ and typ not in KNOWN_PRIMITIVES:
                issues.append(Issue(i, cmd, f"unknown primitive '{typ}'", "error"))
            if not name:
                issues.append(Issue(i, cmd, "missing object name", "error"))
            else:
                if name in created_objs:
                    issues.append(Issue(i, cmd, f"object '{name}' redefined", "warning"))
                created_objs.add(name)

        # create_material explicit
        if cmd == "create_material":
            name = args.get("name")
            if not name:
                issues.append(Issue(i, cmd, "missing material name", "error"))
            elif name in created_mats:
                issues.append(Issue(i, cmd, f"material '{name}' redefined", "warning"))
            else:
                created_mats.add(name)

        # assign_material and transforms
        if cmd in ("assign_material",):
            obj = args.get("object")
            mat = args.get("material")
            if isinstance(obj, str) and obj not in created_objs:
                issues.append(Issue(i, cmd, f"unknown object '{obj}'", "error"))
            if isinstance(mat, str) and mat not in created_mats:
                issues.append(Issue(i, cmd, f"unknown material '{mat}'", "error"))

        if cmd in ("scale_object", "move_object", "rotate_object"):
            target = args.get("name") or args.get("object")
            if isinstance(target, str) and target not in created_objs:
                issues.append(Issue(i, cmd, f"unknown target '{target}'", "error"))

        if cmd == "add_particle_system":
            host = args.get("object")
            if isinstance(host, str) and host not in created_objs:
                issues.append(Issue(i, cmd, f"particle host unknown '{host}'", "error"))

        # Generic cross-check using COMMAND_ARG_TYPES
        if cmd in COMMAND_ARG_TYPES:
            for key, kind in COMMAND_ARG_TYPES[cmd].items():
                if key not in args:
                    continue
                val = args.get(key)
                if isinstance(val, str):
                    if kind == "obj" and val not in created_objs:
                        issues.append(Issue(i, cmd, f"unknown object '{val}' (arg:{key})", "error"))
                    if kind == "mat" and val not in created_mats:
                        issues.append(Issue(i, cmd, f"unknown material '{val}' (arg:{key})", "error"))
                    if kind == "prim" and val.lower() not in KNOWN_PRIMITIVES:
                        issues.append(Issue(i, cmd, f"unknown primitive '{val}' (arg:{key})", "error"))

    return issues


def run_on_scene(quality: str = "low") -> List[Issue]:
    from scenes.quasar_bh.scene import PRESETS, DISK_RINGS
    from scenes.quasar_bh.scene import build_environment, build_black_hole, build_ring
    from scenes.quasar_bh.scene import build_disk_animation, build_jets, build_camera

    p = PRESETS[quality]
    disk_rings = DISK_RINGS[: p["disk_ring_count"]]

    batch: List[Dict[str, Any]] = []
    batch += build_environment(p)
    batch += build_black_hole()
    for i, ring in enumerate(disk_rings):
        batch += build_ring(i, ring)
    batch += build_disk_animation(
        disk_rings,
        p["total_frames"],
        p["disk_rotations"],
        p["disk_step"],
        p["pulse_inner"],
        p["particles"],
    )
    batch += build_jets(p["particles"])
    batch += build_camera(p["total_frames"], p["cam_step"], p["dof"])

    return validate_batch(batch)
