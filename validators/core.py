from dataclasses import dataclass
from typing import List


@dataclass
class Issue:
    index: int
    cmd: str
    message: str
    severity: str = "error"


def format_issues(issues: List[Issue]) -> str:
    if not issues:
        return "No issues."
    return "\n".join(f"#{it.index:03d} [{it.severity}] {it.cmd}: {it.message}" for it in issues)
