import ast
import os
from typing import Dict, List, Tuple

from .batch_validator import validate_batch
from .core import Issue


def _is_candidate_list(node: ast.AST) -> bool:
    if not isinstance(node, ast.List):
        return False
    # list must contain at least one dict with 'cmd' key as string
    for el in node.elts:
        if isinstance(el, ast.Dict):
            for k in el.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str) and k.value == "cmd":
                    return True
    return False


def _collect_batches_from_ast(tree: ast.AST) -> List[Tuple[int, ast.AST]]:
    batches: List[Tuple[int, ast.AST]] = []

    for node in ast.walk(tree):
        if _is_candidate_list(node):
            batches.append((getattr(node, "lineno", 0), node))
    return batches


def _safe_literal_eval(node: ast.AST):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def scan_and_validate(root: str) -> Dict[str, List[Tuple[int, List[Issue]]]]:
    results: Dict[str, List[Tuple[int, List[Issue]]]] = {}
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            path = os.path.join(dirpath, fname)
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    src = fh.read()
                tree = ast.parse(src, filename=path)
            except Exception:
                continue

            file_results: List[Tuple[int, List[Issue]]] = []
            batches = _collect_batches_from_ast(tree)
            for lineno, node in batches:
                literal = _safe_literal_eval(node)
                if not isinstance(literal, list):
                    continue
                # ensure list of dicts with 'cmd'
                if not all(isinstance(el, dict) and "cmd" in el for el in literal):
                    continue
                issues = validate_batch(literal)
                if issues:
                    file_results.append((lineno, issues))

            if file_results:
                results[path] = file_results

    return results


if __name__ == "__main__":
    import sys
    from .core import format_issues

    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    res = scan_and_validate(root)
    if not res:
        print("No issues found in project literals.")
        raise SystemExit(0)
    for path, items in res.items():
        print(path)
        for lineno, issues in items:
            print(f"  at line {lineno}:")
            print(format_issues(issues))
    raise SystemExit(1)
